# ROADMAP

**这份文件只写还没做的事。** 做完即删，并在 `CHANGELOG.md` 记一笔、`cairn/LOG.md` 记数字。

**当前焦点**：里程碑 2 的核实轮。第 1 批 `tgad_em.*` 已在 0.3.0 对上原文；Asada Table I 转引的 13 篇都读了原文（后 6 篇未发布）。第 2 批 TDC 读了 3 篇（分辨率有出处，抖动只有 Henzler 的上界量级）。第 3 批 UCIe 16 条里 15 条对上联盟公开材料（规范本身因许可证不能读）。第 4 批里本库能直接取的两篇已读。以上都在 0.4.0 发布。第 4 批剩下的车辆、角反射器、窗函数也建了条目，fmcw_radar 在 #19 里把最后 6 条改掉并已验收，它的表里没有 survey 了（未发布）。第 7 批里 `liu2025.*` 已按刊出版核过（mmw60_trx 在本库 #26 里请求，未发布）。#29（mmw60_trx 请求 802.11ad / ay 的 PHY 数）已从公开提案建了条目并验收。以上在 0.5.0 发布。第 7 批里能用公开材料核的 11 条已改（未发布），DeepScaleTool 已按工具原文件核过（未发布）。2026-11-17 用户确认许可后发来 10 篇 IEEE Xplore 原文：`horowitz2014.*`、`rx60.comm_iscas2015`、`antenna60.okada2013_dbi` 4 条改 spec，Asada 表后 6 行建了条目（未发布）。共享表只剩 1 条 survey：`ucie.standard.lane_repair` 的降到 x8（见第 3 批）。以上在 0.6.0 发布。

## 报回上游（本库不改别的库；要它们做的在那个库开 issue，对方回报后本库验收、关 issue）

### mmw60_trx —— pin 在 `65ff5e4`，mmw60_trx#76 已验收；本库 #26、#29、#33、#43、#48 都已验收并由它关闭
- `data/regulatory.yaml` 在 `65ff5e4` 之后多了 10 条雷达档（#50），它用不上，下次因别的事重新 pin 时一起；不为此单开 issue。
- 它在 #63 里定了两件：ISCAS 2015 的 7.1 dB 照原文作双边带，另列单边带一行（它本地的 `assumed.rx_nf_dsb_to_ssb_db` = 3 dB）；Asada [5] 的 PAE 剔掉（`assumed.pa60_table1_pae_excluded`，示例 09 的中位数 8.5 → 8.8 %）。都在它本地，本库不用做什么。
- 它自己记了：示例 09 用的 Table I 中位数 3.3 dB 把 [1]（偏置不当）与 [11]（48 / 52 GHz）也算进去了，重算会动示例输出，在它的 ROADMAP C10 待定。本库不用做什么。

### fmcw_radar —— pin 在 `18241cd`，fmcw_radar#26（重新 pin）与 #27（合规检查）已验收；它的表里没有 survey 了
- **#50 待它关**：44 个 `fcc15255.*` 引用已按条登记。它请本库留意一件事：§15.255(c)(2) 的关断时间，一段 ≥ 2 ms 的关断被 33 ms 窗口截断时，截下来的片段算不算（它按整段计；另一种读法多扣最多 4 ms，6.4 ms 的帧在 14 dBm 档任何帧率都不合规）。条文没写，本库以后若读到 FCC 的测量规程或 KDB 对这一点的说法，在 #50 或新 issue 里告诉它。
- 它自己记了（它的 ROADMAP P1 #5）：目标 RCS 是常数，不随距离、视角、频段变（示例 05 的车在 5.3 m，按 ISO 中心约 4.3 dBsm，比它的 10 低约 5.7 dB；同一个三面角 77 GHz 比 60 GHz 多 2.17 dB）。要按"种类 + 尺寸 / 视角"算时它再来对接；本库已有 `target_rcs.iso19206_3_car_rear`（距离下降的参数）、`target_rcs.iso19206_3_car_30m`（一周的上下界）、`target_rcs.trihedral_peak`（公式），到时看要不要补 derived。
- 它的 `tdc_jitter_s` 仍是 1 ps 占位，用户定暂不开 issue（见里程碑 2 第 2 批）。
- 它在 #15 里选了只算氧气，信道不含水汽，记在它自己的 ROADMAP。以后要算总气体衰减，本库再补 P.676 Table 2 与水汽那一支，并先定 1013.25 hPa 按总压还是干空气压读。

### d2d_link —— pin 在 `bbc0ccb`，#2 已验收
- 它定了：眼罩保留含抖动的比法并标明"比规范严"；BER 按 `ucie.raw_ber_by_rate` 分档；TX 0.4 V 作最坏情况默认值；QDR 有了出处。
- 下次要它动的只有 `ucie.standard.lane_repair` 若查到"降到 x8"的原文（见里程碑 2 第 3 批）。
- 它在本库开的 #22（原始 BER 的速率区间条目）已答复：原文只有离散速率，不加；它维持表外速率退回 1e-27 并告警。

## 里程碑 2：核实轮

每条 survey 要么查到原文、改成 spec（带 quote + section），要么在 note 里写明为什么读不到。按"决定哪个库的结论"排序，批号与 `cairn/Reference/README.md` 一致（第 4 批 fmcw_radar 的 14 条已在 #19 了结）：

- 第 2 批 · **TDC**（fmcw_radar 的两个占位：`60g_sensing.tdc_res_s` 5 ps、`60g_sensing.tdc_jitter_s` 1 ps）：Wu、Staszewski、Long（JSSC 2014）已读，建了 `adpll60.wu_jssc2014_tdc`（未发布）：分辨率 12.2 ps，带内相噪 −78 dBc/Hz（理论）/ −77（实测），由 TDC 量化主导。**原文没有给 TDC 自身的抖动**；它引的 TDC 原文 [23]（Staszewski et al., TCAS-II 2006）也读了，同样只有分辨率（90 nm 17–21 ps）。fmcw 已在 #17 改引 `tdc_res_s`（12.2 ps）并验收。**抖动的出处现在有分量了**：fmcw 报回，12.2 ps 步长下 1 ps 抖动只有 0.08 LSB，打不散量化，默认配置每帧 2.75 个鬼目标；抖动 1 / 1.8 / 2.44 / 3 ps 对应 2.75 / 2.08 / 0.92 / 0.16 个。Wu 文 [35] Henzler et al.（ISSCC 2008）已读，建了 `tdc.henzler_isscc2008`（spec）与 `tdc.henzler_isscc2008_single_shot_s`（derived，3.29e-12 s，未发布）：单次精度 0.7 LSB × 4.7 ps，定义为反复测同一间隔时输出码字的标准差。它是 90 nm 局部无源插值 TDC，结构与 Wu 2014 不同，且含离散化与测试脉冲的抖动，只能当量级（上界）。**用户 2026-11-14 定：暂不给 fmcw 开 issue**，它的 `tdc_jitter_s` 仍是 1 ps 占位。日后要换时，issue 里写明：1 ps → 3.29 ps 按它报回的扫描会让鬼目标从每帧 2.75 降到 0.16 左右（3 ps 时），而 3.29 ps 是别的结构的 TDC、且是上界量级；用不用由它定。
- 第 3 批 · **UCIe**（d2d_link 的判定全悬在 0.65 UI 上）：16 条里 15 条已对上联盟公开的 Hot Chips 2023 教程与 2022 白皮书，改为 spec，另建 2 条（未发布）。**规范本身不能读**：许可协议禁止把规范输入 AI 系统，用户也不要把规范发给 Claude。剩下 `ucie.standard.lane_repair` 的"降到 x8"：联盟白皮书、Hot Chips 2023 教程与 Das Sharma、Pasdast 的 IEEE Trans. CPMT 2022（2026-11-17 读原文，用户确认许可）都只说标准封装靠降宽修复、高级封装用备用 lane，没说降到几条；只有规范本身可能有，而规范不能读。条目仍是 survey，`ucie.yaml` 不为这一句改。
- 第 5 批 · **array_tx 的互耦值**（它的 ROADMAP A1；fmcw 的 `rx_coupling_c1_db` 占位也取它）。
- 第 6 批 · **Halo_Serdes #11 的 4 条条文**。

**要取的原文**：清单在 `cairn/Reference/README.md`（按上面的顺序分批，标明哪些要用户下载、哪些放行站点后本库自己取）。

## 其余待办

- **`itu_p676.gamma_o_dry_sea_level` 的 note 注明水汽那句的读法**：note 里"水汽另有 0.251 dB/km，合计 0.348"是把 1013.25 hPa 当干空气压算的；当总压读是 0.344（fmcw_radar#15 指出）。数值不受影响。改 note 会让 fmcw 需重新 pin，等 `atmosphere.yaml` 下次因别的原因改动时一起改（这条是本库新建的，不在迁入表里，不用记 `CHANGED`）。
- **读取器给合并表也解析别名**：`ref(..., table)` 与消费方垫片在合并表上的查找都不认 `aliases:`。mmw60_trx 在 #23 里自己在垫片里补了一份（`_resolve`：先查表，再查 `aliases()`，警告指向调用方）。把这段做成读取器的公开函数（如 `resolve(key, table)`，`ref` 带 `table` 时也走它），垫片就能更薄。改 `reader.py` 会让三个库都需重新 pin，等下一次必须动 `reader.py` 时一起做。
- **迁入条目 note 里的"本库"**指 mmw60_trx 或 d2d_link（各文件头写明）。条目下一次因核实而改时，把"本库"与它们仓库里的路径改成明确的库名，记进 `CHANGED`。
- 若有库要 Wu 2019 JSSC 那颗 PLL 的实测数（不是 pllsim 的模型输出），为论文本身单开一条 survey / spec 条目；mmw60 的 `survey.clock_profile_wu19` 不搬。
- **Harris 1978 表 I 有两行对不上自己的定义**（`harris1978.blackman`、`harris1978.exact_blackman` 的 note 有复算数）：Blackman 的 3-dB / 6-dB 宽偏大约 2 %，Exact Blackman 一行旁瓣、相干增益、带宽都与式 (31a) 的系数不符。有没有勘误可查 Nuttall, IEEE Trans. ASSP 29(1), 1981（📥）。有消费方要用 Exact Blackman 的数时再做。
- `liu2025.k_threshold_stf` 的 312.5 kHz（802.11 VHT 子载波间距）不是条目，只写在 cite 里；核实轮补一条 `ieee80211.*` 的 spec 条目，RECOMPUTE 改读它。

- **EDMG 的接收灵敏度**：公开材料里没找到（TGay CID 1620 要求补，被采纳的 18/0713r3 只补了 EVM；#33 时按标题再搜了 sensitivity / minimum input / receiver / requirement，翻了两份性能要求文件与动议汇编，仍没有）。mmw60_trx 在本地写 assumed（沿用 DMG 的同调制档，`dmg.sc_mcs_extended` 进来后 SC 的高阶档也配上了）；mmw60_trx#61 起 SC 改用它按 #33 的码实测的门限，OFDM 仍借 DMG 同档。
- **#43 里公开材料没有的三处**：Short SSW 用哪种 PPDU、哪个 MCS 发（控制模式长度下限 14 字节装不下 6 字节，SFD 只写"在 EDMG PPDU 的数据域里"）；EDMG OFDM 16 / 64-QAM 的交织置换（17/1568r0 只说在一个 OFDM 符号内交织，1170r2 写 TBD）；EDMG OFDM 的填充规则（#33、#43 两次都没找到）。EDMG 的 TRN 单元长度也没有收（DMG 的 4992 码片已在 `dmg.control_phy_encoding`、`dmg.sc_ppdu_chips`）。
- **#48 里公开材料没有的**：DMG 前导 STF 2176 码片（= 17 × 128）的组成，0433r2 写的 14 × Ga128 + −Ga128（1920 码片）是旧的，控制 PHY 的 6400 码片同样只有长度；EDMG OFDM 的 N_SYMS（30.6.6.2，本库没收）。"数据信道用 EDMG-CEF 估"与"EDMG OFDM 包的 L-CEF 用 OFDM 排法"两句标准里有、公开文件里没有，现在只在条目 note 里写明是用户对照标准确认的；以后若找到公开原句，补进 quote。

## 开放问题

1. knowledge-vault 本会话没有挂上，没读。下次挂上它的会话先看里面有没有出处表或文献笔记，再决定合并还是只引用。
