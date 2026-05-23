"""Generate experiment result figures for the paper."""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Load results
results_path = Path(__file__).parent / "results" / "main_results.json"
with open(results_path, "r", encoding="utf-8") as f:
    all_results = json.load(f)

# Aggregate per-method metrics
methods = ["naive_rag", "self_rag", "crag", "graph_rag", "ta_graphrag"]
method_labels = ["Naive RAG", "Self-RAG", "CRAG", "GraphRAG", "TA-GraphRAG"]
colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974"]
highlight = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#D4A017"]

ems = []
f1s = []
faiths = []

for method in methods:
    e, f, fa = [], [], []
    for qkey, qdata in all_results.items():
        if method in qdata.get("methods", {}):
            r = qdata["methods"][method]
            e.append(r.get("em", 0) * 100)
            f.append(r.get("f1", 0) * 100)
            fa.append(r.get("faithfulness", 0) * 100)
    ems.append(np.mean(e))
    f1s.append(np.mean(f))
    faiths.append(np.mean(fa))

output_dir = Path(__file__).parent / "results" / "figures"
output_dir.mkdir(parents=True, exist_ok=True)

# === Figure 1: Bar chart comparing all methods ===
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

x = np.arange(len(methods))
width = 0.6

# EM
bars = axes[0].bar(x, ems, width, color=colors, edgecolor="white", linewidth=0.8)
axes[0].set_ylabel("Score (%)")
axes[0].set_title("Exact Match")
axes[0].set_xticks(x)
axes[0].set_xticklabels(method_labels, rotation=25, ha="right", fontsize=9)
axes[0].set_ylim(0, max(ems) * 1.4 + 5)
for bar, val in zip(bars, ems):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f"{val:.1f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

# F1
bars = axes[1].bar(x, f1s, width, color=colors, edgecolor="white", linewidth=0.8)
axes[1].set_ylabel("Score (%)")
axes[1].set_title("F1 Score")
axes[1].set_xticks(x)
axes[1].set_xticklabels(method_labels, rotation=25, ha="right", fontsize=9)
axes[1].set_ylim(0, max(f1s) * 1.3 + 5)
for bar, val in zip(bars, f1s):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f"{val:.1f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

# Faithfulness
bars = axes[2].bar(x, faiths, width, color=colors, edgecolor="white", linewidth=0.8)
axes[2].set_ylabel("Score (%)")
axes[2].set_title("Faithfulness")
axes[2].set_xticks(x)
axes[2].set_xticklabels(method_labels, rotation=25, ha="right", fontsize=9)
axes[2].set_ylim(0, max(faiths) * 1.2 + 5)
for bar, val in zip(bars, faiths):
    axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f"{val:.1f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

plt.tight_layout()
fig.savefig(output_dir / "main_results_bar.png", dpi=300, bbox_inches="tight")
print(f"Saved: {output_dir / 'main_results_bar.png'}")

# === Figure 2: Radar chart ===
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
categories = ["EM", "F1", "Faithfulness"]
cat_angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
cat_angles += cat_angles[:1]

for i, method in enumerate(methods):
    values = [ems[i], f1s[i], faiths[i]]
    values += values[:1]
    ax.plot(cat_angles, values, "o-", linewidth=2, label=method_labels[i],
            color=colors[i], markersize=5)
    ax.fill(cat_angles, values, alpha=0.08, color=colors[i])

ax.set_xticks(cat_angles[:-1])
ax.set_xticklabels(categories, fontsize=11)
ax.set_ylim(0, 100)
ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.15), fontsize=9)
ax.set_title("Method Comparison (HotpotQA)", fontsize=13, pad=20)

fig.savefig(output_dir / "radar_comparison.png", dpi=300, bbox_inches="tight")
print(f"Saved: {output_dir / 'radar_comparison.png'}")

# === Figure 3: Per-question F1 heatmap ===
questions = []
method_f1_matrix = []
for qkey in sorted(all_results.keys()):
    qdata = all_results[qkey]
    questions.append(f"Q{qkey[1:]}")
    row = []
    for method in methods:
        if method in qdata.get("methods", {}):
            row.append(qdata["methods"][method].get("f1", 0) * 100)
        else:
            row.append(0)
    method_f1_matrix.append(row)

fig, ax = plt.subplots(figsize=(8, 6))
matrix = np.array(method_f1_matrix)
im = ax.imshow(matrix, cmap="YlOrRd", aspect="auto", vmin=0, vmax=50)

ax.set_xticks(np.arange(len(methods)))
ax.set_yticks(np.arange(len(questions)))
ax.set_xticklabels(method_labels, rotation=30, ha="right", fontsize=10)
ax.set_yticklabels(questions, fontsize=10)

for i in range(len(questions)):
    for j in range(len(methods)):
        val = matrix[i, j]
        color = "white" if val > 25 else "black"
        ax.text(j, i, f"{val:.1f}", ha="center", va="center", fontsize=8, color=color)

ax.set_title("F1 Score per Question (%)", fontsize=13)
fig.colorbar(im, ax=ax, shrink=0.8, label="F1 (%)")

plt.tight_layout()
fig.savefig(output_dir / "per_question_heatmap.png", dpi=300, bbox_inches="tight")
print(f"Saved: {output_dir / 'per_question_heatmap.png'}")

print("\nAll figures generated!")
