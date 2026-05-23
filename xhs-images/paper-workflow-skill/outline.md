---
strategy: b
name: Information-Dense
style: notion
style_reason: "Notion极简手绘线条风格，适合知识密集型干货内容，知性质感强"
elements:
  background: off-white-light
  decorations: [thin-lines, minimal-icons, connector-arrows]
  emphasis: highlight-box
  typography: clean-sans
layout: dense
image_count: 6
---

## P1 Cover
**Type**: cover
**Hook**: "用Claude Code从零写论文｜7步全流程AI工作流"
**Visual**: 手绘线条风格的学术论文写作流程图，中央是论文图标，周围7个步骤节点用细线连接
**Layout**: sparse
**Key Text**: 主标题 + 副标题"从文献调研到实验运行，一个Skill搞定"

## P2 Content - 流程总览
**Type**: content
**Message**: 7步完整工作流全貌
**Visual**: 纵向流程图，7个步骤用方框+箭头串联，每步一行简短说明
**Layout**: dense
**Key Text**:
1. 文献收集 → arxiv搜索下载
2. PDF转MD → pymupdf4llm批量转换
3. 信息提取 → 6维度结构化提取
4. 方法融合 → 5角度横向对比
5. 论文撰写 → LaTeX+引用验证
6. 实验运行 → pipeline+baseline
7. 论文润色 → 6模块自动分析

## P3 Content - 并行加速 + 引用验证
**Type**: content
**Message**: 两大核心亮点
**Visual**: 左右两栏对比。左侧"并行加速"：多个subagent图标同时工作。右侧"拒绝编造"：三层验证流程（引用池→元信息→WebSearch）
**Layout**: comparison
**Key Text**:
- 并行加速：N篇论文 = N个subagent同时处理
- 三层引用验证：论文引用池 → 自身元信息 → 外部WebSearch确认

## P4 Content - 实验实现
**Type**: content
**Message**: 实验代码实现要点
**Visual**: 代码架构图，展示模块化结构
**Layout**: dense
**Key Text**:
- uv管理Python环境，DeepSeek API调用LLM
- 先定义模块接口契约 → 再写实现（防集成bug）
- 小规模测试(10条) → 确认流程正确 → 再全量跑
- 结果JSON保存 → 自动填入LaTeX表格

## P5 Content - 实际成果
**Type**: content
**Message**: 用这套流程完成了什么
**Visual**: 成果展示卡片，图标+数字
**Layout**: dense
**Key Text**:
- TA-GraphRAG 论文完整产出
- 10篇文献 → 5角度融合 → 1个创新方法
- 6模块pipeline + 4个baseline对比实验
- 25条引用全部外部验证，0编造
- matplotlib可视化图表3张
- 全部代码开源 GitHub

## P6 Ending
**Type**: ending
**Message**: CTA + 技术栈总结
**Visual**: 底部号召 + 技术栈图标排列
**Layout**: balanced
**Key Text**:
- "收藏=学会，点赞=支持🔥"
- 技术栈：Claude Code / uv / Tectonic / DeepSeek API
- GitHub: github.com/mbt1909432/paper-workflow
- 适用于：研究生论文 / 会议投稿 / 文献综述
