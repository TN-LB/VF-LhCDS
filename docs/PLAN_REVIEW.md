# VF-LhCDS plan 审查与修改说明

审查日期：2026-09-09。对象：上传的 `VF-LhCDS.zip` 中的任务计划、算法规格、实验计划、工作流和 prompts，以及作为语义依据的 `papers/veri_free_lhcds_v3_1_submit.md`。

## 一、结论

原计划的主路线是合理的：先建立独立真值，再实现精确 closure oracle，之后接入左优先分治，最后开展安全优化与基线实验。本次不改变这条算法路线，而是修正实现契约、消除跨文件矛盾，并缩小第一个正确性版本的工作范围。

最重要的修改是把“做完一个模块”改成“兑现一项证明义务”：每项任务现在对应明确的定理前提、可观察行为、独立测试及验收证据。测试通过不等于数学证明，文档修改也不等于代码已经实现。

四份 `papers/` 文件保持逐字节不变。对严格区间前提等需要补充论证的地方，在 `THEORY_TO_CODE_AUDIT.md` 中单独给出实现层澄清，没有静默改写论文。本文所述小图检查未发现主链—分治—结构抽取路线的反例，但不构成整个证明稿的形式化验证。

## 二、必须修正的正确性边界

### 1. 区分“分治端点”和“oracle 搜索上界”

原计划规定 core 缩减后的 `Y'`，但没有充分约束其在分治控制流中的用途。这容易让实现把 `Y'` 当作新的主链端点，或据此重新计算分隔参数。

依据：Lemma 1.15、Theorem 1.16，以及 §1.6 / Lemma 1.22。论文明确允许缩减后的上界不属于主链，因此它不能直接继承主链端点的用途。

修改后的规则：

```text
lambda = d_h(Y, X)                     # 使用原始主链端点
Y_oracle = Y ∩ core_ceil(lambda)(G)     # 只缩减本次 oracle 的搜索范围
Z = global_F(lambda, X, Y_oracle)
terminal ⇔ Z == Y                     # 仍与原始 Y 比较
```

递归子区间仍为 `(X,Z)`、`(Z,Y)`；终止层仍在原图的 `G[Y\X]` 上抽取。不能用 `Y_oracle` 重算 lambda、判断终止、抽取叶子或替换递归端点。

已加入一个 8 顶点反例：`K4` 与“三角形加一个悬挂顶点”的不交并。在 `h=2` 时，根查询参数为 `5/4`；2-core 删除悬挂顶点，但该 core 不是主链集合。若永久替换原始端点，低密度答案可能被错误地缩成三角形，丢失 maximality。

### 2. 区分 restricted optimum 与全局 F_h(lambda)

原规格把 `X ⊊ F_h(lambda) ⊆ Y` 作为所有 oracle 请求的前提，但测试又要求全局查询和任意较大 lambda。当 lambda 高于所有子图密度时，全局 F 就是空集，严格前提无法成立。

修改为两个契约：

```text
largest_restricted(lambda, X, Y_oracle)
global_F(lambda, certified_bounds)
```

前者求区间内的最大包含意义 maximizer；后者只有在 `F_h(lambda)` 被证明包含于该区间时，才承诺全局结果。严格的 `X ⊊ F` 进展条件只用于分治分隔查询。

补充论证说明 closure 构造也适用于 `X=F`，以及如何处理 `X=Y`；没有把任意局部最优解冒充全局 F。全局零参数查询必须满足 `Y_oracle=V`；任意较小上界的零参数结果只能称为 restricted optimum。

### 3. 参考主链必须独立生成，不能循环验证

原计划要求主链测试，但没有明确独立、完整的生成方法；某些表述还把它列为可选项。若通过待验证的分隔递归产生“预期主链”，会让结构错误在两条路径中同时出现。

修改为：按顶点数 j，穷举得到 `M_j = max_{|S|=j} mu_h(S)`；枚举直线 `M_j-lambda*j` 的非负交点、相邻交点的精确有理中点、零参数和足够大的上界，再用穷举 F 取出所有不同链集合。

只扫描 `mu_h(S)/|S|` 不够，因为后续断点是 outer density，可能不等于任何诱导子图自身的密度。本次检查找到了一个 7 顶点实例，具体边集和断点保存在审查结果 JSON 中。

### 4. 两种 tie-breaking 必须分开

oracle 的 `+|S|` 是在主目标最优解中选最大基数，由 union closure 得到唯一最大包含集合；输出的 lexicographic order 则是在等密度 LhCDS 之间决定固定 k 的顺序。二者不是同一种 tie-breaking。

原重编号测试要求“顶点重命名后逐一对应输出”，对截断于并列密度层的 fixed-k 答案并不成立：原始 ID 的字典序改变，合法选择也可能改变。

修改为：先映射完整真值集合，再按照新 ID 的顺序重新排序，最后截取 top-k。两个不交的边交换 ID 块，就是最小的直观见证。

### 5. “终止层所有分量密度相等”需要缩小适用范围

Theorem 1.16 保证的是通过反邻接条件、实际被输出的分量满足该层密度；不是 `G[Y\X]` 的所有连通分量都满足。

反例：`h=2` 的 `K4` 外接一个悬挂顶点。最后增量只有该顶点，增量外密度为 1，但这个单点自身的边密度为 0。它因为与 X 有边而被拒绝。

已把规格、任务和测试统一为“只有被输出分量才保证层密度”，并要求普通图边连通性，而非 clique-adjacency。

### 6. 保留已接受的真实任意精度回退

`DECISIONS.md` 的 D005 已要求固定宽度不安全时自动使用 arbitrary-precision backend；原算法规格和 prompt 03 却只要求接口预留或 test-only backend，并允许溢出后直接退出。两者不一致。

修改后保留 D005：计数、分数、目标比较、容量、残量更新和总流量都必须安全；在精确预检查后选择 checked 128-bit 或真实任意精度执行路径。不能用“留好了接口”满足自动回退要求。

新增建议测试：在极小图上使用很大的精确有理参数，触发真实回退，而不必构造不切实际的大图。资源耗尽需要显式报告，不能静默近似或将部分结果当作完成。

## 三、简化任务范围与执行顺序

原 9 个 phase 重新组织为 6 个里程碑：

| 里程碑 | 核心结果 |
|---|---|
| M0 | 契约审查、快照和仓库骨架 |
| M1 | 直接定义真值、穷举 F、独立主链 |
| M2 | 图/clique 基础设施、精确 closure oracle |
| M3 | 左优先 fixed-k solver、测试及正确性冻结 |
| M4 | 可选的安全 core 与有依据的优化 |
| M5 | 已验证基线、实验及复现发布 |

M3 可以独立完成，不依赖外部 baseline 是否能获得或编译。

第一个正确性版本只要求一个 materialized clique 后端；保留聚合 footprint 和端点计数复用。streaming、其他 max-flow 算法、并行、component-wise 调度、tie-inclusive 输出及额外 oracle cache 都转为后续可选项，不能继续出现在首版验收门槛中。

这里的简化不削弱精确数值要求：checked 128-bit 和 arbitrary precision 是同一精确 Dinic 算法的容量类型与执行路径，不是两套需要同时优化的新算法。

也修正了消融设计：聚合 footprint 和 materialized storage 已属于 B0，不能又被当成首个优化。full-chain 与 early-stop 的输出数量本就不同，应比较对应前缀，而不是要求整个输出文件 hash 相同。

## 四、把“理论证明”“实现证据”“实验结果”拆开

新增并填充 `docs/THEORY_TO_CODE_AUDIT.md`，将 O01–O12 对应到精确定理编号、前提、实现契约及测试 ID。它是论证表；`CLAIM_TRACEABILITY.md` 则专门存放真实代码符号、命令、日志和 commit，避免两份文档重复维护不同的语义。

测试改为 T01–T17，并给出明确的 smoke、全枚举、higher-h 和 seeded 层级，不再把“足够多随机测试”当作无边界任务。参考 maximality 仍必须检查所有 proper supersets；两个三角形通过普通桥边连接的例子说明，仅检查单顶点扩展会漏掉更大的 compact 超集。

完整基本递归的 `2r-1` 计数明确为 logical interval queries；零参数不需要最小割，所以它不必等于实际 mincut 次数。该界也不意味着 O(k) 或实际可扩展性。

大图验证区分：

- `definition-checked`：真正执行删除子集与超集检查。
- `structural-checked`：顶点、计数、密度、连通性、排序等检查。
- `cross-implementation-agreement`：与另一已审查实现一致。

后两者不单独证明 maximality 或答案完整性；也不能在算法内部加候选验证来掩盖 solver 错误。

## 五、基线、实验与确认流程的同步修正

D012 已确认 DCLDS 是独立并行工作，原 README、baseline audit 和实验矩阵却仍要求重新确认归属。本次保留该决定，新增明确的 `09b_dclds_baseline_adapter.md`，把 DCLDS 与 IPPV 列为 general-h 主比较目标。仅核实公开出版/仓库元数据，没有展开 DCLDS 算法技术比较，也没有导入其技术。

DCLDS 的出版信息由出版社检索结果支持，其仓库元数据也可查；这不等于已验证仓库 commit、许可证、构建、算法细节或输出正确性。公开来源记录在 `BASELINE_AUDIT.md` 的 E1–E4。保存快照只能证明所提供内容的版本，不独立证明研究时间优先性或新颖性。

h=2/h=3 专用方法按实际比较主张纳入，历史方法无法获得时明确记录限制，而不是要求先重实现所有方法才能推进。

计时统一为端到端、包含初始枚举的 post-load、以及有明确边界的 post-index 诊断计时。外部验证另行计时；baseline 自带候选验证属于其算法成本，不能扣掉。

保留全体声明顶点，包括 isolates；`k=0` 按理论定义拒绝。原 AGENTS 的“一切选择都先询问”改为仅对新的、会影响定义、结论或实验公平性的决定询问；既有决定和证明已经确定的事项不再反复阻塞。新修订决策标记为 `specified-in-revision`，没有伪称为此前的 owner confirmation。

## 六、本次实际检查了什么

执行了独立的审查脚本 `review/math_sanity.py`：

```text
python review/math_sanity.py --output review/math_sanity_results.json
```

已完成并通过：

1. 1–5 顶点的全部有标号简单图，在 h=2、3 下的 2,198 个图/h 实例。
2. 固定种子 20260909 的另外 150 个图/h 实例，覆盖 6–8 顶点和 h=2、3、4、h>n 的采样情况。
3. 4 项具名边界检查：多顶点 maximality、重编号并列顺序、被拒绝分量的层密度，以及不属于主链的 core 上界。

普通实例合计 2,348 个；具名边界检查另外列示。检查范围包括直接定义真值、独立主链、所有主链端点对的 separator、core 包含与受限最优一致性、正参数查询的 footprint 恒等式与扰动目标、原图结构抽取和完整 logical call 计数。

脚本使用穷举 F，不是生产 max-flow 实现。因此本次**没有**完成生产 C++ solver、max-flow/min-cut 后端、真实 128-bit 回退实现、ASan/UBSan、baseline 构建或性能实验。所有正式实现任务仍保持未勾选。有限样例通过也不替代一般性证明。

## 七、交付文件与建议入口

主入口：`docs/IMPLEMENTATION_PLAN.md`。
执行入口：`docs/TASKS.md`。
理论契约：`docs/ALGORITHM_SPEC.md` 与 `docs/THEORY_TO_CODE_AUDIT.md`。
独立验收：`docs/CORRECTNESS_TEST_PLAN.md`。
改动说明：本文件。
本次运行记录与反例：`review/math_sanity_results.json`。
内容保全与文档检查：`review/artifact_audit.json`、`review/source_snapshot_sha256.json`。

相关 README、AGENTS、架构、决策、实验/复现文件及全部任务 prompts 已同步。修改包不携带 `.git/` 和 macOS 元数据；原始上传 ZIP 保持不变。归档中的审查脚本仅用于解释本次修改，不占用正式生产实现目录。

下一步应从 M0 开始按修订后的契约推进；不需要先补齐 streaming、并行或所有历史 baseline。
