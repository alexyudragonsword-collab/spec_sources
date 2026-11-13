# ROADMAP

**这份文件只写还没做的事。** 做完即删，并在 `CHANGELOG.md` 记一笔、`cairn/LOG.md` 记数字。

**当前焦点**：三个消费方的迁移已验收（2026-11-13，issue 都已关）。下一步是 0.2.0：给 17 个旧前缀键改名（新名表见"其余待办"，动手前与用户确认），做的时候在 mmw60_trx 开 issue；然后是里程碑 2 的核实轮。

## 报回上游（本库不改别的库；要它们做的在那个库开 issue，对方回报后本库验收、关 issue）

现在没有进行中的。下一个是 0.2.0 改名，只涉及 mmw60_trx（fmcw_radar、d2d_link 不读这 17 个键）。

## 里程碑 2：核实轮

每条 survey 要么查到原文、改成 spec（带 quote + section），要么在 note 里写明为什么读不到。按"决定哪个库的结论"排序：

1. **60 GHz CMOS PA 的 Psat / P1dB**（决定 mmw60_trx 同台表每格的 MCS）：`tgad_em.pa_rapp_*` / `tgad_em.pa_ampm_*` / `tgad_em.pa_model_shape`（预设 PA 的 AM/PM 仍是 11ad 评估方法学的），`pa60.eumc2011_table1` 里 13 行转引的原文（[1]–[15]，参考文献表在 Asada EuMC 2011 那篇里）。
2. **TDC 抖动**（fmcw_radar 的 1 ps 占位，`60g_sensing.tdc_jitter_s`）：找 60 GHz FMCW ADPLL 的 TDC 输入参考抖动，进本库成 survey / spec 条目，fmcw 再引用。
3. **UCIe 眼罩**（d2d_link 的判定全悬在 0.65 UI 上）：`ucie.rx_eye_width_ui@24-32`、`ucie.rx_eye_width_ui`、`ucie.rx_eye_height_mv`，然后是其余 13 条 ucie.*。
4. **fmcw_radar 的 14 条**（fmcw_radar@2e5cbb6 自己表里的 spec / survey）：
   - 5 条前端数已经读本库并登记（`consumers.yaml`）：`60g_sensing.tx_power_dbm`、`60g_sensing.nf_db`、`60g_sensing.p1db_oob_dbm`、`60g_sensing.p1db_inband_dbm`、`60g_sensing.tx_rx_isolation_db`。
   - 9 条只在 fmcw 的 survey 迁进本库并核实，fmcw 改成引用：大气 `oxygen.60g_db_per_km`、`oxygen.77g_db_per_km`（ITU-R P.676）；RCS `rcs.human_dbsm`、`rcs.car_dbsm`、`rcs.corner_reflector_dbsm`；窗函数主瓣宽度 `window.rect_3db_bins`、`window.hann_3db_bins`、`window.hamming_3db_bins`、`window.blackman_3db_bins`（Harris 1978 Table I）。做的时候在 fmcw_radar 开 issue。
5. **array_tx 的互耦值**（它的 ROADMAP A1；fmcw 的 `rx_coupling_c1_db` 占位也取它）。
6. **Halo_Serdes #11 的 4 条条文**。
7. 其余 survey：`liu2025.*`（刊出版）、`fcc15255.*`、`ieee80211ay.*`、`survey.n_sd_*`、`survey.eht_tone_mapper_dtm`、`survey.ldpc_ppdu_encoding_thresholds`、`survey.dmg_sensitivity_assumptions`、`survey.rx60_comm_iscas2015`、`survey.antenna60_okada2013_dbi`、能耗三组。

**要用户下载的 PDF**（IEEE Xplore 对脚本返回空页）——放进 `cairn/Reference/`（PDF 本身不入库，`.gitignore`）：
- 60 GHz PA：Asada EuMC 2011 Table I 的 [1]–[15]（先取 Psat − P1dB 极端的 [1]、[2]、[6]、[15]）；22 nm 的 MDPI 那篇（脚本 403；可能给 OFDM 工作点）。
- TDC：W. Wu, R. B. Staszewski, J. R. Long, "A 56.4-to-63.4 GHz Multi-Rate All-Digital Fractional-N PLL for FMCW Radar Applications in 65 nm CMOS", IEEE JSSC 2014（候选，未读）；它引用的 TDC 原文。
- UCIe：UCIe 1.1 / 2.0 规范（UCIe 联盟站点填表下载）；Das Sharma et al., IEEE Trans. CPMT 2022；"Analysis of UCIe 48/64 GT/s Electrical Links"（2025，ResearchGate 395249532）。
- fmcw：Harris, "On the use of windows for harmonic analysis with the DFT", Proc. IEEE 1978（Table I）；60 / 77 GHz 人体与车辆 RCS 的测量论文（各一篇即可）。
- mmw60：Liu et al., "Wi-Fi 8: Embracing the Millimeter-Wave Era", IEEE Commun. Mag. 2025；Okada et al., IEEE JSSC 2013（6 dBi 封装天线）；ISCAS 2015 的 60 GHz 7.1 dB NF 接收机；Horowitz ISSCC 2014；Sarangi & Baas ISCAS 2021（DeepScaleTool）；IEEE 802.11-2020 / 802.11ax-2021 / 802.11be 的相关表（IEEE GET 计划）。
- 脚本能自己取的（不用下载）：47 CFR §15.255（eCFR）、ITU-R P.676 与 M.2003（ITU 站点）、IEEE 802.11-09/0296r16（mentor 文档服务器）、Murmann ADC survey（GitHub）、Liu 2025 的 arXiv 版。

## 其余待办

- **mmw60 带来的 17 个旧前缀键改名**（`survey.*` 12 个、`derived.*` 5 个：前缀是标签，不是领域；核实轮把 survey 改成 spec 后，键名就和标签矛盾）。
  - 时机：mmw60 迁完之后、里程碑 2 动这些条目之前，单独出 0.2.0；不和迁移放在一起（迁移那一步只做搬家，指纹与示例文本都不动）。
  - 做法：17 个旧键都写进数据文件的 `aliases:`（读取时 `DeprecatedKeyWarning`），`keys.lock` 记 `aliased=0.2.0`，至少留到 0.3.0。mmw60 重新 pin 一次，改约 30 处调用和示例 04 / 08 / 09 的期望输出（只是键名，数不动）；指纹必须逐位不变。fmcw、d2d 不读这些键，不受影响。
  - 拟定的新名（动手前再确认）：

    | 旧键 | 新键 |
    |---|---|
    | `survey.horowitz_mult32_pj` / `survey.horowitz_add32_pj` | `horowitz2014.mult32_pj` / `horowitz2014.add32_pj` |
    | `survey.walden_fom_fj` / `survey.walden_fom_range_fj` | `adc_survey.walden_fom_fj` / `adc_survey.walden_fom_range_fj` |
    | `survey.node_scale_45_to_7nm` | `deepscale.node_scale_45_to_7nm` |
    | `survey.n_sd_11ac` / `survey.n_sd_11be` | `ieee80211ac.n_sd` / `ieee80211be.n_sd` |
    | `survey.eht_tone_mapper_dtm` | `ieee80211be.ldpc_tone_mapping_distance` |
    | `survey.ldpc_ppdu_encoding_thresholds` | `ieee80211.ldpc_ppdu_encoding_thresholds` |
    | `survey.rx60_comm_iscas2015` | `rx60.comm_iscas2015` |
    | `survey.dmg_sensitivity_assumptions` | `dmg.sensitivity_assumptions` |
    | `survey.antenna60_okada2013_dbi` | `antenna60.okada2013_dbi` |
    | `derived.cfo_liu2025_hz` | `liu2025.cfo_from_ppm_hz` |
    | `derived.k_threshold_stf` / `derived.k_threshold_ltf_only` | `liu2025.k_threshold_stf` / `liu2025.k_threshold_ltf_only` |
    | `derived.rapp_p1db_below_psat_db` | `tgad_em.rapp_p1db_below_psat_db` |
    | `derived.pa60_rapp_p_asada_eumc2011` | `pa60.asada_eumc2011_rapp_p` |

    新前缀 `horowitz2014`、`adc_survey`、`deepscale`、`ieee80211ac`、`ieee80211be`、`ieee80211`、`antenna60` 要在 `FILE_PREFIXES` 与 AGENTS.md 的布局表里登记；`LEGACY_PREFIX_KEYS` 清空。
- **迁入条目 note 里的"本库"**指 mmw60_trx 或 d2d_link（各文件头写明）。条目下一次因核实而改时，把"本库"与它们仓库里的路径改成明确的库名，记进 `CHANGED`。
- 若有库要 Wu 2019 JSSC 那颗 PLL 的实测数（不是 pllsim 的模型输出），为论文本身单开一条 survey / spec 条目；mmw60 的 `survey.clock_profile_wu19` 不搬。
- `derived.k_threshold_stf` 的 312.5 kHz（802.11 VHT 子载波间距）不是条目，只写在 cite 里；核实轮补一条 `ieee80211.*` 的 spec 条目，RECOMPUTE 改读它。

## 开放问题

1. knowledge-vault 本会话没有挂上，没读。下次挂上它的会话先看里面有没有出处表或文献笔记，再决定合并还是只引用。
