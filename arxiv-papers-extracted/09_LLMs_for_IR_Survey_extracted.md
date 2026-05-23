---
title: "Large Language Models for Information Retrieval: A Survey"
authors: ["Yutao Zhu", "Huaying Yuan", "Shuting Wang", "Jiongnan Liu", "Wenhan Liu", "Chenlong Deng", "Haonan Chen", "Zheng Liu", "Zhicheng Dou", "Ji-Rong Wen"]
date: 2025-05-22
arxiv_id: "2505.17474"
org: "Renmin University of China; Beijing Academy of Artificial Intelligence"
---

## Abstract（摘要）

- **解决了什么问题**：信息检索（IR）系统从基于词项的方法到神经模型的演进过程中，面临数据稀缺、可解释性不足以及生成上下文看似合理但可能不准确响应等挑战。本综述系统梳理了大语言模型（LLMs）如何应用于改进IR系统的各个组件。

- **核心思路/方法**：对LLMs与IR系统的融合进行全面综述，按照IR系统的四个关键模块进行组织：查询重写器（Query Rewriter）、检索器（Retriever）、重排器（Reranker）和阅读器（Reader），并进一步探讨了利用LLMs作为搜索代理（Search Agent）的前沿方向。

- **主要结论**：LLMs在查询理解、语义匹配、细粒度排序和答案生成等方面显著提升了IR系统的性能。从查询重写到检索、重排序和阅读模块，LLMs通过先进的语言理解、语义表示和上下文处理能力丰富了IR流程的各个方面。搜索代理代表了未来IR的新范式。

## Methodology（方法论）

> 本论文为综述类型，以下总结其分类框架和分类方法。

### 整体分类框架

论文将LLMs在IR中的应用分为两大类：
1. **增强传统IR组件**：查询重写器、检索器、重排序器、阅读器
2. **搜索代理（Search Agent）**：LLMs作为自主代理执行多种IR任务

### 按模块详细分类

**1. 查询重写器（Query Rewriter，Section 3）**
- **场景**：Ad-hoc检索、对话式搜索
- **重写格式**：问题（Questions）、关键词（Keywords）、融入答案的段落（Answer-incorporated Passages）
- **方法**：
  - Prompting（零样本、少样本、Chain-of-Thought）
  - 监督微调（SFT）
  - 强化学习（RL），利用下游反馈信号（如排序分数、QA评估结果）作为奖励
- **代表方法**：HyDE、Query2Doc、BEQUE、LLMCS、CONVERSER等

**2. 检索器（Retriever，Section 4）**
- **利用LLMs生成搜索数据**：
  - 搜索数据精炼（Search Data Refinement）
  - 训练数据增强（Training Data Augmentation）：伪查询生成、相关性标签生成、完整样例生成
  - 代表方法：InPairs、Gecko、UDAPDR、SPTAR、ART等
- **利用LLMs作为检索器骨干网络**：
  - 稠密检索器（Dense Retriever）：RepLLaMA、NV-Embed、ChatRetriever等；改进现有能力和引入新能力（指令跟随、上下文学习、长度泛化）
  - 生成式检索器（Generative Retriever）：DSI、LLM-URL、CorpusLM等；通过微调LLMs或提示LLMs直接生成文档标识符

**3. 重排序器（Reranker，Section 5）**
- **有监督重排序器**：
  - 编码器型（monoBERT）
  - 编码器-解码器型（monoT5、DuoT5、RankT5、ListT5）
  - 解码器型（RankLLaMA、TSARankLLM、PE-Rank）
- **无监督重排序器**（通过Prompting）：
  - 逐点方法（Pointwise）：相关性生成、查询生成
  - 列表方法（Listwise）：RankGPT等，使用滑动窗口策略
  - 成对方法（Pairwise）：PRP等，使用排序算法聚合
- **利用LLMs进行训练数据增强**：ExaRanker、InPars-Light、RankVicuna、RankZephyr
- **推理密集型重排序器**（Reasoning-intensive Rerankers）：基于大型推理模型（LRMs，如DeepSeek-R1）的思路，通过蒸馏或强化学习注入推理能力；代表方法：ReasonRank、Rank1、Rank-R1、TFRank

**4. 阅读器（Reader，Section 6）**
- **被动阅读器（Passive Reader）**：
  - 一次检索阅读器（Once-Retrieval）：REALM、RAG、REPLUG、Atlas等
  - 周期性检索阅读器（Periodic-Retrieval）：RETRO、RALM、IRCoT等
  - 非周期检索阅读器（Aperiodic-Retrieval）：FLARE、Self-RAG
- **主动阅读器（Active Reader）**：SelfAsk、DSP、PlanRAG等，LLMs主动向搜索引擎发起查询
- **压缩器（Compressor）**：抽取式（LeanContext、RECOMP、FILCO）和生成式（TCRA、xRAG）方法压缩检索到的文档

**5. 搜索代理（Search Agent，Section 7）**
- **架构**：单代理框架（Search-R1、ReSearch、R1-Searcher、Atom-Searcher）、多代理框架（MindSearch、KwaiAgents、Alita、OWL）
- **信息获取模块**：基于API的方法、基于浏览的方法
- **优化方法**：策略性检索优化（Strategic Retrieval Optimization）、迭代检索调优（Iterative Retrieval Tuning）、自主开放网络搜索（Autonomous Open-Web Search）
- **基准与资源**：QA基准（单跳QA、多跳QA、专家级挑战）、任务导向基准、代理数据集和平台

## Contribution（贡献）

- **系统性综述框架**：提出了按IR系统四大核心模块（查询重写器、检索器、重排序器、阅读器）组织LLM4IR研究的分类框架，覆盖了从查询理解到答案生成的完整IR流程。
- **搜索代理前瞻**：首次在综述中系统性地梳理了利用LLMs作为搜索代理的前沿研究，包括单代理/多代理架构、信息获取模块、优化方法等，指出这是未来IR的新范式。
- **推理密集型重排序的纳入**：涵盖了基于大型推理模型（LRMs）的最新研究进展，如通过强化学习和蒸馏将推理能力注入重排序器。
- **对未来方向的全面展望**：从查询重写、检索、重排序、阅读、搜索代理、评估和偏差七个维度详细讨论了未来研究方向。
- **配套资源**：创建了GitHub仓库（https://github.com/RUC-NLPIR/LLM4IR-Survey）持续收集相关论文和资源。

## Limitation（局限性）

### 论文自身承认的各模块局限性

**查询重写器**：
- **概念漂移（Concept Drifts）**：LLMs的知识库过于庞大，可能引入不相关信息，导致查询偏离原始意图。
- **检索性能与扩展效果的负相关**：扩展查询往往能提升弱模型的得分，但对强模型反而有负面影响。

**检索器**：
- LLMs参数量巨大、推理时间过长，难以满足检索器快速响应的需求。
- LLMs生成的伪查询与真实用户查询之间存在不匹配，可能影响检索效果。
- LLMs通常缺乏领域特定知识，需要高效的微调策略。

**重排序器**：
- 依赖API调用和大量参数，LLM排序过程成本高且效率低。
- 列表方法存在位置偏差（positional bias），文档顺序打乱后性能甚至低于BM25。
- 现有研究主要聚焦于开放域数据集（如MSMARCO），对领域内数据集、非标准排序数据集和推理密集型数据集的适应性有待探索。

**阅读器**：
- 面临有效查询重构、最优检索频率、正确文档理解、准确段落提取和有效内容摘要等挑战。
- LLMs即使有额外参考文档也可能生成不忠实答案，可靠性问题仍存在。

**搜索代理**：
- 需要确保检索文档的有效性，否则不可靠信息可能加剧LLM的幻觉问题。
- LLM输出中可能存在偏见和攻击性内容。

**评估**：
- 传统排序评估指标（如nDCG、MRR）无法衡量文档在答案生成中的作用。
- 文本生成评估依赖词法匹配，无法评估事实性和细微语义差异。
- IR系统中存在对LLM生成文本的"源偏差"（source bias）问题。

## Evaluation（评估）

### 使用的数据集

- **排序任务**：MS MARCO（Passage Ranking、Document Ranking）、TREC-DL 2019、TREC-DL 2020、BEIR
- **嵌入/检索基准**：MTEB（Massive Text Embedding Benchmark）
- **QA任务**：Natural Questions（NQ）、TriviaQA、HotpotQA、2WikiMultiHopQA、SimpleQA、PopQA
- **专家级基准**：HLE（Humanity's Last Exam）、BrowseComp
- **推理密集型基准**：BRIGHT、R2MED
- **代理评估**：GAIA、AssistantBench、WebArena、SWE-bench、RE-Bench、WebWalkerQA
- **任务导向基准**：Magnetic-One、MLE-bench、MLAgentBench、RESEARCHTOWN、SpaBench

### 评估指标

- **排序评估**：NDCG@10、MRR（Mean Reciprocal Rank）、MAP（Mean Average Precision）、Precision、Recall
- **生成评估**：BLEU、ROUGE（论文指出这些指标存在依赖词法匹配、对细微差异不敏感、无法评估事实性等局限）

### 关键实验结果（论文中引用的代表性结果）

- 在TREC-DL19上，BM25基线NDCG@10为50.58；有监督方法monoBERT达到70.50，monoT5达到71.48；无监督方法RankGPT-3.5（使用ChatGPT）达到75.59，PRP-Allpair（FLAN-UL2 20B）达到71.88。
- LLM-based嵌入器（如RepLLaMA）已主导MTEB等主要文本检索基准。
- RepLLaMA的单独第一阶段检索精度已超过传统方法的多阶段检索精度。
- 生成式检索器在大规模文档语料上的覆盖仍具挑战性；更多模型参数通常带来更好性能。

## Key Insights（关键洞察）

### 可借鉴的方法思路

- **LLM作为数据增强引擎**：利用LLMs生成伪查询、相关性标签和完整训练样例来增强检索模型训练数据，是解决领域标注数据不足的有效范式。其中"生成-过滤"迭代范式（如round-trip filtering）可显著提升合成数据质量。
- **Prompting的三种策略层次**：零样本、少样本和Chain-of-Thought在查询重写和重排序中各有适用场景；CoT特别适合对话式搜索的多轮查询重写。
- **无监督重排序的三种范式对比**：逐点方法效率高但性能一般、列表方法性能好但存在位置偏差且成本高、成对方法在小模型（20B）上即可达到竞争力结果。
- **RAG的多层次检索策略**：一次检索、周期性检索、非周期性检索各有适用场景；主动阅读器让LLM自主发起检索是更接近人类信息获取方式的新范式。
- **知识蒸馏降低部署成本**：将大型LLM的排序能力蒸馏到小模型（如RankVicuna、RankZephyr）是缓解API成本和推理延迟的有效路径。
- **强化学习优化查询生成**：DeepRetrieval等方法使用检索指标作为奖励，无需监督数据即可训练查询生成器。
- **推理模型的新范式**：大型推理模型（LRMs，如DeepSeek-R1）的逐步推理链能力为重排序器带来了新的优化思路，通过RL或蒸馏可将推理能力注入排序模型。

### 对本研究的启发

- 该综述为理解LLMs在IR各环节的应用提供了完整的分类体系，可作为研究LLM-enhanced IR的路线图。
- 搜索代理代表了从"检索-排序"到"自主搜索与推理"的范式转变，是未来IR研究的重要方向。
- 推理密集型重排序（Reasoning-intensive Reranking）是一个新兴且快速发展的方向，结合LRMs的推理能力和IR的排序需求，具有很大研究潜力。
- 评估体系的革新（从排序评估到生成评估、从相关性到有用性）是LLM时代IR研究的关键挑战之一。
