# Codex Prompt Index for VF-LhCDS

这些 prompt 按依赖顺序组织。每次只执行一个主 prompt；完成、审查并提交后再进入下一阶段。除非 prompt 明确允许，不要把多个阶段合并成一次大改动。

## 建议顺序

| 阶段 | Prompt | 主要产物 | 进入条件 |
|---|---|---|---|
| 0 | `00_theory_audit_and_repo_bootstrap.md` | 理论到代码审计、仓库骨架 | 四篇材料已放入 `papers/` |
| 1 | `01_exhaustive_reference_oracle.md` | Python 小图真值实现 | 阶段 0 的语义问题已记录 |
| 2 | `02_graph_and_clique_infrastructure.md` | C++ 图和 clique 基础设施 | reference tests 通过 |
| 3 | `03_exact_closure_oracle.md` | 精确 `F_h(lambda)` oracle | clique 枚举已对拍 |
| 4 | `04_divide_and_conquer_solver.md` | 完整 top-k solver | oracle differential tests 通过 |
| 5 | `05_differential_test_campaign.md` | 大规模小图对拍与反例缩减 | 完整 solver 可运行 |
| 6 | `06_cli_telemetry_and_output_contract.md` | CLI、规范输出、telemetry | 正确性门禁通过 |
| 7 | `07_safe_clique_core_reduction.md` | 安全高密度 reduction | 无 reduction 版本稳定 |
| 8 | `08_profile_guided_optimization.md` | 性能优化与回归证据 | 有基准 profile |
| 9 | `09_ippv_baseline_adapter.md` | IPPV 固定版本和适配器 | baseline provenance 已审计 |
| 10 | `10_h2_h3_baseline_adapters.md` | LDS/LTDS 系列适配器 | 各基线许可证已确认 |
| 11 | `11_experiment_harness.md` | 统一实验执行与结果校验 | proposed/baselines 均可运行 |
| 12 | `12_ablation_and_scalability.md` | 消融、扩展性和参数实验 | 主实验配置冻结 |
| 13 | `13_correctness_review.md` | 独立正确性审查 | release candidate |
| 14 | `14_performance_review.md` | 性能与公平性审查 | 主实验已跑至少一轮 |
| 15 | `15_reproducibility_release.md` | 可复现发布包 | 结论和表格冻结 |
| Debug | `99_minimize_a_failure.md` | 最小化失败样例 | 任意测试失败 |

## 每次启动方式

在仓库根目录启动 Codex，然后发送：

```text
/plan
Read AGENTS.md and the files listed in the selected prompt.
Execute prompts/<PROMPT_FILE>.
Do not work on later phases.
```

阶段结束后要求 Codex 使用 `AGENTS.md` 的 Completion report format。测试未运行时，不接受“完成”状态。

## 并行工作规则

只有以下任务适合 worktree 并行：

- baseline provenance/adapter 审计；
- dataset manifest 和下载脚本；
- 与核心 solver 无共享接口的结果可视化脚本。

oracle、exact arithmetic、clique index、solver recursion 和 output semantics 不要并行修改，除非接口与回归语料已经冻结。
