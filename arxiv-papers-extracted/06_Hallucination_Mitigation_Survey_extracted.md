---
title: "A Comprehensive Survey of Hallucination Mitigation Techniques in Large Language Models"
authors: ["S.M Towhidul Islam Tonmoy", "S M Mehedi Zaman", "Vinija Jain", "Anku Rani", "Vipula Rawte", "Aman Chadha", "Amitava Das"]
date: 2024-01-09
arxiv_id: "2401.01313"
org: "AI Institute, University of South Carolina"
---

## Abstract（摘要）
- **解决了什么问题**: 大语言模型（LLMs）在生成类人文本时存在"幻觉"问题——生成看似事实但缺乏依据的内容，这是阻碍LLMs安全部署到实际生产系统中的最大障碍。
- **核心思路/方法**: 对32种以上幻觉缓解技术进行系统性综述，提出一个详细的分类体系（taxonomy），涵盖数据集利用、任务类型、反馈机制和检索类型等参数。
- **主要结论**: 该综述构建了LLM幻觉缓解技术的系统化分类框架，覆盖了提示工程（Prompt Engineering）和模型开发（Developing Models）两大类方法，并分析了各类技术的局限性和未来研究方向。

## Methodology（方法论）
> 本文为综述论文，方法论部分总结其分类框架和分类方法。

- **一级分类**: 将幻觉缓解技术分为两大类——**Prompt Engineering（提示工程）** 和 **Developing Models（模型开发）**。

- **Prompt Engineering 下的子分类**:
  1. **Retrieval Augmented Generation (RAG)**: 检索增强生成，按检索时机进一步分为：
     - Before generation（生成前检索）: LLM-Augmenter, FreshPrompt
     - During generation（生成时检索）: Knowledge Retrieval, D&Q框架, EVER
     - After generation（生成后检索）: RARR, High Entropy Word Spotting and Replacement
     - End-to-End RAG: Lewis等人的端到端RAG（DPR + BART联合训练）
  2. **Self-refinement through feedback and reasoning（通过反馈和推理进行自我修正）**: CoVe（链式验证）, CoNLI（链式自然语言推理）, ChatProtect, Self-Reflection, SC reasoning, Mind's Mirror, DRESS, MixAlign 等
  3. **Prompt Tuning（提示调优）**: UPRISE, SynTra

- **Developing Models 下的子分类**:
  1. **Introducing new decoding strategy（新解码策略）**: CAD（上下文感知解码）, DoLa（对比层解码）, ITI（推理时干预）
  2. **Utilization of Knowledge Graph（知识图谱利用）**: RHO, FLEEK
  3. **Introducing faithfulness-based loss function（基于忠实度的损失函数）**: THAM Framework, Loss Weighting Method (mFACT)
  4. **Supervised fine-tuning（有监督微调）**: Knowledge Injection, HAR, Fine-tuning for Factuality, BEINFO, R-Tuning, TWEAK

- **分类维度**: 该综述按6个维度对各工作进行系统化整理：缓解技术类型、是否包含检测机制、任务类型、评估指标、评估所用LLM、数据集。

## Contribution（贡献）
- 提出了一个系统化的分类法（taxonomy），用于对LLM及视觉语言模型（VLMs）的幻觉缓解技术进行分类。
- 综合了32种以上幻觉缓解技术的关键特征，为该领域未来的结构化研究提供指引。
- 讨论了这些技术固有的局限性和挑战，并提出了潜在解决方案和未来研究方向。
- 提供了一个详细的汇总表格（Table 1），从缓解技术、检测、任务、指标、评估模型、数据集、局限性七个维度对比所有综述工作。

## Limitation（局限性）
- **综述层面**: 该综述覆盖的文献截至2024年初，LLM领域发展迅速，部分最新方法可能未包含在内。
- **各技术自身的局限性（综述中明确列出）**:
  - FreshPrompt: 依赖Google搜索API，答案可能过时
  - RARR: 评估指标不完全覆盖归因的所有方面；不适用于长文档；计算密集
  - EVER: 仅关注通过文本归因来减少幻觉，依赖可能存在不准确的参考信息
  - CoVe: 仅解决直接陈述的事实性幻觉；额外的验证步骤增加了计算成本
  - Mind's Mirror: 实验主要使用单一教师模型（GPT-3.5）和学生模型（T5-Base）；LLM自我评估中的缺陷可能传播到蒸馏的小模型
  - UPRISE: 对直接表述为语言建模的任务（如共指消解和常识推理）影响有限
  - DoLa: 未探索指令遵循或人类反馈学习等维度；仅依赖模型内部知识，缺乏外部检索模块，无法纠正训练中获取的错误信息
  - HALOCHECK: 仅包含一个弱开源LLM（BLOOM 7B）的实验，且仅聚焦NBA领域
  - 多语言摘要方法（mFACT）: 使用机器翻译构建训练数据，翻译错误可能限制指标质量；加权损失方法在不同语言上的忠实度提升不一致
  - RHO: 模型识别统计模式但无法感知因果关系等定性关系

## Evaluation（评估）
> 本文为综述论文，以下汇总各技术使用的评估设置。

- **使用的数据集**（代表性数据集）:
  - QA任务: FreshQA, HotPotQA, TriviaQA, Natural Questions (NQ), TruthfulQA, PubMedQA, MedQuAD, QUEST, MultiSpan-QA, FuzzyQA, ParaRel, MMLU
  - 摘要任务: CNN-DM, XSum, XL-Sum, QMSum, ACI-Bench, SummEval, QAGS-Xsum
  - 对话任务: OpenDialKG, FaithDial, TopiOCQA
  - 幻觉检测: HaluEVAL, FactCC, FEVER
  - 其他: HILT, FATE, CFTriviaQA, WebNLG, GenWiki, MSMARCO, BLIP, CC3M

- **评估指标**（代表性指标）:
  - 忠实度/归因: FactScore, AIS (Attributable to Identified Sources), mFACT, FactCC, AlignScore, FactKB, HVI (Hallucination Vulnerability Index)
  - 生成质量: BLEU, ROUGE-1/2/L, METEOR, CIDEr, BERTScore, GPT-4自动评估
  - 分类/匹配: Accuracy, F1-score, Exact Match (EM), Precision, Recall
  - 校准: Expected Calibration Error (ECE), Brier score
  - 专有指标: HaloCheck, G-EVAL

- **关键实验结果**（代表性发现）:
  - RAG方法（如LLM-Augmenter）通过外部知识检索和迭代反馈显著降低幻觉
  - CoVe通过链式验证在Wikidata问题和长文本生成中减少幻觉
  - DoLa在TruthfulQA上持续提升LLaMA系列模型的真实性
  - ITI显著提升LLaMA模型在TruthfulQA上的表现
  - EVER在短形式QA、传记生成和多跳推理中优于检索和非检索基线
  - HAR使用反事实数据集微调的模型在文本锚定方面显著优于事实数据集训练的模型

## Key Insights（关键洞察）
- **分类框架的启发**: 幻觉缓解可从提示工程和模型开发两个层面系统切入，提示工程方法无需修改模型即可部署，实用性更强；模型开发方法虽然成本更高但可能带来更深层次的改善。
- **RAG的三阶段划分**: 按检索时机分为生成前、生成中、生成后三类，这是一个实用的技术选型框架——不同时机适用于不同场景。
- **自我修正范式的价值**: CoVe和CoNLI等方法表明，让模型自我验证和修正是降低幻觉的有效途径，且不需要外部知识源。
- **解码策略的重要性**: DoLa和ITI表明，通过对比不同层的logit或在推理时干预注意力头，可以在不重新训练的情况下提升模型真实性。
- **知识图谱的补充作用**: KG方法（RHO、FLEEK）提供了结构化外部知识，有助于生成更忠实的响应。
- **反事实数据的价值**: HAR方法表明，利用LLM幻觉生成的反事实数据集反而能增强模型的归因能力，是一种"以毒攻毒"的思路。
- **多语言幻觉的特殊挑战**: 跨语言迁移方法虽然提升了摘要性能，但会放大幻觉问题，需要专门的指标（如mFACT）来评估。
