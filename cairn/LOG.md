# Project Cairn 日志

本文件按倒序记录实质性进展 —— 最新条目在本行正下方。每条保持简短（摘要 + 指针），
结论沉淀进 `cairn/<topic>.md`。

## 2026-11-13 · 里程碑 1：开库，三张表合成 80 条（feat/m1-shared-tables，0.1.0）

- 源：mmw60_trx@13024e0（125 条：spec 10 / survey 51 / assumed 56 / derived 8）、d2d_link@6789810（16 条 survey）、fmcw_radar@2e5cbb6（39 条，只登记 5 条引用）。三个检出都核过 HEAD 就是这三个 SHA。
- 迁入 80 条：mmw60 63（spec 10、survey 48、derived 5）+ d2d 16（加 `ucie.`）+ 新 derived 1（隔离度 40 − 20）。按标签：spec 10、survey 64、derived 6、assumed 0。7 个领域文件。
- **和指令不一样的地方**：指令写"spec 10 + survey 51 = 61 条"，实际只迁了 48 条 survey。留下的 3 条按铁律 2 不该进共享表：两条 clock_profile 的值是 mmw60 仓库里的文件名（x10 那条还用了它的 assumed 底噪），dsp_ip 那条是姊妹库的综合估计。理由写在 `tests/test_extraction.py::MMW60_STAYS`，要改判就改那里。
- derived 8 条逐条看：跟着走 5 条（cfo、k_threshold_stf、k_threshold_ltf_only 只用 liu2025.*；rapp_p1db_below_psat_db 只用 tgad_em.*；pa60_rapp_p_asada_eumc2011 用 pa60.asada_eumc2011 + tgad_em 的形状）。留下 3 条（isi_beyond_gi_k16_db 用 assumed.cr_rms_delay_ns；pa60_obo_at_evm_limit_db 用 assumed.pa60_operating_rule；irr_after_cal_measured_db 是 mmw60 示例 03 的读数）。迁走的 5 条连同新的一条，在 `test_iron_rules.py::RECOMPUTE` 里只用共享条目复算：Rapp 闭式 p = 0.81 → 9.497 dB、p = 1.286 → 4.598 dB，二分解出的 p 与表里差 < 0.001。
- grep 守卫查出两处"标签词 + 冒号"：mmw60 第 636 行注释（spec 数 11 对 10），d2d 表头注释 + `rx_eye_width_ui@24-32` 的 note（spec 数 2 对 0）。前者改写进文件头，后者 note 改一处替换，是迁入条目唯一改了的字段（`CHANGED`）。
- mmw60 的 17 个 `survey.` / `derived.` 前缀键**没有改名**：mmw60 的 examples/expected 打印键名（04、08、09 三个示例），迁移那一轮改名会让示例输出动，违背"指纹逐位不变"那轮只做搬家的意思。冻结成旧名，改名排进 ROADMAP。
- fmcw 的 5 条引用里 4 条去掉 `mmw60_trx:` 前缀就是合法的 `ref()`；减法那条读新的 derived 条目。
- knowledge-vault 不在本会话里（指令：没有就跳过），没有读。
- 测试 64 个全绿，ruff 干净；拷贝即用的测试在临时目录里换包名 import，整包 80 条、只拷 ucie 的 16 条都能读。
- 下一步：用户合并后，把合并提交的完整 SHA 填进三份迁移说明，按 mmw60 → fmcw → d2d 转给各库。
