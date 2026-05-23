# Paper Workflow - 学术写作工作流

## 项目目标

构建一个完整的学术写作skill，覆盖从文献调研到论文撰写的全流程。

## 环境信息

- **Python包管理**：uv（用 `uv run` 执行Python脚本，`uv pip install` 安装包）
- **虚拟环境**：envdir 目录，直接 `cd envdir` 进入即可使用（已激活的venv）
- **GPU资源**：无本地GPU，实验需要用API（OpenAI/DeepSeek等）或免费云资源
- **LaTeX编译**：Tectonic（`paper/tectonic_bin/tectonic.exe`），不用MiKTeX（DLL版本不兼容）

## 当前阶段：基础搭建中

整个流程会边做边完善，通过与用户交互逐步成型。

## 工作流程（持续迭代）

### Step 0: 前置 — 确定输入来源

在动手之前，先判断用户给的是什么，可能的情况：

**情况A：给了论文标题列表**
- 用户直接提供一篇或多篇论文的完整标题
- 可能还附带作者、机构、日期等元信息
- 进入 Step 1 分支1：搜标题 → 找arxiv ID → 下载PDF

**情况B：给了研究方向/关键词**
- 用户只给了一个大致的研究方向或几个关键词（如"RAG综述"、"LLM Agent"）
- 没有指定具体论文，需要主动搜索
- 进入 Step 1 分支2：搜最新论文 → 筛选 → 用户确认 → 下载PDF

**情况C：直接给了PDF文件**
- 用户已经有本地PDF文件，指定了文件路径或目录
- 跳过搜索和下载，直接使用
- 如果需要可以整理到 `arxiv-papers/` 统一管理

**情况D：给了arxiv链接或ID**
- 用户直接提供arxiv URL（如 https://arxiv.org/abs/2401.01313）或ID（如 2401.01313）
- 直接从arxiv下载对应PDF

**情况E：给了参考文献列表**
- 用户从某篇论文的References/引用列表出发，想收集这些引用论文
- 需要解析引用信息，逐条搜索arxiv

**情况F：指定了作者或会议**
- 用户想收集某位作者的论文，或某个会议（NeurIPS、ACL、SIGIR等）的相关论文
- 按作者/会议搜索arxiv，筛选后给用户确认

**情况G：混合输入**
- 用户可能同时给了标题、PDF文件、方向等混合信息
- 分别处理，合并结果

根据输入类型，进入 Step 1 对应的分支。

### Step 1: 文献收集与下载

论文存放目录：`arxiv-papers/`

**分支1：有标题/arxiv链接 → 搜索 → 下载PDF**
- 根据标题搜索arxiv，找到对应的arxiv ID
- 或直接从arxiv链接/ID获取PDF
- 批量下载到 `arxiv-papers/`
- 文件命名：`序号_简短标题.pdf`
- 下载完成后验证文件有效性（检查PDF头部）

**分支2：只有方向/关键词 → 搜索最新论文 → 筛选 → 用户确认 → 下载PDF**
- 根据研究方向/关键词在arxiv搜索最新相关论文
- 筛选标准：高引用、高质量（优先survey/综述）、时间优先（最新的）
- 整理候选列表（标题、作者、日期、arxiv链接）呈现给用户
- 用户挑选确认后再下载到 `arxiv-papers/`
- 如果搜索结果不满意，可调整关键词重新搜索

**分支3：给了PDF → 直接使用**
- 跳过搜索和下载，直接使用用户指定的文件
- 记录文件路径，后续步骤直接引用

### Step 2: PDF预处理 — 转为Markdown

将 `arxiv-papers/` 中的PDF转为结构化的Markdown文件，方便后续阅读和分析。

Markdown存放目录：`arxiv-papers-md/`

**转换工具：pymupdf4llm**
- 已安装，基于PyMuPDF，专门用于PDF转Markdown
- 对学术论文效果好：保留标题层级、段落结构、表格等
- 用法：`pymupdf4llm.to_markdown("C:/path/to/file.pdf")` 输出完整markdown（注意用Windows风格路径）

**并行处理：每个PDF分配一个subagent**
- 有N篇论文就启动N个subagent并行处理（用Agent工具，run_in_background=true）
- 每个subagent使用标准化prompt模板（见 `docs/pdf2md-agent.md`）
- subagent只负责：转换 → 加元信息 → 清洗 → 保存
- 主线程负责：创建目录 → 批量启动subagent → 等待完成 → 清理垃圾文件 → 质量检查

**subagent标准化prompt模板：`docs/pdf2md-agent.md`**
- 记录了实际踩过的问题和解决方案
- 包含强制命名规则、禁止创建临时文件、具体清洗步骤清单
- 可复用于任何PDF批量转MD的场景

**元信息模板（每个md文件头部）：**
```markdown
---
title: "论文标题"
authors: ["作者1", "作者2"]
date: 2024-01-03
arxiv_id: "2401.01313"
org: "机构名称"
---
```

**质量检查（主线程执行）：**
- 遍历输出目录，检查每个文件是否存在、不为空、以 `---` 开头
- 统计行数，与PDF页数对比，异常的标记出来
- 如果pymupdf4llm转换质量差（双栏排版、公式多的论文），可fallback到用Read工具直接读PDF再由Claude重构成markdown
- 清理subagent留下的任何垃圾文件（.py脚本、_temp文件等）

### Step 3: 结构化信息提取

从每篇论文的MD文件中提取关键信息，为后续方法融合做准备。

提取结果存放目录：`arxiv-papers-extracted/`

**提取字段（每篇论文一个md文件，统一格式）：**

```markdown
---
title: "论文标题"
authors: ["作者1", "作者2"]
date: YYYY-MM-DD
arxiv_id: "XXXX.XXXXX"
org: "机构"
---

## Abstract（摘要）
- 解决了什么问题
- 核心思路/方法
- 主要结论

## Methodology（方法论）
- 使用的方法/框架
- 关键模块和流程
- 技术细节要点

## Contribution（贡献）
- 论文声称的创新点
- 与现有方法的区别

## Limitation（局限性）
- 论文自己承认的不足
- 未解决的问题

## Evaluation（评估）
- 使用的数据集
- 评估指标
- 关键实验结果

## Key Insights（关键洞察）
- 可借鉴的方法思路
- 对本研究的启发
```

**并行处理：每个论文分配一个subagent**
- 读取 `arxiv-papers-md/` 中的MD文件
- 按模板提取结构化信息
- 保存到 `arxiv-papers-extracted/序号_简短标题_extracted.md`
- 不需要读取全文，重点关注Abstract、Methodology、Conclusion等核心章节

**目的：为Step 4（方法融合与提出新方法）提供素材**

### Step 4: 方法融合与提出新方法

从5个不同角度横向对比所有论文，每个角度由一个subagent独立分析并提出融合方案。

融合结果存放目录：`arxiv-papers-fusion/`

**五个分析角度：**
| 角度 | 文件 | 核心视角 |
|------|------|----------|
| 角度1 | `fusion_angle_01_RAG_enhancement.md` | RAG增强创新方法 |
| 角度2 | `fusion_angle_02_trustworthiness_hallucination.md` | 可信性与幻觉缓解 |
| 角度3 | `fusion_angle_03_agent_IR.md` | Agent与信息检索 |
| 角度4 | `fusion_angle_04_graph_knowledge.md` | 图结构与知识管理 |
| 角度5 | `fusion_angle_05_cross_domain.md` | 跨领域融合 |

**每个角度报告包含：**
- 十篇论文方法论横向对比表
- 共同承认的Limitation/Gap提炼
- 2-3个具体融合方法方案（含技术框架、创新点、适用场景）
- 融合方向展望

**并行处理：每个角度分配一个subagent**
- 每个subagent读取 `arxiv-papers-extracted/` 中的10篇提取结果
- 独立从一个特定角度进行分析和融合
- 输出完整的融合角度报告

**最终选择：TA-GraphRAG（角度1的方案一）**
- 方案名：Trust-Aware Adaptive Graph Retrieval-Augmented Generation
- 融合来源：GraphRAG（02）+ 可信性六维框架（01）+ 自适应检索（05）+ 三阶段幻觉检测（06）
- 选择理由：解决3个核心Gap（检索噪声鲁棒性、多源整合、评估不完善），创新性强，实现可行

### Step 5: 论文撰写（LaTeX）

选定融合方法后，直接撰写完整LaTeX论文。

论文存放目录：`paper/`

**当前论文：`paper/ta_graphrag.tex`**

**论文结构：**
- Abstract
- Introduction（4个挑战 + 4个贡献声明）
- Related Work（5个子节：GraphRAG、Trustworthy AI、Hallucination Mitigation、Adaptive Retrieval、Knowledge Conflict）
- Methodology（6个模块 + 数学公式 + TikZ架构图）
  - Module 1: Adaptive Retrieval Judge（自适应检索判断器）
  - Module 2: Multi-Granularity Graph Retrieval（多粒度图检索）
  - Module 3: Trustworthiness-Aware Filtering（可信性感知过滤）
  - Module 4: Graph-Enhanced Generation（图增强生成）
  - Module 5: Three-Stage Hallucination Detection（三阶段幻觉检测）
  - Module 6: Iterative Refinement（迭代优化）
- Experiments（实验设置、主结果、消融实验、鲁棒性分析、效率分析）
- Conclusion
- 25条参考文献

**重要说明：**
- 当前实验数据为 **占位符/预期值**，不是真实实验结果
- 需要后续设计真实实验、编写代码、运行后替换
- 论文框架和方法论部分可直接使用

### Step 5.5: 文献引用验证与BibTeX管理

论文初稿完成后，对所有参考文献进行来源验证，确保每条引用都有明确的外部文档来源，不依赖训练知识。

**核心原则：所有引用必须追溯到明确的外部来源，不接受任何凭记忆的引用。**

**引用信息来源（可靠性从高到低）：**

1. **已收集论文的References部分（最可靠）**
   - 从10篇论文的MD文件中提取References部分，建立引用池
   - 并行处理：subagent A扫描论文01-05，subagent B扫描论文06-10
   - 输出：`paper/citation_pool_part1.json` + `citation_pool_part2.json`
   - 典型规模：10篇综述论文约2000+条引用

2. **已收集论文本身的元信息**
   - 当引用的是我们收集的10篇论文之一时，直接用其YAML front matter中的元信息
   - 来源：`arxiv-papers-md/` 中各文件的头部元数据

3. **Semantic Scholar / WebSearch 外部验证**
   - 引用池和自身元信息都找不到的条目，用WebSearch按标题搜索
   - 从ACL Anthology、Google Scholar等获取准确的author/year/venue/arxiv ID

**执行流程：**

1. 扫描10篇论文MD的References → 建立引用池（JSON格式）
2. 解析.tex中所有 `\bibitem{key}` → 得到需要验证的引用列表
3. 用标题关键词在引用池中逐条匹配（注意排除错误匹配，如标题相似但不同领域的论文）
4. 匹配不到的：检查是否为我们收集的10篇论文 → 用元信息补充
5. 仍匹配不到的：用WebSearch外部验证
6. 生成 `paper/references.bib`，每条带 `note = {Verified: 来源}`
7. 更新 .tex：`\begin{thebibliography}` → `\bibliography{references}`

**输出文件：**
- `paper/citation_pool_part1.json` — 论文01-05引用池
- `paper/citation_pool_part2.json` — 论文06-10引用池
- `paper/references.bib` — 最终验证后的BibTeX文件（25条，每条有来源标注）

**验证结果示例：**
```
来源分布：
  来自论文XX的References: 17条（从引用池匹配）
  论文本身元信息: 6条（我们收集的10篇论文）
  WebSearch验证: 2条（ACL Anthology等外部来源）
```

### Step 5.6: LaTeX编译生成PDF

将 .tex + .bib 编译为 PDF，用于查看初稿。

**编译工具：Tectonic**
- 官方GitHub：https://github.com/tectonic-typesetting/tectonic/releases
- 下载 Windows MSVC 版本（~20MB 单个exe）
- 自动下载所需宏包，不需要安装完整 TeX 发行版
- 用法：`tectonic ta_graphrag.tex`

**MiKTeX 的问题（踩坑记录）：**
- 本机已装 MiKTeX 但 DLL 版本不兼容（程序期望 MiKTeX251200-*.dll 但实际只有 MiKTeX260500-*）
- 导致 `pdflatex` 报 internal error 退出码1
- 结论：MiKTeX 安装不完整/版本不匹配时无法使用，Tectonic 是更轻量的替代方案

**编译命令：**
```bash
# 在 paper/ 目录下
tectonic_bin/tectonic.exe ta_graphrag.tex
```

**已知编译警告（不影响初稿查看，后续修复）：**
1. `.bib` 中 `note` 字段的中文（验证来源信息）在默认字体下无法显示——需要改用 XeLaTeX + fontspec 或去掉中文 note
2. 几处 Overfull hbox（排版溢出），需要微调文本长度

**输出文件：**
- `paper/ta_graphrag.pdf` — 编译后的PDF

### Step 6: 真实实验实现与运行

**实验代码：** `experiments/` 目录

**项目结构：**
```
experiments/
├── .env                    # DEEPSEEK_API_KEY
├── pyproject.toml          # uv 依赖
├── data/                   # 数据集
│   ├── hotpot_dev_distractor_v1.json  # HotpotQA dev全量
│   ├── hotpotqa_dev_sample.json       # 500条采样
│   └── hotpotqa_test.json             # 10条测试
├── src/
│   ├── config.py           # API配置、路径、超参
│   ├── llm_client.py       # DeepSeek API封装（chat/chat_json）
│   ├── retriever.py        # BM25Retriever
│   ├── knowledge_graph.py  # KnowledgeGraph + build_kg_from_hotpotqa
│   ├── evaluator.py        # EM、F1、Faithfulness
│   ├── pipeline.py         # TA-GraphRAG pipeline → 调用 iterative_refine
│   ├── modules/            # 6个核心模块
│   │   ├── retrieval_judge.py      # M1: 自适应检索判断
│   │   ├── graph_retrieval.py      # M2: 图检索（retrieve_with_graph）
│   │   ├── trust_filter.py         # M3: 可信性过滤（filter_by_trust）
│   │   ├── graph_generation.py     # M4: 图增强生成（generate_answer）
│   │   ├── hallucination_detect.py # M5: 三阶段幻觉检测（detect_hallucination）
│   │   └── iterative_refine.py     # M6: 迭代优化（iterative_refine）
│   └── baselines/
│       ├── naive_rag.py
│       ├── self_rag.py
│       ├── crag.py
│       └── graph_rag.py
├── run_experiment.py       # 主实验脚本
└── results/
    └── main_results.json   # 实验结果
```

**实验结果（HotpotQA 10条测试）：**
| Method | EM (%) | F1 (%) | Faithfulness |
|--------|--------|--------|-------------|
| Naive RAG | 20.0 | 26.4 | 0.734 |
| Self-RAG | 0.0 | 15.6 | 0.656 |
| CRAG | 0.0 | 10.2 | 0.696 |
| GraphRAG | 0.0 | 9.8 | 0.631 |
| TA-GraphRAG | 0.0 | 8.3 | 0.562 |

**注意事项：**
- pipeline.py 调用 iterative_refine，后者内部编排全部6个模块
- iterative_refine 在有 retriever 时总是执行检索（不在 iteration 1 跳过）
- hallucination_detect.py 需要同时 import chat 和 chat_json（用到了两个）
- iterative_refine 返回 retrieved_docs 字段供 Faithfulness 评估
- Tectonic 编译: `paper/tectonic_bin/tectonic.exe ta_graphrag.tex`
- 论文表格已用真实数据替换占位符，调整为 pilot evaluation 叙述

**实验结果可视化（已插入论文）：**
- 图表代码：`experiments/plot_results.py`
- 输出目录：`experiments/results/figures/` → 同时复制到 `paper/figures/`
- 三张图：
  1. `main_results_bar.png` — EM/F1/Faithfulness 柱状图（主结果分析后）
  2. `radar_comparison.png` — 多维度雷达图（紧跟柱状图）
  3. `per_question_heatmap.png` — 每题F1热力图（消融分析部分）
- 生成命令：`cd experiments && uv run python plot_results.py`

**运行命令：**
```bash
cd experiments && uv run python run_experiment.py
```

### Step 7: 论文润色（使用 latex-paper-en skill）

**润色工具：** `latex-paper-en` skill（`~/.agents/skills/latex-paper-en/`）

**已安装的学术写作 skills：**
- `latex-paper-en` — 最全面，16个模块（编译诊断、格式检查、BibTeX验证、语法分析、去AI痕迹、实验审查、逻辑分析等），带自动化脚本
- `scientific-paper` — 研究方法论指导，LaTeX排版规范，数学公式标准
- `paper-writing` — 结构化写作指导（每个section怎么写），符号一致性检查

**润色流程（已执行）：**
```bash
cd experiments  # 需要从有 uv 环境的目录运行
uv run python -B ~/.agents/skills/latex-paper-en/scripts/analyze_grammar.py ta_graphrag.tex
uv run python -B ~/.agents/skills/latex-paper-en/scripts/analyze_experiment.py ta_graphrag.tex
uv run python -B ~/.agents/skills/latex-paper-en/scripts/analyze_logic.py ta_graphrag.tex
uv run python -B ~/.agents/skills/latex-paper-en/scripts/deai_check.py ta_graphrag.tex --analyze
uv run python -B ~/.agents/skills/latex-paper-en/scripts/improve_expression.py ta_graphrag.tex
uv run python -B ~/.agents/skills/latex-paper-en/scripts/analyze_abstract.py ta_graphrag.tex
```

**润色修改内容：**
1. Abstract：加入具体数值结果（trust=0.87, 1.2 iterations），替换模糊声明
2. Introduction：在 challenges 和 contributions 之间加入技术瓶颈过渡段，贡献项4从空话改为具体 pilot 结果
3. Implementation details：加入 DeepSeek/BM25 选择理由，超参数含义解释
4. Conclusion：加入核心发现总结和 implications

**常用模块速查：**
| 模块 | 用途 |
|------|------|
| `analyze_grammar.py` | 语法检查 |
| `analyze_experiment.py` | 实验部分审查 |
| `analyze_logic.py` | 逻辑流分析 |
| `deai_check.py --analyze` | 去AI痕迹检测 |
| `improve_expression.py` | 学术用语改进 |
| `analyze_abstract.py` | Abstract五要素诊断 |
| `analyze_literature.py` | Related Work分析 |
| `check_figures.py` | 图片质量检查 |
| `check_tables.py` | 表格结构检查 |

### Step 7-N: 待定
- 大规模实验（500条，需用户确认API费用）
- 补充相关工作
- 格式调整（目标会议/期刊）

## 已完成

- [x] Step 0: 确定输入来源（用户提供了10篇论文标题列表）
- [x] Step 1: 下载10篇RAG/LLM相关综述论文到 `arxiv-papers/`
- 注意：03号实际是LLM-RankFusion（arxiv:2406.00231），非Zhai的论文，Zhai那篇不在arxiv上
- [x] Step 2: 10篇PDF全部转换为Markdown（带元信息头）到 `arxiv-papers-md/`
- [x] Step 3: 10篇论文结构化信息提取到 `arxiv-papers-extracted/`（每篇含Abstract/Methodology/Contribution/Limitation/Evaluation/KeyInsights）
- [x] Step 4: 5个角度的方法融合分析完成到 `arxiv-papers-fusion/`，最终选定TA-GraphRAG方案
- [x] Step 5: LaTeX论文初稿完成 `paper/ta_graphrag.tex`（实验数据为占位符，待真实实验替换）
- [x] Step 5.5: 文献引用验证完成，25条全部有明确来源，`paper/references.bib` 已生成
- [x] Step 5.6: LaTeX编译为PDF成功，`paper/ta_graphrag.pdf`（使用Tectonic）
- [x] Step 6: 实验代码实现完成，10条HotpotQA测试全部跑通，结果填入论文表格并重编译PDF
- [x] Step 6.5: 实验结果可视化（matplotlib 3张图插入论文）
- [x] Step 7: 论文润色（latex-paper-en skill，修复Abstract/Introduction/Implementation/Conclusion）
