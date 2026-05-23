# Result Narrative Strategies

How to frame experiment results when things don't go as expected. Based on real experience.

---

## Scenario 1: Your Method Underperforms Baselines

This happens often in early research. The key is honest framing with insightful analysis.

### Strategy: Pilot Evaluation + Internal Metrics

Instead of claiming superiority, position as a feasibility study:

**Abstract framing:**
> We conduct a pilot evaluation (N=10) on HotpotQA to validate the pipeline's functional correctness and analyze internal quality metrics including trust scores, hallucination rates, and convergence behavior.

**Table presentation:**
- Show all methods' scores honestly (EM, F1, Faithfulness)
- Add a second table of **internal metrics** unique to your method (trust score, hallucination score, iterations)
- This gives reviewers something novel even if EM/F1 aren't state-of-the-art

**Analysis section:**
1. **Acknowledge the gap directly** — don't hide it
2. **Analyze why** — identify specific failure modes (e.g., "the trust filter's conservative threshold discards relevant evidence for multi-hop questions")
3. **Show what works** — highlight modules that function correctly (e.g., "hallucination detection correctly flags 70% of unsupported claims")
4. **Propose specific improvements** — tie each failure to a concrete fix

### Key Phrases

Instead of:
- ~~"significantly outperforms"~~
- ~~"achieves state-of-the-art"~~
- ~~"superior performance"~~

Use:
- "demonstrates the feasibility of..."
- "provides a foundation for..."
- "analysis reveals that Module X achieves..."
- "we identify three key failure modes and propose targeted remedies"

## Scenario 2: Small Sample Size

When N is small (10-50 samples), results are noisy. Frame carefully.

### Strategy: Qualitative + Quantitative

- **Quantitative:** Report exact numbers but label clearly as "pilot study" or "preliminary evaluation"
- **Qualitative:** Pick 2-3 representative examples and do case analysis
  - Show the full pipeline trace (what each module did)
  - Explain why a particular question succeeded or failed
  - This is often more convincing than aggregate numbers

### Example Case Analysis Format

```markdown
**Case Study: Multi-hop Reasoning Failure**

Question: "What government position was held by the woman who portrayed X?"

Pipeline trace:
1. Retrieval Judge: confidence=0.85 (correctly identified as needing retrieval)
2. Graph Retrieval: retrieved 3 documents, missed the key bridging entity
3. Trust Filter: correctly kept all 3 docs (trust scores 0.72-0.89)
4. Generation: produced partial answer based on available evidence
5. Hallucination Detection: flagged low support (score=0.4)
6. Iterative Refinement: 2nd iteration retrieved additional context but still incomplete

Root cause: The knowledge graph lacked the cross-document relation linking the actress to the government position.
```

## Scenario 3: Ablation Doesn't Show Clear Trends

When removing modules doesn't consistently hurt performance.

### Strategy: Module-Level Metric Analysis

Instead of end-to-end ablation (which requires large N to show statistical significance), analyze each module's internal behavior:

| Module | Metric | Value | Interpretation |
|--------|--------|-------|----------------|
| Retrieval Judge | Precision | 0.80 | Correctly identifies 80% of questions needing retrieval |
| Trust Filter | Retention Rate | 0.65 | Filters 35% of low-trust documents |
| Hallucination Detect | Flag Rate | 0.30 | Flags 30% of answers as potentially hallucinated |
| Iterative Refine | Avg Iterations | 1.2 | Most questions converge in 1-2 rounds |

This shows the pipeline is working as designed, even if end-to-end metrics don't improve.

## Scenario 4: Only One Dataset Works

When your method only shows improvement on one evaluation dimension.

### Strategy: Claim the Specific Contribution

Be specific about what your method contributes:

> While TA-GraphRAG does not achieve the highest EM/F1 scores in this pilot evaluation, it demonstrates the value of integrating trust-awareness into the RAG pipeline. The trust filter successfully identifies and flags low-confidence evidence (precision=0.78), and the hallucination detection module provides explainable verification cues that are absent from baseline methods.

This positions the contribution as a **new capability** rather than a **performance improvement**.

## General Principles

1. **Never fabricate or cherry-pick results.** Reviewers and reproducibility checks will catch this.
2. **Report all numbers, even unfavorable ones.** Omission is worse than poor results.
3. **Use the correct statistical language.** "Pilot study" (N<50), "evaluation" (N≥50), "benchmark" (full dataset).
4. **Distinguish methodological contribution from empirical contribution.** A novel framework with modest results is still publishable if the analysis is thorough.
5. **Be honest about limitations.** A well-analyzed failure is more valuable than an unexplained success.
6. **Frame around what was learned, not what was achieved.** "Our analysis reveals three key failure modes in trust-aware retrieval..." is stronger than "Our method achieves X% F1."

## Updating the Paper After Experiments

When filling real data into placeholder tables:

1. **Adjust the narrative to match the data.** Don't keep claims that the data doesn't support.
2. **Update abstract and introduction** to reflect actual findings, not aspirational goals.
3. **Revise contribution statements** — if a claimed contribution isn't supported by experiments, either remove it or reframe it.
4. **Add a "Lessons Learned" or "Analysis" section** if results are unexpected. This shows intellectual honesty.
5. **Revise the conclusion** to accurately summarize what was demonstrated vs. what remains future work.
