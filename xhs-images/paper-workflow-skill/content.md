用Claude Code从零写论文｜7步全流程AI工作流

花了几个月时间，用 Claude Code 搭了一套完整的学术论文写作工作流 Skill，从文献调研到实验运行到论文成稿，全程AI辅助。

分享一下完整流程：

📚 Step 1 文献收集：输入关键词自动搜索arxiv，批量下载
📄 Step 2 PDF转MD：pymupdf4llm批量转换，每篇一个subagent并行
🔍 Step 3 信息提取：6维度结构化提取（Method/Contribution/Limitation...）
🧩 Step 4 方法融合：5个角度横向对比，提出创新方法
✍️ Step 5 论文撰写：自动生成LaTeX + 三层引用验证
🧪 Step 6 实验运行：先10条测试 → 确认流程 → 再全量跑
✨ Step 7 论文润色：6模块自动分析（语法/逻辑/去AI痕迹）

核心亮点：
⚡ 并行加速 - N篇论文 = N个agent同时处理，10篇15分钟搞定
🔒 三层引用验证 - 引用池 → 元信息 → WebSearch，25条0编造
💰 成本可控 - 10条测试才几毛钱

实际产出：TA-GraphRAG论文
10篇文献 → 5角度融合 → 6模块pipeline → 25条验证引用 → 完整论文PDF

全部代码开源👇
github.com/mbt1909432/paper-workflow

适用于：研究生论文 / 会议投稿 / 文献综述 / 方法验证

收藏=学会 🔖 点赞=支持 ❤️
评论区告诉我你想用来写什么论文！
