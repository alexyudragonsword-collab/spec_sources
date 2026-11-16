# ROADMAP

**这份文件只写还没做的事。** 做完即删，并在 `CHANGELOG.md` 记一笔、`cairn/LOG.md` 记数字。

**当前焦点**：里程碑 2 的核实轮。第 1 批 `tgad_em.*` 已在 0.3.0 对上原文；Asada Table I 转引的 13 篇读了 7 篇，剩 6 篇等用户下载。第 2 批 TDC 读了 3 篇（分辨率有出处，抖动只有 Henzler 的上界量级）。第 3 批 UCIe 16 条里 15 条对上联盟公开材料（规范本身因许可证不能读）。第 4 批里本库能直接取的两篇已读。以上都在 0.4.0 发布。第 4 批剩下的车辆、角反射器、窗函数也建了条目，fmcw_radar 在 #19 里把最后 6 条改掉并已验收，它的表里没有 survey 了（未发布）。第 7 批里 `liu2025.*` 已按刊出版核过（mmw60_trx 在本库 #26 里请求，未发布）。#29（mmw60_trx 请求 802.11ad / ay 的 PHY 数）已从公开提案建了条目并验收。以上在 0.5.0 发布。第 7 批里能用公开材料核的 11 条已改（未发布），剩 6 条 survey 都要用户下载原文。

## 报回上游（本库不改别的库；要它们做的在那个库开 issue，对方回报后本库验收、关 issue）

### mmw60_trx —— pin 在 `3123b65`，本库 #26、#29 已验收（由它关闭）；#33 已建条目，待它重新 pin
- #33 合并后在 #33 给它新 PIN，一次 pin 齐：0.5.0 的 `__init__.py`、第 7 批改的 `energy` / `ieee80211` / `liu2025` / `regulatory`、#33 的 12 条。告诉它 `adc_survey.walden_fom_fj` 70 → 70.815、区间改为 [38.36, 120.19]（同台表的功耗数会动约 1%）；EDMG 灵敏度没有公开出处；BRP / TRN 单元长度没做。
- 它要按 EDMG 灵敏度换算距离时，在本地写 assumed（见下面"其余待办"的 EDMG 灵敏度一条）；`ay_ofdm` / `ay_sc` 接新键是它自己的 PR，本库不用做什么。
- 它自己记了：示例 09 用的 Table I 中位数 3.3 dB 把 [1]（偏置不当）与 [11]（48 / 52 GHz）也算进去了，重算会动示例输出，在它的 ROADMAP C10 待定。本库不用做什么。

### fmcw_radar —— pin 在 `f87cc9b`，#19 已验收；它的表里没有 survey 了
- 它自己记了（它的 ROADMAP P1 #5）：目标 RCS 是常数，不随距离、视角、频段变（示例 05 的车在 5.3 m，按 ISO 中心约 4.3 dBsm，比它的 10 低约 5.7 dB；同一个三面角 77 GHz 比 60 GHz 多 2.17 dB）。要按"种类 + 尺寸 / 视角"算时它再来对接；本库已有 `target_rcs.iso19206_3_car_rear`（距离下降的参数）、`target_rcs.iso19206_3_car_30m`（一周的上下界）、`target_rcs.trihedral_peak`（公式），到时看要不要补 derived。
- 它的 `tdc_jitter_s` 仍是 1 ps 占位，用户定暂不开 issue（见里程碑 2 第 2 批）。
- 它在 #15 里选了只算氧气，信道不含水汽，记在它自己的 ROADMAP。以后要算总气体衰减，本库再补 P.676 Table 2 与水汽那一支，并先定 1013.25 hPa 按总压还是干空气压读。

### d2d_link —— pin 在 `bbc0ccb`，#2 已验收
- 它定了：眼罩保留含抖动的比法并标明"比规范严"；BER 按 `ucie.raw_ber_by_rate` 分档；TX 0.4 V 作最坏情况默认值；QDR 有了出处。
- 下次要它动的只有 `ucie.standard.lane_repair` 若查到"降到 x8"的原文（见里程碑 2 第 3 批）。
- 它在本库开的 #22（原始 BER 的速率区间条目）已答复：原文只有离散速率，不加；它维持表外速率退回 1e-27 并告警。

## 里程碑 2：核实轮

每条 survey 要么查到原文、改成 spec（带 quote + section），要么在 note 里写明为什么读不到。按"决定哪个库的结论"排序，批号与 `cairn/Reference/README.md` 一致（第 4 批 fmcw_radar 的 14 条已在 #19 了结）：

- 第 1 批 · **60 GHz CMOS PA 的 Psat / P1dB**（决定 mmw60_trx 同台表每格的 MCS）：`tgad_em.*` 已在 0.3.0 对上原文。`pa60.eumc2011_table1` 里 Asada 转引的 13 行已读 7 行（[1] [2] [6] [9] [11] [13] [15]，未发布），P1dB / Psat / PAE 都与原文相同，但 [11] 是 48 GHz 的数，不是 60 GHz。剩 6 行（[5] [7] [8] [10] [12] [14]）要用户下载，题名见 `cairn/Reference/README.md`；它们在已读原文的对比表里都出现过且与 Asada 相符（[5] 的电压 1.0 V 对 1.2 V 除外），优先级低于第 2、3 批。
- 第 2 批 · **TDC**（fmcw_radar 的两个占位：`60g_sensing.tdc_res_s` 5 ps、`60g_sensing.tdc_jitter_s` 1 ps）：Wu、Staszewski、Long（JSSC 2014）已读，建了 `adpll60.wu_jssc2014_tdc`（未发布）：分辨率 12.2 ps，带内相噪 −78 dBc/Hz（理论）/ −77（实测），由 TDC 量化主导。**原文没有给 TDC 自身的抖动**；它引的 TDC 原文 [23]（Staszewski et al., TCAS-II 2006）也读了，同样只有分辨率（90 nm 17–21 ps）。fmcw 已在 #17 改引 `tdc_res_s`（12.2 ps）并验收。**抖动的出处现在有分量了**：fmcw 报回，12.2 ps 步长下 1 ps 抖动只有 0.08 LSB，打不散量化，默认配置每帧 2.75 个鬼目标；抖动 1 / 1.8 / 2.44 / 3 ps 对应 2.75 / 2.08 / 0.92 / 0.16 个。Wu 文 [35] Henzler et al.（ISSCC 2008）已读，建了 `tdc.henzler_isscc2008`（spec）与 `tdc.henzler_isscc2008_single_shot_s`（derived，3.29e-12 s，未发布）：单次精度 0.7 LSB × 4.7 ps，定义为反复测同一间隔时输出码字的标准差。它是 90 nm 局部无源插值 TDC，结构与 Wu 2014 不同，且含离散化与测试脉冲的抖动，只能当量级（上界）。**用户 2026-11-14 定：暂不给 fmcw 开 issue**，它的 `tdc_jitter_s` 仍是 1 ps 占位。日后要换时，issue 里写明：1 ps → 3.29 ps 按它报回的扫描会让鬼目标从每帧 2.75 降到 0.16 左右（3 ps 时），而 3.29 ps 是别的结构的 TDC、且是上界量级；用不用由它定。
- 第 3 批 · **UCIe**（d2d_link 的判定全悬在 0.65 UI 上）：16 条里 15 条已对上联盟公开的 Hot Chips 2023 教程与 2022 白皮书，改为 spec，另建 2 条（未发布）。**规范本身不能读**：许可协议禁止把规范输入 AI 系统，用户也不要把规范发给 Claude。剩下 `ucie.standard.lane_repair` 的"降到 x8"在公开材料里没找到，要的话可读 Das Sharma et al., IEEE Trans. CPMT 2022（📥，期刊论文不受规范许可约束）。
- 第 5 批 · **array_tx 的互耦值**（它的 ROADMAP A1；fmcw 的 `rx_coupling_c1_db` 占位也取它）。
- 第 6 批 · **Halo_Serdes #11 的 4 条条文**。
- 第 7 批 · 其余 survey，都要用户下载原文：`horowitz2014.*`（ISSCC 2014）、`rx60.comm_iscas2015`（ISCAS 2015）、`antenna60.okada2013_dbi`（JSSC 2013，实验室网站只有题录）、`deepscale.node_scale_45_to_7nm`（DeepScaleTool，ISCAS 2021 或工具本身的 .xlsm）。下载前先看许可条款。

**要取的原文**：清单在 `cairn/Reference/README.md`（按上面的顺序分批，标明哪些要用户下载、哪些放行站点后本库自己取）。

## 其余待办

- **`itu_p676.gamma_o_dry_sea_level` 的 note 注明水汽那句的读法**：note 里"水汽另有 0.251 dB/km，合计 0.348"是把 1013.25 hPa 当干空气压算的；当总压读是 0.344（fmcw_radar#15 指出）。数值不受影响。改 note 会让 fmcw 需重新 pin，等 `atmosphere.yaml` 下次因别的原因改动时一起改（这条是本库新建的，不在迁入表里，不用记 `CHANGED`）。
- **读取器给合并表也解析别名**：`ref(..., table)` 与消费方垫片在合并表上的查找都不认 `aliases:`。mmw60_trx 在 #23 里自己在垫片里补了一份（`_resolve`：先查表，再查 `aliases()`，警告指向调用方）。把这段做成读取器的公开函数（如 `resolve(key, table)`，`ref` 带 `table` 时也走它），垫片就能更薄。改 `reader.py` 会让三个库都需重新 pin，等下一次必须动 `reader.py` 时一起做。
- **迁入条目 note 里的"本库"**指 mmw60_trx 或 d2d_link（各文件头写明）。条目下一次因核实而改时，把"本库"与它们仓库里的路径改成明确的库名，记进 `CHANGED`。
- 若有库要 Wu 2019 JSSC 那颗 PLL 的实测数（不是 pllsim 的模型输出），为论文本身单开一条 survey / spec 条目；mmw60 的 `survey.clock_profile_wu19` 不搬。
- **Harris 1978 表 I 有两行对不上自己的定义**（`harris1978.blackman`、`harris1978.exact_blackman` 的 note 有复算数）：Blackman 的 3-dB / 6-dB 宽偏大约 2 %，Exact Blackman 一行旁瓣、相干增益、带宽都与式 (31a) 的系数不符。有没有勘误可查 Nuttall, IEEE Trans. ASSP 29(1), 1981（📥）。有消费方要用 Exact Blackman 的数时再做。
- `liu2025.k_threshold_stf` 的 312.5 kHz（802.11 VHT 子载波间距）不是条目，只写在 cite 里；核实轮补一条 `ieee80211.*` 的 spec 条目，RECOMPUTE 改读它。

- **EDMG 的接收灵敏度**：公开材料里没找到（TGay CID 1620 要求补，被采纳的 18/0713r3 只补了 EVM；#33 时按标题再搜了 sensitivity / minimum input / receiver / requirement，翻了两份性能要求文件与动议汇编，仍没有）。mmw60_trx 在本地写 assumed（沿用 DMG 的同调制档），`dmg.sc_mcs_extended` 补上后它能配齐 EDMG SC 的高阶档。
- **EDMG OFDM 的数据域填充规则与 BRP / TRN 单元长度**（#33 里没做）：前者公开材料里没找到；后者 mmw60 写的是"如顺手"，要的话从 TGad 0433r2 的 21.8 与 TGay 的 TRN 文件（11-17/0213、0430 等）取。

- **47 CFR §15.255(c)(2) 的雷达限值**（2026-11-16 读 eCFR 时看到，未建条目）：雷达类器件默认峰值 EIRP 10 dBm、峰值传导 −10 dBm；57.0–59.4 GHz 室内 20 / 室外 30 dBm；57.0–61.56 GHz 3 dBm（满足关断时间可到 20）；57.0–64.0 GHz 14 dBm（33 ms 里关断 ≥ 25.5 ms），室外固定或车载作业 20 dBm（关断 ≥ 16.5 ms）；61.0–61.5 GHz 窄带可到平均 40 / 峰值 43 dBm。fmcw_radar 若要按合规上限算 EIRP，从这一节建条目。

## 开放问题

1. knowledge-vault 本会话没有挂上，没读。下次挂上它的会话先看里面有没有出处表或文献笔记，再决定合并还是只引用。
