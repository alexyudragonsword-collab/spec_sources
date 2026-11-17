# 变更记录 / Changelog

按版本记录。每条写**做了什么**和**为什么**；数字原值在 `cairn/LOG.md`。
下游重新 pin 时读这里：`consumers.yaml` 里登记的条目，数值或键名每变一次，这里就有一行 `` `<引用>` = <值> ``（铁律 4，`tests/test_consumers.py` 守着）。

## 0.6.0 —— 里程碑 2 核实轮收尾：第 7 批、DMG / EDMG 的码与扇区扫描、DeepScaleTool、IEEE Xplore 原文 10 篇（2026-11-17）

版本号随 `__init__.py` 变；`reader.py` 没动。共享表 153 条（0.5.0 是 133 条）：spec 136、survey 1、derived 16。

- **`mmw60_trx` 需重新 pin**：它 vendor 的 `__init__.py`（版本号）、`data/energy.yaml`、`data/frontend60.yaml`、`data/pa60.yaml` 在 `76ee72a`（#33 时 pin、已验收）之后变了。值变了的只有 `deepscale.node_scale_45_to_7nm` 0.175 → 0.1746（它只在同台表按 7 nm 重算的灵敏度节读，数字功耗在那里动 −0.23 %）；其余是 survey 改 spec（值不变）、新增条目与 note。
- **`fmcw_radar` 需重新 pin**：`data/frontend60.yaml` 在 `f87cc9b` 之后变了，只是 `rx60.comm_iscas2015`、`antenna60.okada2013_dbi` 两条 survey 改 spec，值不变；它读的 `rx60.radar_iwr6843*`、`isolation.*` 没动。
- d2d_link（`bbc0ccb`）vendor 的文件没动，不用为 0.6.0 重新 pin。
- 账本新增 20 个键（adc_survey 1、deepscale 1、dmg 8、edmg 4、pa60 6），记 `added=0.6.0`。
- 共享表只剩 1 条 survey：`ucie.standard.lane_repair` 的"降到 x8"。规范本身不能读，联盟白皮书、Hot Chips 2023 教程与 Das Sharma 2022 都没写。
- 许可：IEEE Xplore 的条款限制把内容交给 AI 工具。默认不发 Xplore 原文；用户确认其许可允许后才读，读完删本地副本（`cairn/Reference/README.md` 末两节）。

### IEEE Xplore 原文 10 篇（用户下载并确认其许可允许交给本库读）
- 用户 2026-11-17 发来 10 篇 IEEE Xplore 原文，确认其许可允许；本库读完删掉了本地副本（上传原件与抽出的文字、渲染图）。
- 改成 spec，值不变（`VERIFIED`）：
  - `horowitz2014.mult32_pj` 3.1 pJ、`horowitz2014.add32_pj` 0.1 pJ：Horowitz ISSCC 2014 Figure 1.1.9（45 nm、0.9 V，编码字体，渲染出来读）；
  - `rx60.comm_iscas2015`：Luo 等（清华）ISCAS 2015 摘要与 Table I。NF 7.1 dB 是三个信道上的最小双边带 NF，note 注明单边带约再高 3 dB；
  - `antenna60.okada2013_dbi` 6.0 dBi：Okada 等 JSSC 2013，系统要求与测量两段。
- 新增 6 条 spec：Asada Table I 其余 6 行的原文，`pa60.suzuki_isscc2008`、`pa60.kurita_rfic2009`、`pa60.bohsali_rfic2009`、`pa60.dawn_ims2009`、`pa60.pinel_isscc2008`、`pa60.chowdhury_isscc2008`。13 行至此都读过原文：P1dB、Psat 全对；[5] 的 PAE 5.0 % 与电压 1.0 V 原文里没有（Suzuki 没给效率，电压 1.2 V）；[8] 的增益 4.4 是正文 S21（汇总表 4.2）；[14] 的 5.5 是图上标注（正文 S21 5.6）。`pa60.eumc2011_table1` 的值不变，note 改写（`CHANGED` 里的替换句同步）。
- `ucie.standard.lane_repair` 仍是 survey：Das Sharma、Pasdast，IEEE Trans. CPMT 2022 只写标准封装靠降宽修复，没写降到 x8。`ucie.yaml` 没改。
- 共享表 153 条：spec 136、survey 1、derived 16。账本新增 6 个键，记 `added=unreleased`。

### DeepScaleTool：读工具原文件（不经 IEEE Xplore）
- 论文读作者的 arXiv 预印本 2102.10195v1（CC BY 4.0），工具读 SourceForge 上的 `DeepScaleTool.xlsm`（GPLv3，2021-03-03）。论文正文没有直接给 45 → 7 nm 的能量比；工具的能量倍数在 VBA 宏 `Sub Energy()` 里，是各节点相对能量（65 nm = 1）两格之比。宏源码用 olevba 当文本读出，没有执行。
- 新增 `deepscale.energy_by_node`（spec）：130 … 7 nm 共 11 个节点的相对能量，45 nm 0.63、7 nm 0.11。互证：论文 Fig. 2 截图 130 → 45 nm 的能量倍数 4 = 2.52 / 0.63；工具存档的单元格 90 → 32 nm 3.432 = 1.51 / 0.44。
- `deepscale.node_scale_45_to_7nm` 改成由它复算的 derived：0.11 / 0.63 = 0.1746（迁入时 0.175，Halo_Serdes 取的 3 位；`CORRECTED`）。
- 共享表 147 条：spec 126、survey 5、derived 16。账本新增 1 个键，记 `added=unreleased`。

### 验收：#33（mmw60_trx 重新 pin 到 `76ee72a`）
- mmw60_trx 在 mmw60_trx#60 合并 `53a9a16`（重新 pin 的提交 `3ea11be`：只换 vendor 文件，另改两处写死旧数的测试）。9 个 vendor 文件去掉出处头后与 `76ee72a` 逐字节相同，`3ea11be` 与它现在的 main `50f30df` 都是；本库本地跑它的 `vendor_check --strict`：9 个 verbatim（另 241 个因本地缺它的其它 sibling 跳过）；它带齐 sibling 是 250 verbatim。
- 指纹：本库在本地对 `23d0130`（父提交）与 `3ea11be` 各录一次（`MMW60_NO_JIT=1`），69 个值逐位相同；它的指纹不覆盖功耗列。合并表 180 → 193 条（#33 的 12 条与 `adc_survey.ti_sar_ge40gs_4to7nm`），未核实 20 → 9。
- 动的数只在功耗列：转换器功耗 × 70.815 / 70 = ×1.0116，它报示例 02 / 04 / 06 / 09 / 10 / 11 的 pJ/bit 涨 0.1–1 %（同台表最好一行 592 → 596，ay SC 188 → 189）；MCS 上限与 EVM 底板不动。
- 接线在 mmw60_trx#61（`50f30df`）：扩展 SC 档并进它借门限的对应关系，两张 LDPC 表进 SC 编码 PER（它自己实测的门限表），控制 PHY、时间常数与 SSW 帧算扇区扫描时长。都按键读，本地表里没有抄数，不按条登记。
- 更正：#33 的回复说它 vendor 的文件里 survey "从 14 条减到 3 条"，漏数了 `frontend60.yaml` 的 2 条，应为 16 → 5（少 11 条不变）。

### #33（mmw60_trx 请求）：DMG / EDMG 的 LDPC 与编码、扩展 SC MCS、控制 PHY 与扇区扫描
- 标准本身不能读，全部取自公开文件，用户对照 IEEE 802.11-2024 逐行核对一致（K1–K11）：TGad 采纳的规范文本 11-10/0433r2；REVmc 的 11-16/0233r0（扩展 SC MCS）；TGay 的 SFD 11-15/1358r9、11-16/1495r1，已采纳的 17/1061r1（动议 #264）、17/0214r1（动议 #178）。表格从 docx 逐格取，公式是嵌入图片、渲染出来读。
- 新增 12 条（11 spec、1 derived）：
  - `dmg.ldpc_matrices`：码长 672、Z = 42，码率 1/2、5/8、3/4、13/16 的基矩阵（-1 为零块）；
  - `dmg.data_encoding`：扰码 x⁷ + x⁴ + 1（周期 127，初值 7 位在头部），SC 与 OFDM 的码字数与填充公式；
  - `dmg.sc_mcs_extended`：MCS 9.1、12.1–12.6 的调制、码率、速率（2695 … 8085 Mb/s）；`dmg.ldpc_r7_8_punctured`：这几档的 7/8 是 13/16 码打掉前 48 个校验位（624 / 546）；
  - `dmg.control_phy`（STF 5120 码片、CEF 1152、头部 40 位、DBPSK、Ga32、等效 1/2）与 derived `dmg.control_phy_rate_bps` = 27.5 Mb/s；
  - `dmg.phy_timing`：SIFS 3 µs、SBIFS 1 µs、BRPIFS 20 µs、slot 3 µs、控制 PHY 前导 3564 ns 等；`dmg.ssw_frame`：SSW 帧 26 字节、SSW 字段 1 / 9 / 6 / 2 / 6 位；
  - `edmg.ldpc_672_r7_8`（588 信息位的新 7/8 码）、`edmg.ldpc_1344_lifting`（1344 码长的提升矩阵，7/8 作用于 3/4 并两两合行）、`edmg.sc_encoding`（码率表、N_CBPB、N_BLKS）、`edmg.short_ssw`（48 位）。
- 新测试 `test_the_ldpc_tables_agree_with_each_other`：EDMG 提升矩阵的 -1 与 DMG 基矩阵的零块逐格相同；672 位 7/8 矩阵等于 3/4 矩阵第 1+3、2+4 行之和。两份文件相隔六年，互相印证。
- 没有做的：EDMG 的最低灵敏度在公开材料里没有（TGay CID 1620 的解决方案只补了 EVM）；EDMG OFDM 的填充规则没找到；BRP / TRN 单元长度（mmw60 写的"如顺手"）这次没做。
- 修正（PR #35 合并之后）：`dmg.phy_timing` 的 `rifs_s`、`sifs_s`、`sbifs_s`、`brpifs_s`、`slot_s` 原写成 `1e-06` 这样没有小数点的指数式，PyYAML 按 YAML 1.1 读成字符串；改写成 `1.0e-06` 等，值不变。新测试 `test_no_number_in_exponent_form_was_read_as_text` 扫全表守着。
- 共享表 146 条：spec 125、survey 6、derived 15。账本新增 12 个键，记 `added=unreleased`。

### 第 7 批：能用公开材料核的 survey
- 放行 www.ecfr.gov（环境 "rf design"，用户批准）。
- **`fcc15255.*` 4 条** → spec（值不变）：读 eCFR 上 47 CFR §15.255 的现行条文（2026-11-12 版）。频段 57–71 GHz 在节标题与 (c) 首句；平均 40 dBm、峰值 43 dBm 在 (c)(1)(i)。迁入时 cite 写的 "(a)" 在现行条文里讲的是卫星，出处已改正。同一节 (c)(2) 有雷达类器件的限值，记进 ROADMAP。
- **`liu2025.per_target`** → spec（值不变）：arXiv v1 第 V 节原句 "the SNR required to achieve the specified PER (10−2 )"。顺带更正 `liu2025.k_threshold` 的 note：#26 时写"arXiv 版只写 the 1250 KHz"是错的，v1 也写了 "4 × 312.5 KHz"。
- **802.11 的 4 条** → spec（值不变），读 mentor 上的公开文件，用户对照标准核对一致（标准本身因许可不能读）：
  - `ieee80211ac.n_sd`：TGac 框架 11-09/0992r21（20 / 40 MHz 与 11n 相同；80 MHz 3 DC、11 个边带空、8 导频；160 = 2 × 80）、TGn 联合提案 11-05/1102r4（52、108）、TGax 11-15/0330r5（"11ac 80 MHz … payload 234 data, 8 pilots"）；
  - `ieee80211be.n_sd`：TGbe 框架 11-19/1262r23 的 Nsd_total 表（2×996 1960、4×996 3920、484+996 1448）与 11-15/0330r5 的 234；
  - `ieee80211be.ldpc_tone_mapping_distance`：TGax 框架 11-15/0132r17 Table 6（242 / 484 / 996 = 9 / 12 / 20）与 996 段的 D_TM = 20，TGbe 框架 "Existing RUs: identical to 802.11ax"；
  - `ieee80211.ldpc_ppdu_encoding_thresholds`：TGn 11-05/1102r4 Table 13（912 / 1464 / 2916）与步骤 (d) 的判据（0.1 / 1.2 / 0.3，公式图渲染出来读）。
- **ADC survey**：新增 `adc_survey.ti_sar_ge40gs_4to7nm`（spec）：Murmann ADC survey 2026-08-01 版里 ≥ 40 GS/s、4–7 nm 的 6 行时间交织 SAR（FOMW_hf 67.00 / 74.63 / 38.36 / 74.85 / 120.19 / 42.98 fJ）。两条统计改成由它复算的 derived（`CORRECTED`，测试允许改成 derived）：
  - `adc_survey.walden_fom_fj` = 70.815（迁入时 70：Halo_Serdes 把中位数 70.8 取了整）；
  - `adc_survey.walden_fom_range_fj` = [38.36, 120.19]（迁入时取到 0.1）。
- 还剩要用户下载的：Horowitz ISSCC 2014、ISCAS 2015 的 60 GHz 接收机、Okada JSSC 2013（实验室网站只有题录）、DeepScaleTool（ISCAS 2021）。
- 共享表 134 条：spec 114、survey 6、derived 14。账本新增 1 个键，记 `added=unreleased`。

## 0.5.0 —— 里程碑 2 续：车辆与角反射器、窗函数、Liu 2025 刊出版、802.15.3c 模型与 802.11ad / ay 的 PHY 数（2026-11-16）

版本号随 `__init__.py` 变；`reader.py` 没动。共享表 133 条（0.4.0 是 102 条）：spec 104、survey 17、derived 12。

- **`mmw60_trx` 需重新 pin**：它 vendor 的文件里只有 `__init__.py`（版本号）变了；它的数据文件在 #29 里已 pin 到 `3123b65`，之后没动。
- fmcw_radar（`f87cc9b`，#19）、d2d_link（`bbc0ccb`，#2）vendor 的文件在各自 pin 之后都没动，也都不 vendor `__init__.py`，不用为 0.5.0 重新 pin。三个库的数据都已在各自的 issue 里验收。
- 新数据文件：`data/windows.yaml`（`harris1978.*`）、`data/ieee802153c.yaml`（`tg3c.*`）。账本新增 31 个键（车辆与角反射器 4、窗函数 5、Liu 2025 刊出版 4、tg3c 4、dmg 5、edmg 9），记 `added=0.5.0`。
- 测试机制：`tests/test_extraction.py` 新增 `CORRECTED`（迁入条目按原文改值）；`RECOMPUTE` 支持表格逐列比。
- 许可：IEEE 802.11-2024（及 GET 计划里同类的 IEEE 标准）禁止输入 AI，与 UCIe 规范一样不读；802.11 的数改从 mentor.ieee.org 的公开提案取，用户对照标准核对。

### 验收：#29（mmw60_trx 重新 pin 到 `3123b65`）
- mmw60_trx 在 mmw60_trx#49 合并 `29eb6fe`（重新 pin 的提交 `2400c5b`，只做 pin、没接线）。9 个 vendor 文件去掉出处头后与 `3123b65` 逐字节相同，本库本地跑它的 `vendor_check --strict` 这 9 个都是 verbatim；它带齐 sibling 是 250 verbatim、0 skipped。
- 指纹：本库在本地对 `e662238`（父提交）与 `2400c5b` 各录一次（`MMW60_NO_JIT=1`），69 个值逐位相同。它的合并表 157 → 171 条（多出 14 条 `dmg.*` / `edmg.*`），未核实 22 → 20。它报 pytest、ruff 绿。
- 它手算核过 Δf、355 = 336 + 16 + 3、GI 样本数、OFDM MCS 1 与 SC MCS 21 的速率、信道间 DC 偏移每档 0.46875 MHz；可见变化只有示例 08 里 `dmg.sensitivity_assumptions` 的标签从 survey 变成 spec。EDMG 灵敏度它第一轮不用，要按距离换算时在本地写 assumed。`ay_ofdm` / `ay_sc` 接新键另开 PR。

### #29（mmw60_trx 请求）：802.11ad（DMG）/ 802.11ay（EDMG）单信道 PHY 的数
- **IEEE 802.11-2024 不能用**：用户经 IEEE GET 计划下载后，许可条款禁止把它输入 AI 系统（与 UCIe 规范同类）。本库不读标准，只读公开文件，再请用户对照标准核对（用户只回报哪几行对不上，没把标准内容发给本库）；2026-11-16 核对全部一致。
- 读的公开文件（PDF 只放本地）：TGad 采纳的完整提案规范文本 IEEE 802.11-10/0433r2；R&S 白皮书 1MA220_3e（2017，Table 4-1 转引 IEEE 802.11-2016 第 20 章；为取它在环境里放行了 scdn.rohde-schwarz.com，用户批准）；TGay 的 11-17/0597r1、11-17/0628r1、11-17/0909r0、11-15/1358r9（SFD）、11-18/0713r3、11-18/1152r0。采纳它们的动议号读自 TGay 动议汇编 11-17/0186r37（2020-12，最终版）。
- 新增 14 条（12 spec、2 derived）：
  - DMG：`dmg.phy_params`（2.64 GHz / 1.76 GHz、336 + 16 + 3、GI 48.4 ns、导频 ±10…±150、SC 块 64 + 448）、`dmg.sc_mcs`（MCS 1–12）、`dmg.ofdm_mcs`（13–24）、`dmg.tx_evm_db`（MCS 0–24 与扩展 9.1、12.1–12.6）、`dmg.rx_sensitivity_dbm`（MCS 0–31，判据 PER 1% / 4096 字节）；
  - EDMG（NCB = 1）：`edmg.ofdm_params`（GI 18.18 / 36.36 / 72.72 ns）、`edmg.ofdm_pilot_tones_ncb1`（导频位置随信道变，含信道 1–8 的中心频率与 DC 偏移）、`edmg.ofdm_pilot_values_ncb1`、`edmg.ofdm_mcs`（MCS 1–20 与 EVM）、`edmg.sc_params`（1.76 GHz、512 码片块、GI 32 / 64 / 128）、`edmg.sc_mcs`（MCS 1–21 与 EVM）、`edmg.sc_mcs_variants`（π/2-8PSK、π/2-64NUC）；
  - derived：`edmg.ofdm_rate_mbps`、`edmg.sc_rate_mbps`（单流速率，短 / 普通 / 长 GI），在 `RECOMPUTE` 里由上面的条目复算；`test_rule2` 的比较改成表格逐列比。
- 迁入的两条 survey 改成 spec（`VERIFIED`，值不变）：`ieee80211ay.channel_centres_ghz`（11-17/0597r1 Table 2）、`dmg.sensitivity_assumptions`（11-10/0433r2 21.3.3.8 原句"assumes 5 dB implementation loss and 10 dB noise factor"，迁入时是二手转引）。
- **发现**：
  - 2010 年的 TGad 提案文本与 2016 年标准（经 R&S）的 EVM 不同：SC MCS 1–12 几乎每档都改了，OFDM MCS 22、24 两档也改了；灵敏度只差 MCS 2（−67 → −66）。本库取 R&S 的值，note 记旧值。
  - EDMG 的 MCS 表在 TGay 里改过两次：OFDM 从 19 档（SQPSK / QPSK）到 20 档（DCM BPSK / DCM QPSK，加 64-QAM 1/2），SC 从 20 档到 21 档（加 π/2-BPSK 7/8 与 64-QAM 1/2）。本库按最后被采纳的 2018 年文本。
  - EDMG 的接收灵敏度在公开材料里没找到：TGay 有评论（CID 1620）要求补上灵敏度与 EVM，被采纳的解决方案 18/0713r3 只补了 EVM。没有建条目。
- 共享表 133 条：spec 104、survey 17、derived 12。账本新增 14 个键，记 `added=unreleased`。

### 验收：#26（mmw60_trx 重新 pin 到 `7aae876`）
- mmw60_trx 在 mmw60_trx#37 合并 `121b612`（重新 pin 的提交 `4d018e5`），vendor 9 个文件，比原来多了 `data/ieee802153c.yaml`。9 个文件去掉出处头后与 `7aae876` 逐字节相同，本库本地跑它的 `vendor_check --strict`：这 9 个都是 verbatim（另 241 个因本地缺它的其它 sibling 跳过）；它自己带上三个 sibling 跑：250 verbatim、0 skipped。
- 指纹：本库在本地对 `5e474e7`（父提交）与 `4d018e5` 各录一次（`MMW60_NO_JIT=1`），69 个值逐位相同；两边同有一项因没装 numba 报错。它的合并表 147 → 155 条（多出 4 条 `liu2025.*`、4 条 `tg3c.*`），未核实 43 → 22。它报 pytest、ruff 绿。
- 它有两条本地 note 点名 `tg3c.*`（`assumed.pn_apply_sides` → `tg3c.pn_model`、`tg3c.pn_psd0_examples_dbchz`；`assumed.pa_obo_reference` → `tg3c.pa_modified_rapp_shape`），由它的守卫核对键名，所以 vendor 了新文件。
- 它撤回了"0396 的拟合与 TGad 那颗是同一颗 PA"的判断，在它的 `cairn/spec-sources.md`、`cairn/external-validation.md`、ROADMAP C4 与示例 12 的说明里追加更正；0396 印刷的公式缺指数也记进了它的 `cairn/spec-sources.md`。

### #26（mmw60_trx 请求）：Liu 2025 刊出版，及它引的两份 IEEE 802.15 文件
- 用户从 IEEE Xplore 下载了刊出版（IEEE Commun. Mag. 63(3), pp. 69–75, 2025-03, doi 10.1109/MCOM.002.2400059），两份 802.15 文件取自 mentor.ieee.org（公开）。PDF 只放本地。
- `liu2025.*`：21 条对上刊出版，survey → spec。
  - 18 条值不变（`VERIFIED`）：TABLE 2 各行（MCS、PPDU、信道、1T1R、73.44 GHz、4096 bytes、40 ppm、相噪 1 MHz / 100 MHz / −93 dBc/Hz、OBO 8 dB）与 Simulation Configuration / Results 的 ±625 / ±156.25 kHz、±2.94 MHz、5.88 MHz、4.7，Introduction 的 14 GHz。
  - **3 条按刊出版改了值**（新的 `CORRECTED` 类，`tests/test_extraction.py`）：
    - `liu2025.table1_scs_hz` 16× 一列 1.25 MHz → **5 MHz**（刊出版三列都以 802.11ac 为基准，arXiv 版那一列是 802.11be）；
    - `liu2025.table1_bandwidth_hz` 16× 一列去掉 5120 MHz，最高 2560 MHz；
    - `liu2025.receiver_cfo_statement`："…for CFO and PN" → "…for CFO and used phase tracking only on the receiving end"（相噪在接收端做了相位跟踪）。
  - `liu2025.per_target` 仍是 survey：刊出版没有"specified PER (10^-2)"这句，note 写明。
  - 新增 4 条 spec：`liu2025.table1_idft_period_s`（800 / 400 / 200 ns）、`liu2025.table1_idft_size`（64/128/256/512）、`liu2025.cfo_algorithm_statement`（Discussion："CFO 估计补偿是算法问题"）、`liu2025.mlo_bf_training_statement`（60 GHz 扇区扫描可由 sub-7 GHz 触发、反馈）。
- 新数据文件 `data/ieee802153c.yaml`，前缀 `tg3c.*`，4 条 spec：
  - `tg3c.pn_model`：802.15-06-0477 slide 9 提出的 1 极点 1 零点模型，PSD(0) **−87** dBc/Hz、fp 1 MHz、fz 100 MHz；
  - `tg3c.pn_psd0_examples_dbchz`：slide 10 的四档示例 −96 / −93 / −90 / −87。Liu 的 −93 是其中一档，不是 0477 提出的值；
  - `tg3c.pa_modified_rapp_shape`：slide 5 的修正 Rapp 公式。**原文没给参数**（slide 13 自己也这么说），所以 Liu 的"modified Rapp model [15]"在 [15] 里查不到参数；
  - `tg3c.pa_ghorbani_nec_gaas`：802.15-06-0396 slide 10 的 NEC GaAs pHEMT 60 GHz PA Ghorbani 拟合（x1–x4 = 10 / 0.71 / 4.66 / 0，y1–y4 = −5.4×10⁴ / 4 / 2980 / 0.11），slide 8 的输入 P1dB −11 dBm。
- **发现**：
  - 0396 slide 10 印的 Ghorbani 公式分子少了指数。按印的式子，u = 0.3 V 处 AM-PM 是 −644°；分子写成 x1·u^x2、y1·u^y2 才与图上的拟合曲线相符（1.43 V、−17.4°）。
  - mmw60_trx 猜 TGad 的修正 Rapp 参数（g 4.65、α 2560、β 0.114）与这组 Ghorbani 参数是同一颗 PA 的拟合。复算不支持：几个相近的数在两个模型里是不同位置的参数；TGad 的 CMOS PA 在 0.58 V 饱和、AM-PM 为正（u = 0.3 V 时 +13.9°），NEC 的 GaAs PA 约 1.5 V、−17.4°。
- 共享表 119 条：spec 90、survey 19、derived 10。账本新增 8 个键，记 `added=unreleased`。

### 里程碑 2 第 4 批（续）：乘用车 RCS 与三面角反射器
- 放行 rosap.ntl.bts.gov 与 www.osti.gov（环境 "rf design"，用户批准），取到两份公开的政府报告。
- **乘用车**：NHTSA DOT HS 813 648（2025-01）。报告用两颗 76–77 GHz 车载雷达，按 ISO 19206-3:2021 的方法测了一个乘用车替身和轿车、两厢、MPV、SUV、轻卡；它转引了 ISO 的 RCS 边界，乘用车都落在边界内。新增：
  - `target_rcs.iso19206_3_car_rear`（spec）：车尾直线接近，40 m 以外平均 20 dBsm、上下各 10 dB，更近按 0.013 dB/m² ·(D − 40 m)² 下降；
  - `target_rcs.iso19206_3_car_30m`（spec）：30 m 一周各视角的上下界（车尾 2–25、车头 1–19、侧面 13–30 dBsm）；
  - `target_rcs.iso19206_3_car_rear_far_lower_dbsm`（derived）= 20 − 10 = 10 dBsm，在 `RECOMPUTE` 里复算。

  fmcw_radar 原记的乘用车 10 dBsm 正好是这条带子的下界，中心是 20 dBsm。ISO 19206-3 本身要购买，没读，读的是 NHTSA 报告里转引的表。
- **三面角反射器**：Sandia SAND2008-0396（A. W. Doerry，2008）。`target_rcs.trihedral_peak`（spec）：三角形 4πa⁴/(3λ²)、方形 12πa⁴/λ²、四分之一圆 15.6a⁴/λ²，a 是内棱长，峰值方向与每块板成 35.26°。用原文 Table 1 复核到 0.1 dB 以内。
  - **发现**：fmcw_radar 原记"10 cm 边、60 GHz、约 20 dBsm"，按三角形的式 1 实为 12.2 dBsm；接近 20 dBsm 的是方形（21.8 dBsm）。反射器尺寸与形状是用的人自己定的，本表只登记公式。
- 共享表 106 条：spec 56、survey 40、derived 10。账本新增 4 个键，记 `added=unreleased`。

### 验收：fmcw_radar#19（乘用车 RCS、角反射器、4 条窗函数）
- fmcw_radar 合并 `4495310`（0.2.13），pin `f87cc9b`，多 vendor `data/windows.yaml`。6 个文件去掉出处头后与 pin 逐字节相同，`vendor_check --strict` 里都是 verbatim。它报测试 203 个，CI 3.10–3.13 绿。
- 登记 5 条引用（它表里这 5 条原是 survey）：
  - `target_rcs.iso19206_3_car_rear_far_lower_dbsm` = 10.0（它标 derived；它的场景都在 15 m 以内，ISO 中心在那里只有 4–12 dBsm，所以取下界不取中心 20）
  - `harris1978.rect#bw_3db_bins` = 0.89
  - `harris1978.hann#bw_3db_bins` = 1.44
  - `harris1978.hamming#bw_3db_bins` = 1.3
  - `harris1978.blackman#bw_3db_bins` = 1.68（它 cite 里的 "exact" 已改掉）
- 角反射器它保持 20 dBsm，改记成自己的 assumed：15.6 cm 三角形三面角（60 GHz；77 GHz 档相当于 13.8 cm），cite 指向 Doerry 式 (1) 与 `target_rcs.trihedral_peak`。不是引用，不登记；原 cite 的"10 cm、~10² m²"已更正。
- 指纹：`0d32179` 对 `4495310` 2035 个值逐位相同，本库在本地重跑复核过。它的表现在 assumed 25、spec 11、derived 3，**survey 0**：迁移时它自己表里的 14 条 spec / survey 全部了结（13 条经登记的引用读本库，角反射器归它自己）。
- 它记下的后续（它的 ROADMAP P1 #5）：目标 RCS 是常数，不随距离、视角、频段变（示例 05 的车在 5.3 m，按 ISO 中心约 4.3 dBsm，比它低约 5.7 dB；同一个三面角 77 GHz 比 60 GHz 多 2.17 dB）。要按"种类 + 尺寸 / 视角"算时它再来对接。

### 里程碑 2 第 4 批（完）：窗函数（Harris 1978 表 I）
- 用户从 IEEE Xplore 下载 F. J. Harris, Proc. IEEE 66(1), 1978。新数据文件 `data/windows.yaml`，前缀 `harris1978.*`，一个窗一条（spec），value 是表 I 的一整行 10 列（最高旁瓣、衰减速率、相干增益、等效噪声带宽、3-dB 宽、扇贝损失、最坏处理损失、6-dB 宽、75 % / 50 % 重叠相关）：
  - `harris1978.rect`、`harris1978.hann`（表里的 cos^α α = 2）、`harris1978.hamming`、`harris1978.blackman`：3-dB 宽 0.89 / 1.44 / 1.30 / 1.68 bins，等于 fmcw_radar 本地表里的 4 个数；
  - `harris1978.exact_blackman`：3-dB 宽 1.52。
- 按原文的窗定义（DFT-even，即 scipy 的 `sym=False`）逐列数值复算：矩形、Hann 全部相符，Hamming 只有扇贝损失差 0.03 dB（表 1.78，复算 1.75；表自己的最坏处理损失 3.10 按 1.75 算才对得上）。
  - **Blackman** 只有两列宽度不符：3-dB 宽复算 1.644（表 1.68），6-dB 宽 2.299（表 2.35）；其余 7 列相符。
  - **Exact Blackman** 一行与原文自己的系数（式 (31a)）几乎每列都不符：旁瓣 −68.2 dB（表与正文 −51）、相干增益 0.427（原文说这类窗的相干增益就是 a0 = 0.4266，表 0.46）、3-dB 宽 1.609（表 1.52）。照原文登记，note 写明不要当这个窗的性质用。
  - **发现**：fmcw_radar 的 `window.blackman_3db_bins` 在 cite 里写成 exact Blackman，它的值 1.68 与它的代码（scipy blackman，0.42 / 0.5 / 0.08）都是 Blackman 一行。
- 共享表 111 条：spec 61、survey 40、derived 10。账本新增 5 个键，记 `added=unreleased`。

### 验收：mmw60_trx#27（0.4.0）
- mmw60_trx 合并 `5de5b3a`，pin `8e5f2e2`（0.4.0）。8 个 vendor 文件去掉出处头后与 pin 逐字节相同，`vendor_check --strict` 无 stale。
- 指纹（b16b6a0 对 5de5b3a，69 个值）逐位相同。`all_entries()` 130 → 137，多出的正是 7 条 `pa60.*`；未核实仍是 42。它的 spec 相关测试 15 过 2 跳过。
- 它改了两处文档的文字：`cairn/comparison-table.md` 注明 7 行已读原文、[1] 的 9.0 dB 原作者归因于偏置、正常偏置里最软约 5.6–6.0 dB、[11] 是 48 / 52 GHz；`cairn/spec-sources.md` 追加更正。它另把"示例 09 的 3.3 dB 中位数包括了 [1] 与 [11]"记进自己的 ROADMAP C10。

### 答复：#22（d2d_link 请求原始 BER 的速率区间条目）
- 不加。公开材料里的 BER 表只列离散速率（4 / 8 / 12 / 16 / 24 / 32 Gb/s），UCIe 的速率本身就是这 6 档，28 GT/s 不是它的工作速率；1.1、2.0、4.0 白皮书与教程概览篇也没有按区间给 BER。眼罩能有 `@24-32` 区间条目，是因为原文眼罩表的表头就写着 "24-32Gb/s"。把空档填成 1e-15 是推断，共享表不收（铁律 2）；d2d_link 若要按邻档判，应作为它自己本地表里的 assumed。

## 0.4.0 —— 里程碑 2：PA、TDC、UCIe、大气与行人 RCS 对上原文（2026-11-14）

版本号随 `__init__.py` 变；`reader.py` 没动。共享表 102 条（0.3.0 是 84 条）：spec 53、survey 40、derived 9。

- **`mmw60_trx` 需重新 pin**：它 vendor 的文件里变了 `__init__.py`（版本号）与 `data/pa60.yaml`（第 1 批新增 7 条、`pa60.eumc2011_table1` 的 note）。读到的已有的数一个不变，它的 `all_entries()` 会多 7 条。
- fmcw_radar 已在 [#17](https://github.com/alexyudragonsword-collab/fmcw_radar/issues/17) 里 pin 到 `e49979f`，d2d_link 已在 [#2](https://github.com/alexyudragonsword-collab/d2d_link/issues/2) 里 pin 到 `bbc0ccb`（都已验收）。它们 vendor 的文件之后都没动，也都不 vendor `__init__.py`，不用为 0.4.0 重新 pin。
- 新数据文件：`data/atmosphere.yaml`、`data/radar_targets.yaml`、`data/adpll60.yaml`、`data/tdc.yaml`。账本新增 18 个键（大气 5、行人 RCS 1、PA 7、ADPLL 1、TDC 2、UCIe 2），记 `added=0.4.0`。

### 验收：d2d_link#2（UCIe 第 3 批）
- d2d_link 从 `0cbd4e9` 快进到 `d5d34a6`（0.17.0），5 个提交：重新 pin `bd1e087`，再按 issue 的 4 点各一个提交。3 个 vendor 文件去掉出处头后与 `bbc0ccb` 逐字节相同，`vendor_check --strict` 里它们都是 verbatim。它的测试 267 个通过、4 个跳过。
- 指纹逐个提交复核（3597 个值）：重新 pin、眼罩标注（第 1 点）、TX 摆幅文档（第 3 点）、QDR 显示（第 4 点）都逐位不变；只有 BER 一个提交（第 2 点，`f868f3c`）动了 974 个值，全在统计引擎的眼、BER、采样相位和随之变化的游标、时域样本上。那个提交在 `src/` 下只改了垫片里用 `ref` 展开 `ucie.raw_ber_by_rate` 的 23 行。
- 解析出的 BER 目标：表里 12 格（2 种封装 × 6 个速率）逐格与 `ucie.raw_ber_by_rate` 相同；5 个内置配置（都是 32 GT/s）从 1e-27 变成 1e-15。表外速率退回 1e-27。
- 它的处理：眼罩保留"含抖动的眼对眼罩"的比法，在报表里写明比规范更严；BER 按表取（32 GT/s 的余量 x1 +0.091 → +0.205，x5 耦合 −0.121 → −0.010 仍不过）；TX 0.4 V 保留为最坏情况的默认值；QDR 有了出处，并修了把 QDR 印成"16 GHz DDR"的显示错误。它也把规范的许可约束写进了自己的 AGENTS 与 CONTRIBUTING。

### 验收：fmcw_radar#17（TDC 分辨率）
- fmcw_radar 合并 `0d32179`，pin `e49979f`，多 vendor `data/adpll60.yaml`。5 个文件去掉出处头后与 pin 逐字节相同，`vendor_check --strict` 没有 stale。它的测试 200 个通过、2 个跳过。
- 登记 1 条引用：`adpll60.wu_jssc2014_tdc#tdc_res_s` = 1.22e-11（60 GHz 档；77 GHz 档仍是它自己的 5 ps 占位，不读本库）。
- 指纹：相对 `ffc703e` 动了 720 / 2035 个值（值的总数随检出的鬼目标变多）。在 `ffc703e` 上只改这一个数、用它的工具重新导出时钟剖面：剖面与它提交的逐字节相同，2035 个值与 `0d32179` 逐位相同，变化全部来自这一个数。
- **它报回的后果**：步长 5 → 12.2 ps 后，1 ps 的 TDC 抖动只有 0.08 LSB，打不散周期性量化误差。默认 60 GHz 配置下每帧检出 2.75 个鬼目标（原来 0），ISLR −28.6 → −22.6 dB。扫抖动 1 / 1.8 / 2.44 / 3 ps 得每帧 2.75 / 2.08 / 0.92 / 0.16 个。TDC 自身抖动的出处因此直接决定它的鬼目标结论，见 ROADMAP 第 2 项。

### 验收：mmw60_trx#25、fmcw_radar#15
- mmw60_trx 重新 pin 到 0.3.0：合并 `b16b6a0`。
  - 8 个文件去掉出处头后与 `9a443ba` 逐字节相同。
  - 指纹在 97353e0 与 b16b6a0 之间 69 个值逐位相同。
  - `all_entries()` 130 条，未核实 42 条。
- fmcw_radar 改成引用 3 条（选了只算氧气）：合并 `ffc703e`，pin `dfaa36b`。
  - 4 个文件逐字节相同。
  - 指纹对 79d040a 动了 319 / 1979 个值。在 79d040a 上只把两个氧气数换成新值，1979 个值就与 ffc703e 逐位相同，所以全部变化都只由这两个数引起。
  - 登记 3 条引用：
    - `itu_p676.gamma_o_dry_sea_level#db_per_km@f_ghz=60` = 14.651
    - `itu_p676.gamma_o_dry_sea_level#db_per_km@f_ghz=77.5` = 0.091
    - `target_rcs.deep2019_pedestrian_77g#co_pol_min_dbsm` = -10.0
  - fmcw 自己加了第四个标签 derived（必须带 upstream，note 写公式）。氧气两条标 derived，人体 RCS 标 spec。

### 里程碑 2 第 3 批：UCIe 对上联盟公开的教程与白皮书
- **UCIe 规范本身不能读**：规范下载页的最终用户许可协议禁止把规范（全部或部分）输入任何 AI 系统，包括用它分析、解读或提取。本库因此不读规范，读联盟公开的两份材料：Hot Chips 2023 的 UCIe 教程 "Electrical, Form-Factor, and Compliance"（slides 52–81）与 2022 年 2 月的 UCIe 1.0 白皮书 "Building an open chiplet ecosystem"（为此在环境 "rf design" 里放行了 www.uciexpress.org、uciexpress.org、hc2023.hotchips.org、www.hc2023.hotchips.org，用户批准）。
- `data/ucie.yaml` 16 条里 15 条值与原文相同，由 survey 改为 spec（`VERIFIED`），值和单位一个不变：速率、前向时钟、两条 BER、三条眼罩、TX 摆幅、两种封装的凸点间距 / reach / 宽度、先进封装的修复方式。`ucie.standard.lane_repair` 仍是 survey：原文只写降宽，没写降到 x8；它的 note 写明读到了什么（`CHANGED` 一次替换）。
- 新增 2 条 spec：`ucie.raw_ber_by_rate`（分速率、分封装的原始 BER 表）、`ucie.advanced.spare_lanes_per_32` = 2。
- **发现**（写进各条 note）：
  - 三条眼罩（40 mV；0.75 UI @ 4–16 Gb/s；0.65 UI @ 24–32 Gb/s 开均衡）是**信道合规的眼罩**：用无噪声、无抖动的行为级 TX / RX 模型仿真信道，不是收端含抖动的眼图规格。d2d_link 的判定落在 0.65 UI 上，若把它当成含抖动的收端判据，就比原文更严。
  - **原始 BER 分速率**：1e-27 只到先进封装 12 Gb/s、标准封装 8 Gb/s，更高速率是 1e-15，靠 CRC 与重传。迁入时 cite 说 2022 白皮书有"BER < 1e-27"，那份白皮书里没有这句。
  - TX 摆幅 0.4 V 是**最小值**，不是标称值；另建议最高 < 0.85 V。
  - 前向时钟：每个速率都有时钟 = 速率 / 2 一档，24 / 32 GT/s 另有速率 / 4 一档。
  - 先进封装每 32 条数据通道 2 条备用，x64 模块即 4 条。
- 共享表 102 条：spec 53、survey 40、derived 9。账本新增 2 个键。

### 里程碑 2 第 2 批：60 GHz ADPLL 的 TDC
- `data/adpll60.yaml`（新，前缀 `adpll60`，没有库 vendor 它）：`adpll60.wu_jssc2014_tdc`（spec，Wu、Staszewski、Long，JSSC 2014）。TDC 平均时间分辨率 12.2 ps（1.2 V；字段 `tdc_res_s` 按秒记为 1.22e-11，fmcw_radar 按秒读，引用不做换算），100 MHz 参考；按原文公式 ℒ = (2π)²/12 · (Δtres/TV)² / fR，60 GHz 下理论带内相噪 −78 dBc/Hz（复算 −77.54），实测 −77 dBc/Hz（环路带宽约 1.5 MHz），由 TDC 量化主导。
- **原文没有给 TDC 自身的输入参考抖动**：fmcw_radar 的两个占位里，`tdc_res_s`（5 ps）有原文数 12.2 ps 可引，`tdc_jitter_s`（1 ps）没有。摘要的 590.2 fs 是合成器输出的积分抖动，不是 TDC 的。
- 更正：原文清单说这篇在 TU Delft 机构库有免费全文，实际那条记录只有元数据。
- 又读了 Wu 文引的 TDC 原文 [23]（Staszewski et al., TCAS-II 2006，90 nm GSM 用）：分辨率 17–21 ps、INL < 0.7 LSB，也没有 TDC 自身的抖动。没有库读这些数，不建条目，只记在 `cairn/Reference/README.md`。
- `data/tdc.yaml`（新，前缀 `tdc`，没有库 vendor 它）：读了 Wu 文 [35] Henzler et al., ISSCC 2008（90 nm 局部无源插值 TDC）。`tdc.henzler_isscc2008`（spec）：分辨率 4.7 ps（1.2 V），单次精度 0.7 LSB（反复测同一间隔时输出码字的标准差），INL ±1.2、DNL ±0.6 LSB。`tdc.henzler_isscc2008_single_shot_s`（derived）= 0.7 × 4.7 ps = 3.29e-12 s，在 `RECOMPUTE` 里复算。它是能找到的唯一一个 TDC 自身随机误差的量级，但结构不同、含离散化与测试脉冲的抖动，note 写明是上界量级。

### 里程碑 2 第 1 批（部分）：Asada Table I 的 7 行对上原文
- 用户从 IEEE Xplore 下了 4 篇 ISSCC 文摘，是 Table I 里 Psat − P1dB 的两端（[1]、[13]）与 Psat 的两端（[6]、[2]）。`data/pa60.yaml` 新增 4 条 spec：
  - `pa60.chan_isscc2009`（[1]）：P1dB 2.5、Psat 11.5 dBm，差 9.0 dB；
  - `pa60.lai_isscc2010`（[2]）：0.9 / 1.0 V 两档；
  - `pa60.law_isscc2010`（[6]）：P1dB 18.2、Psat 19.9 dBm，差 1.7 dB；
  - `pa60.tanomura_isscc2008`（[13]）：0.7 / 1.0 V 两档，带汇总表的 ± 范围；
  - `pa60.martineau_isscc2010`（[15]，第五篇，2026-11-14）：1.2 / 1.8 V 两档，P1dB 11.0 / 11.5、Psat 16.6 / 18.1 dBm，差 5.6 / 6.6 dB；
  - `pa60.kuo_mwcl2009`（[9]，2026-11-14）：1.8 / 2.4 / 3 V 三档，差 3.5 / 4.5 / 6.0 dB，漏压越高压缩越平缓；
  - `pa60.jin_esscirc2007`（[11]，2026-11-14）：Psat 8、P1dB 5 dBm，差 3.0 dB，**但在 48 GHz 测**；增益峰值 25 dB 在 52 GHz，60 GHz 时只有 11 dB。
- **7 行里 P1dB、Psat、峰值 PAE 都与原文相同**，`pa60.eumc2011_table1` 的值不动。不同之处：
  - 增益有两格不同：[1] 原文表是 15.8（Asada 写 16.0）；[13] 的 15.2 是 0.7 V 的线性增益，同一行另外三格是 1.0 V 的（1.0 V 是 14.3）。
  - [11] 四格都在原文里，但不是 60 GHz 的数：Asada 把 52 GHz 的峰值增益与 48 GHz 的功率扫描放进了 60 GHz 的对比表。原文 Fig. 9 只有 6 个点、间隔 5 dB，增益从最低一点就在下降，正文的 P1dB 5 dBm 在图上读不出来。
  - [13] 那格 15.2 的来路：Kuo（[9]）的对比表把 Tanomura 写成 15.2 / 10 / 11 / 8.2 / 150 mW / 1 V，与 Asada 一行完全相同，看来是从这里转抄的。
  - [2] 原文前后不一：正文与题名是 Psat 17.9 / OP1dB 15.4 dBm、PAE 11.7 %，它自己的汇总表是 17.7 / 15.1、11.1 %。Asada 抄的是汇总表，条目两套都记。
- **发现**：Table I 里唯一接近 TGad Rapp 9.5 dB 的 [1]（9.0 dB），原作者自己说 P1dB 偏低可能是各级偏置不当造成的提前压缩。去掉这一行，13 行里最大是 [15] 的 5.6 dB。[15] 的原文读了：这 5.6 dB 是正常的 A 类 cascode 平缓压缩，而且它的 Psat 是功率扫描终点（Pin = 10 dBm）的输出、曲线仍在上升，真实的差只会更大；同一颗 PA 在 1.8 V 时是 6.6 dB。`pa60.eumc2011_table1` 的 note 写明了这几点，并把"本库"改成库名（`CHANGED` 登记）。
- 顺带核了 Asada 参考文献表的两处笔误：[8] 的页码，Lai 与 Law 都写 Bohsali RFIC 2009 pp. 31–34，Asada 写 39–42；[15] 的题名，原文是 "18dBm Power Amplifier"（1.8 V 时的 Psat），Asada 写成 "18 dB"。
- 共享表 97 条：spec 34、survey 55、derived 8。账本新增 7 个键，记 `added=unreleased`。（加上第 2 批：100 条，spec 36、derived 9；账本再加 3 个键。第 3 批后见上面。）

### 里程碑 2 第 4 批（部分）：大气衰减与行人 RCS
- `data/atmosphere.yaml`（新，前缀 `itu_p676`）：ITU-R P.676-13 的逐线法，只录氧气 / 干空气这一支。
  - spec 3 条：Table 1 的 44 条谱线（`itu_p676.oxygen_lines`）、式 (1)–(9)（`itu_p676.method`）、图 1 的条件（`itu_p676.figure1_conditions`）。
  - derived 2 条：
    - 海平面干大气的氧气比衰减 `itu_p676.gamma_o_dry_sea_level`：57 / 60 / 64 / 76 / 77 / 77.5 / 81 GHz 依次为 10.079 / 14.651 / 6.836 / 0.108 / 0.096 / 0.091 / 0.065 dB/km；
    - 峰值 `itu_p676.gamma_o_dry_sea_level_peak`：15.06 dB/km @ 60.81 GHz。

    两条都在 `RECOMPUTE` 里用共享条目复算；与独立实现 itur（P.676-12）一致，到 4 位小数。
  - **发现**：fmcw_radar 记的 77 GHz 氧气衰减 0.4 dB/km 实为总气体衰减（标准大气下氧气 0.098 加水汽 0.251，合计 0.348）。氧气本身在 77–77.5 GHz 只有 0.09–0.10 dB/km。
    - **更正**（fmcw_radar#15 指出）：0.348 是把 1013.25 hPa 当干空气压算的（itur 的 `p` 参数是干空气压，总压 1023.2）。若当总压读，是 0.096 + 0.249 = 0.344。条目只登记干大气，数值不受影响；`itu_p676.gamma_o_dry_sea_level` 的 note 里那句"合计 0.348"等这个文件下次改时注明读法（ROADMAP）。
- `data/radar_targets.yaml`（新，前缀 `target_rcs`）：`target_rcs.deep2019_pedestrian_77g`（spec，arXiv:1910.13706），77 GHz 行人同极化 RCS −10 到 +5 dBsm，交叉极化约低 10 dB。**是射线追踪仿真，不是实测**，note 写明。
- 当时共享表 90 条：spec 27、survey 55、derived 8。账本新增 6 个键，记 `added=unreleased`（发版时换成版本号）。

## 0.3.0 —— 里程碑 2 第一批：TGad 评估方法学对上原文；退役 0.2.0 的别名（2026-11-13）

**下游重新 pin**（铁律 4）：
- `mmw60_trx` 需重新 pin：它 vendor 的 `data/ieee80211.yaml` 里 9 条 `tgad_em.*` 由 survey 改为 spec，并新增 4 条；5 个数据文件删掉了 `aliases:`；`__init__.py` 的版本号变了。**数值一个不变**，指纹应逐位不变。示例 09 期望输出第 15 行打印的 `tgad_em.pa_rapp_p [survey, unverified]` 会变成 spec 标签。它已经不读旧名（#23），别名退役不影响它。
- `fmcw_radar` 需重新 pin：它 vendor 的 `data/frontend60.yaml` 只删了两行别名（它不读那两个旧名），读到的 5 个数不变。可以择机。
- `d2d_link` 需重新 pin：自 0.2.0 起只差 `reader.py` 里删掉的版本号那一行（本版没碰 `reader.py`、`ucie.yaml`）。可以择机。

### TGad 评估方法学对上原文（IEEE 802.11-09/0296r16）
- **为什么**：mmw60_trx 预设 PA 的 AM/PM 至今用的是 TGad EM 的参数，这 9 条原来只读到搜索摘录。放行 mentor.ieee.org 后读了 r16（2010-01-20），并取 r09 对照；公式是 .doc 里嵌入的公式对象，转成 PDF 后渲染第 4–5 页读的。
- 9 条由 survey 改为 spec：`tgad_em.pa_rapp_g` / `pa_rapp_asat` / `pa_rapp_p` / `pa_ampm_alpha` / `pa_ampm_beta` / `pa_ampm_q1` / `pa_ampm_q2` / `pa_model_shape` / `pn_model_shape`，带 quote 与 section。**值、单位都没变**，原来的数和原文逐个相同（g 4.65、Asat 0.58、s 0.81，α 2560、β 0.114、q1 2.4、q2 2.3，两个公式的形状也相同）。`tests/test_extraction.py::VERIFIED` 记着它们。
- 新增 4 条 spec，都是原文写明、而消费方一直标着"原文没说"的：
  - `tgad_em.pn_params`：PSD0 −90 dBc/Hz、fp 1 MHz、fz 100 MHz、PSD(∞) −130 dBc/Hz；
  - `tgad_em.pn_sides`：相噪"modeled at both transmitter and receiver"；
  - `tgad_em.pa_backoff_definition`：回退 = 10·log10(Average TX Power / Psat)；
  - `tgad_em.pa_backoff_recommended_db`：OFDM 8 dB、单载波 0.5 dB。
- 共享表 84 条：spec 23、survey 55、derived 6、assumed 0。

### 退役 0.2.0 的 17 个别名
- 前提：mmw60_trx 已不读旧名（它把 `DeprecatedKeyWarning` 设成了测试错误，#23），fmcw_radar、d2d_link 不读这 17 个键。各数据文件的 `aliases:` 删掉，`keys.lock` 补 `retired=0.3.0`，旧名再读是 KeyError。

### 其他
- mmw60_trx 已重新 pin 到 0.2.0（`e573d4d`；[#23](https://github.com/alexyudragonsword-collab/mmw60_trx/issues/23)，它的合并提交 `97353e0`），读旧键名的调用全部改掉。
- `cairn/Reference/README.md`：原文清单。
  - 已读：TGad EM r16 / r09、Asada EuMC 2011。
  - 待取：按里程碑 2 分批，Asada Table I 转引的 13 篇题名已从它的参考文献表里读出来；ROADMAP 里原来那份"脚本能取"的说法在本环境里有一半不成立，已改。
  - `.gitignore` 加了 `*.doc` / `*.docx`。

- mmw60_trx 已重新 pin 到 0.2.0（`e573d4d`；[#23](https://github.com/alexyudragonsword-collab/mmw60_trx/issues/23)，它的合并提交 `97353e0`），读旧键名的调用全部改掉，`consumers.yaml` 里它的 pin 已更新。fmcw_radar、d2d_link 仍在 `d7b4d1e`，择机重新 pin（见 0.2.0 一节）。

## 0.2.0 —— 17 个旧前缀键改名（2026-11-13）

**下游重新 pin**（铁律 4；`consumers.yaml` 的 `vendored:` 核对）：
- `mmw60_trx` 需重新 pin：它 vendor 的 5 个数据文件里有 17 个键改了名，`__init__.py` 里多了版本号，`reader.py` 少了版本号。旧键名在 0.2.x 仍能读，但会发 `DeprecatedKeyWarning`，读出来的条目 `.key` 是新名，所以示例 08 / 09 打印的键名会变（更正：原写 04 / 08 / 09，04 打印的是 mmw60 本地的键，不在改名之列）；数值不变，指纹应逐位不变。0.3.0 之前要把调用改成新名。见 mmw60_trx 的 issue。
- `fmcw_radar` 需重新 pin：它 vendor 的 `data/frontend60.yaml` 里改名的两条（`rx60.comm_iscas2015`、`antenna60.okada2013_dbi`）它不读，`reader.py` 只少了一行版本号。读到的 5 个数不变，可以择机重新 pin。
- `d2d_link` 需重新 pin：`reader.py` 只少了一行版本号，`data/ucie.yaml` 与 `legacy_keys/d2d_link.yaml` 都没变。可以择机重新 pin。

### 改名（铁律 3，走弃用期）
- **为什么**：这些键的前缀是标签，不是领域；里程碑 2 把 survey 核实成 spec 之后，键名就和标签矛盾了。按 mmw60 迁完、核实轮动这些条目之前的时机做。
- 17 个键：旧名写进各数据文件的 `aliases:`（`since: "0.2.0"`），读取时发 `DeprecatedKeyWarning`；`keys.lock` 里记 `aliased=0.2.0`，至少留到 0.3.0。

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

- 条目里指向旧名的 3 处交叉引用跟着改，登记在 `tests/test_extraction.py::CHANGED`：`adc_survey.walden_fom_fj` 的 note，以及 `liu2025.k_threshold_stf`、`liu2025.k_threshold_ltf_only` 的 cite。值、单位、标签都不变。
- 新前缀 `horowitz2014`、`adc_survey`、`deepscale`、`ieee80211`、`ieee80211ac`、`ieee80211be`、`antenna60`。标签不能再当前缀（`LEGACY_PREFIX_KEYS` 删掉，改成一律禁止）。
- 版本号从 `reader.py` 挪到 `__init__.py`：以后单纯升版本，不会再让只 vendor `reader.py` 的消费方变成"需重新 pin"。

### 三个消费方的迁移验收（2026-11-13）
- mmw60_trx（[#21](https://github.com/alexyudragonsword-collab/mmw60_trx/issues/21)，合并 `b8fc55b`）、fmcw_radar（[#13](https://github.com/alexyudragonsword-collab/fmcw_radar/issues/13)，`79d040a`）、d2d_link（[#1](https://github.com/alexyudragonsword-collab/d2d_link/issues/1)，`0cbd4e9`）都已按 spec_sources@`d7b4d1e` 迁完。本库在各自 main 上独立复核：
  - vendored 文件与 PIN 逐字节相同：8 / 2 / 3 个；
  - 指纹重录逐位相同：68、1979、3597 个值（d2d 补装 scikit-rf 后录全）；
  - mmw60 经垫片读出的 125 条旧条目 `repr` 逐条相同。
- 三份迁移说明删除；fmcw 那 14 条的清单移到 ROADMAP 里程碑 2。
- `consumers.yaml` 加 `vendored:` 一节（铁律 4 的第二种登记）：整份 vendor 的消费方按文件登记（库、pin、文件）。这些文件在某个消费方的 pin 之后改了，CHANGELOG 必须写一行 `` `<库>` 需重新 pin ``（`tests/test_consumers.py` 用 git 历史核对，CI 改成完整检出）。按条连值登记仍只用于在自己表里抄了数的引用（fmcw 的 5 条）。

## 0.1.0 —— 开库：三张表合成一处（2026-11-13）

**为什么**：同一类外部数字散在三个库里各一张表（mmw60_trx 125 条、fmcw_radar 39 条、d2d_link 16 条），表放在某个消费方里，改一次键名就打断别人，核实一条原文也只惠及一个库。

- **读取器** `src/spec_sources/reader.py`：公开名字是 mmw60_trx `mmw60.spec` 的超集（`SpecNumber` 字段、顺序、默认值与校验信息都相同），外加 `ref()`、`aliases()`、`legacy_keys()`、`merge_tables()`、`audit_tags()`。加载器拒绝同一映射里的重复键（`yaml.safe_load` 会静默保留后一个）、未知字段与跨表重复键。
- **数据**按出处的领域分 7 个文件（`AGENTS.md` 有表），共 80 条：spec 10、survey 64、derived 6、assumed 0。
  - 从 mmw60_trx@13024e0b012923071d827cc557b0da5eb9a9b2aa 迁入 63 条：spec 10、survey 48、derived 5，每个字段与源表相等。
  - 留在 mmw60_trx 的 62 条：assumed 56；derived 3（两条用到它的 assumed，一条是它自己示例 03 的读数）；survey 3（`survey.clock_profile_wu19`、`survey.clock_profile_wu19_x10` 指向它仓库里的文件、后者还用了它的 assumed 底噪；`survey.dsp_ip_dpd_poly_p4` 是姊妹库的综合估计）——铁律 2。
  - 从 d2d_link@6789810ccb6328324673222b2f64cc21f748451e 迁入 16 条（全是 survey），键名加 `ucie.` 前缀；旧的裸键名在 `legacy_keys/d2d_link.yaml`，给它的垫片用。
  - 新增 1 条 derived：`isolation.tx_rx_tue2018_no_ebg_min_db` = 40 − 20 = 20 dB，接住 fmcw_radar 在引用里做的减法（铁律 6）。
- **迁入时改的两处写法**（铁律 5）：mmw60_trx 表第 636 行的注释写着"改成 source: spec"，让 `grep -c "source: spec"` 得 11、实际 10（它的守卫只数 survey / assumed，没发现）；节注释改写后放进 `data/frontend60.yaml` 的文件头。d2d_link 的 `ucie.rx_eye_width_ui@24-32` 的 note 写着"改 source: spec 或删去"，改成"改成 spec 标签或删去"（它的表头注释还有一处，表头已重写）；这是迁入条目唯一改动的字段，登记在 `tests/test_extraction.py::CHANGED`。
- **登记**（`consumers.yaml`，fmcw_radar@2e5cbb61cef62819804fad89a197b0412b2eb84d 的 5 条引用）：
  - `rx60.radar_iwr6843#tx_power_dbm` = 12.0（fmcw_radar `60g_sensing.tx_power_dbm`）
  - `rx60.radar_iwr6843#nf_db` = 12.0（`60g_sensing.nf_db`）
  - `rx60.radar_iwr6843#p1db_in_oob_dbm` = -12.0（`60g_sensing.p1db_oob_dbm`）
  - `rx60.radar_iwr6843_fig7_2#p1db_inband_dbm@gain_db=40` = -34.0（`60g_sensing.p1db_inband_dbm`）
  - `isolation.tx_rx_tue2018_no_ebg_min_db` = 20.0（`60g_sensing.tx_rx_isolation_db`；原引用 `#with_ebg_db-improvement_max_db`）
- **守卫**：六条铁律各有测试（`AGENTS.md` 写明哪条对哪个测试）；迁入条目逐字段对 `tests/fixtures/` 的源表副本（文件头写库名与完整 SHA，有姊妹库检出时再对 `git show` 逐字节）；`src/spec_sources/` 拷到临时目录、换个包名 import 并运行。`keys.lock` 是发布过的键的账本。
- **迁移说明**：`cairn/migration-mmw60_trx.md`、`cairn/migration-fmcw_radar.md`、`cairn/migration-d2d_link.md`；三个库本轮不改，要它们做的在 ROADMAP"报回上游"。每份都在那个库 pin 提交的临时 worktree 上演练过：指纹 d2d 3345 / fmcw 1979 / mmw60 68 个值逐位相同，mmw60 经垫片读出的 125 条旧条目逐字段相同；演练查出的问题写进了说明。
- `audit_tags`（给消费方本地表用的守卫）只报铁律 5 禁止的：非标签行里的 `source: <标签>`、注释与 cite / note / quote / section / unit 里的 `source:`。值映射里的 `source` 键是数据（mmw60 的 `assumed.pa60_surveyed_pick`），不报；共享表另有更严的测试（`grep -c "source:"` 等于条目数）。
- CI：ruff + pytest（Python 3.10 / 3.12）。依赖只有 PyYAML。LICENSE 与 mmw60_trx 相同（MIT）。
