---
title: "LLM-RankFusion: Mitigating Intrinsic Inconsistency in LLM-based Ranking"
authors: ["Yifan Zeng", "Ojas Tendolkar", "Raymond Baartmans", "Qingyun Wu", "Lizhong Chen", "Huazheng Wang"]
date: 2024-01-01
arxiv_id: "2406.xxxxx"
org: "Oregon State University, Pennsylvania State University"
---

# LLM-RankFusion: Mitigating Intrinsic Inconsistency in LLM-based Ranking

**Yifan Zeng\* , Ojas Tendolkar\* , Raymond Baartmans\*** , **Qingyun Wu** , **Lizhong Chen** , **Huazheng Wang**

> \*Equal Contribution. Preprint. Under review.

1Oregon State University, 2Pennsylvania State University

{zengyif,tendolko,baartmar,lizhong.chen,huazheng.wang}@oregonstate.edu

{qingyun.wu}@psu.edu

## Abstract

Ranking passages by prompting a large language model (LLM) can achieve promising performance in modern information retrieval (IR) systems. A common approach to sort the ranking list is by prompting LLMs for a pairwise or setwise comparison which often relies on sorting algorithms. However, sorting-based methods require consistent comparisons to correctly sort the passages, which we show that LLMs often violate. We identify two kinds of intrinsic inconsistency in LLM-based pairwise comparisons: _order inconsistency_ which leads to conflicting results when switching the passage order, and _transitive inconsistency_ which leads to non-transitive triads among all preference pairs. Our study of these inconsistencies is relevant for understanding and improving the stability of any ranking scheme based on relative preferences. In this paper, we propose `LLM-RankFusion`, an LLM-based ranking framework that mitigates these inconsistencies and produces a robust ranking list. `LLM-RankFusion` mitigates order inconsistency using in-context learning (ICL) to demonstrate order-agnostic comparisons and calibration to estimate the underlying preference probability between two passages. We then address transitive inconsistency by aggregating the ranking results from multiple rankers. In our experiments, we empirically show that `LLM-RankFusion` can significantly reduce inconsistent comparison results, improving the ranking quality by making the final ranking list more robust. Our code is available at https://github.com/XHMY/LLM-RankFusion

## 1 Introduction

Large language models (LLMs) have demonstrated strong zero-shot and few-shot capabilities in many natural language processing tasks [1, 46, 47]. This enables the effective integration of these LLMs in modern information retrieval (IR) systems [45, 20]. Without supervised training on labeled data in a specific task, LLMs can adapt to the task by prompt and pipeline design. Recent work has tried to apply LLMs in text ranking and shown promising performance [32, 5, 38, 28]. Text ranking is an important task in modern recommendation systems and search engines, which refines the order of the retrieved passages to improve the output quality [25]. Traditional supervised text ranking methods mostly rely on large amounts of human-annotated labels [2, 3, 42, 29]. Typical LLM-based ranking approaches prompt LLMs to generate partial orders, comparisons, or relevance scores without additional training in advance.

Despite the great potential of LLMs in passage ranking, they can also suffer from significant inconsistency. Previous work shows LLM-based ranking is sensitive to the order of input passages in the prompt, which stems from the positional bias of LLMs [44, 27, 39]. In a pairwise comparison between two passages, the results can conflict before and after swapping the passages. We identify this as **order inconsistency**. Even if we can fully mitigate the order inconsistency within a single comparison, there is still a concern about inconsistency among multiple different comparisons. For example, PRP-Sort [32] uses sorting algorithms to efficiently produce a full ranked list from pairwise comparisons. However, these sorting algorithms typically assume the transitivity of comparisons to correctly sort the passage, which we show that LLMs often cannot guarantee. (e.g. _d_1 ≻ _d_2, _d_2 ≻ _d_3 ⇒ _d_1 ≻ _d_3, where _di_ represents a passage and ≻ means "preferred to"). We identify this as **transitive inconsistency**, which has been ignored in previous works. Due to the transitive inconsistency, we show that the ranker's performance is highly sensitive to the initial input order of the retrieved documents. Ranking systems expect to produce a robust ranking list to present to users, but if different initial orderings can lead to significant variant ranked lists, the reliability of the LLM's rankings can be brought into question. Our analysis of this inconsistency can be easily extended to setwise and listwise comparisons, as both ranking schemes rely on relative preferences and are fundamentally pairwise in nature. This broad applicability highlights that identifying and addressing these inconsistencies in pairwise ranking is relevant for improving the reliability of any ranking scheme based on relative preferences.

We propose the `LLM-RankFusion` framework as shown in Figure 1 to produce a consistent ranking list by mitigating the above inconsistencies. To mitigate order inconsistency, we first use calibration to address the conflict before and after swapping the passages. It calculates the preference probability based on the logit output, which then produces the preference without bias in position. To further let LLM realize the preference should be order agnostic, we propose the in-context learning (ICL) ranking prompt. The ICL prompt uses an example to demonstrate the swapping of passages doesn't affect the preference. While we can greatly reduce order inconsistency by ICL and calibration, the improved pairwise comparison still does not address transitive inconsistency directly. We use rank aggregation to further mitigate the transitive inconsistency. Rank aggregation is a commonly used post-process method in combining multiple ranking lists and yielding a robust ranking result [12, 23, 36]. We aggregate the ranking list proposals from LLM-based pairwise and setwise rankers with different underlying sorting algorithms or different LLMs that are responsible to make preference decisions.

In experiments, we show that ICL and calibration can reduce the effect of positional bias and increase the NDCG score significantly. We then show the effectiveness of aggregation in addressing transitive inconsistency by forming a consensus from multiple ranking lists. In summary, the contributions of this paper are:

- We investigate order inconsistency and, for the first time, identify and study transitive inconsistency in LLM-based ranking.
- We address order inconsistency by ICL and calibration. The improvement is significant in most LLMs.
- We bridge the area of LLM-based ranking with rank aggregation to mitigate the impact of transitive inconsistency in pairwise and setwise comparisons.
- We show the promising empirical performance of the aggregation method by studying the aggregation among different sorting algorithms and LLMs.

## 2 Related Work

**LLM-based ranking approaches** have been developed with distinct ranking schemes. Pointwise approaches [21, 35, 10] aim to estimate the relevance between a query and a single document. Listwise [38, 28] ranking methods aim to directly rank a list of documents by inserting the query and document list into an LLM's prompt and instructing it to output the reranked document identifiers, though they rely on the strong capability of LLMs, suffer from positional bias and are sensitive to document order in the prompt [49]. Pairwise ranking methods [32] provide the query and a pair of documents to the LLM, which is instructed to generate the identifier of the more relevant document; these pairwise comparisons are then aggregated using efficient sorting algorithms like Heapsort or Bubblesort to produce the final ranking. The Setwise approach [50] is also proposed to compare a set of documents at a time to further improve efficiency.

**Rank aggregation** has been widely used in many information retrieval tasks [14, 12]. Previous works [31, 15] also use aggregation to form the ranking list from pairwise comparison. We employ Borda count [9] to aggregate different ranking lists in our paper. Borda count assigns a score to each item based on its position in each input ranking and sums these scores to produce the final aggregated ranking. While other rank aggregation methods exist, such as Markov Chain-based methods [12], supervised learning approaches [26], and unsupervised methods like Kemeny rank aggregation [18], many of these are either NP-hard or not specifically designed for list aggregation. By using the simple and computationally efficient Borda count method, we aim to demonstrate the power of combining LLM-based ranking with aggregation, even without resorting to more complex aggregation techniques.

## 3 Inconsistency of LLM-based ranking

### 3.1 Inconsistency of Pairwise Comparisons

In this work, we identify and distinguish two types of inconsistencies that LLM-based rankers exhibit:

1. **Order Inconsistency:** The LLM's judgment on a pair of passages changes depending on the order they are presented in the prompt, which is also known as positional bias [27].
2. **Transitive Inconsistency:** The LLM makes a series of three or more judgments that logically contradict each other, over a set of three or more passages, i.e., _d_1 ≻ _d_2, _d_2 ≻ _d_3, _d_3 ≻ _d_1.

Under the pairwise ranking approach, each LLM query produces a pairwise comparison results on _di, dj_, the result can be _di ≻ dj_ or _dj ≻ di_, where _d_ represents a passage and ≻ means "preferred to". While we focus on pairwise comparisons in this work, our analysis of these two types of inconsistency can be easily extended to setwise or listwise ranking schemes. This is because both setwise and listwise comparisons still rely on relative preferences between individual passages, and are therefore fundamentally pairwise in nature. For example, the result of a setwise comparison _di ≻ dj, dk_ can be represented as two implicit pairwise comparisons, _di ≻ dj_ and _di ≻ dk_. Therefore, our inconsistency analysis can not only be applied to setwise and listwise ranking, but any ranking scheme that involves relative comparisons between passages.

### 3.2 Inconsistency Measurement

We measure the inconsistency in comparisons of a variety of LLMs using the TREC-DL2019 test set. We construct the pairwise preference among all passages using PRP-Allpair [32]. The order inconsistency can be shown in Table 1. In a pairwise ranking scheme, we ask the LLM to output `A` to select the first passage or `B` to select the second passage. We query both the permutations of passages and collect the logits of token `A` and token `B`. For an LLM with no positional bias, switching the order of a pair of passages will not affect the preference judgment, which leads to the average logits of `A` and `B` being equal. However, we can observe from Table 1 that the logits of these tokens typically suffer from an obvious discrepancy. This indicates that the LLM's choice is often biased towards either `A` or `B`, which implies order inconsistency.

We represent pairwise comparisons using a tournament graph - a complete graph where each vertex represents a passage and edges represent preferences between passages. In this graph, directed edges _di → dj_ indicate that passage _di_ is preferred over _dj_, while undirected edges indicate ties. Following PRP-Sort [32], we handle cases of order inconsistency (where swapping passage positions leads to different preferences) by marking them as ties in the graph. While these ties are treated equally in the graph structure, we note that the underlying passages may have different ground truth relevance scores.

To measure transitive inconsistency, we first construct the tournament graph by performing all pairwise comparisons between passages and marking order inconsistent pairs (those that change preference when swapped) as ties. We then count the number of inconsistent triads in the graph, following the method of Kulakowski [19]. An inconsistent triad occurs when three passages form a cycle of strict preferences - for example, when _d_1 is preferred over _d_2, _d_2 is preferred over _d_3, but _d_3 is preferred over _d_1, violating transitivity. The count of such triads serves as our metric for transitive inconsistency. As shown in Table 2, we observe that the frequency of inconsistent triads varies across different LLMs, with larger models generally exhibiting fewer transitive inconsistencies.

### 3.3 The Impact of Inconsistency

As shown in Tables 1 and 2, LLM-based rankers can exhibit significant amounts of inconsistency across judgments. Applying sorting-based ranking schemes based on non-transitive pairwise comparisons can produce volatile result rankings that are highly sensitive to the initial order of candidate passages. This can have particularly adverse effects if that initial ordering is a "hard list" for the chosen sorting method, as demonstrated in Table 3. A hard list is an initial order of passages where the high-relevance passages require many comparisons to be moved to the front of the ranking, increasing the likelihood of encountering a transitive inconsistency which blocks the promotion of the passage. A hard list for one sorting algorithm may not be as hard of a list for another, which is demonstrated in Table 3. By aggregating the full ranked lists from multiple sorting algorithms, we can mitigate the worst-case effects of inconsistency while producing more robust final rankings.

## 4 Addressing LLM-based Ranking Inconsistency

### 4.1 Mitigating Order Inconsistency

LLMs suffer from positional bias, which leads to the order inconsistency. This will result in conflicting comparisons after swapping the passage position. Previous work handled order inconsistency as ties in the comparison, which ignores the positional bias nature of LLM-based ranking. We propose 2 methods to mitigate the order inconsistency in the `LLM-RankFusion`.

#### 4.1.1 In-Context Learning (ICL)

We design the ICL prompt to utilize the few-shot ability [4] of LLMs to mitigate order inconsistency. The prompt provides the LLM with an example pairwise comparison for both order permutations as shown in Figure 1. This demonstration illustrates that the task is to compare the passages based on their relevance to the query instead of its position in the prompt. As shown in Table 1, using ICL can balance the probability of LLM selecting a passage from either position.

#### 4.1.2 Calibration

In a pairwise ranking scheme, we ask the LLM to output token `A` to select the first passage or `B` to select the second passage in the given prompt. The positional bias makes LLMs more likely to select the passage in a certain position of the prompt instead of only based on relevance. By considering the comparisons from both possible positions, even if the LLM is biased to a specific position, using the average output probability of a passage under all positions may address this bias.

For every pair of passages, we query the LLM with two permutations (_A_ = _di_, _B_ = _dj_) and (_A_ = _dj_, _B_ = _di_). For each output, `A` represents the first passage and `B` represents the second passage in the prompt. We then take the token probability of `A` and `B` from the LLM. We denote S_A(ij) and S_B(ij) as the log probabilities of the output tokens `A` and `B` with the permutation (_A_ = _di_, _B_ = _dj_). P(ij) in [0, 1] is the probability of _di_ preferred to _dj_ with the permutation (_A_ = _di_, _B_ = _dj_). The probability is generated among all candidate tokens by LLM. We know that only token `A` and token `B` represent a valid choice of passage, so we compute P(ij) and P(ji) as following:

> *[Formula: P(ij) = softmax(S_A(ij), S_B(ij))]*

To make the comparison satisfy P_ij + P_ji = 1, we denote the calibrated probability of _di ≻ dj_ as:

> *[Formula: P_ij = (P(ij) + 1 - P(ji)) / 2]*

Finally, we obtain the calibrated preference of _di ≻ dj_ if P_ij > 0.5.

### 4.2 LLM Ranking Aggregation

In passage ranking, we can generate multiple proposed ranking lists using different ranking settings. These settings can include different sorting algorithms to build fully ranked lists from pairwise, setwise, or listwise comparisons, as well as other factors like a specific LLM used for the preference query. Given the inconsistency discussed in Section 3, we know that any configuration of these settings can result in noisy rank results. We cannot assume we know _a priori_ which proposed rank setting is the best, so choosing a single setting that will be affected the least by inconsistency is difficult.

To address noisy ranked list proposals, we propose `LLM-RankFusion`, a rank aggregation pipeline as shown in Algorithm 1. Rank aggregation can address conflicting results by combining these results into a single, coherent ranking, limiting the effects of noisy settings.

Let _C_ = {_d_1, _d_2, ..., _dm_} be the set of _m_ passages, and let _V_ = {_v_1, _v_2, ..., _vn_} be the set of _n_ ranked list proposals. Each proposal _vj_ ranks the passages in order of preference, producing a ranked list _Lj_. We apply Borda count [37, 13, 9] to aggregate these proposals. For each passage _di_ the Borda count is calculated as follows:

> *[Formula: B(di) = sum over j of (m - rij + 1)]*

where _rij_ is the rank of passage _di_ in voter _vj_'s list _Lj_. The passage with the highest Borda count is the winner. The aggregated list _L_ is obtained by sorting the passages in descending order of their Borda counts.

**Algorithm 1: LLM Rank Aggregation Pipeline**

- **Require:** Query _q_, Corpus _D_, Rank settings _R_1, _R_2, ..., _Rk_
- **Ensure:** Aggregated rank list _L_
1. _L_1, _L_2, ..., _Lk_ ← ∅ (Initialize empty rank lists)
2. **for** _i_ ← 1 to _k_ **do**
3.   _Li_ ← RANKING(_q_, _D_, _Ri_) (Generate rank list using rank setting _Ri_)
4. **end for**
5. _L_ ← RANKAGGREGATION(_L_1, _L_2, ..., _Lk_) (Aggregate rank lists)
6. **return** _L_

#### 4.2.1 Aggregation Across Sorting Methods

We aggregate the ranked list proposals from two comparison-based sorting algorithms, Bubblesort and Heapsort. Bubblesort repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order; Heapsort uses a binary heap to sort elements. By combining the ranked lists from algorithms with different properties, the aggregated result becomes more robust to variations in the input data. If one algorithm performs poorly on a particular input, the other algorithm may compensate for it, leading to a more consistent overall ranking.

#### 4.2.2 Aggregation Across LLMs

Individual LLMs might also have unique biases in their preferences and, therefore, unique transitive inconsistency. This motivates aggregation across ranking lists from multiple LLMs. This can help to reduce the impact of any individual LLM, which may be inconsistent in handling certain queries. The aggregated result formed by decisions from multiple LLMs can be more robust and consistent. We group LLMs by their size and aggregate the ranking lists from LLMs with the similar number of parameters.

## 5 Experiments

### 5.1 Experimental Setup

We utilize test sets from TREC, a standard dataset for information retrieval research. Specifically, we use the top 100 passages retrieved by BM25 [22, 34] for each of the queries associated with the TREC-DL2019 and 2020 test sets [8]. Our results are based on the re-ranking of these 100 passages. The LLM ranking scheme is implemented under the same experimental setting of PRP-Sort [32].

We evaluate our results using two metrics: Normalized Discounted Cumulative Gain (NDCG) and average Kendall tau Distance. NDCG is a standard metric used to evaluate the quality of ranked retrieval results. It accounts for the position of relevant documents in the ranking, assigning higher importance to documents appearing earlier. Kendall tau distance is a metric used to measure the dissimilarity between two rankings. We compare our results against pairwise, setwise, and listwise baselines [32, 50, 38].

### 5.2 Addressing Order Inconsistency

We have shown that in-context learning can help to balance the average probability of the two choices given during pairwise ranking in Table 1. In Table 4, we can see that solely using ICL can help improve the ranking performance in most LLMs. Some encoder-decoder models like Flan-UL2 may intrinsically suffer from less positional bias than other decoder-only LLMs [24], so we don't expect much improvement with using ICL for those models. The calibration addresses order inconsistency by calculating preference probability based on comparison from both positions. The improvement from solely using the calibration is also significant, as shown in Table 4. We also find that using these two methods individually cannot improve ranking performance for Flan-UL2, but combining them can bring improvement compared to the baseline. Furthermore, as demonstrated in Table 5, our approach of combining pairwise ranking with ICL and calibration outperforms several baseline methods across different datasets.

### 5.3 Addressing Inconsistency via Aggregation

Table 6 demonstrates the effectiveness of both model and ranking scheme aggregation in improving ranking performance. Model Aggregation consistently outperforms individual models across both datasets, particularly for pairwise ranking. This trend is consistent across different ranking schemes and datasets, showing robustness through aggregation. On ranking scheme aggregation, we observe that combining different approaches mitigates individual weaknesses. Scheme Aggregation shows balanced performance, often achieving scores close to or exceeding the best individual scheme. This suggests that aggregating across ranking schemes can provide a more stable and potentially superior ranking, leveraging the strengths of both pairwise and setwise approaches, as well as different sorting algorithms.

**Aggregation across sorting algorithms** attempts to mitigate the impact of the initial order on an individual sorting algorithm. As seen in Table 7 and Table 9 in the appendix, `LLM-RankFusion` provides significant benefits to baseline sorting-based ranking approaches. Each of the initial orderings underwent re-ranking from both pairwise prompting with Bubblesort and Heapsort, and the two final rank lists were aggregated using Borda count. NDCG@10 and Kendall-tau distance were recorded and averaged across each final list for each model. In all models, we see an increase in NDCG@10 as well as reduced inconsistency with lower Kendall-tau distances. ICL and calibration significantly increase the NDCG while also reducing the Kendall-tau distance, and the aggregation further reduces the inconsistency of the worse sorting algorithm (in this case Bubblesort), while keeping NDCG relatively constant. This is a promising result, showing that `LLM-RankFusion` can improve both consistency and ranking quality by aggregating the rankings produced by different sorting algorithms.

**Aggregation across LLMs** attempts to produce a final ranking that is less sensitive to the individual biases of different LLMs. This can be observed by comparing Table 8 to previous Table 7 and Table 9 in the appendix, as the average Kendall-tau distance of the aggregated rankings can always achieve a medium performance among the LLMs it aggregates from. This shows promising results of `LLM-RankFusion` to find a consensus ranking list that achieves _balanced or even superior_ performance. In a typical passage ranking case, we don't assume we know which LLM is better at ranking the specific passage list. Hence, it is particularly useful if we can get at least medium performance rankings by aggregating multiple proposals.

### 5.4 Computation Cost

The performance of LLM-based passage ranking is mainly determined by the LLM inference performance and the number of comparisons required to sort a list. The aggregation in `LLM-RankFusion` requires that takes in individual ranking lists and the time cost depends on the slowest model if individual rankings are computed in parallel. The calibration doesn't bring additional inference costs because it only collects the output logits and calculates preference probability based on two permutations of passages. The ICL leads to a longer prompt, which slightly increases the computation during inference as shown in Table 14 in the appendix.

## 6 Conclusion

In this paper, we focus on addressing order inconsistency and transitive inconsistency we identify in LLM-based ranking. These inconsistencies can significantly impact the reliability of LLM-based ranking systems. To mitigate these issues, we proposed the `LLM-RankFusion` pipeline, which incorporates in-context learning (ICL) and calibration to address order inconsistency and rank aggregation to tackle transitive inconsistency. Our experiments demonstrated that ICL and calibration effectively reduce order inconsistency, leading to improved NDCG scores. Furthermore, we showed that aggregation mitigates transitive inconsistency by forming a consensus from multiple ranking lists. By exploring the idea of aggregating the decisions of multiple LLMs in the specific domain of passage ranking, our work highlights the potential of combining the strengths of different LLMs.

## References

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_, 2023.
- [2] Payal Bajaj, Daniel Campos, Nick Craswell, Li Deng, Jianfeng Gao, Xiaodong Liu, Rangan Majumder, Andrew McNamara, Bhaskar Mitra, Tri Nguyen, et al. Ms marco: A human generated machine reading comprehension dataset. _arXiv preprint arXiv:1611.09268_, 2016.
- [3] Luiz Bonifacio, Vitor Jeronymo, Hugo Queiroz Abonizio, Israel Campiotti, Marzieh Fadaee, Roberto Lotufo, and Rodrigo Nogueira. mmarco: A multilingual version of the ms marco passage ranking dataset. _arXiv preprint arXiv:2108.13897_, 2021.
- [4] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. _Advances in neural information processing systems_, 33:1877-1901, 2020.
- [5] Wenshuo Chao, Zhi Zheng, Hengshu Zhu, and Hao Liu. Make large language model a better ranker. _arXiv preprint arXiv:2403.19181_, 2024.
- [6] Wei-Lin Chiang, Zhuohan Li, Zi Lin, Ying Sheng, Zhanghao Wu, Hao Zhang, Lianmin Zheng, Siyuan Zhuang, Yonghao Zhuang, Joseph E. Gonzalez, Ion Stoica, and Eric P. Xing. Vicuna: An open-source chatbot impressing gpt-4 with 90%* chatgpt quality, March 2023.
- [7] Hyung Won Chung, Le Hou, Shayne Longpre, Barret Zoph, Yi Tay, William Fedus, Yunxuan Li, Xuezhi Wang, Mostafa Dehghani, Siddhartha Brahma, et al. Scaling instruction-finetuned language models. _Journal of Machine Learning Research_, 25(70):1-53, 2024.
- [8] Nick Craswell, Bhaskar Mitra, Emine Yilmaz, Daniel Campos, and Ellen M Voorhees. Overview of the trec 2019 deep learning track. _arXiv preprint arXiv:2003.07820_, 2020.
- [9] de Borda. Memoire sur les elections par scrutin (memoir on elections by ballot), 1784.
- [10] Andrew Drozdov, Honglei Zhuang, Zhuyun Dai, Zhen Qin, Razieh Rahimi, Xuanhui Wang, Dana Alon, Mohit Iyyer, Andrew McCallum, Donald Metzler, and Kai Hui. Parade: Passage ranking using demonstrations with large language models, 2023.
- [11] Paul Duetting, Vahab Mirrokni, Renato Paes Leme, Haifeng Xu, and Song Zuo. Mechanism design for large language models. _arXiv preprint arXiv:2310.10826_, 2023.
- [12] Cynthia Dwork, Ravi Kumar, Moni Naor, and D Sivakumar. Rank aggregation revisited, 2001.
- [13] Peter Emerson. The original borda count and partial voting. _Social Choice and Welfare_, 40(2):353-358, 2013.
- [14] Mohamed Farah and Daniel Vanderpooten. An outranking approach for rank aggregation in information retrieval. In _Proceedings of the 30th annual international ACM SIGIR conference on Research and development in information retrieval_, pages 591-598, 2007.
- [15] Lukas Gienapp, Maik Frobe, Matthias Hagen, and Martin Potthast. Sparse pairwise re-ranking with pre-trained transformers. In _Proceedings of the 2022 ACM SIGIR International Conference on Theory of Information Retrieval_, pages 72-80, 2022.
- [16] Reinhard Heckel, Nihar B Shah, Kannan Ramchandran, and Martin J Wainwright. Active ranking from pairwise comparisons and when parametric assumptions do not help. 2019.
- [17] Albert Q Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, Blanche Savary, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Emma Bou Hanna, Florian Bressand, et al. Mixtral of experts. _arXiv preprint arXiv:2401.04088_, 2024.
- [18] John G Kemeny and LJ Snell. Preference ranking: an axiomatic approach. _Mathematical models in the social sciences_, pages 9-23, 1962.
- [19] Konrad Kulakowski. Inconsistency in the ordinal pairwise comparisons method with and without ties. _European Journal of Operational Research_, 270(1):314-327, 2018.
- [20] Yongqi Li, Xinyu Lin, Wenjie Wang, Fuli Feng, Liang Pang, Wenjie Li, Liqiang Nie, Xiangnan He, and Tat-Seng Chua. A survey of generative search and recommendation in the era of large language models. _arXiv preprint arXiv:2404.16924_, 2024.
- [21] Percy Liang, Rishi Bommasani, Tony Lee, Dimitris Tsipras, Dilara Soylu, Michihiro Yasunaga, Yian Zhang, Deepak Narayanan, Yuhuai Wu, Ananya Kumar, et al. Holistic evaluation of language models, 2023.
- [22] Jimmy Lin, Xueguang Ma, Sheng-Chieh Lin, Jheng-Hong Yang, Ronak Pradeep, and Rodrigo Nogueira. Pyserini: An easy-to-use python toolkit to support replicable ir research with sparse and dense representations, 2021.
- [23] Shili Lin. Rank aggregation methods. _Wiley Interdisciplinary Reviews: Computational Statistics_, 2(5):555-570, 2010.
- [24] Nelson F Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. Lost in the middle: How language models use long contexts. _Transactions of the Association for Computational Linguistics_, 12:157-173, 2024.
- [25] Tie-Yan Liu et al. Learning to rank for information retrieval. _Foundations and Trends in Information Retrieval_, 3(3):225-331, 2009.
- [26] Yu-Ting Liu, Tie-Yan Liu, Tao Qin, Zhi-Ming Ma, and Hang Li. Supervised rank aggregation. In _Proceedings of the 16th international conference on World Wide Web_, pages 481-490, 2007.
- [27] Yao Lu, Max Bartolo, Alastair Moore, Sebastian Riedel, and Pontus Stenetorp. Fantastically ordered prompts and where to find them: Overcoming few-shot prompt order sensitivity. _arXiv preprint arXiv:2104.08786_, 2021.
- [28] Xueguang Ma, Xinyu Zhang, Ronak Pradeep, and Jimmy Lin. Zero-shot listwise document reranking with a large language model. _arXiv preprint arXiv:2305.02156_, 2023.
- [29] Rodrigo Nogueira and Kyunghyun Cho. Passage re-ranking with bert. _arXiv preprint arXiv:1901.04085_, 2019.
- [30] R OpenAI. Gpt-4 technical report. _arXiv_, pages 2303-08774, 2023.
- [31] Ronak Pradeep, Rodrigo Nogueira, and Jimmy Lin. The expando-mono-duo design pattern for text ranking with pretrained sequence-to-sequence models. _arXiv preprint arXiv:2101.05667_, 2021.
- [32] Zhen Qin, Rolf Jagerman, Kai Hui, Honglei Zhuang, Junru Wu, Jiaming Shen, Tianqi Liu, Jialu Liu, Donald Metzler, Xuanhui Wang, et al. Large language models are effective text rankers with pairwise ranking prompting. _arXiv preprint arXiv:2306.17563_, 2023.
- [33] Siddartha Y Ramamohan, Arun Rajkumar, and Shivani Agarwal. Dueling bandits: Beyond condorcet winners to general tournament solutions. _Advances in Neural Information Processing Systems_, 29, 2016.
- [34] Stephen Robertson, Hugo Zaragoza, et al. The probabilistic relevance framework: bm25 and beyond. _Foundations and Trends in Information Retrieval_, 3(4):333-389, 2009.
- [35] Devendra Singh Sachan, Mike Lewis, Mandar Joshi, Armen Aghajanyan, Wen tau Yih, Joelle Pineau, and Luke Zettlemoyer. Improving passage retrieval with zero-shot question generation, 2023.
- [36] Frans Schalekamp and Anke van Zuylen. Rank aggregation: Together we're strong. In _2009 Proceedings of the Eleventh Workshop on Algorithm Engineering and Experiments (ALENEX)_, pages 38-51. SIAM, 2009.
- [37] Nihar B Shah and Martin J Wainwright. Simple, robust and optimal ranking from pairwise comparisons. _Journal of machine learning research_, 18(199):1-38, 2018.
- [38] Weiwei Sun, Lingyong Yan, Xinyu Ma, Shuaiqiang Wang, Pengjie Ren, Zhumin Chen, Dawei Yin, and Zhaochun Ren. Is chatgpt good at search? investigating large language models as re-ranking agents, 2023.
- [39] Raphael Tang, Xinyu Zhang, Xueguang Ma, Jimmy Lin, and Ferhan Ture. Found in the middle: Permutation self-consistency improves listwise ranking in large language models. _arXiv preprint arXiv:2310.07712_, 2023.
- [40] Yi Tay, Mostafa Dehghani, Vinh Q Tran, Xavier Garcia, Jason Wei, Xuezhi Wang, Hyung Won Chung, Siamak Shakeri, Dara Bahri, Tal Schuster, et al. Ul2: Unifying language learning paradigms. _arXiv preprint arXiv:2205.05131_, 2022.
- [41] Gemma Team, Thomas Mesnard, Cassidy Hardin, Robert Dadashi, Surya Bhupatiraju, Shreya Pathak, Laurent Sifre, Morgane Riviere, Mihir Sanjay Kale, Juliette Love, et al. Gemma: Open models based on gemini research and technology. _arXiv preprint arXiv:2403.08295_, 2024.
- [42] Nandan Thakur, Nils Reimers, Andreas Ruckle, Abhishek Srivastava, and Iryna Gurevych. Beir: A heterogenous benchmark for zero-shot evaluation of information retrieval models. _arXiv preprint arXiv:2104.08663_, 2021.
- [43] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothee Lacroix, Baptiste Roziere, Naman Goyal, Eric Hambro, Faisal Azhar, et al. Llama: Open and efficient foundation language models. _arXiv preprint arXiv:2302.13971_, 2023.
- [44] Peiyi Wang, Lei Li, Liang Chen, Dawei Zhu, Binghuai Lin, Yunbo Cao, Qi Liu, Tianyu Liu, and Zhifang Sui. Large language models are not fair evaluators. _arXiv preprint arXiv:2305.17926_, 2023.
- [45] Likang Wu, Zhi Zheng, Zhaopeng Qiu, Hao Wang, Hongchao Gu, Tingjia Shen, Chuan Qin, Chen Zhu, Hengshu Zhu, Qi Liu, et al. A survey on large language models for recommendation. _arXiv preprint arXiv:2305.19860_, 2023.
- [46] Yifan Zeng, Yiran Wu, Xiao Zhang, Huazheng Wang, and Qingyun Wu. Autodefense: Multiagent llm defense against jailbreak attacks. _arXiv preprint arXiv:2403.04783_, 2024.
- [47] Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang, Junjie Zhang, Zican Dong, et al. A survey of large language models. _arXiv preprint arXiv:2303.18223_, 2023.
- [48] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric Xing, et al. Judging llm-as-a-judge with mt-bench and chatbot arena. _arXiv preprint arXiv:2306.05685_, 2023.
- [49] Yutao Zhu, Huaying Yuan, Shuting Wang, Jiongnan Liu, Wenhan Liu, Chenlong Deng, Zhicheng Dou, and Ji-Rong Wen. Large language models for information retrieval: A survey. _arXiv preprint arXiv:2308.07107_, 2023.
- [50] Shengyao Zhuang, Honglei Zhuang, Bevan Koopman, and Guido Zuccon. A setwise approach for effective and highly efficient zero-shot ranking with large language models, 2023.

## A Technical Appendix

### A.1 Limitations

The aggregation process in `LLM-RankFusion` requires fully sorted individual ranked lists, which increases the computation costs. Additionally, the use of ICL leads to longer prompts, increasing the overhead during inference. Another limitation of our study is that the experiments were conducted on limited IR datasets (TREC-DL2019 and TREC-DL2020), and other aggregation methods were not included in the current research.

### A.2 Future Work

Future Work can focus on LLM-based rank aggregation approaches that decide the comparison strategy on-the-fly and directly aggregate from pairwise comparisons without relying on sorting algorithms [33, 16, 15]. Exploring the potential of aggregating LLM-based decisions in other tasks and domains beyond passage ranking could lead to a more general understanding of the effectiveness of combining the intelligence of multiple LLMs for improved performance and consistency in a wider range of applications [11].

### A.3 Example Passage Ranking

We show an example passage ranking that contain 15 passages for a query. The details of these 15 passages are shown in Table 10 and Table 11. The ranking results from different settings are shown in Table 12.

### A.4 Implementation details

We use LLMs with a variety of sizes in our experiments: **GPT** [30]: GPT-3.5-Turbo-1106, GPT4-1106; **LLaMA-3** [43]: LLaMA-3-70B, LLaMA-3-8B; **Vicuna** [48, 6]: Vicuna-v1.5-13b; **Mixtral** [17]: Mixtral-8x7b-v0.1; **Gemma** [41] Gemma-7B; **Flan-T5** [7, 40] Flan-UL2, Flan-T5-XXL. This aims to explore the capacity of different sizes of LLMs and the trade-off between efficiency and ranking quality.

The LLM inference is implemented based on HuggingFace. The instruction fine-tuned version of the model is used if available. The temperature of LLM is set to 0, which means _argmax_ will be applied to the candidate tokens during generation. We use 2 x NVIDIA H100 80GB HBM3 and 4 x Tesla V100-SXM3-32GB GPUs to run our experiment.

### A.5 Prompt

We show a comparison prompt example in Table 13. The first two rounds of chat is the in-context Learning (ICL) prompt. We expect the LLM can learn the order-agnostic property from the demonstration of ICL prompt.

### A.6 Performance

The average number of comparisons required to rank a list is 3574.21 +/- 501.23 for Bubblesort and 972.77 +/- 47.69 for Heapsort. We benchmark the comparison rate of different LLM rankers in Table 14. The prompt is longer after applying ICL, which decreases the LLM inference performance. We only generate 1 token for each comparison on those open-source LLMs. Each pairwise comparison involves prompting the LLM in two different passage permutations. It requires 2 prompt and generate operations to finish a single pairwise comparison. We benchmark the performance on NVIDIA H100 80GB HBM3 GPU.

### A.7 Analysis of Prompt Design Sensitivity

To evaluate the robustness of our proposed methods against variations in prompt design, we conducted additional experiments using GPT-4 to generate 10 different pairwise ranking prompt templates. Each template maintained the core task of comparing passage relevance while varying factors such as wording, formatting, and instruction style. We tested these prompts using Llama-3-8B on the TREC-DL2019 dataset under different configurations. The results in Table 15 demonstrate two key benefits of our approach:

1. **Enhanced Performance:** The combination of ICL and calibration substantially improves ranking quality, with NDCG scores increasing by approximately 8 points compared to the baseline across both sorting algorithms.
2. **Reduced Variance:** The baseline exhibits considerable sensitivity to prompt design, as evidenced by the high standard deviations (3.07-4.63). In contrast, configurations using ICL and calibration show markedly lower variance (1.61-1.92), indicating more stable performance across different prompt designs.
