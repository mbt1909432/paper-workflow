---
title: "LLM-RankFusion: Mitigating Intrinsic Inconsistency in LLM-based Ranking"
authors: ["Yifan Zeng", "Ojas Tendolkar", "Raymond Baartmans", "Qingyun Wu", "Lizhong Chen", "Huazheng Wang"]
date: 2024-01-01
arxiv_id: "2406.xxxxx"
org: "Oregon State University, Pennsylvania State University"
---

## Abstract（摘要）

- **解决的问题**：LLM在用于排序（passage ranking）时存在内在不一致性（intrinsic inconsistency），具体表现为两种：**顺序不一致性（order inconsistency）**——交换段落前后位置会导致比较结果冲突；**传递不一致性（transitive inconsistency）**——LLM的偏好判断不满足传递性（如 d1 > d2, d2 > d3 但 d3 > d1），导致基于排序算法的排名结果高度敏感且不稳定。
- **核心思路/方法**：提出LLM-RankFusion框架，通过三个层面缓解不一致性：(1) 使用In-Context Learning（ICL）提示让LLM学习顺序无关的比较；(2) 使用校准（calibration）方法估计两个段落之间的底层偏好概率；(3) 使用排名聚合（rank aggregation，Borda count）从多个排名器聚合结果以缓解传递不一致性。
- **主要结论**：ICL和校准能有效减少顺序不一致性，显著提高NDCG分数；排名聚合通过形成共识排名缓解传递不一致性，使最终排名更鲁棒。

## Methodology（方法论）

- **使用的方法/框架**：LLM-RankFusion，一个基于LLM的排序框架，结合ICL、校准和排名聚合三个模块。
- **关键模块和流程**：
  1. **In-Context Learning (ICL)**：设计ICL提示，提供一个示例展示两种排列顺序下的成对比较，让LLM理解偏好应与位置无关。
  2. **Calibration（校准）**：对每对段落查询两种排列（A=di, B=dj 和 A=dj, B=di），收集logits，计算校准后的偏好概率 P_ij = (P(ij) + 1 - P(ji)) / 2，确保 P_ij + P_ji = 1，最终以 P_ij > 0.5 判断偏好。
  3. **Rank Aggregation（排名聚合）**：使用Borda count方法，对每个段落在不同排名列表中的位置进行评分求和，按Borda分数降序排列得到最终聚合排名。
  4. **聚合维度**：(a) 跨排序算法聚合（Bubblesort + Heapsort）；(b) 跨LLM聚合（按模型规模分组）。
- **技术细节要点**：
  - 排序算法选择Bubblesort和Heapsort，二者性质不同，一个算法在特定输入上表现差时另一个可补偿。
  - 校准不增加额外推理开销，仅收集输出logits计算偏好概率。
  - 使用锦标赛图（tournament graph）建模成对比较，通过不一致三元组数量衡量传递不一致性。

## Contribution（贡献）

- **首次识别并研究LLM排序中的传递不一致性**，同时研究顺序不一致性。
- **提出ICL和校准方法解决顺序不一致性**，在大多数LLM上取得显著改进。
- **将排名聚合领域与LLM排序相结合**，通过聚合缓解传递不一致性对成对和集合比较的影响。
- **验证了聚合方法的有效性**，研究了跨排序算法和跨LLM两种聚合策略，展示了有前景的实证性能。

**与现有方法的区别**：此前工作（如PRP-Sort）将顺序不一致性简单处理为平局（ties），忽略了LLM位置偏差的本质；此前工作也未关注传递不一致性问题。本文首次系统性地从概率校准和排名聚合角度解决这两类不一致性。

## Limitation（局限性）

- **论文自己承认的不足**：
  1. 聚合过程需要完整的排序后排名列表，增加了计算成本。
  2. ICL导致提示更长，增加了推理开销。
  3. 实验仅在有限的IR数据集（TREC-DL2019和TREC-DL2020）上进行，未覆盖更多数据集。
  4. 未纳入其他聚合方法（如Markov Chain方法、Kemeny聚合等）进行对比。
- **未解决的问题**：
  1. 尚未探索不依赖排序算法、直接从成对比较聚合的方法。
  2. 尚未将LLM决策聚合拓展到passage ranking以外的其他任务和领域。

## Evaluation（评估）

- **使用的数据集**：TREC-DL2019、TREC-DL2020（标准信息检索基准数据集），每个查询取BM25检索的前100个段落进行重排。
- **评估指标**：
  - NDCG（Normalized Discounted Cumulative Gain），主要关注NDCG@10
  - 平均Kendall tau距离（衡量排名间不一致性/不稳定性）
- **关键实验结果**：
  1. ICL单独使用即可在大多数LLM上提升排序性能，校准同样带来显著改进，二者结合效果更好。
  2. ICL+校准的成对排序方法在多个数据集上优于多种基线方法。
  3. 跨排序算法聚合在所有模型上均提高NDCG@10并降低Kendall-tau距离。
  4. 跨LLM聚合总能达到被聚合模型中的中等性能水平，实现了平衡甚至更优的排名效果。
  5. 提示设计敏感性分析表明：ICL+校准不仅提升约8个NDCG点，还将方差从3.07-4.63降至1.61-1.92。
- **使用的LLM**：GPT-3.5-Turbo、GPT-4、LLaMA-3-70B/8B、Vicuna-v1.5-13b、Mixtral-8x7b、Gemma-7B、Flan-UL2、Flan-T5-XXL。

## Key Insights（关键洞察）

- **可借鉴的方法思路**：
  1. **校准概率估计**：通过两种排列的平均logits消除位置偏差，是一种轻量且有效的去偏策略，可推广到其他需要消除LLM偏差的场景。
  2. **ICL去偏**：用示例展示期望行为（顺序无关性），利用LLM的few-shot学习能力隐式纠正偏差。
  3. **排名聚合思路**：当单一方法的输出不可靠时，通过Borda count等简单聚合方法从多个不同配置中提取共识，是提升鲁棒性的通用策略。
  4. **不一致性量化**：使用锦标赛图中不一致三元组数量来衡量传递不一致性，是一种清晰的可量化指标。
- **对本研究的启发**：
  1. LLM作为排序器时存在系统性不一致，在设计基于LLM的排序/评估系统时需要显式处理。
  2. 多模型/多策略聚合是一种不依赖先验知识即可提升鲁棒性的实用方法。
  3. 消除位置偏差的ICL+校准组合策略对其他涉及偏好判断的LLM任务（如LLM-as-a-judge）也有参考价值。
