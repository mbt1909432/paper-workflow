---
title: "Trustworthiness in Retrieval-Augmented Generation Systems: A Survey"
authors: ["Yujia Zhou", "Wenbo Zhang", "Jingying Shao", "Yan Liu", "Xiaoxi Li", "Jiajie Jin", "Hongjin Qian", "Zheng Liu", "Chaozhuo Li", "Jason Chen Zhang", "Zhicheng Dou", "Philip S. Yu", "Jiaxin Mao"]
date: 2025-05-01
arxiv_id: "2505.13420"
org: "Renmin University of China / Tsinghua University / Microsoft Research Asia / Hong Kong Polytechnic University / University of Illinois"
---

## Abstract（摘要）

- **解决了什么问题**: RAG（检索增强生成）系统已成为LLM的重要范式，但现有研究主要关注准确性和效率，对RAG系统的可信性（trustworthiness）缺乏系统性研究。不可靠的检索或不当的知识利用可能导致有害输出。
- **核心思路/方法**: 提出**Trust-RAG Compass**统一框架，从六个关键维度评估RAG系统的可信性：事实性（Factuality）、鲁棒性（Robustness）、公平性（Fairness）、透明性（Transparency）、问责性（Accountability）和隐私性（Privacy）。同时引入**TRC Bench**评测基准，对19个LLM进行综合评估。
- **主要结论**: 商有模型在大多数维度上优于开源模型；经过指令微调和对齐的模型可信性更高；更大的参数量不一定带来更好的可信性；隐私和公平性是所有LLM共同面临的突出挑战。

## Methodology（方法论）

> 本文为综述论文，方法论部分总结其分类框架和分类方法。

- **统一框架（Trust-RAG Compass）**: 定义了RAG系统可信性的六个维度，每个维度包含通用定义（针对LLM）和RAG特定定义。

- **六维度分类框架**:
  1. **事实性（Factuality）**: 确保生成信息准确 truthful，关注内部知识与外部知识的冲突、检索文档中的噪声、长上下文处理
  2. **鲁棒性（Robustness）**: 系统面对攻击和噪声的稳定性，从攻击机制（检索阶段攻击、后门攻击、交互层攻击、结构攻击）和防御策略（证据过滤、鲁棒聚合、鲁棒训练、Agent-based防御）两个视角综述
  3. **公平性（Fairness）**: 最小化偏见，涉及知识源不平衡、知识可靠性、检索算法偏见、信息整合中的偏见放大
  4. **透明性（Transparency）**: 使系统过程可理解，包括检索透明性和信息整合透明性
  5. **问责性（Accountability）**: 追踪和归责机制，涵盖来源归属、证据验证、推理可追溯性、责任分配
  6. **隐私性（Privacy）**: 保护个人数据，涉及数据提取攻击、推理攻击、检索引发的隐私风险及防御

- **分类方法**: 每个维度按三个标准对现有工作进行分类：
  1. 可信性阶段（Input / Generation / Checking）
  2. 方法类型（Attack / Defense / Evaluation）
  3. 研究对象（Generator / Retriever）

- **研究趋势**: 综述发现各维度均出现了从静态方法到基于Agent的动态、自适应方法的范式转变。

- **评测基准（TRC Bench）**: 覆盖六个维度，使用特定数据集和评估方法对各维度进行量化评测。

## Contribution（贡献）

- 提出了统一的RAG可信性框架（Trust-RAG Compass），定义了六个关键维度，为后续研究提供结构化基础。
- 对RAG可信性相关的现有文献进行了详细综述，按维度系统梳理了攻击、防御和评估方法，识别了研究空白和有前景的方向。
- 建立了实用的评测基准TRC Bench，对19个LLM（11个开源 + 8个商有）进行了全面评估，提供了不同模型在各可信性维度上的性能对比。
- 开源了代码和数据集（https://github.com/smallporridge/TrustworthyRAG）。

## Limitation（局限性）

- 论文指出隐私和公平性是所有模型（包括商有模型）普遍面临的重大挑战，当前方法尚未有效解决。
- 开源模型在事实性和问责性方面仍显著落后于商有模型，当前的开源对齐策略对复杂RAG场景可能仍不充分。
- 指令微调后的开源模型在隐私保护上表现甚至更差（隐私得分降至0），说明对齐可能引入新的隐私风险。
- 静态模型知识与动态信息之间的冲突仍是核心挑战，在Agent化RAG中误差可能在多步推理中传播。
- 现有评测基准主要关注最终输出，忽略了Agent推理过程本身的复杂性。
- 未来需要在多模态数据、长上下文和记忆管理、工具集成等方面进一步研究。

## Evaluation（评估）

- **使用的数据集**:
  - 事实性: RGB benchmark（50个样本）
  - 鲁棒性: HotpotQA（50个问题，3篇和10篇参考文档两组设置）
  - 公平性: CrowS-Pair数据集（50个性别相关样本）
  - 透明性: HotpotQA（50个问题，使用GPT-4辅助构建key-facts）
  - 问责性: HotPotQA（50个问题，10篇检索文档）
  - 隐私性: Enron Email数据集（50个问题，BM25检索top-3文档）

- **评估指标**:
  - 事实性: 不包含伪造答案的比例
  - 鲁棒性: F1分数（在3篇和10篇参考文档设置下的性能变化）
  - 公平性: 对偏见陈述的支持率
  - 透明性: Recall（关键事实覆盖率）、Precision（有支撑的陈述比例）、Fact Density（每条原子陈述覆盖的关键事实数）
  - 问责性: 引用的Precision、Recall和F1分数
  - 隐私性: 拒绝回答的比例

- **关键实验结果**:
  - 商有模型在事实性、问责性、透明性、隐私性上普遍优于开源模型
  - Gemini-3.1-pro事实性最优（74.0），GPT-5.4-pro隐私最优（83.7），Claude-Opus-4.6透明性最优（89.6）
  - 指令微调模型在鲁棒性、问责性和透明性上优于对应base模型
  - 模型规模增大不必然提升可信性，训练数据质量和对齐策略同样重要
  - 隐私是所有模型的最大弱点，开源模型隐私得分普遍接近0

## Key Insights（关键洞察）

- **可借鉴的方法思路**:
  - 六维可信性框架提供了一个系统化的RAG评估视角，可作为设计和评估RAG系统的清单
  - 各维度均出现从静态到Agent-based动态方法的趋势，值得在具体应用中关注
  - TRC Bench评测方法设计实用，可作为RAG系统可信性评估的参考方案
  - 将NLI模型作为"oracle"函数来评估推理步骤的忠实度，是一个可复用的评估技巧

- **对本研究的启发**:
  - 在构建RAG系统时，不能仅关注准确性，还需系统性考虑鲁棒性、公平性、隐私等维度
  - 隐私和公平性是当前最薄弱的环节，是未来研究的重要方向
  - Agent化RAG带来新的可信性挑战（误差传播、记忆污染、工具安全），需要过程级别的评估
  - 指令微调对提升可信性有显著作用，但可能损害隐私保护能力，需要权衡
  - 未来RAG系统应从静态流水线转向自适应、Agent驱动的架构，在可信性约束下联合优化检索、推理和行动
