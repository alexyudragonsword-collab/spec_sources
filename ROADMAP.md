# ROADMAP

**这份文件只写还没做的事。** 做完即删，并在 `CHANGELOG.md` 记一笔、`cairn/LOG.md` 记数字。

**当前焦点**：里程碑 2 的核实轮。第 1 批 `tgad_em.*` 已在 0.3.0 对上原文；Asada Table I 转引的 13 篇读了 7 篇（未发布），剩 6 篇等用户下载。第 4 批里本库能直接取的两篇已读，建了 `itu_p676.*`、`target_rcs.*`（未发布）。mmw60_trx #25、fmcw_radar #15 已验收关闭，现在没有等对方回报的 issue。

## 报回上游（本库不改别的库；要它们做的在那个库开 issue，对方回报后本库验收、关 issue）

### mmw60_trx —— 下次开 issue 时重新 pin（现在 pin 在 0.3.0 `9a443ba`）
- 还要再 pin 一次：未发布一节改了它 vendor 的 `data/pa60.yaml`（第 1 批新增 4 条、`pa60.eumc2011_table1` 的 note），读到的已有的数不变。等下一次发版或下一批一起开 issue。issue 里要告诉它：它迁来的 note 拿 [1]（9.0 dB）对照 TGad Rapp 的 9.5 dB，而原作者自己把 [1] 的 P1dB 偏低归于偏置不当；去掉 [1]，正常偏置里最软的是 [15]（5.6 dB，1.8 V 时 6.6 dB，且 Psat 是扫描终点，真实的差更大）；[9] 在 3 V 时也到 6.0 dB；[11] 一行是 48 GHz 的数，不该算进 60 GHz 的分布；它的文档或结论里如果用 [1] 说明 9.5 dB 有实测佐证，由它决定改不改。

### fmcw_radar —— 剩 6 条等原文（现在 pin 在 `e49979f`，#17 已验收）
- 车辆 RCS、角反射器、4 条窗函数主瓣宽度：原文下载、建好条目后另开 issue（见里程碑 2 第 4 项）。
- 它在 #15 里选了只算氧气，信道不含水汽，记在它自己的 ROADMAP。以后要算总气体衰减，本库再补 P.676 Table 2 与水汽那一支，并先定 1013.25 hPa 按总压还是干空气压读。

### d2d_link —— 择机重新 pin，不单开 issue
- 0.2.0 / 0.3.0 对它只改了 `reader.py` 的一行版本号，读到的数不变。等第 3 批（UCIe 眼罩）给它开 issue 时一并重新 pin；那之前它本地的 `vendor_check --strict` 会报 pin 过期，CI 不受影响（CI 检出在 pin 上）。

## 里程碑 2：核实轮

每条 survey 要么查到原文、改成 spec（带 quote + section），要么在 note 里写明为什么读不到。按"决定哪个库的结论"排序：

1. **60 GHz CMOS PA 的 Psat / P1dB**（决定 mmw60_trx 同台表每格的 MCS）：`tgad_em.*` 已在 0.3.0 对上原文。`pa60.eumc2011_table1` 里 Asada 转引的 13 行已读 7 行（[1] [2] [6] [9] [11] [13] [15]，未发布），P1dB / Psat / PAE 都与原文相同，但 [11] 是 48 GHz 的数，不是 60 GHz。剩 6 行（[5] [7] [8] [10] [12] [14]）要用户下载，题名见 `cairn/Reference/README.md`；它们在已读原文的对比表里都出现过且与 Asada 相符（[5] 的电压 1.0 V 对 1.2 V 除外），优先级低于第 2、3 项。
2. **TDC**（fmcw_radar 的两个占位：`60g_sensing.tdc_res_s` 5 ps、`60g_sensing.tdc_jitter_s` 1 ps）：Wu、Staszewski、Long（JSSC 2014）已读，建了 `adpll60.wu_jssc2014_tdc`（未发布）：分辨率 12.2 ps，带内相噪 −78 dBc/Hz（理论）/ −77（实测），由 TDC 量化主导。**原文没有给 TDC 自身的抖动**；它引的 TDC 原文 [23]（Staszewski et al., TCAS-II 2006）也读了，同样只有分辨率（90 nm 17–21 ps）。fmcw 已在 #17 改引 `tdc_res_s`（12.2 ps）并验收。**抖动的出处现在有分量了**：fmcw 报回，12.2 ps 步长下 1 ps 抖动只有 0.08 LSB，打不散量化，默认配置每帧 2.75 个鬼目标；抖动 1 / 1.8 / 2.44 / 3 ps 对应 2.75 / 2.08 / 0.92 / 0.16 个。Wu 文 [35] Henzler et al.（ISSCC 2008）已读，建了 `tdc.henzler_isscc2008`（spec）与 `tdc.henzler_isscc2008_single_shot_s`（derived，3.29e-12 s，未发布）：单次精度 0.7 LSB × 4.7 ps，定义为反复测同一间隔时输出码字的标准差。它是 90 nm 局部无源插值 TDC，结构与 Wu 2014 不同，且含离散化与测试脉冲的抖动，只能当量级（上界）。**用户 2026-11-14 定：暂不给 fmcw 开 issue**，它的 `tdc_jitter_s` 仍是 1 ps 占位。日后要换时，issue 里写明：1 ps → 3.29 ps 按它报回的扫描会让鬼目标从每帧 2.75 降到 0.16 左右（3 ps 时），而 3.29 ps 是别的结构的 TDC、且是上界量级；用不用由它定。
3. **UCIe 眼罩**（d2d_link 的判定全悬在 0.65 UI 上）：`ucie.rx_eye_width_ui@24-32`、`ucie.rx_eye_width_ui`、`ucie.rx_eye_height_mv`，然后是其余 13 条 ucie.*。
4. **fmcw_radar 的 14 条**（fmcw_radar@2e5cbb6 自己表里的 spec / survey）：
   - 5 条前端数已经读本库并登记（`consumers.yaml`）：`60g_sensing.tx_power_dbm`、`60g_sensing.nf_db`、`60g_sensing.p1db_oob_dbm`、`60g_sensing.p1db_inband_dbm`、`60g_sensing.tx_rx_isolation_db`。
   - 9 条只在 fmcw 的 survey，要迁进本库并核实，fmcw 再改成引用。氧气两条与人体 RCS 已在 fmcw#15 改成引用并登记（`consumers.yaml`）。剩 6 条：RCS `rcs.car_dbsm`、`rcs.corner_reflector_dbsm`；窗函数主瓣宽度 `window.rect_3db_bins`、`window.hann_3db_bins`、`window.hamming_3db_bins`、`window.blackman_3db_bins`（Harris 1978 Table I）。原文下载后建条目，再在 fmcw_radar 开 issue。
5. **array_tx 的互耦值**（它的 ROADMAP A1；fmcw 的 `rx_coupling_c1_db` 占位也取它）。
6. **Halo_Serdes #11 的 4 条条文**。
7. 其余 survey：`liu2025.*`（刊出版）、`fcc15255.*`、`ieee80211ay.*`、`ieee80211ac.n_sd` / `ieee80211be.n_sd`、`ieee80211be.ldpc_tone_mapping_distance`、`ieee80211.ldpc_ppdu_encoding_thresholds`、`dmg.sensitivity_assumptions`、`rx60.comm_iscas2015`、`antenna60.okada2013_dbi`、能耗三组（`horowitz2014.*`、`adc_survey.*`、`deepscale.*`）。

**要取的原文**：清单在 `cairn/Reference/README.md`（按上面的顺序分批，标明哪些要用户下载、哪些放行站点后本库自己取）。

## 其余待办

- **`itu_p676.gamma_o_dry_sea_level` 的 note 注明水汽那句的读法**：note 里"水汽另有 0.251 dB/km，合计 0.348"是把 1013.25 hPa 当干空气压算的；当总压读是 0.344（fmcw_radar#15 指出）。数值不受影响。改 note 会让 fmcw 需重新 pin，等 `atmosphere.yaml` 下次因别的原因改动时一起改（这条是本库新建的，不在迁入表里，不用记 `CHANGED`）。
- **读取器给合并表也解析别名**：`ref(..., table)` 与消费方垫片在合并表上的查找都不认 `aliases:`。mmw60_trx 在 #23 里自己在垫片里补了一份（`_resolve`：先查表，再查 `aliases()`，警告指向调用方）。把这段做成读取器的公开函数（如 `resolve(key, table)`，`ref` 带 `table` 时也走它），垫片就能更薄。改 `reader.py` 会让三个库都需重新 pin，等下一次必须动 `reader.py` 时一起做。
- **迁入条目 note 里的"本库"**指 mmw60_trx 或 d2d_link（各文件头写明）。条目下一次因核实而改时，把"本库"与它们仓库里的路径改成明确的库名，记进 `CHANGED`。
- 若有库要 Wu 2019 JSSC 那颗 PLL 的实测数（不是 pllsim 的模型输出），为论文本身单开一条 survey / spec 条目；mmw60 的 `survey.clock_profile_wu19` 不搬。
- `liu2025.k_threshold_stf` 的 312.5 kHz（802.11 VHT 子载波间距）不是条目，只写在 cite 里；核实轮补一条 `ieee80211.*` 的 spec 条目，RECOMPUTE 改读它。

## 开放问题

1. knowledge-vault 本会话没有挂上，没读。下次挂上它的会话先看里面有没有出处表或文献笔记，再决定合并还是只引用。
