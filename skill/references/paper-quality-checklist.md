# Paper Quality Checklist

论文质量自检清单，用于 Step 7 润色阶段和投稿前最终检查。

---

## 一、自洽性检查（最重要）

### 1.1 贡献-验证对应

Introduction 的每个贡献点必须在后续章节中完整对应：

```
Introduction 贡献点
      ↓ 必须一一对应
Method 技术设计
      ↓ 必须一一验证
Experiments 实验结果
      ↓ 必须支撑
Conclusion 结论陈述
```

**自检表格模板：**

| 贡献点 (Introduction) | Method 章节 | Experiment 验证 | 检查 |
|----------------------|-------------|-----------------|------|
| (1) 提出 XX 模块 | Sec 3.2 | Table X Ablation: w/o XX | ☐ |
| (2) 设计 YY 机制 | Sec 3.4 | Table X Ablation: w/o YY | ☐ |
| (3) 达到 SOTA | - | Table 1 Main Results | ☐ |

**自检问题：**
- [ ] 每个贡献点在 Method 中有详细描述？
- [ ] Method 中每个设计在 Ablation Study 中验证？
- [ ] 实验结果回答了 Introduction 的研究问题？
- [ ] Conclusion 只总结有实验支撑的结论？

### 1.2 数值自洽

| 检查点 | 常见错误 |
|--------|----------|
| Abstract 数值 | 与 Results 表格不一致（如 Abstract 5.2%，Table 5.18%） |
| "提升了 X%" | 计算错误：(ours - baseline) / baseline × 100% |
| Best 标注 | 粗体标错位置 |
| 图中趋势 | 正文说上升，图中下降 |
| 数字精度 | 有的 85.2%，有的 86.15%，全文不统一 |

### 1.3 术语自洽

创建术语对照表，全文 Ctrl+F 检查：

| 标准术语 | 禁止混用 | 规则 |
|----------|---------|------|
| our method | ~~our approach, the proposed method~~ | 选一个统一 |
| accuracy | ~~acc, classification accuracy~~ | 除非空间限制 |
| state-of-the-art | ~~SOTA, state of the art~~ | 选一种 |
| fine-tune / pre-train | ~~finetune, fine tune~~ | 统一连字符 |
| 缩写首次出现 | 必须给全称 | LLM → Large Language Model (LLM) |

### 1.4 引用自洽

- [ ] 每个 `\cite{}` 在 .bib 中有对应条目
- [ ] .bib 中没有被引用的孤立条目
- [ ] "如图X所示" 与实际图表内容匹配
- [ ] 引用编号连续无跳跃

**快速检查命令：**
```bash
# 未引用的文献
grep -oP '\\bibitem\{[^}]+\}' references.bib | sed 's/\\bibitem{//;s/}//' | while read key; do grep -q "\\cite{.*$key.*}" paper.tex || echo "未引用: $key"; done

# 引用但不存在的文献
grep -oP '\\cite\{[^}]+\}' paper.tex | sed 's/\\cite{//;s/}//' | tr ',' '\n' | sort -u | while read key; do grep -q "\\bibitem{$key}" references.bib || echo "不存在: $key"; done
```

---

## 二、各章节写作模板

### 2.1 Abstract（四句话法则）

1. **背景/问题**：[Field] has achieved progress in [task]. However, [gap] remains.
2. **方法**：We propose [method], a [framework] that [key innovation].
3. **结果**：Experiments on [datasets] show [X]% improvement over SOTA.
4. **意义**：Our work provides insights into [problem].

### 2.2 Introduction（五段法）

| 段落 | 功能 | 关键句型 |
|------|------|---------|
| P1 | 大背景 | "[Field] is important because..." |
| P2 | 现有局限 | "However, existing methods suffer from..." |
| P3 | 解决思路 | "To address this, we propose..." |
| P4 | 贡献列表 | "The main contributions are: (1)... (2)... (3)..." |
| P5 | 论文组织 | "The rest of the paper is organized as follows..." |

### 2.3 Experiments（RQ 结构）

用 Research Question 组织实验：
- **RQ1**: 主方法是否有效？→ Main Results Table
- **RQ2**: 各组件贡献多大？→ Ablation Study
- **RQ3**: 方法在不同设置下是否鲁棒？→ Parameter Sensitivity / Cross-dataset
- **RQ4**: 效率如何？→ Efficiency Analysis

### 2.4 Section 推荐长度

| 章节 | 建议长度 | 常见问题 |
|------|----------|----------|
| Abstract | 150-250 词 | 缺少具体数值 |
| Introduction | 1-1.5 页 | 贡献点与实验不对应 |
| Related Work | 0.5-1 页 | 只罗列不分析 |
| Method | 2-3 页 | 缺实现细节 |
| Experiments | 2-3 页 | 只报数字不解释 |
| Conclusion | 0.5 页 | 重复 Abstract |

---

## 三、审稿人预判策略

写论文时提前堵住审稿人可能的质疑：

| 审稿人可能的问题 | 论文中应有的回应 | 位置 |
|-----------------|----------------|------|
| baseline 不公平 | 统一超参数、硬件环境 | Implementation Details |
| 缺少消融实验 | 每个组件单独验证 | Ablation Study |
| 方法太简单 | 强调组合创新 + 实验支撑 | Method + Results |
| 为什么选这个设计 | 设计理由或对比实验 | Method / Ablation |
| 数据集太少 | 覆盖多样性 + 标准benchmark | Experimental Setup |
| 泛化性不足 | 补充跨领域实验 | Additional Results |

**Rebuttal 通用模板：**
```
We thank the reviewer for the constructive feedback.

[针对具体问题的回应]. Following R[X]'s suggestion, we [采取的行动].
Results in Table R[X] show [结果].

[如有补充实验]
We conducted additional experiments on [dataset]. Our method achieves [X]%,
outperforming [baseline] by [Y]%. As shown in Table R1:
```

---

## 四、数据修改红线

| ✅ 允许 | ❌ 禁止 |
|--------|--------|
| 调整精度格式 | 捏造不存在的实验 |
| 补充遗漏的数据点 | 删除不利的真实数据 |
| 不同种子重跑 | 只报告最好的一次 |
| 合并相似实验 | 伪造统计显著性 |
| 微调使趋势更清晰 | 篡改至结论相反 |

---

## 五、数据一致性验证脚本

从实验 JSON → LaTeX 表格 → 正文数值，全链路一致性检查：

```python
import json, re

def verify_paper_data(results_json, tex_path):
    """验证实验结果 JSON 与论文 .tex 中的数据一致"""
    with open(results_json) as f:
        results = json.load(f)
    with open(tex_path) as f:
        tex = f.read()

    errors = []
    # 检查 JSON 中的数值是否出现在 tex 中
    for method, metrics in results.get("methods", {}).items():
        for metric, value in metrics.items():
            # 灵活匹配：允许 1 位小数差异
            pattern = re.escape(f"{value:.1f}")
            if pattern not in tex and f"{value:.2f}" not in tex:
                errors.append(f"{method}.{metric}={value} not found in tex")

    if errors:
        print("数据不一致:")
        for e in errors:
            print(f"  - {e}")
    else:
        print("一致性验证通过")
```

---

## 六、学术写作常见问题

### 6.1 句子层面

| 规则 | 正确 | 错误 |
|------|------|------|
| 单句 ≤ 35 词 | 拆为多个简单句 | 50 词长句 |
| 主动语态 | "We improved..." | "It was found that..." |
| 精确动词 | "improve" | "make an improvement" |
| 时态一致 | Method 用现在时, Results 用过去时 | 混用 |

### 6.2 过渡词使用

| 功能 | 推荐 |
|------|------|
| 顺承 | Furthermore, Moreover |
| 转折 | However, Nevertheless |
| 因果 | Therefore, Consequently |
| 对比 | Compared to, Unlike |

**注意**：避免连续用同类型过渡词（Furthermore... Moreover... Additionally... 连用显得AI痕迹重）

### 6.3 禁用表达

| ❌ 避免 | ✅ 替换 |
|---------|--------|
| "significantly" (无统计检验) | 报告具体数字 |
| "dramatically" | "by X%" |
| "comprehensive experiments" | 具体benchmark名称 |
| "to the best of our knowledge" | 直接陈述，或加引用 |

---

## 七、Devil's Advocate 模板（Step 4.5 用）

在方法选定后、论文撰写前，用以下模板进行对抗性审阅：

```markdown
# Reviewer Challenge Report

## Method: [方法名]

### Challenge 1: [最强质疑]
**质疑**: "为什么 [核心假设] 成立？[基线方法] 已经解决了这个问题。"
**反驳/调整**:
- 如果有理论支撑 → 引用并说明
- 如果是实验验证 → 在实验中补充对比
- 如果无法反驳 → 调整方法设计

### Challenge 2: [实现可行性]
**质疑**: "这个方法在 [实际场景] 下可行吗？计算复杂度是多少？"
**反驳/调整**: ...

### Challenge 3: [创新性质疑]
**质疑**: "这和 [已有方法] 有什么本质区别？只是组合已有技术？"
**反驳/调整**: 强调组合创新的非平凡性 + 涌现效果

### Challenge 4: [评估公平性]
**质疑**: "对比基线的实现是否公平？超参数是否一致？"
**反驳/调整**: 确保 Implementation Details 中说明统一设置

### Challenge 5: [泛化性质疑]
**质疑**: "只在一个数据集上验证了？换到 [领域] 还有效吗？"
**反驳/调整**: 补充跨域实验或说明局限性

## 结论
- [ ] 所有 Challenge 已有应对方案
- [ ] 需要调整方法设计的地方：[列出]
- [ ] 需要补充实验的地方：[列出]
```

### 完整性关卡清单

#### Step 3.5: 提取验证
- [ ] 每个文件6个必填节都有内容
- [ ] 无占位符文字（TODO/TBD）
- [ ] Methodology有具体技术名称
- [ ] Evaluation至少提到一个数据集/指标
- [ ] 失败率 < 30%（否则重跑失败的文件）

#### Step 6.7: 实验验证
- [ ] 结果JSON存在且有效（无NaN/空字段）
- [ ] 所有方法名与论文Methodology匹配
- [ ] 无不可能值（EM/F1 > 100%，负分）
- [ ] 结果文件时间戳晚于代码最后修改时间
