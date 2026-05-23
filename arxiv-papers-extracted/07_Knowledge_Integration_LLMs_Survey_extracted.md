---
title: "Trends in Integration of Knowledge and Large Language Models: A Survey and Taxonomy of Methods, Benchmarks, and Applications"
authors: ["Zhangyin Feng", "Weitao Ma", "Weijiang Yu", "Lei Huang", "Haotian Wang", "Qianglong Chen", "Weihua Peng", "Xiaocheng Feng", "Bing Qin", "Ting Liu"]
date: 2024-10-23
arxiv_id: "2311.05876"
org: "Harbin Institute of Technology"
---

## Abstract（摘要）
- **解决的问题**：LLMs在知识密集型任务中存在知识过时、长尾知识学习困难、幻觉（hallucination）等问题，现有知识编辑（Knowledge Editing）和检索增强（Retrieval Augmentation）两类方法的研究缺乏系统性综述。
- **核心思路/方法**：对知识与大语言模型整合的研究进行全面综述，提出了涵盖方法分类法（taxonomy）、基准数据集（benchmarks）和应用场景的完整框架。核心将方法分为两大方向——知识编辑（修改模型参数或输入来更新知识）和检索增强（在推理阶段利用外部知识而不修改参数）。
- **主要结论**：提供了该领域的系统分类与方法对比，指出了多源知识增强、多模态LLM知识整合、基于LLM的智能体（Agent）、知识增强方法分析等未来研究方向。

## Methodology（方法论）

> 本文为综述论文，方法论部分总结其分类框架和分类方法。

### 总体分类框架
论文将"知识与大语言模型整合"方法分为两大方向：

#### 一、知识编辑（Knowledge Editing, §2）
按照模型处理结构划分为三个层面：
- **输入编辑（Input Editing, §2.1）**
  - **Prompt Augmented（提示增强）**：通过在提示中加入外部知识来增强LLM，如IKE（设计copy/update/retain三类提示）、SuperICL（引入小模型作为插件增强ICL）、PKG（训练辅助参数知识引导框架生成背景文档）、KAPING（从知识图谱检索相关事实整合到提示中）。
  - **Prompt Editing（提示编辑）**：通过解构和精炼提示来提升LLM回答准确性，如MemPrompt（结合用户反馈记忆改进提示）、PACE（利用LLM自身判断批评和精炼提示）、MeLLo（将原始问题分解为子问题并基于自检机制调整输出）。
- **模型编辑（Model Editing, §2.2）**
  - **Knowledge Plug-in（知识插件）**：引入外部参数插件编辑LLM而不改变原始权重。如NKB/CALINET（调整FFN输出的额外记忆槽）、SERAC（维护范围分类器和反事实模型）、T-Patcher（为每个错误添加可训练补丁到最后一层FFN）、GRACE（通过适配器中的离散码本实现序列编辑）。
  - **Locate-then-Edit（定位-编辑）**：先定位存储知识的具体参数，再进行针对性修改。如KN（基于积分梯度评估知识神经元贡献）、ROME（引入因果重要性计算并插入新的键值对向量）、MEMIT（基于ROME扩展到同时处理数千条编辑）、PMET（同时优化MHSA和FFN的隐藏状态）。
  - **Overall Editing（整体编辑）**：直接修改模型而不定位特定参数。如KE（训练双向LSTM超网络预测参数更新）、MEND（使用梯度低秩分解优化超网络学习）、Task Arithmetic（通过任务向量进行模型编辑）。
- **知识编辑评估（Assess Knowledge Editing, §2.3）**
  - 三大评估属性：**可靠性（Reliability）**——编辑后模型对编辑输入产生正确预测的成功率；**泛化性（Generality）**——编辑后模型能否同步更新相关事实（含portability、多跳问题等评估）；**局部性（Locality）**——编辑是否保留与编辑事实无关的知识。
  - 基准数据集：ZsRE、CounterFact、CounterFact+、Bi-ZsRE、MQUAKE、RippleEdits、Eva-KELLM、KLoB。

#### 二、检索增强（Retrieval Augmentation, §3）
围绕四个关键问题展开：
- **检索判断（Retrieval Judgement, §3.1）**——何时触发检索？
  - **基于校准的方法**：设定度量指标和阈值（如实体流行度、token概率/置信度）来决定是否检索，如FLARE（基于置信度的主动检索）。
  - **基于模型的方法**：分为普通设定（直接判断是否需要检索，如LLM自评）和检索设定（先检索再判断文档相关性，如用NLI模型识别不相关文档）。
- **文档检索（Document Retrieval, §3.2）**——如何检索相关文档？
  - **基于检索器的方法**：稀疏检索器（BM25/TF-IDF）、稠密检索器（DPR，将文本编码到连续语义空间）、商业搜索引擎。还涉及将检索器适配到LLM的方法（如REPLUG LSR用黑盒LLM信号改进检索模型、AAR利用小源LM提供偏好信号训练检索器、Query2doc生成伪文档扩展查询、Rewrite-Retrieve-Read框架重写查询）。
  - **基于LLM的方法（生成式检索）**：生成文档标识符（如GENRE、DSI、SEAL、Multiview）或直接生成完整文档（如GENREAD、RECITE、PKG、COOK）。
- **文档利用（Document Utilization, §3.3）**——如何利用检索到的文档？
  - **输入增强（Input Enhancement）**：将检索文档作为输入提示的一部分（如简单前缀拼接或REPLUG并行编码集成方案）。
  - **推理验证（Reasoning Verification）**：用检索知识引导链式推理过程（如IRCoT交织检索与CoT、Self-ask分步子问题检索、ReAct交替推理与行动、Verify-and-Edit后编辑推理链）。
  - **回答验证（Answer Verification）**：对LLM已有回答进行后处理修正（如RR用推理步骤检索知识验证、RARR检索证据后修订文本保持风格、LLM-AUGMENTER检索证据链验证候选响应）。
- **知识冲突（Knowledge Conflict, §3.4）**——如何解决不同来源的知识矛盾？
  - **内部冲突（Internal Conflict）**：LLM参数化知识与检索文档之间的不一致。方法包括反事实上下文微调、提示策略改进上下文忠实性。
  - **外部冲突（External Conflict）**：多个检索文档之间的不一致。研究表明模型倾向于选择与参数化知识一致的答案。
- **基准数据集（Benchmark, §3.5）**
  - Single-hop QA：NQ、TriviaQA、PopQA
  - Multi-hop QA：HotPotQA、2WikiMultiHopQA、MuSiQue、Bamboogle
  - Fact Verification：FeVer、FEVEROUS、FoolMeTwice
  - Complex Reasoning：StrategyQA、CommonsenseQA/2.0、CSQA、TempQuestions、INFOTABS

## Contribution（贡献）
- 提供了知识与大语言模型整合领域的首个系统性综述，涵盖知识编辑和检索增强两大方向的完整分类法。
- 对不同方法进行了深入分析和对比，覆盖方法、基准数据集和前沿应用三个维度。
- 指出了多源知识增强、多模态LLM知识整合、LLM智能体、知识增强方法分析等未来研究方向。
- 与已有综述的区别：相比Hu et al. (2023)专注于小规模预训练语言模型、Yao et al. (2023b)仅关注知识编辑、Zhang et al. (2023b)侧重知识更新策略，本文提供了对知识编辑和检索增强两大方向的深度详细分析。

## Limitation（局限性）
- 论文指出当前知识编辑方法主要围绕三元组事实知识，限制了可编辑知识的范围。
- 当前检索增强方法主要关注从Wikipedia或Web检索非结构化文本，知识来源和格式较为单一。
- 知识冲突问题目前仅有分析性研究，尚未提出有效的解决方案。
- 当前知识增强方法主要关注生成结果，其他方面（如副作用分析）仍需深入研究。
- 现有方法在实际复杂场景中的有效性有待验证，如LLM在多源、多格式证据整合方面的能力不足。
- 知识定位方法的选择（知识存储参数与可高效编辑参数不一定相同）仍是一个未解决的问题。

## Evaluation（评估）

### 知识编辑评估
- **数据集**：ZsRE、CounterFact、CounterFact+、Bi-ZsRE、MQUAKE、RippleEdits、Eva-KELLM
- **评估指标**：Reliability（可靠性）、Generality（泛化性）、Locality（局部性），部分还包括Portability（可移植性）和Cross-Lingual（跨语言）
- **关键发现**：当前方法难以将编辑知识从一种语言有效迁移到另一种语言；知识编辑可能导致模型整体鲁棒性下降。

### 检索增强评估
- **数据集**：
  - Single-hop QA：Natural Questions、TriviaQA、PopQA
  - Multi-hop QA：2WikiMultiHopQA、HotPotQA、MuSiQue、Bamboogle
  - Fact Verification：FeVer、FEVEROUS、FoolMeTwice
  - Complex Reasoning：StrategyQA、CommonsenseQA、CommonsenseQA2.0、CSQA、TempQuestions、INFOTABS
- **评估指标**：EM（Exact Match）、F1、Accuracy、ROUGE
- **关键发现**：LLMs在处理知识冲突时表现出强烈的确认偏差（confirmation bias），倾向于依赖参数化记忆；随着无关证据数量增加，LLM过滤无关证据的能力下降。

## Key Insights（关键洞察）
- **知识编辑 vs 检索增强的互补性**：知识编辑适合持久性地更新模型内部知识，检索增强适合在推理时灵活引入外部知识而不修改参数，两者解决不同层面的知识整合问题。
- **可借鉴的分类思路**：知识编辑按"输入-模型-评估"三层面分类，检索增强按"判断-检索-利用-冲突"四环节分类，这一框架可作为设计知识整合系统的参考。
- **知识冲突是重要但尚未解决的问题**：LLM在面对参数化知识与外部知识矛盾时表现出强烈的确认偏差，未来需要从数据过滤和模型微调等角度解决。
- **多源异构知识整合是重要方向**：现实场景中需要整合不同来源、不同格式的知识证据，当前方法在此方面能力有限。
- **知识编辑的鲁棒性风险**：编辑知识可能对模型整体鲁棒性产生负面影响，在实际部署中需要谨慎评估。
- **对RAG系统设计的启发**：检索判断（何时检索）、文档检索（如何检索）、文档利用（如何使用检索结果）三个环节可以独立优化，也可以联合优化。
