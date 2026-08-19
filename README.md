# Verification-Free LhCDS: Codex Implementation Kit

这套文件用于把 `veri_free_lhcds_v3_1_submit.md` 中的理论结果转成一个可验证、可优化、可复现实验的实现工程。默认项目名为 **VF-LhCDS**，可以在建仓库时重命名。

## 1. 权威材料与用途

将以下四份文件放到目标仓库的 `papers/` 目录，文件名保持不变：

- `veri_free_lhcds_v3_1_submit.md`：算法语义与正确性的唯一首要来源。
- `2023-icde-lds.md`：`h=2` 情形的层次结构、分治顺序和工程组织参考。
- `2408.14022v1.md`：通用 `h` 的精确基线 IPPV，以及实验数据集和参数参考。
- `2504.10937v1.md`：`h=2` 的 LDScvx 和 `h=3` 的 LTDScvx 基线及实验方法参考。

材料之间若有术语、tie-breaking 或问题定义差异，以你的理论稿为准，不允许 Codex 自动“统一”或修正。

## 2. 建议仓库布局

```text
vf-lhcds/
├── AGENTS.md
├── CMakeLists.txt
├── README.md
├── papers/
│   ├── veri_free_lhcds_v3_1_submit.md
│   ├── 2023-icde-lds.md
│   ├── 2408.14022v1.md
│   └── 2504.10937v1.md
├── docs/
│   ├── IMPLEMENTATION_PLAN.md
│   ├── ALGORITHM_SPEC.md
│   ├── ARCHITECTURE.md
│   ├── CORRECTNESS_TEST_PLAN.md
│   ├── EXPERIMENT_PLAN.md
│   ├── BASELINE_AUDIT.md
│   ├── REPRODUCIBILITY.md
│   ├── CLAIM_TRACEABILITY.md
│   ├── DECISIONS.md
│   └── TASKS.md
├── prompts/
├── reference/                 # Python 小图真值实现
├── include/vflhcds/
├── src/
├── tests/
├── tools/
├── scripts/
├── configs/
├── datasets/                  # 不提交原始大图
├── baselines/                 # git submodule 或固定 commit 的外部代码
└── results/                   # 原始日志、manifest、聚合表
```

本 kit 中除 `AGENTS.md` 外的根级文档，建议复制到仓库的 `docs/`；`prompts/` 原样复制。

## 3. 推荐实施顺序

1. 运行 `prompts/00_theory_audit_and_repo_bootstrap.md`，只做语义审计和仓库骨架。
2. 完成 Python 小图真值程序，不先写高性能算法。
3. 完成 C++ 图与 clique 基础设施。
4. 独立实现并验证 `F_h(lambda)` 精确 closure oracle。
5. 接入左优先分治与终止层叶节点抽取。
6. 做大量 differential testing，达到正确性门禁后再优化。
7. 加入安全的 clique-core reduction、缓存和网络缩减。
8. 固定基线 commit、适配统一 I/O，再跑消融和主实验。
9. 使用 `/review` 分别做正确性审查、性能审查和复现审查。

## 4. 三条不可妥协的原则

### 4.1 先有真值，再有性能

小图 exhaustive oracle 是整个工程的 correctness anchor。任何优化都必须对同一随机种子集合与真值版本做回归。

### 4.2 正确性路径不用浮点数

`lambda=a/b`、密度、断点比较、closure capacity 和输出排序都必须使用精确整数或精确分数。浮点数只允许出现在展示和性能报告中。

### 4.3 基线按 `h` 分层比较

- `h=2`：VF-LhCDS、IPPV、LDS-Opt、LDScvx、LDSflow。
- `h=3`：VF-LhCDS、IPPV、LTDScvx、LTDSflow。
- `h>=4`：VF-LhCDS 与支持任意 `h` 的精确方法，例如 IPPV；其他方法不能被描述为通用 LhCDS 基线。

## 5. 当前必须先核实的外部项目

截至 2026-08-19，公开代码库中存在 `s01bvral/DCLDS`，其 README 声称实现了 divide-and-conquer LhCDS。它与本算法主题高度重合。开始写论文性能结论前，应先查明：

- 是否是你或合作者的现有工程；
- 是否对应已发表、投稿中或未公开论文；
- 算法定义、oracle、分治 separator 和 tie-breaking 是否相同；
- 许可证、commit、实验配置和可复现性；
- 若为独立工作，是否应作为最直接基线或相关工作。

不要在 provenance 未确认前复制其中代码，也不要先声称“新 SOTA”。

## 6. Codex 使用方式

每个 prompt 都按照 Goal、Context、Deliverables、Boundaries、Verification 组织。先在仓库根目录启动 Codex，再明确附上对应文件路径。多模块并行时，可分别使用 worktree，但只能在接口和测试契约已经合并后并行开发。

每个阶段结束都应要求 Codex 报告：

- 修改了哪些文件；
- 运行了哪些命令；
- 测试结果和随机种子；
- 尚未解决的风险；
- 是否更新了 `CLAIM_TRACEABILITY.md` 和 `DECISIONS.md`。

## 7. 建议的第一条 Codex 消息

```text
/plan
Read AGENTS.md, docs/IMPLEMENTATION_PLAN.md, docs/ALGORITHM_SPEC.md,
docs/CORRECTNESS_TEST_PLAN.md, and the four files under papers/.
Then execute prompts/00_theory_audit_and_repo_bootstrap.md.
Do not implement the production solver until the semantic audit is accepted.
```
