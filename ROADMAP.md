# ROADMAP

**这份文件只写还没做的事。** 做完即删，并在 `CHANGELOG.md` 记一笔、`cairn/LOG.md` 记数字。

**当前焦点**：里程碑 2 的核实轮。第 1 批 `tgad_em.*` 已在 0.3.0 对上原文，剩 Asada Table I 转引的 13 篇等用户下载（先下 4 篇）。第 4 批里本库能直接取的两篇已读，建了 `itu_p676.*`、`target_rcs.*`（未发布）。mmw60_trx 的 0.3.0 重新 pin 在 [#25](https://github.com/alexyudragonsword-collab/mmw60_trx/issues/25)。

## 报回上游（本库不改别的库；要它们做的在那个库开 issue，对方回报后本库验收、关 issue）

### fmcw_radar、d2d_link —— 择机重新 pin，不单开 issue
- 0.2.0 / 0.3.0 对它们只改了 `reader.py` 的一行版本号和 fmcw `frontend60.yaml` 里两条它不读的键名 / 别名，读到的数不变。等里程碑 2 给它们开 issue 时一并重新 pin；那之前它们本地的 `vendor_check --strict` 会报 pin 过期，CI 不受影响（CI 检出在 pin 上）。

## 里程碑 2：核实轮

每条 survey 要么查到原文、改成 spec（带 quote + section），要么在 note 里写明为什么读不到。按"决定哪个库的结论"排序：

1. **60 GHz CMOS PA 的 Psat / P1dB**（决定 mmw60_trx 同台表每格的 MCS）：`tgad_em.*` 已在 0.3.0 对上原文。剩 `pa60.eumc2011_table1` 里 Asada 转引的 13 行，要逐行对原文，13 篇都要用户下载，题名与先下哪 4 篇见 `cairn/Reference/README.md`。
2. **TDC 抖动**（fmcw_radar 的 1 ps 占位，`60g_sensing.tdc_jitter_s`）：找 60 GHz FMCW ADPLL 的 TDC 输入参考抖动，进本库成 survey / spec 条目，fmcw 再引用。
3. **UCIe 眼罩**（d2d_link 的判定全悬在 0.65 UI 上）：`ucie.rx_eye_width_ui@24-32`、`ucie.rx_eye_width_ui`、`ucie.rx_eye_height_mv`，然后是其余 13 条 ucie.*。
4. **fmcw_radar 的 14 条**（fmcw_radar@2e5cbb6 自己表里的 spec / survey）：
   - 5 条前端数已经读本库并登记（`consumers.yaml`）：`60g_sensing.tx_power_dbm`、`60g_sensing.nf_db`、`60g_sensing.p1db_oob_dbm`、`60g_sensing.p1db_inband_dbm`、`60g_sensing.tx_rx_isolation_db`。
   - 9 条只在 fmcw 的 survey 迁进本库并核实，fmcw 改成引用：大气 `oxygen.60g_db_per_km`、`oxygen.77g_db_per_km`（ITU-R P.676）；RCS `rcs.human_dbsm`、`rcs.car_dbsm`、`rcs.corner_reflector_dbsm`；窗函数主瓣宽度 `window.rect_3db_bins`、`window.hann_3db_bins`、`window.hamming_3db_bins`、`window.blackman_3db_bins`（Harris 1978 Table I）。做的时候在 fmcw_radar 开 issue。
   - 进度：
     - 大气已建 `itu_p676.gamma_o_dry_sea_level`。fmcw 改成引用时数会动：60 GHz 由 15.0 变为 14.651；77.5 GHz 由 0.4 变为 0.091 dB/km——0.4 实为总气体衰减，fmcw 要不要连水汽一起算是它自己的事，要的话本库再补 Table 2 和水汽那一支。
     - 人体 RCS 已有 `target_rcs.deep2019_pedestrian_77g`（仿真，−10…+5 dBsm）。车辆、角反射器、窗函数等下载。

     给 fmcw 开 issue 等这一批齐了再开。
5. **array_tx 的互耦值**（它的 ROADMAP A1；fmcw 的 `rx_coupling_c1_db` 占位也取它）。
6. **Halo_Serdes #11 的 4 条条文**。
7. 其余 survey：`liu2025.*`（刊出版）、`fcc15255.*`、`ieee80211ay.*`、`ieee80211ac.n_sd` / `ieee80211be.n_sd`、`ieee80211be.ldpc_tone_mapping_distance`、`ieee80211.ldpc_ppdu_encoding_thresholds`、`dmg.sensitivity_assumptions`、`rx60.comm_iscas2015`、`antenna60.okada2013_dbi`、能耗三组（`horowitz2014.*`、`adc_survey.*`、`deepscale.*`）。

**要取的原文**：清单在 `cairn/Reference/README.md`（按上面的顺序分批，标明哪些要用户下载、哪些放行站点后本库自己取）。

## 其余待办

- **读取器给合并表也解析别名**：`ref(..., table)` 与消费方垫片在合并表上的查找都不认 `aliases:`。mmw60_trx 在 #23 里自己在垫片里补了一份（`_resolve`：先查表，再查 `aliases()`，警告指向调用方）。把这段做成读取器的公开函数（如 `resolve(key, table)`，`ref` 带 `table` 时也走它），垫片就能更薄。改 `reader.py` 会让三个库都需重新 pin，等下一次必须动 `reader.py` 时一起做。
- **迁入条目 note 里的"本库"**指 mmw60_trx 或 d2d_link（各文件头写明）。条目下一次因核实而改时，把"本库"与它们仓库里的路径改成明确的库名，记进 `CHANGED`。
- 若有库要 Wu 2019 JSSC 那颗 PLL 的实测数（不是 pllsim 的模型输出），为论文本身单开一条 survey / spec 条目；mmw60 的 `survey.clock_profile_wu19` 不搬。
- `liu2025.k_threshold_stf` 的 312.5 kHz（802.11 VHT 子载波间距）不是条目，只写在 cite 里；核实轮补一条 `ieee80211.*` 的 spec 条目，RECOMPUTE 改读它。

## 开放问题

1. knowledge-vault 本会话没有挂上，没读。下次挂上它的会话先看里面有没有出处表或文献笔记，再决定合并还是只引用。
