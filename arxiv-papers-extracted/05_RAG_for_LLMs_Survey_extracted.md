---
title: "Retrieval-Augmented Generation for Large Language Models: A Survey"
authors: ["Yunfan Gao", "Yun Xiong", "Xinyu Gao", "Kangxiang Jia", "Jinliu Pan", "Yuxi Bi", "Yi Dai", "Jiawei Sun", "Meng Wang", "Haofen Wang"]
date: 2024-03-28
arxiv_id: "2312.10997"
org: "Tongji University, Fudan University"
---

## Abstract（摘要）

- **解决的问题**：大语言模型（LLMs）存在幻觉（hallucination）、知识过时、推理过程不透明且不可追溯等问题，尤其在知识密集型任务中表现不佳。
- **核心思路/方法**：通过检索增强生成（RAG），从外部数据库引入知识以增强LLM的准确性和可信度，实现参数化知识与非参数化外部知识的协同融合。
- **主要结论**：系统梳理了RAG的三大范式演进（Naive RAG、Advanced RAG、Modular RAG），深入分析了"检索-生成-增强"三大核心组件的关键技术，总结了26个下游任务、近50个数据集及评估框架，并指出了未来研究方向。

## Methodology（方法论）

本文为综述型论文，其分类框架和方法总结如下：

### 三大RAG范式分类

1. **Naive RAG（朴素RAG）**
   - 最早的方法论，遵循"Retrieve-Read"框架
   - 流程：索引（Indexing）→ 检索（Retrieval）→ 生成（Generation）
   - 索引阶段：原始数据清洗、文本分块、向量编码、存入向量数据库
   - 检索阶段：查询向量化、相似度计算、Top-K检索
   - 生成阶段：查询+检索文档合成prompt，LLM生成回答
   - 局限：检索精度和召回不足、幻觉问题、冗余信息干扰

2. **Advanced RAG（高级RAG）**
   - 针对Naive RAG不足提出改进，仍保持链式结构
   - **预检索优化**：索引结构优化（数据粒度增强、元数据附加、混合检索）和查询优化（查询改写、查询变换、查询扩展）
   - **后检索优化**：重排序（Reranking）和上下文压缩（Context Compression），减少信息过载

3. **Modular RAG（模块化RAG）**
   - 最大灵活性和适应性，继承并发展前两种范式
   - **新模块**：搜索模块（Search）、RAGFusion多查询策略、记忆模块（Memory）、路由模块（Routing）、预测模块（Predict）、任务适配模块（Task Adapter）
   - **新模式**：Rewrite-Retrieve-Read、Generate-Read、ReciteRead、Demonstrate-Search-Predict（DSP）、ITER-RETGEN迭代式检索生成
   - 支持自适应检索（FLARE、Self-RAG）和与微调/强化学习的集成

### 三大核心组件技术细节

**检索（Retrieval）**：
- 检索来源：非结构化文本、半结构化数据（PDF）、结构化数据（知识图谱）、LLM自身生成内容
- 检索粒度：Token → Phrase → Sentence → Proposition → Chunk → Document（文本），Entity → Triplet → Sub-Graph（KG）
- 索引优化：分块策略（固定分块、滑动窗口、Small2Big）、元数据附件、结构化索引（层级索引、知识图谱索引）
- 查询优化：查询扩展（Multi-Query、Sub-Query、CoVe）、查询变换（Query Rewrite、HyDE、Step-back Prompting）、查询路由（元数据路由、语义路由）
- 嵌入：稀疏编码（BM25）与密集检索（BERT系列PLM），混合检索策略
- 微调嵌入模型：LSR（LM-supervised Retriever）、PROMPTAGATOR、LLM-Embedder
- 适配器（Adapter）：UPRISE、AAR、PRCA、BGM

**生成（Generation）**：
- 上下文筛选（Context Curation）：重排序（规则方法和模型方法）、上下文选择/压缩（LLMLingua、PRCA、RECOMP）
- LLM微调：领域适配微调、SANTA框架（三阶段训练）、强化学习对齐、知识蒸馏、协调检索器和生成器的联合微调（RA-DIT）

**增强过程（Augmentation）**：
- 迭代检索（Iterative Retrieval）：反复搜索知识库，如ITER-RETGEN
- 递归检索（Recursive Retrieval）：逐步细化查询，如IRCoT（CoT引导检索）、ToC（澄清树）
- 自适应检索（Adaptive Retrieval）：LLM自主决定检索时机，如FLARE（基于生成置信度触发）、Self-RAG（反射token控制）

## Contribution（贡献）

1. **系统性综述**：对RAG方法进行了全面系统的回顾，划分为Naive RAG、Advanced RAG和Modular RAG三大范式，将RAG研究置于LLM发展大背景下进行语境化分析。
2. **核心技术剖析**：识别并深入讨论了RAG过程中"检索"、"生成"和"增强"三大核心组件的关键技术，阐明了各组件如何协同工作形成有效的RAG框架。
3. **评估体系总结**：系统梳理了RAG的评估方法，覆盖26个任务、近50个数据集，概述了评估目标、指标、基准和工具，并展望了RAG的未来发展方向。

## Limitation（局限性）

论文指出的当前RAG面临的挑战和未解决问题：

1. **RAG vs 长上下文**：随着LLM上下文窗口扩展至200K+ token，RAG的必要性受到讨论。虽然RAG仍有不可替代的优势（效率、可追溯性），但在超长上下文场景下需要新的RAG方法。
2. **鲁棒性不足**：检索中噪声或矛盾信息会损害输出质量（"错误信息比没有信息更糟糕"），需要更强的抗对抗/反事实输入能力。
3. **混合方法的最佳集成方式未确定**：RAG与微调的最优整合方式（顺序、交替、端到端联合训练）仍需探索。
4. **RAG的缩放定律不确定**：LLM的缩放定律是否适用于RAG模型尚不明确，参数量仍落后于LLM。
5. **工程化挑战**：检索效率、大规模知识库文档召回、数据安全（防止LLM泄露文档来源/元数据）等工程问题尚未解决。
6. **多模态RAG仍处于早期**：图像、音频、视频等多模态RAG正在扩展，但尚不成熟。
7. **评估标准化不足**：现有评估指标多为传统度量，尚未形成成熟、标准化的RAG评估方法。

## Evaluation（评估）

### 下游任务与数据集
综述覆盖26个下游任务，主要包括：
- **问答（QA）**：单跳QA（Natural Questions、TriviaQA、SQuAD、WebQuestions、PopQA、MS MARCO）、多跳QA（HotpotQA、2WikiMultiHopQA、MuSiQue）、长文本QA（ELI5、NarrativeQA、ASQA、QMSum）、领域QA（Qasper、COVID-QA、CMB）、多选QA（QuALITY、ARC、CommonsenseQA）、图谱QA（GraphQA）
- **对话**：对话生成（Wizard of Wikipedia）、个人对话（KBP、DuleMon）、任务导向对话（CamRest）、推荐（Amazon）
- **信息抽取**：事件参数抽取（WikiEvent、RAMS）、关系抽取（T-REx、ZsRE）
- **推理**：常识推理（HellaSwag）、CoT推理、复杂推理（CSQA）
- **其他**：语言理解（MMLU）、语言建模（WikiText-103）、事实验证（FEVER、PubHealth）、文本生成（Biography）、文本摘要（WikiASP、XSum）、文本分类、代码搜索（CodeSearchNet）、数学（GSM8K）、机器翻译（JRC-Acquis）

### 评估指标
- **检索质量**：Hit Rate、MRR、NDCG、Recall、Precision
- **生成质量**：EM（Exact Match）、F1、BLEU、ROUGE/ROUGE-L、Accuracy、Cosine Similarity
- **质量评分维度**：上下文相关性（Context Relevance）、答案忠实度（Faithfulness）、答案相关性（Answer Relevance）
- **能力评估维度**：噪声鲁棒性（Noise Robustness）、负面拒绝（Negative Rejection）、信息整合（Information Integration）、反事实鲁棒性（Counterfactual Robustness）

### 评估基准与工具
- **基准（Benchmarks）**：RGB（评估噪声鲁棒性、负面拒绝、信息整合、反事实鲁棒性）、RECALL（评估反事实鲁棒性）、CRUD（评估知识密集型QA、纠错、摘要）
- **工具（Tools）**：RAGAS（基于LLM评判质量评分）、ARES（使用LLM判断各评估方面）、TruLens（RAG三元组评估）

## Key Insights（关键洞察）

1. **RAG范式的演进逻辑**：从Naive RAG到Advanced RAG再到Modular RAG，体现了从简单"检索-读取"到多模块灵活编排的进化，Modular RAG的核心思想是模块可替换、流程可重组、支持迭代/自适应检索。
2. **检索优化的多层次策略**：预检索（索引优化+查询优化）→ 后检索（重排序+压缩）→ 增强过程（迭代/递归/自适应），形成完整优化链路。
3. **RAG与微调互补而非互斥**：RAG擅长动态知识更新和精确信息检索，微调擅长深层次的模型行为和风格定制，两者可在不同层面互补增强。
4. **自适应检索是重要趋势**：让LLM自主判断何时需要检索（如Self-RAG的反射token、FLARE的置信度阈值），将RAG从被动工具提升为主动智能体行为。
5. **评估体系的系统性**：不仅评估下游任务性能，还需关注检索质量、生成质量、噪声鲁棒性等多个维度，RAGAS/ARES/TruLens等自动化评估工具值得关注。
6. **多模态扩展**：RAG已从纯文本扩展到图像（RA-CM3、BLIP-2）、音频、视频、代码等多模态场景，是多模态AI的重要技术路径。
7. **工程生态发展**：LangChain、LlamaIndex等工具栈的成熟推动了RAG的实际部署，未来趋向定制化、简易化和专业化。
