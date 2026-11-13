# Project Cairn 日志

本文件按倒序记录实质性进展 —— 最新条目在本行正下方。每条保持简短（摘要 + 指针），
结论沉淀进 `cairn/<topic>.md`。

## 2026-11-13 · 里程碑 1：开库，三张表合成 80 条；三份迁移说明各演练一遍（feat/m1-shared-tables，0.1.0）

- 源：mmw60_trx@13024e0（125 条：spec 10 / survey 51 / assumed 56 / derived 8）、d2d_link@6789810（16 条 survey）、fmcw_radar@2e5cbb6（39 条，只登记 5 条引用）。三个检出的 HEAD 核过就是这三个 SHA。
- 迁入 **80 条**：mmw60 63（spec 10、survey 48、derived 5）+ d2d 16（加 `ucie.`）+ 新 derived 1（隔离度 40 − 20 = 20 dB）。按标签：spec 10、survey 64、derived 6、assumed 0。7 个领域文件。
- **和指令不一样**：指令写"spec 10 + survey 51 = 61 条"，实际只迁 48 条 survey。留下的 3 条按铁律 2 不进共享表：两条 clock_profile 的值是 mmw60 仓库里的文件名（x10 那条还用了它的 assumed 底噪），dsp_ip 那条是姊妹库的综合估计。理由在 `tests/test_extraction.py::MMW60_STAYS`（ROADMAP 开放问题 1）。
- derived 8 条：跟着走 5 条（cfo、k_threshold_stf、k_threshold_ltf_only 只用 liu2025.*；rapp_p1db_below_psat_db 只用 tgad_em.*；pa60_rapp_p_asada_eumc2011 用 pa60.asada_eumc2011 + tgad_em 的形状）；留下 3 条（用了 assumed.cr_rms_delay_ns、assumed.pa60_operating_rule，或是示例 03 的读数）。共享的 6 条在 `RECOMPUTE` 里只用共享条目复算：Rapp 闭式 p = 0.81 → 9.497 dB、p = 1.286 → 4.598 dB。
- grep 守卫查出两张源表数错：mmw60 第 636 行注释（spec 数 11 对 10），d2d 表头 + 一条 note（spec 数 2 对 0）。那条 note 是迁入条目唯一改了的字段（`CHANGED`）。
- mmw60 的 17 个 `survey.` / `derived.` 前缀键**没改名**：它的示例 04 / 08 / 09 打印键名，改名会让示例输出动；冻结成旧名，改名排进 ROADMAP。
- 测试 58 个（3.13 与 3.10 都绿），ruff 干净。变异检查：注释写进标签词、登记值 12 → 13（也试了只改 consumers.yaml 不改 CHANGELOG）、改名不留别名、留别名不记账本、derived 不写复算、未知字段——每种都红，还原后绿。
- **演练**（各库 pin 提交的临时 worktree，没推）：d2d 指纹 3345 / 3345 逐位相同，pytest 250 passed / 12 skipped；fmcw 1979 / 1979，197 passed / 2 skipped；mmw60 指纹 68 / 68，且经垫片读出的 125 条旧条目 8 个字段逐条相同。三库 `vendor_check --strict` 里 spec_sources 的文件都 verbatim（mmw60 8 个、d2d 3 个、fmcw 2 个）。
- 演练查出、已写进说明与 ROADMAP 的：d2d / mmw60 的 `example_drift.spec_values` 按路径读表（d2d 的一条测试因此红过）；d2d 的 `_strip_header` 会吃掉 YAML 正文第一行注释；mmw60 / fmcw 的 `test_vendor_check` 写死了 pin；第一版 `audit_tags` 把 mmw60 值映射里的 `source` 键也报了——改成只报规则禁止的，共享表另有更严的测试。
- knowledge-vault 不在本会话里（指令：没有就跳过），没读。
- 下一步：用户合并后，把合并提交的完整 SHA 填进三份迁移说明的 `<PIN>`，按 mmw60 → fmcw → d2d 转给各库。
