---
title: "Graph Retrieval-Augmented Generation: A Survey"
authors: ["Boci Peng", "Yun Zhu", "Yongchao Liu", "Xiaohe Bo", "Haizhou Shi", "Chuntao Hong", "Yan Zhang", "Siliang Tang"]
date: 2024-09-01
arxiv_id: "2408.08515"
org: "Peking University, Zhejiang University, Ant Group, Renmin University of China, Rutgers University"
---

## Abstract（摘要）
- **解决了什么问题**：传统RAG（检索增强生成）在处理复杂关系型知识时存在三个核心局限：(1) 忽视实体间的关系（Neglecting Relationships）；(2) 检索结果存在冗余信息（Redundant Information），导致"lost in the middle"问题；(3) 缺乏全局信息（Lacking Global Information），难以应对Query-Focused Summarization（QFS）等任务。GraphRAG利用图结构信息实现更精确和全面的检索，以解决上述问题。
- **核心思路/方法**：提出GraphRAG的统一工作流，将其分解为三个阶段：Graph-Based Indexing（G-Indexing）、Graph-Guided Retrieval（G-Retrieval）和Graph-Enhanced Generation（G-Generation）。系统性地分类和总结每个阶段的核心技术、训练方法和增强策略。
- **主要结论**：GraphRAG通过利用图中关键的关系型知识，显著提升了信息检索的相关性、准确性和全面性，有效克服了传统RAG的关键局限。GraphRAG仍是一个新兴领域，需要更多研究来推进其发展。

## Methodology（方法论）

本文为综述类型论文，其方法论主要体现在对GraphRAG领域的分类框架和系统化梳理上。

### 整体框架
GraphRAG的目标函数可形式化为：给定查询q和文本属性图G，通过图检索器p_θ(G*|q,G)和答案生成器p_φ(a|q,G*)联合建模目标分布p(a|q,G)。整个流程分为三个核心阶段：

### 1. Graph-Based Indexing（G-Indexing）
图数据库的构建和索引，是GraphRAG的基础。

- **图数据来源**分为两大类：
  - **开放知识图谱**：包括通用知识图谱（如Wikidata、Freebase、DBpedia、YAGO、ConceptNet、ATOMIC）和领域知识图谱（如CMeKG、CPubMed-KG、Wiki-Movies）
  - **自构建图数据**：从文档、表格等非图数据源构建图，如文档图、实体关系图、专利短语图等

- **索引方法**分为四种：
  - **图索引（Graph Indexing）**：保留完整图结构，支持BFS、最短路径等图搜索算法
  - **文本索引（Text Indexing）**：将图数据转换为文本描述，利用稀疏/稠密检索
  - **向量索引（Vector Indexing）**：将图数据转化为向量表示，支持LSH等高效搜索
  - **混合索引（Hybrid Indexing）**：结合上述多种索引方法

### 2. Graph-Guided Retrieval（G-Retrieval）
从图数据库中提取与查询相关的信息，面临两个核心挑战：候选子图爆炸性增长和文本-图相似度度量不足。

- **检索器（Retriever）分类**：
  - **非参数检索器（Non-parametric）**：基于启发式规则或传统图搜索算法，效率高但准确性可能不足
  - **基于语言模型的检索器（LM-based）**：利用判别式或生成式LM进行检索，自然语言理解能力强
  - **基于GNN的检索器（GNN-based）**：擅长理解和利用复杂图结构
  - **混合检索器**：多阶段策略结合不同类型检索器

- **检索范式（Retrieval Paradigm）**：
  - **一次性检索（Once Retrieval）**：单次查询获取所有相关信息
  - **迭代检索（Iterative Retrieval）**：分为非自适应和自适应两种，后续检索依赖先前结果
  - **多阶段检索（Multi-Stage Retrieval）**：线性分为多个阶段，不同阶段使用不同检索器

- **检索粒度（Retrieval Granularity）**：
  - **节点（Nodes）**：精确检索单个元素
  - **三元组（Triplets）**：以主-谓-宾结构表示关系数据
  - **路径（Paths）**：捕获实体间关系序列
  - **子图（Subgraphs）**：捕获全面的关系上下文
  - **混合粒度（Hybrid）**：结合多种粒度

- **检索增强（Retrieval Enhancement）**：
  - **查询增强**：查询扩展（Query Expansion）和查询分解（Query Decomposition）
  - **知识增强**：知识合并（Knowledge Merging）和知识剪枝（Knowledge Pruning），包括重排序和LLM-based剪枝

### 3. Graph-Enhanced Generation（G-Generation）
将检索到的图数据与查询结合以生成响应。

- **生成器（Generator）分类**：
  - **GNNs**：适用于判别式任务，直接编码图数据
  - **LMs**：包括encoder-only（如BERT，用于判别式任务）、encoder-decoder和decoder-only（如GPT-4、LLaMA，用于生成式任务）
  - **混合模型（Hybrid Models）**：级联范式（Cascaded，GNN输出作为LM输入）和并行范式（Parallel，GNN和LM并行处理后合并输出）

- **图格式（Graph Formats）**——将图数据转换为LM可处理的形式：
  - **图语言（Graph Languages）**：邻接/边表、自然语言、代码形式（GML/GraphML）、语法树、节点序列
  - **图嵌入（Graph Embeddings）**：使用GNN将图表示为嵌入向量，通过prompt tuning或FiD方法与文本表示整合

- **生成增强（Generation Enhancement）**：
  - **预生成增强**：语义丰富化检索到的图数据，如用LLM重写图数据
  - **中生成增强**：生成过程中调整策略，如约束解码、多步推理
  - **后生成增强**：整合多个生成响应，如社区摘要排序、子问题答案合并、多模型输出融合

### 4. 训练策略
- **无训练（Training-Free）**：依赖精心设计的prompt控制LLM的检索和生成能力
- **有训练（Training-Based）**：包括检索器的远程监督训练、自监督预训练、强化学习训练；生成器的SFT微调和专用损失函数训练
- **联合训练**：统一模型同时优化检索和生成目标，或交替训练检索器和生成器

## Contribution（贡献）
- 提供了GraphRAG领域首个全面系统性综述，给出了GraphRAG的形式化定义，明确了包含G-Indexing、G-Retrieval、G-Generation三个阶段的通用工作流
- 系统讨论了GraphRAG各阶段（G-Indexing、G-Retrieval、G-Generation）的核心技术，分析了模型选择、方法设计和增强策略，并对比了各模块的训练方法
- 梳理了GraphRAG的下游任务、基准评测、应用领域、评估指标和工业系统，讨论了当前挑战和未来研究方向
- 建立了持续更新的仓库 https://github.com/pengboci/GraphRAG-Survey 以追踪该领域最新进展

## Limitation（局限性）
论文指出的现有GraphRAG领域的局限性和未来挑战包括：
- **动态图处理**：大多数GraphRAG方法基于静态数据库，难以快速更新新出现的实体和关系
- **多模态信息整合**：现有知识图谱主要以文本为主，缺乏图像、音频、视频等多模态信息
- **可扩展高效检索**：工业级知识图谱可能包含数百万甚至数十亿实体，现有方法主要针对小规模知识图谱
- **图基础模型结合**：如何将图基础模型有效集成到GraphRAG流程中仍待探索
- **检索上下文的无损压缩**：检索到的图信息转换为长序列后，LLM难以处理，需要有效的无损压缩技术
- **缺乏标准基准**：GraphRAG缺乏统一标准的基准评测
- **应用范围有限**：当前应用主要集中在客服系统、推荐系统、KBQA等，有待扩展到医疗、金融、法律、智慧城市等更广泛领域

## Evaluation（评估）

### 使用的数据集
- **KBQA**：WebQSP、WebQ、CWQ、GrailQA、QALD10-en、SimpleQuestions、MetaQA、Natural Questions、TriviaQA、HotpotQA、Mintaka、FreebaseQA等
- **CSQA**：CSQA（CommonsenseQA）、OBQA（OpenBookQA）、MedQA、SocialIQA、PIQA、RiddleSenseQA
- **信息抽取**：ZESHEL、CoNLL（实体链接）；T-Rex、ZsRE（关系抽取）
- **其他**：Creak、FACTKG（事实验证）；FB15K-237、FB15k、WN18RR、NELL995（链接预测）；OpenDialKG（对话系统）；Yelp（推荐）
- **GraphRAG专用基准**：STARK、GraphQA、GRBENCH、CRAG

### 评估指标
- **下游任务评估（生成质量）**：Accuracy、Exact Match（EM）、F1、Recall、BERTScore、GPT-4 Average Ranking、BLEU、ROUGE-L、METEOR、Hits@K、MRR、NDCG@K
- **检索质量评估**：答案覆盖率与检索子图大小的比率、查询相关性（query relevance）、多样性（diversity）、忠实度评分（faithfulness score）

### 关键实验结果
作为综述论文，本文未报告具体实验数值结果，但通过Table 1系统汇总了各方法在各基准数据集上使用的评测指标，涵盖了数十篇GraphRAG相关论文的方法-数据集-指标对应关系。

## Key Insights（关键洞察）
- **图结构信息的价值**：GraphRAG的核心优势在于利用实体间的显式关系（而非仅依赖语义相似度），能捕获传统文本RAG无法表示的结构化关系知识，这对于需要多跳推理的场景尤为重要
- **检索粒度的权衡**：不同检索粒度（节点、三元组、路径、子图）在检索效率和上下文完整度之间需要平衡，复杂场景推荐使用混合粒度方法
- **图格式转换是关键环节**：将图数据转换为LLM可理解的形式是GraphRAG的独特挑战，图语言（自然语言、代码形式、语法树等）和图嵌入各有优劣，前者直观但可能过长，后者紧凑但难以保留精确信息
- **工业界实践参考**：微软GraphRAG、Neo4j NaLLM/LLM Graph Builder、NebulaGraph GraphRAG、蚂蚁集团GraphRAG等工业系统的技术路线为实际应用提供了直接参考
- **对本研究启发**：在构建RAG系统时，应考虑引入图结构来增强关系推理能力；检索阶段可结合多种检索器（非参数+LM+GNN）以平衡效率和准确性；图数据的构建可以从文档中自动抽取实体和关系来形成知识图谱
