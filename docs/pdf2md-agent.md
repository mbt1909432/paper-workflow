# PDF to Markdown 转换 Subagent 规范

## 遇到过的问题及解决方案

### 问题1：subagent输出文件命名不统一
- 现象：有的输出 `_raw.md`、`_temp.md`，有的直接输出最终文件名
- 原因：subagent自由发挥，没有强制命名规则
- 解决：在prompt中明确指定输出文件名，禁止使用中间文件名

### 问题2：部分subagent未添加元信息头
- 现象：10个subagent中3个只做了PDF转MD，没加YAML front matter
- 原因：prompt中对元信息的要求不够强制
- 解决：将元信息头作为必须步骤，明确写出模板和提取规则

### 问题3：subagent留下垃圾文件
- 现象：`cleanup.py`、`_temp_output.md`、`process_09.py`等中间文件
- 原因：subagent用Python脚本做中间处理，写入了临时文件
- 解决：要求subagent用管道/内存处理，只写最终文件

### 问题4：转换质量参差不齐
- 现象：有的subagent做了清洗（去页脚、修断字），有的没做
- 原因：prompt中清洗步骤不够具体
- 解决：列出具体清洗规则清单

## Subagent Prompt 模板

以下是经过优化后的标准prompt，直接用于Agent工具：

```
你的任务是将一篇学术论文PDF转换为结构化的Markdown文件。严格按以下步骤执行。

## 输入
- PDF文件：{PDF_PATH}
- 输出文件：{OUTPUT_PATH}（必须是这个文件名，不要改名）

## 步骤1：转换
用Python和pymupdf4llm读取PDF转为markdown：
```python
import pymupdf4llm
md_text = pymupdf4llm.to_markdown("PDF路径")
```
将结果保存到输出路径。

## 步骤2：添加元信息头
读取输出文件的第一页内容，在文件最开头插入YAML front matter：
```markdown
---
title: "论文完整标题"
authors: ["作者1", "作者2", ...]
date: YYYY-MM-DD
arxiv_id: "XXXX.XXXXX"
org: "主要机构名称"
---
```
从PDF内容中提取这些信息，不要编造。

## 步骤3：清洗
执行以下清洗操作：
1. 删除独立的页码行（单独一行的数字）
2. 删除arxiv水印/页脚（如 `arXiv:XXXX.XXXXX ...`）
3. 删除重复的页眉/期刊头（如 `J. ACM, Vol. ...`）
4. 删除图片占位符文本（如 `**==> picture ... <==**`），保留图片标题
5. 修复PDF分栏导致的断字（如 `knowledgeintensive` → `knowledge-intensive`）
6. 修复章节标题格式（如 `## **标题**` → `## 标题`）
7. 压缩连续空行，最多保留2个换行

## 步骤4：保存和验证
- 用Write工具保存最终文件到指定输出路径
- 确认文件存在且不为空
- 确认文件以 `---` 开头（元信息头）

## 禁止事项
- 不要创建任何临时文件、脚本文件
- 不要使用 _raw、_temp 等中间命名
- 只输出一个最终文件到指定路径
```
