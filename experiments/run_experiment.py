"""Run experiments on HotpotQA test set (10 samples).
Usage: cd experiments && uv run python run_experiment.py
"""
import json
import time
from tqdm import tqdm
from src.config import DATA_DIR, RESULTS_DIR
from src.retriever import BM25Retriever
from src.evaluator import evaluate_batch, exact_match, f1_score, faithfulness_score
from src.pipeline import build_context_documents, run_ta_graphrag
from src.baselines.naive_rag import naive_rag
from src.baselines.self_rag import self_rag
from src.baselines.crag import crag
from src.baselines.graph_rag import graph_rag


def run_all_methods(question: str, retriever: BM25Retriever, example: dict) -> dict:
    """Run all methods on a single question and return results."""
    results = {}

    # 1. Naive RAG
    print("  Running naive_rag...")
    r = naive_rag(question, retriever)
    results["naive_rag"] = r

    # 2. Self-RAG
    print("  Running self_rag...")
    r = self_rag(question, retriever)
    results["self_rag"] = r

    # 3. CRAG
    print("  Running crag...")
    r = crag(question, retriever)
    results["crag"] = r

    # 4. GraphRAG
    print("  Running graph_rag...")
    r = graph_rag(question, retriever, example)
    results["graph_rag"] = r

    # 5. TA-GraphRAG (full pipeline)
    print("  Running ta_graphrag...")
    r = run_ta_graphrag(question, retriever, example)
    results["ta_graphrag"] = r

    return results


def main():
    # Load test data
    test_path = DATA_DIR / "hotpotqa_test.json"
    with open(test_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)
    print(f"Loaded {len(test_data)} test examples")

    all_results = {}

    for i, example in enumerate(tqdm(test_data, desc="Processing")):
        question = example["question"]
        ground_truth = example["answer"]
        print(f"\n[{i+1}/{len(test_data)}] Q: {question[:80]}...")
        print(f"  GT: {ground_truth}")

        # Build retriever from example context
        docs = build_context_documents(example)
        retriever = BM25Retriever(docs)

        # Run all methods
        try:
            method_results = run_all_methods(question, retriever, example)
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

        # Evaluate each method
        for method_name, result in method_results.items():
            prediction = result.get("answer", "")
            em = exact_match(prediction, ground_truth)
            f1 = f1_score(prediction, ground_truth)
            faith = faithfulness_score(prediction, result.get("retrieved_docs", []))

            result["em"] = em
            result["f1"] = f1
            result["faithfulness"] = faith
            result["ground_truth"] = ground_truth

            print(f"  {method_name}: EM={em:.1f} F1={f1:.3f} Faith={faith:.2f} Ans={prediction[:60]}...")

        all_results[f"q{i}"] = {
            "question": question,
            "ground_truth": ground_truth,
            "methods": method_results,
        }

        # Rate limiting
        time.sleep(1)

    # Aggregate results
    print("\n" + "="*60)
    print("AGGREGATE RESULTS")
    print("="*60)

    for method in ["naive_rag", "self_rag", "crag", "graph_rag", "ta_graphrag"]:
        ems = []
        f1s = []
        faiths = []
        for qkey, qdata in all_results.items():
            if method in qdata.get("methods", {}):
                r = qdata["methods"][method]
                ems.append(r.get("em", 0))
                f1s.append(r.get("f1", 0))
                faiths.append(r.get("faithfulness", 0))

        if ems:
            print(f"  {method:15s}: EM={sum(ems)/len(ems)*100:.1f}%  F1={sum(f1s)/len(f1s)*100:.1f}%  Faith={sum(faiths)/len(faiths)*100:.1f}%")

    # Save results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / "main_results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
