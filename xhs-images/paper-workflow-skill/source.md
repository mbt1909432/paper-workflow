# 用Claude Code从零写一篇学术论文 | 全流程AI工作流

## 背景

作为一名研究者，我花了几天时间用 Claude Code 搭建了一套完整的学术论文写作工作流 Skill。从文献调研到实验运行到论文成稿，全程AI辅助。今天把这个工作流分享出来。

## 完整流程（7步）

### Step 1: 文献收集
- 输入研究方向关键词，自动从arxiv搜索下载最新论文
- 支持批量并行下载，自动命名归档
- 示例：输入"RAG LLM survey"，自动收集10篇高质量综述

### Step 2: PDF转Markdown
- 用 pymupdf4llm 批量转换PDF为结构化Markdown
- 每篇论文一个subagent并行处理
- 自动添加元信息（标题、作者、日期、arxiv ID）

### Step 3: 结构化信息提取
- 从每篇论文提取6大维度：Abstract、Methodology、Contribution、Limitation、Evaluation、Key Insights
- 并行处理，10篇论文同时提取

### Step 4: 多角度方法融合
- 从5个不同角度横向对比所有论文
- 每个角度生成对比表 + Gap分析 + 融合方案
- 用户选择最佳方案 → 成为论文核心创新点

### Step 5: LaTeX论文撰写 + 引用验证
- 自动生成完整LaTeX论文（Abstract到Conclusion）
- 25条参考文献全部外部验证，拒绝编造引用
- 三层验证：论文引用池 → 自身元信息 → WebSearch外部确认

### Step 6: 实验实现与运行
- uv管理Python环境，DeepSeek API调用LLM
- 6模块pipeline + 4个baseline对比实验
- 小规模测试(10条)验证流程，再决定是否全量跑

### Step 7: 论文润色
- latex-paper-en skill 自动分析语法、逻辑、实验、去AI痕迹
- 6个分析模块逐一跑，输出修改建议
- 最终编译为PDF

## 核心亮点

1. **全程可复现**：每个步骤都有标准化模板和检查清单
2. **并行加速**：文献处理、信息提取、方法融合全部并行subagent
3. **拒绝编造**：引用验证三重保障，每条引用可追溯外部来源
4. **成本可控**：10条测试仅花几毛钱，确认无误再全量跑
5. **打包为Skill**：整个工作流封装为可复用的skill，下次直接用

## 实际成果

用这套流程，我完成了一篇 TA-GraphRAG 论文：
- 10篇文献调研 → 5角度融合 → 提出创新方法
- 6模块pipeline实验代码 + 4个baseline
- 完整LaTeX论文 + 实验图表 + 引用验证
- 全部代码开源：github.com/mbt1909432/paper-workflow

## 技术栈
- Claude Code (Claude Opus 4.6)
- uv (Python包管理)
- Tectonic (LaTeX编译)
- pymupdf4llm (PDF转MD)
- DeepSeek API (实验LLM调用)
- matplotlib (实验结果可视化)

## 适用场景
- 研究生写课程论文/毕业论文
- 研究者快速验证新方法
- 文献综述写作
- 会议/期刊投稿
