# Project Cairn 日志

本文件按倒序记录实质性进展 —— 最新条目在本行正下方。每条保持简短（摘要 + 指针），
结论沉淀进 `cairn/<topic>.md`。

## 2026-11-26 · #59 收尾：**更正** BRPIFS 20 → 44 µs；通知 fmcw_radar FCC 23-35 第 62 段（feat/issue59-jcas60）

- 用户对照标准确认 BRPIFS = 44 µs。`dmg.phy_timing#brpifs_s` 2.0e-05 → 4.4e-05。公开出处：TGad 12/0020r19 SB001 对 D5.0 的 CID 6297（"no later than a BRPIFS (44 us)"）、TGay 17/0418r1 slide 10（"SIFS=3 us; BRPIFS=44 us"）。两段引文逐字核过，quote 去掉 0433r2 Table 90 的 "aBRPIFS 20usec"。
- **更正（修正 #33 的判断）**：#33 记 20 µs，#33、#43 用户两次核对 `phy_timing` 都没指出，#59 复核时先回"核对 OK"，单问这一格才改。0433r2 已四处被证实是旧版（STF、AGC、Golay 128 / 64、BRPIFS）。
- 谁受影响：jcas60 读 `brpifs_s`（`bf.py:57`、对照表里是 2e-05）；mmw60_trx 只读 `sbifs_s`、`control_preamble_s`。
- L-STF：按 jcas60 的取材限制答"没有查到"，并入 ROADMAP"其余待办"里 #48 那条。
- fmcw_radar#46：FCC 23-35 第 62 段要求实测占用带宽（§2.1049，99 % 功率；Valeo 意见含过冲与回扫）；它的 `compliance.py` 取指令扫频，影响判档与 61–61.5 GHz 档的 500 MHz 上限。
- **更正（下条的膝部对照）**：P1dB + 3 dB 处单点对 Rapp（p = 1 / 2 / 3 → 1.81 / 2.61 / 3.17 dB），A 压缩 1.69 dB、等效 p ≈ 0.86，B 2.22 dB、p ≈ 1.48；下条写的"都更像 p ≈ 1–1.8"偏粗，A 比 p = 1 还缓。
- 共享表仍 187 条；199 个测试（197 通过，2 跳过）。

## 2026-11-26 · #59：接收机压缩曲线、长 Golay 对、BRP 帧；更正双站 PPDU 的间隔（feat/issue59-jcas60）

- 两个子代理分读：接收机压缩（arXiv、OSTI、英飞凌 / TI 数据手册；MDPI 与 TU/e 被站点挡住）与 BRP 帧（TGad / TGay / TGbf 的 mentor 文件）。本库回原文核了文中数、两张图（看过原图，读数与图一致）、0327r1 的 SIFS 句、TGad CID 1097 的 18 块、18/0400r0、0433r2 9.6.0f。
- 压缩：A（22 nm FDSOI，57.25 GHz）IP1dB −21.8，P1dB+3 dB 处压缩 1.68 dB；B（45 nm SOI，67 GHz）IP1dB −21.5，P1dB+3 处 2.22 dB；按 Rapp 对照（p = 1 / 2 / 3 时 1.81 / 2.61 / 3.17 dB），两条都更像 p ≈ 1–1.8。BGT60TR13C：RX P1dB −10 / −5 dBm，TX→RX 隔离 50 dB（不含封装）。
- 长 Golay 对：W_256、W_512 由穷举唯一确定，与 SFD Table 30、17/0430r0 新 Table 2 一致。
- 更正：#57 的 `spacing` 只写 BRPIFS；同一方连发是 SIFS。子代理报的 BRP Sensing 元素"CID 514 去掉 UID/AID"与 0947r3 原文对不上，本库只按用户的标准核对保留 8 字节，note 写明。
- 共享表 183 → 187；198 个测试（196 通过）。L-STF 的构成与 BRPIFS（20 还是 44 µs）待用户。

## 2026-11-26 · 验收 jcas60 的 #57 重新 pin；**更正**三次指纹复核的录法（feat/issue59-jcas60）

- PR #58 合并（main `3a6e190`）。jcas60 在 #5 合并 `f54dc21`，重新 pin 是分支上的 `ab7a81e`（父 `5739fba`）：6 个文件去头后与 `3a6e190` 逐字节相同，`vendor_check --strict` 16 verbatim，表 96 → 98、未核实 1；指纹 993 个值里 284 个变（都是用到 Golay 码片的量），与它报的一致。它关了 #57，开了 #59（4 问）。
- **更正（修正 #48、#50、#54 验收时的判断）**：三个库的 `fingerprint.py` 都把自己所在仓库的 `src` 插到 `sys.path` 前面；那三次本库拿父提交的工具录另一个目录，录到的仍是父提交，"逐位相同"没有测到重新 pin。这次同样录法给出 0 个变、与 jcas60 的 284 不符才查出。各用自己的工具重做：mmw60 #48 69 个相同，fmcw #50 2153 个相同，jcas60 #54 507 个相同；结论不变。
- #59 进行中：Golay 256 / 512（SFD 与 17/0430r0 的 D / W，递推等于 SFD 的表，W 唯一）已查到；L-STF 只查到"15 改 17 段"（TGad 10/1291r2 CID 508），组成没有查到；压缩曲线与 BRP 帧在读。

## 2026-11-25 · #57：更正 DMG Golay 表；EDMG TRN 细节、双站 PPDU；验收 jcas60 的 #54 重新 pin（feat/issue57-trn-bistatic-golay）

- PR #56 合并（main `0d17de6`）。jcas60 在 #3 重新 pin（`abb216d`），本库拆出重新 pin 单独核：507 个指纹值相同，6 个文件逐字节相同，表 89 → 96；它关了 #54，又开 #57（4 问）。
- **更正（修正 #48 的判断）**：查第 1 流的 Golay 对时，TGay SFD 15/1358r9 6.10.2 与 17/0430r0 写 i = 1 的 Ga128 / Gb128、Ga64 / Gb64 等于 DMG 的，但其 D / W（[1 8 2 4 16 32 64] / [−1 −1 −1 −1 +1 −1 −1]；[2 1 4 8 16 32] / [+1 +1 −1 −1 +1 −1]）生成的序列与本库（0433r2）的表各有 64 / 32 位不同；SFD 的四张表与其递推逐位相同。用户对照标准确认是 SFD 版。#48 记的"六张表与递推一致、用户核对一致"对 0433r2 自身成立，但 0433r2 是旧版。Ga32 / Gb32 无公开定稿、用户未核，拆成 `dmg.golay_sequences_32`（survey）。
- #57：i = 1 的 Golay 对就是 DMG 的；TRN 用旋转 π/2-BPSK，n 的起点原文没有；单站的 TRN 类型没有限定，协调单站有 PSDU（RA = TA），任意波形的条件针对整个 TRN 场；新建 `ieee80211bf.dmg_bistatic_ppdu`。
- 共享表 181 → 183（spec 165、survey 2）；195 个测试（193 通过，2 跳过）。

## 2026-11-25 · #54 第二部分：802.11bf 的 60 GHz 感知、DMG / EDMG 的 TRN 场（feat/issue54-bf-sensing）

- PR #55 合并（main `14e84fd`），在 #54 答了第一部分。第一组读 TGbf 公开文件：两个子代理分读 PPDU / TRN 与流程（转写的文件分别 115、138 份），本库回原文抽查了约 40 句关键句，全部在原文里，条目的每段引文再由生成脚本逐段核对；动议号从两份动议汇编核对。
- 列 S1–S7 请用户对照 802.11bf 与 802.11-2024 核对：都一致。
- DMG TRN：4 × 320 + 1152 + 4 × 640 = 4992，与 `dmg.sc_ppdu_chips` 闭合；CE 段就是 SC 包的 CEF。0433r2 的 AGC 是 4 个 Ga64（4736），旧版。EDMG TRN：6 × TRN_BL × N_TRN，单链 128 时 768；Sync 子字段 18 × 128 = 2304。
- 调度：Interburst / Intraburst 的字节数在 D0.3 是 1 / 2、SA 投票对调成 2 / 1，单位由 TSF units 改为 µs（CID 6108、6109）；按字节数推上限 65 535 µs / 255 µs，原文没写范围。
- 7 条新 spec，前缀 ieee80211bf 新登记；共享表 174 → 181（spec 157 → 164）；3 个新测试，两处改符号的变异都能抓到。195 个测试（193 通过，2 跳过）。

## 2026-11-25 · #54 第一部分：登记 jcas60、P.676 加 60.48 GHz、§15.255 的答复（feat/issue54-jcas60-part1）

- fmcw 在 11-18 关了 #50。新库 jcas60（60 GHz 通感一体）开 #54：802.11bf 的 DMG / EDMG 感知条目；通信设备顺带感知时 §15.255 适用哪一款；60.48 GHz 的氧气衰减。它的里程碑 0（`8cb40e0`）已按 `f9ce3f2` vendor 6 个文件。
- 复核：6 个文件去头后与 `f9ce3f2` 逐字节相同；本地 `vendor_check --strict` spec_sources 全 verbatim；它的表 89 条、未核实 0。登记进 `vendored:`。
- 60.48 GHz：14.9925 → 14.993 dB/km（itur 一致）。
- 法规：环境放行了 docs.fcc.gov、www.fcc.gov、apps.fcc.gov、www.federalregister.gov。FR 全文页跳反爬页读不到，改读 FCC 23-35 原件（41 页）。条文与 R&O 都没有"既通信又感知"的说法；KDB 检索页 503。
- 802.11bf：TGbf 清单 3105 个文件（2247 个 00bf），DMG 相关的约 110 个；两个子代理分读 PPDU / TRN 与流程，待核对。

## 2026-11-18 · 验收 #50：fmcw_radar 重新 pin 到 18241cd 并接入合规检查（feat/accept-issue50-fmcw）

- PR #52 合并（main `18241cd`），在 #50 给了 PIN 与六个答复。fmcw_radar 先在 #26 单独重新 pin（`036bb9b`，父 `8bd37e4`），再在 #27 接入（`5ffbafd`）。
- 复核：7 个登记文件去头后与 `18241cd` 逐字节相同；本地 `vendor_check --strict` spec_sources 7 verbatim（26 缺 sibling 跳过）；指纹 `8bd37e4` 对 `036bb9b`（同一工具）2153 个值逐位相同，`036bb9b` 对 `5ffbafd` 原有 2153 个不变、新增 247 个全是 `compliance.*`；它的表 23 → 37 条。
- 它的 `upstream:` 读 44 个 `fcc15255.*` 数，与本库值和类型都相同；按条登记，fmcw_radar 登记 14 → 58。固定件换成 `5ffbafd` 的表。
- 它的结果：默认 22 dBm 超 `radar_57_64` 的 14 dBm 8.0 dB；帧周期至少 31.90 ms。它问关断被窗口截断时的计法，记进 ROADMAP（条文没写）。

## 2026-11-18 · #50：47 CFR §15.255(c)(2) 的雷达各档（feat/issue50-fcc15255-radar，未发布）

- PR #51 合并（main `e86bd88`）后 mmw60 关了 #48；#43 在 11-17 就关了。fmcw_radar 开了 #50：它默认扫 58–62 GHz、EIRP 22 dBm，没有上限检查。
- 读 eCFR 现行条文（2026-11-16 版，该节修订仍是 2023-08-23，与 11-16 读的逐字节相同；API 现在要求压缩，curl 加 --compressed）与 §15.3 定义。建 10 条 spec：默认 10 dBm（传导 −10）、57–59.4 室内 20 / 室外 30、57–61.56 为 3 或（关断 ≥ 16.5 ms）20、57–64 为 14（关断 ≥ 25.5 ms，必须）或室外固定 / 车载 20（≥ 16.5 ms）、61.0–61.5 平均 40 / 峰值 43（档外 10 / 13）、无人机 60–64 为 20（≤ 121.92 m）、换档至少停 33 ms。
- 原文比 ROADMAP 转述多出：每段关断须连续 ≥ 2 ms、14 dBm 档没有降功率分支、室外档车厢内除外、61 GHz 档的 ≤ 500 MHz 条件与档外限值、(b)(3)、(c)(2)(iv)。§15.3 没有室内 / 室外 / 固定 / 车载的定义。
- 每段 quote 用脚本对过原文；新测试把每档的频段边界与 dBm 限值对回自己的 quote（14 改 15 即失败）。共享表 164 → 174（spec 147 → 157）；测试 103 个（101 通过，2 跳过）。

## 2026-11-18 · 验收 #48：mmw60_trx 重新 pin 到 65ff5e4（feat/accept-issue48-repin）

- PR #49 合并（main `65ff5e4`），在 #48 给了 PIN。mmw60_trx 在 #76 合并 `147ef1d`（父提交 `f547d8d`），重新 pin 与它的 OFDM 接收机改动在同一个提交里。
- 复核：9 个文件去头后与 `65ff5e4` 逐字节相同；本地 `vendor_check --strict` 9 verbatim（108 缺 sibling 跳过）；指纹：`f547d8d` 对"`f547d8d` + `147ef1d` 的 vendor 文件"，同一个 `fingerprint.py`，69 个值逐位相同；合并表 208 → 214、未核实 4。
- 它用上了 EDMG-STF / EDMG-CEF（`ay/training.py`，按键读）；OFDM 比 SC 门限多出的量平均 0.84 → 0.19 dB（换训练场单项：13 dB 理想链 EVM 多丢 0.79 → 0.65 dB）。hFilt、DMG CEF、Golay 这轮没用。
- `consumers.yaml`：mmw60_trx pin → `65ff5e4`、at `147ef1d`、issue mmw60_trx#76。数据未动，共享表 164 条。

## 2026-11-18 · #48：EDMG OFDM 包的训练场、DMG CEF 拼法、hFilt、Golay 序列（feat/issue48-ofdm-training，未发布）

- mmw60 开了 #48（4 项），先问 EDMG OFDM 包的数据用哪个场估信道。读 mentor 公开文件：17/1806r3 30.12.3.4（TXTIME）、17/0596r0（EDMG-CEF，动议 #219）、17/0546r0（EDMG-STF，动议 #209）、0433r2 21.3.6 / 21.9。列 N1–N6 请用户对照标准核对，一致；用户另外确认：标准明写数据信道用 EDMG-CEF 估，EDMG OFDM 包的 L-CEF 用 OFDM 排法（两句公开文件里没有，写进 note）。
- 单流 EDMG OFDM 包：1.76 GHz 段 2176 + 1152 + 1024 + 1088 码片；2.64 GHz 段 EDMG-STF 3840 样点（30 × 128 = 1.4545 µs）、EDMG-CEF 2 × 704 = 1408 样点（P = [+1, −1]，长 GI 192）。
- CEF 非零音 352 = 355 − 3，模都为 1；STF 非零 88 个，全在 4 的倍数号音上。Golay 递推按 0 ≤ n < 2^K 截断算再倒过来，六张表逐位相等，三对非周期互补；Gu512 / Gv512 只周期互补（循环自相关和只在零延迟 = 1024）。hFilt 73 抽头、对称、h36 = 256，整数范数 428.679，多相和 246 / 244 / 244。
- 0433r2 的 CEF 波形式里 Gu、Gv 带上标 R，定义式与图 134 / 135 不带，按后者记。原文"n ≥ 2^k 时为 0"只对最后一级成立（D_1 = 64）。
- 6 条新 spec，共享表 158 → 164（spec 141 → 147）；4 个新测试，102 个（100 通过，2 跳过）。mmw60 需重新 pin。

## 2026-11-17 · 验收 ρ = 2 更正的重新 pin：mmw60_trx#70（feat/accept-rho2-repin）

- PR #46 合并（main `25b2c5e`），在 #43 贴了原句、给了 PIN。mmw60_trx 在 #70 合并 `d27046b`（父提交 `4d1a06b`）。
- 复核：9 个文件去头后与 `25b2c5e` 逐字节相同；本地 `vendor_check --strict` 9 verbatim（241 缺 sibling 跳过）；指纹 `4d1a06b` 对 `d27046b` 69 个值逐位相同；合并表 208、未核实 4；`sc_rho2_codeword` 读得到。
- 它建了 SC MCS 1 的重复码：门限 −1.23 dB（原来借 DMG 灵敏度推的 −1.48 dB 偏乐观 0.25 dB）；4096 字节 196 个码字（本地复算一致）；PN 前 16 位 0000111011110010。
- `consumers.yaml`：mmw60_trx pin → `25b2c5e`、at `d27046b`、issue mmw60_trx#70。数据未动，共享表 158 条。

## 2026-11-17 · 更正 `dmg.data_encoding` 的 ρ = 2（feat/data-encoding-rho2）

- PR #45 合并（main `5ae7a38`）。mmw60 在 #43 追问 SC MCS 1 的码字。0433r2 21.6.3.2.2 的 ρ = 2 一段（公式图 image177–185 渲染出来读）：L_Z = L_CW/2ρ = 168，c = (b, 168 个零, p_1…p_336)，"Replace bits L_Z + 1 though 336 … XOR'ed by a PN sequence … LFSR used for data scrambling … initialized to the all ones vector and reinitialized … after every codeword"。
- 本库 #33 的 note 写成换"校验后半段"，读错了：换的是补的零。用户核对标准一致（M1）。
- 改 note，加 `sc_rho2_codeword`、`sc_rho2_pn`；新测试：1/2 码 H（336 × 672）后 336 列满秩，随机数据编出的 (数据, 零, 校验) 满足 H·cᵀ = 0。
- 数据值不变，共享表 158 条；测试 98 个（96 通过，2 跳过）。mmw60 需再 pin。

## 2026-11-17 · 验收 #43：mmw60_trx 重新 pin 到 563cff4（feat/accept-issue43）

- PR #44 合并（main `563cff4`），在 #43 给了 PIN。mmw60_trx 在 mmw60_trx#67 合并 `636208a`（pin 的提交 `6781b81`）。
- 复核：9 个文件去头后与 `563cff4` 逐字节相同（`6781b81`、`52449b6` 都是）；本地 `vendor_check --strict` 9 verbatim（241 缺 sibling 跳过）；指纹 `24f0d35` 对 `6781b81` 69 个值逐位相同（它报 68，数法不同）。合并表 203 → 208，未核实 4。
- 它按码字切分算 SSW 帧：12.582 → 14.909 µs（本地复算一致）；N = 64 一轮扫描 1738.5 → 2036.4 µs。DCM 静态配对已用上（#68）。
- 它追问 ρ = 2 的码字：本库 `dmg.data_encoding` 的 note 读错了（写成换校验后半段，原文换的是补零的第 169–336 位）。等用户核对后另改。
- `consumers.yaml`：mmw60_trx pin → `563cff4`、at `636208a`、issue mmw60_trx#67。数据未动，共享表 158 条。

## 2026-11-17 · #43：控制 PHY 的码字、EDMG 前导、OFDM 调制映射；更正 #33 的三条（feat/issue43-cphy-edmg-ofdm，未发布）

- PR #42 合并（main `30a4db1`）。mmw60 开了 #43（4 项）。读 mentor 的公开文件，列 L1–L11 请用户对照标准核对：后来的文件与标准一致。
- 更正：`dmg.control_phy` STF 5120 → 6400 码片；`dmg.phy_timing` 前导 1745 / 3564 → 1891 / 4291 ns；`edmg.short_ssw` Packet Type 2 → 1、RF Chain ID 2 → 3 位，单播 11 位改为 SS-BSSID 10 + Unassociated 1，新增群播格式。#33 时取自 0433r2（2010）与 1358r9（2015），当时标的"核对一致"没覆盖这几处。
- 新增 5 条：`dmg.control_phy_encoding`（88 位 + 168 位 / 码字，Length 120 → 7 个码字；SSW 帧 14.909 µs）、`dmg.sc_ppdu_chips`（2176 / 1152 / 1024）、`edmg.sc_siso_preamble`（SISO 无 EDMG-STF / CEF）、`edmg.control_mode_encoding`、`edmg.ofdm_modulation_mapping`（DCM 矩阵、STP / DTP 42 组、16 / 64-QAM）。
- 互证：17/1586r1 的 48 位例子用新位宽低位在前逐字段拆回（旧位宽拆不回）；码字切分对 14–1023 每个 Length 都等于闭式。3 个新测试。
- 没有：Short SSW 的 PPDU 类型；OFDM 16 / 64-QAM 交织置换；OFDM 填充。
- 共享表 153 → 158 条：spec 141、survey 1、derived 16。测试 97 个（95 通过，2 跳过）。mmw60 需重新 pin。

## 2026-11-17 · 验收 0.6.0 的重新 pin：mmw60_trx#63、fmcw_radar#21（feat/accept-0.6.0-repins）

- PR #41 合并即 0.6.0（main `a9af261`），在 mmw60_trx#63、fmcw_radar#21 各给了 PIN。
- mmw60：合并 `bd0b125`（pin 的提交 `1a70205`）。9 个文件去头后与 `a9af261` 逐字节相同；本地 `vendor_check --strict` 9 verbatim（241 缺 sibling 跳过）；指纹 `64bea53` 对 `1a70205` 69 个值逐位相同。合并表 193 → 202（vendor +7，它本地 assumed +2，与 pin 同一提交），未核实 9 → 4。
- mmw60 定了两件：ISCAS 2015 作双边带、另列单边带一行（本地 assumed 3 dB）；Asada [5] 的 PAE 剔掉（示例 09 中位数 8.5 → 8.8 %）。两条 assumed 只记 3 dB 与行号，不抄本库的数，不按条登记。
- fmcw：合并 `49c1e76`。6 个文件去头后逐字节相同，`vendor_check` 里都是 verbatim（唯一的 adapted 是 array_tx 的 coupling.py）；指纹 `4495310` 对 `49c1e76` 2035 个值逐位相同。
- `consumers.yaml` 两库 pin → `a9af261`。数据未动，共享表 153 条；测试 94 个（92 通过，2 跳过）。

## 2026-11-17 · 发布 0.6.0（feat/release-0.6.0）

- PR #40 合并（main `cca7a21`）。用户定：先发 0.6.0，再给 mmw60_trx、fmcw_radar 各开一个重新 pin 的 issue。
- 0.6.0 收进 0.5.0 之后的：第 7 批（#34）、#33 的 12 条与 `phy_timing` 修正（#35、#36，mmw60 已验收）、DeepScaleTool（#39）、Xplore 原文 10 篇（#40）。共享表 133 → 153 条（spec 104 → 136，survey 17 → 1，derived 12 → 16）。
- 改了 `__init__.py` 与 `pyproject.toml` 的版本号；CHANGELOG"未发布"改成 0.6.0，头部几条重写成发版说明；`keys.lock` 20 个键 `added=unreleased` → `added=0.6.0`（只换键行）。
- mmw60_trx（`__init__.py`、energy、frontend60、pa60）与 fmcw_radar（frontend60）要重新 pin；d2d_link 不用。

## 2026-11-17 · 10 篇 IEEE Xplore 原文：survey 5 → 1（feat/xplore-batch，未发布）

- PR #39 合并（main `4863ff0`）。用户上传 10 篇 Xplore 原文；与上一轮"不发原文"相反，先停下来问，用户确认其许可允许。读完删本地副本。
- Horowitz ISSCC 2014 Fig. 1.1.9（渲染）：32 位整数乘 3.1、加 0.1 pJ（45 nm、0.9 V）→ 两条改 spec。
- ISCAS 2015（Luo 等，清华）：NF 7.1、增益 64、调节 28、OP1dB −5.5、177 mW 全对 → spec；7.1 是三信道最小的双边带 NF。Okada JSSC 2013：收发天线各 6.0 dBi → spec。
- Asada 表后 6 行新建 6 条：[7] [10] [12] [14] 四格全对；[8] 增益 4.4 是 S21（表 4.2）；[14] 5.5 是图注（正文 5.6）；[5] 无 PAE、电压 1.2 V（Asada 写 5.0 %、1.0 V）。13 行 P1dB、Psat 全对。
- Das Sharma CPMT 2022：标准封装降宽、高级封装每 32 条 2 个备用，没有 x8 → `ucie.standard.lane_repair` 仍 survey，`ucie.yaml` 不动（免得 d2d 为一句 note 重新 pin）。
- 共享表 147 → 153 条：spec 136、survey 1、derived 16。测试 94 个（92 通过，2 跳过）。mmw60（energy / frontend60 / pa60）、fmcw（frontend60）需重新 pin。

## 2026-11-16 · DeepScaleTool：读 arXiv 预印本与工具原文件（feat/deepscale-tool，未发布）

- PR #38 合并（main `a1da0f8`）。用户定按默认做：不发 Xplore 原文；DeepScaleTool 读 arXiv，其余列 Xplore 地址给用户核对。
- arXiv:2102.10195v1（CC BY 4.0）正文没有 45 → 7 nm 的能量比，只有例子（130 → 45 nm 面积 8.3、45 → 32 nm 功耗 1.238）。工具 `DeepScaleTool.xlsm`（SourceForge，GPLv3）的 `Sub Energy()` 是查表：各节点相对能量（65 nm = 1），45 nm 0.63、7 nm 0.11，倍数 = 两格之比（显示 3 位）。宏里另算的二次式没被写回单元格。
- 互证：Fig. 2 截图 130 → 45 nm 能量 4 = 2.52 / 0.63；存档单元格 90 → 32 nm 3.432 = 1.51 / 0.44；Fig. 3 读图 7 / 45 nm 约 0.18。
- 新建 `deepscale.energy_by_node`（spec）；`deepscale.node_scale_45_to_7nm` 改 derived：0.11 / 0.63 = 0.17460 → 0.1746（迁入 0.175，CORRECTED，−0.23 %）。
- 共享表 146 → 147 条：spec 126、survey 5、derived 16。测试 94 个（92 通过，2 跳过）。mmw60 需重新 pin（`energy.yaml`）。

## 2026-11-16 · IEEE Xplore 的许可：删掉本地 12 篇 Xplore 原文（feat/xplore-licence）

- PR #37 合并（main `b16245a`），#33 验收留言已发。
- 要请用户下载剩下几篇前查许可：搜索结果一致说 IEEE Xplore 的条款限制 AI（不得上传给 AI 工具、不得存放在 AI 工具里；机构订阅许简短引用，有的机构协议许做摘要）。条款原文没读到（条款页 418，图书馆转述页不在白名单）。
- 用户定：删。删了 12 篇（Asada 表 7 篇、Wu、Staszewski、Henzler、Harris、Liu 刊出版）在 `cairn/Reference/` 的 PDF、会话上传目录的原件、scratchpad 的 6 个渲染 / 抽字目录；按 sha256 复查容器里没有剩下。git 从没跟踪过它们。由它们建的条目不动。
- 剩下标 📥 的 11 篇都在 Xplore 上，不再请用户下载；取法待用户定。DeepScaleTool 有 arXiv 2102.10195 与 GPLv3 工具，不经 Xplore。
- 只改了文档：`cairn/Reference/README.md` 末节（只追加）、ROADMAP 三处。数据未动，共享表 146 条。

## 2026-11-16 · 验收 #33：mmw60_trx 重新 pin 到 76ee72a（feat/accept-issue33）

- PR #36 合并（main `76ee72a`），在 #33 给了 PIN，一次 pin 齐 0.5.0、第 7 批与 #33 的 12 条。mmw60_trx 在 mmw60_trx#60 合并 `53a9a16`（pin 的提交 `3ea11be`），接线在 #61（`50f30df`）。
- 复核：9 个 vendor 文件去两行头后与 `76ee72a` 逐字节相同（`3ea11be`、`50f30df` 都是）；本地 `vendor_check --strict` 9 个 verbatim（241 个因缺 sibling 跳过）。指纹 `23d0130` 对 `3ea11be` 69 个值逐位相同（`MMW60_NO_JIT=1`）。合并表 180 → 193，未核实 20 → 9。
- 动的数只在功耗列（指纹不覆盖）：ADC 功耗 ×1.0116，它报 pJ/bit 涨 0.1–1 %（同台表最好一行 592 → 596）。
- #61 按键读新条目，本地表没抄数，不按条登记。它的注释记了控制 PHY 的码字切分规则与 EDMG PPDU 前导长度本库没有（扫描时长取下限），记进 ROADMAP。
- **更正**：#33 回复里写它 vendor 的文件 survey "14 → 3"，漏了 `frontend60.yaml` 的 2 条，应为 16 → 5（少 11 条不变）。
- `consumers.yaml`：mmw60_trx pin `3123b65` → `76ee72a`、at `53a9a16`，文件仍是 9 个；issue 一栏写 mmw60_trx#60。数据未动，共享表 146 条。

## 2026-11-16 · `dmg.phy_timing` 的 5 个时间常数被读成字符串（feat/phy-timing-floats，未发布）

- PR #35 合并（main `af582c1`）。给 mmw60 写 PIN 前逐键打印新条目，发现 `rifs_s`、`sifs_s`、`sbifs_s`、`brpifs_s`、`slot_s` 读出来是 `'1e-06'` 这样的字符串：PyYAML 按 YAML 1.1 解析，指数式没有小数点就不算浮点数。`data_preamble_s: 1.745e-06` 有小数点，没事。
- 改写成 `1.0e-06`、`3.0e-06`、`2.0e-05`，值不变。全表扫一遍，别处没有这种写法（`'8.6'` 这类是有意加引号的论文号，`edmg.sc_encoding` 的 `"624/672"` 照原文成文本）。
- 新测试 `test_no_number_in_exponent_form_was_read_as_text`：旧数据上失败（5 处），改后通过。测试 94 个（92 通过，2 跳过）。条目数不变，仍 146。
- 键还没发布（`added=unreleased`），没有消费方读过它们，不用登记；mmw60 的 PIN 等这个合并后再给。

## 2026-11-16 · #33：DMG / EDMG 的 LDPC、编码、扩展 MCS、控制 PHY 与扇区扫描（feat/issue33-ldpc-ctrl-ssw，未发布）

- PR #34 合并（main `559639f`）。mmw60 开了 #33（4 项）。用户定按 3 → 4 → 1 → 2 做，mmw60 的重新 pin 并进 #33 的回复。
- 来源：TGad 0433r2（LDPC 表从 docx 逐格取；SC / OFDM 填充公式是 wmf 图，渲染出来读）、REVmc 16/0233r0、TGay SFD 15/1358r9、16/1495r1、17/1061r1、17/0214r1。用户核对 K1–K11 一致。
- 12 条：DMG 基矩阵 4 张（Z = 42）、编码（x⁷ + x⁴ + 1；N_CW、N_BLKS 等）、扩展 SC MCS 7 档（2695–8085 Mb/s）、7/8 打孔（624 / 546）、控制 PHY（5120 + 1152 码片，27.5 Mb/s derived）、时间常数（SBIFS 1 µs、BRPIFS 20 µs）、SSW 26 字节；EDMG 672 位 7/8、1344 提升矩阵 5 张、SC 编码、Short SSW 48 位。
- 互证：提升矩阵的 -1 与 DMG 零块逐格相同；672 位 7/8 = 3/4 矩阵第 1+3、2+4 行之和（新测试守着）。
- 没有：EDMG 灵敏度（再搜一轮仍无）、EDMG OFDM 填充、BRP / TRN 单元长度。
- 共享表 134 → 146 条：spec 125、survey 6、derived 15。测试 93 个（91 通过，2 跳过）。

## 2026-11-16 · 第 7 批：能用公开材料核的 11 条（feat/batch7-public-sources，未发布）

- PR #32 合并即 0.5.0（main `6ad42bf`）。用户同意：mmw60 的重新 pin issue 等这一批合并后一起开。
- eCFR（放行 www.ecfr.gov）：§15.255 现行条文，`fcc15255.*` 4 条 → spec；迁入 cite 的 "(a)" 改为节标题 / (c)，(c)(1)(i) 40 / 43 dBm。(c)(2) 雷达限值记进 ROADMAP。
- arXiv v1：`liu2025.per_target` → spec。更正：`liu2025.k_threshold` 的 note 原说 arXiv 只写 1250 KHz，v1 其实写了 4 × 312.5 KHz。
- mentor 公开文件：TGn 11-05/1102r4、TGac 09/0992r21、TGax 15/0330r5 与 15/0132r17、TGbe 19/1262r23 → 802.11 的 4 条 → spec，用户核对一致（G1–G4）。
- Murmann ADC survey（GitHub，00b4b85）：6 行 TI-SAR 新建 spec；`walden_fom_fj` 70 → 70.815、区间 [38.4, 120.2] → [38.36, 120.19]，改为 derived（CORRECTED 允许 derived）。
- Okada JSSC 2013：实验室网站只有题录，归入要下载的。剩 6 条 survey 都要用户下载：Horowitz、ISCAS 2015、Okada、DeepScaleTool。
- 共享表 133 → 134 条：spec 114、survey 6、derived 14。测试 92 个（90 通过，2 跳过）。mmw60 需重新 pin。

## 2026-11-16 · 发布 0.5.0（feat/release-0.5.0）

- PR #31 已合并（main `bebefc5`）。用户定：按顺序做——先发版，再做第 7 批，最后是要下载原文的几项。
- 0.5.0 收进 0.4.0 之后的：第 4 批完（车辆、角反射器、窗函数，fmcw #19 验收）、#26（Liu 刊出版与 tg3c，mmw60 验收）、#29（dmg / edmg，mmw60 验收）。共享表 102 → 133 条（spec 53 → 104，survey 40 → 17，derived 9 → 12）。
- 改了 `__init__.py` 与 `pyproject.toml` 的版本号；CHANGELOG"未发布"一节改成 0.5.0；`keys.lock` 31 个键 `added=unreleased` → `added=0.5.0`（只换键行，文件头说明不动）。
- 只有 mmw60_trx 要为 0.5.0 重新 pin（只有 `__init__.py`）；fmcw、d2d 的文件在各自 pin 之后没动。
- 测试 92 个（90 通过，2 跳过）。

## 2026-11-16 · 验收 #29：mmw60_trx 重新 pin 到 3123b65（feat/accept-issue29）

- PR #30 合并（main `3123b65`），在 #29 给了新 PIN。mmw60_trx 在 mmw60_trx#49 合并 `29eb6fe`（pin 的提交 `2400c5b`，只做 pin）。
- 复核：9 个 vendor 文件去两行头后与 `3123b65` 逐字节相同；本地 `vendor_check --strict` 9 个 verbatim（241 个因缺 sibling 跳过）。指纹 `e662238` 对 `2400c5b` 69 个值逐位相同（`MMW60_NO_JIT=1`）。合并表 157 → 171，未核实 22 → 20。
- 它手算核了 Δf、子载波数、GI 样本数、两档速率、DC 偏移步长 0.46875 MHz；示例 08 只有一个标签变化。EDMG 灵敏度它第一轮不用。
- `consumers.yaml`：mmw60_trx pin `7aae876` → `3123b65`、at `29eb6fe`，文件仍是 9 个；issue 一栏写 mmw60_trx#49（请求在本库 #29）。数据未动，共享表 133 条；测试 92 个（90 通过，2 跳过）。

## 2026-11-16 · #29：802.11ad / ay 单信道 PHY 的数，从公开提案建（feat/issue29-dmg-edmg，未发布）

- mmw60_trx 开了 #29。用户下载 IEEE 802.11-2024 后发现许可禁止输入 AI → 不读标准；改读 mentor 上 TGad / TGay 的公开提案与 R&S 1MA220（放行 scdn.rohde-schwarz.com，用户批准），列成 A–E 五组请用户对照标准核对：全部一致。
- 出处：TGad 11-10/0433r2（采纳的规范文本）；R&S 1MA220_3e Table 4-1（引 802.11-2016）；TGay 11-17/0597r1（动议 #208）、0628r1（#220）、0909r0（#262）、11-15/1358r9（SFD）、11-18/0713r3（#451）、1152r0（#489），动议号读自 11-17/0186r37。
- 新增 14 条：`dmg.*` 5 条（参数、SC / OFDM MCS、EVM、灵敏度）、`edmg.*` 9 条（OFDM 参数、导频位置与值、OFDM MCS 20 档、SC 参数、SC MCS 21 档、两种变体，2 张速率表为 derived）。速率复算：OFDM MCS 1 = 792.00 / 729.47 / 630.00 Mbps，SC MCS 21 = 8662.50 / 8085.00 / 6930.00，与提案印的逐档相符。
- 改成 spec（值不变）：`ieee80211ay.channel_centres_ghz`、`dmg.sensitivity_assumptions`（10 dB NF、5 dB 实现损耗，一手原句）。
- 发现：2010 提案的 SC EVM 后来几乎全改（MCS 2 −9 → −7 …），OFDM 22 / 24 改为 −22 / −26；灵敏度只差 MCS 2（−67 → −66）。EDMG 的 MCS 表在 TGay 里改过两次。EDMG 灵敏度公开材料里没有（CID 1620 的解决只补了 EVM）。
- 共享表 119 → 133 条：spec 104、survey 17、derived 12。测试 92 个（90 通过，2 跳过）。mmw60 需重新 pin。

## 2026-11-15 · 验收 #26：mmw60_trx 重新 pin 到 7aae876（feat/accept-issue26）

- PR #27 合并（main `7aae876`），在 #26 给了新 PIN。mmw60_trx 在 mmw60_trx#37 合并 `121b612`（重新 pin 的提交 `4d018e5`），回帖在 #26。
- 复核：9 个 vendor 文件（多了 `ieee802153c.yaml`）去两行头后与 `7aae876` 逐字节相同；本地 `vendor_check --strict` 9 个 verbatim（241 个因缺 sibling 跳过；它带齐 sibling 是 250 verbatim）。指纹 `5e474e7` 对 `4d018e5` 69 个值逐位相同（`MMW60_NO_JIT=1`，两边同有 numba 一项报错）。合并表 147 → 155，未核实 43 → 22。
- 它的两条本地 note 点名 3 个 `tg3c.*` 键，由它的守卫核对；"0396 与 TGad 同一颗 PA"的判断已在它那边撤回并追加更正。
- `consumers.yaml`：mmw60_trx 的 pin `8e5f2e2` → `7aae876`、at `121b612`、文件 8 → 9；issue 一栏写 mmw60_trx#37（请求在本库 #26）。数据未动，共享表 119 条；测试 92 个（90 通过，2 跳过）。

## 2026-11-15 · #26：Liu 2025 刊出版与 802.15-06-0477 / 0396（feat/issue26-liu-journal-tg3c，未发布）

- mmw60_trx 在本库开了 #26。用户从 Xplore 下载刊出版（7 页）；两份 802.15 文件从 mentor.ieee.org 取（17 页、15 页）。公式页与两张表渲染出来读；引文逐段对过文字层（× 是 Symbol 字体的私用码，渲染为 ×）。
- `liu2025.*` 29 条：18 条 VERIFIED（值不变）；3 条 CORRECTED：16× 子载波间距 1.25 → 5 MHz、16× 带宽去掉 5120 MHz、receiver 语句改成"CFO 不补偿、接收端做相位跟踪"；per_target 仍 survey（刊出版无那句）；新增 4 条（IDFT 周期 / 点数、两段原文语句）。
- `tg3c.*` 4 条：相噪模型 −87 dBc/Hz、1 MHz、100 MHz（PSD(∞) 按式 −127）；示例档 −96 / −93 / −90 / −87；修正 Rapp 只有公式；NEC GaAs PA 的 Ghorbani 参数与输入 P1dB −11 dBm。
- 发现：0396 印的 Ghorbani 公式分子缺指数（照印的算 u = 0.3 V 时 AM-PM −644°，加上指数 −17.4°、AM-AM 1.43 V，与图符）。mmw60 猜 TGad 参数与它同源：不支持（TGad 0.58 V 饱和、+13.9°；NEC 约 1.5 V、−17.4°）。
- 测试机制：`tests/test_extraction.py` 新增 CORRECTED（迁入条目按原文改值：旧值 → 新值）；`test_reader.py` 的未核实示例改用 `liu2025.per_target`。
- 共享表 111 → 119 条：spec 90、survey 19、derived 10。测试 92 个（90 通过，2 跳过）。mmw60 需重新 pin。

## 2026-11-14 · 验收 fmcw_radar#19：最后 6 条 survey 了结（feat/accept-fmcw-19）

- PR #24 合并（main `f87cc9b`），以它为 PIN 开了 fmcw [#19](https://github.com/alexyudragonsword-collab/fmcw_radar/issues/19)。fmcw 回报合并 `4495310`（0.2.13）。
- 复核：6 个 vendor 文件去两行头后与 `f87cc9b` 逐字节相同；`vendor_check --strict` 里 6 个都是 verbatim（本地缺 polar_tx，另 26 个跳过，与本库无关；它自己的环境 36 verbatim、0 skipped）。指纹 `0d32179` 对 `4495310` 本地重跑，2035 个值逐位相同。
- 它的选择：乘用车保持 10.0，标 derived，引 `target_rcs.iso19206_3_car_rear_far_lower_dbsm`（场景都在 15 m 内，ISO 中心在那里只有 4–12 dBsm）；角反射器保持 20 dBsm，改记成自己的 assumed（15.6 cm 三角形；77 GHz 档相当于 13.8 cm），cite 指向 `target_rcs.trihedral_peak`；窗函数 4 条标 spec，值 0.89 / 1.44 / 1.3 / 1.68 与引用逐位相等，"exact" 已改掉。
- 它的表：assumed 25、spec 11、derived 3、survey 0；14 条 `upstream:` 都已登记（新增 5 条）。迁移时它的 14 条 spec / survey：13 条读本库，角反射器归它自己。
- 本库：fixture 换成 `fmcw_radar.sources.4495310.yaml`；`consumers.yaml` 按条登记 9 → 14，fmcw 的 pin `e49979f` → `f87cc9b`、文件加 `data/windows.yaml`；ROADMAP 删掉里程碑 2 第 4 批，其余按批号标。测试 91 个（89 通过，2 跳过）。
- 它记下的后续：RCS 是常数，不随距离、视角、频段变（示例 05 的车 5.3 m，ISO 中心约 4.3 dBsm，低 5.7 dB）。

## 2026-11-14 · 第 4 批完：窗函数，Harris 1978 表 I（feat/m2-batch4-car-corner，未发布）

- 用户下载 Harris, Proc. IEEE 66(1), 1978（33 页，文字层是 OCR）。表 I 在 p. 55，渲染出来读。
- 新文件 `data/windows.yaml`，5 条 spec（`harris1978.rect / hann / hamming / exact_blackman / blackman`），每条是表 I 一整行 10 列。3-dB 宽 0.89 / 1.44 / 1.30 / 1.52 / 1.68 bins。
- 复算（DFT-even，N = 1024，补零到 2^22）：rect 0.886、Hann 1.441、Hamming 1.303 与表相符，其余列也相符（Hamming 扇贝 1.75 对表 1.78）。
- Blackman（0.42 / 0.5 / 0.08）：3-dB 宽 1.644（表 1.68），6-dB 宽 2.299（表 2.35），其余 7 列相符。
- Exact Blackman（7938 / 9240 / 1430 ÷ 18608）：旁瓣 −68.2（表 −51）、相干增益 0.427（表 0.46；原文 p. 64 说相干增益就是 a0）、ENBW 1.694（表 1.57）、3-dB 宽 1.609（表 1.52）。照原文登记，note 写明。
- fmcw 的 4 个本地值 = `ref("harris1978.<窗>#bw_3db_bins")`；它的 Blackman cite 写成 exact，值与代码都是 Blackman。
- 共享表 111 条：spec 61、survey 40、derived 10。测试 81 个（79 通过，2 跳过）。fmcw 的 6 条都有了条目，待开 issue。

## 2026-11-14 · 第 4 批续：乘用车 RCS 与三面角反射器（feat/m2-batch4-car-corner，未发布）

- PR #23 已合并（main `e0540f3`）。用户定先做 fmcw 剩下的 6 条。放行 rosap.ntl.bts.gov、www.osti.gov（用户批准）。
- NHTSA DOT HS 813 648（2025-01，65 页）：76–77 GHz 两颗车载雷达，ISO 19206-3:2021 方法。转引的 ISO 边界：车尾固定角 P_FAR 20 dBsm ± 10、D_FAR 40 m、K_DEC 0.013 dB/m²（5 m 处中心约 4.1）；30 m 一周车尾 2–25、车头 1–19、侧面 13–30。轿车、两厢、MPV、SUV、轻卡都在界内；报告不给单车 RCS。建 2 条 spec、1 条 derived（下界 10 dBsm）。
- fmcw 的乘用车 10 dBsm = 这条带子的下界；中心 20 dBsm。
- Sandia SAND2008-0396（Doerry，57 页）：三角形 4πa⁴/(3λ²)、方形 12πa⁴/λ²、四分之一圆 15.6a⁴/λ²；Table 1 按 16.7 GHz 算得 20.5 / 25.5 / 29.4，表 20.5 / 25.5 / 29.3。建 1 条 spec（只登记公式）。
- **发现**：fmcw 的角反射器"10 cm、60 GHz、约 20 dBsm"按三角形是 12.2 dBsm（77 GHz 14.4），方形才 21.8。
- 4 条窗函数等 Harris 1978（Xplore，DOI 10.1109/PROC.1978.10837）。
- 共享表 106 条：spec 56、survey 40、derived 10。测试 80 个（78 通过，2 跳过）。fmcw 需重新 pin（radar_targets.yaml 变了），等窗函数一起开 issue。

## 2026-11-14 · 验收 mmw60_trx#27；答复 #22（feat/accept-mmw60-27）

- PR #21 合并即 0.4.0（main `8e5f2e2`），以它为 PIN 开了 mmw60 [#27](https://github.com/alexyudragonsword-collab/mmw60_trx/issues/27)。mmw60 回报合并 `5de5b3a`。
- 复核：8 个 vendor 文件与 `8e5f2e2` 逐字节相同（去两行头），`vendor_check --strict` 无 stale；指纹 b16b6a0 对 5de5b3a 69 个值逐位相同（两边同有一项因没装 numba 报错）；`all_entries()` 130 → 137，新增的就是 7 条 `pa60.*`，未核实 42 不变；它的 spec 相关测试 15 过 2 跳过。两处文档只加了说明文字。
- d2d_link 在本库开了 #22，要 `ucie.standard.raw_ber_target@12-32`、`ucie.advanced.raw_ber_target@16-32` = 1e-15，让 28 GT/s 不退回 1e-27。查了教程 slide 53、71、概览篇，2022 / 1.1 / 2.0 / 4.0 白皮书：BER 只按离散速率给，UCIe 速率本身只有 6 档。答复"原文没说，不加"，以 not planned 关闭；建议它若要按邻档判，写成本地 assumed。
- 三个下游库都在最新的相关提交上。数据未动，共享表 102 条；测试 80 个（78 通过，2 跳过）。

## 2026-11-14 · 发布 0.4.0（feat/release-0.4.0）

- PR #20 已合并（main `b59898b`）。用户定：发版，再给 mmw60 开 issue。
- 0.4.0 收进里程碑 2 第 1–4 批（部分）：PA 7 行原文、TDC 3 篇、UCIe 15 条对上联盟公开材料、大气与行人 RCS。共享表 84 → 102 条（spec 23 → 53，survey 55 → 40，derived 6 → 9）。
- 改了 `__init__.py` 与 `pyproject.toml` 的版本号；CHANGELOG"未发布"一节改成 0.4.0；`keys.lock` 18 个键 `added=unreleased` → `added=0.4.0`（文件头说明里的 "added=unreleased" 字样一度被一起换掉，已改回）。
- 只有 mmw60_trx 要为 0.4.0 重新 pin（`__init__.py` 与 `pa60.yaml`）；fmcw、d2d 不 vendor `__init__.py`，它们的文件在各自 pin 之后没动。
- 测试 80 个（78 通过，2 跳过）。

## 2026-11-14 · 验收 d2d_link#2（feat/accept-d2d-2）

- PR #19 已合并（main `bbc0ccb`），以它为 PIN 开了 d2d [#2](https://github.com/alexyudragonsword-collab/d2d_link/issues/2)。d2d 回报：main 从 `0cbd4e9` 快进到 `d5d34a6`（0.17.0），5 个提交。
- 复核：3 个 vendor 文件与 `bbc0ccb` 逐字节相同（去头后）；它的测试 267 过 4 跳过；加载后共享条目 18 条，spec 17、survey 1。
- 指纹逐提交（3597 值，装了 scikit-rf）：`bd1e087`（重新 pin）、`2aefc99`（眼罩标注）、`b129196`（TX 文档）、`d5d34a6`（QDR 显示）都逐位不变；`f868f3c`（BER）动了 974 个，全在统计引擎（眼、BER、采样相位、游标、时域样本），`src/` 只改了垫片 23 行。
- BER 目标逐格查：12 格与 `ucie.raw_ber_by_rate` 相同；5 个 32 GT/s 配置 1e-27 → 1e-15；表外 28 GT/s 退回 1e-27（查表这层不告警，它说告警在引擎层）。
- 它报的余量：32 GT/s 下 x1 +0.091 → +0.205、x16 模块 +0.066 → +0.175、x16 repair +0.028 → +0.144、x64 spare +0.093 → +0.195、x5 耦合 −0.121 → −0.010（仍不过）。
- `consumers.yaml` 里 d2d 的 pin 改为 `bbc0ccb`。共享表仍 102 条，测试 80 个（78 通过，2 跳过）。

## 2026-11-14 · 第 3 批：UCIe 对上联盟公开材料（feat/m2-batch3-ucie，未发布）

- PR #18 已合并（main `e7be6b3`）。用户定 fmcw 暂不换 TDC 抖动。
- **规范不能读**：uciexpress.org 的规范下载页附最终用户许可协议，第 (ii) 款禁止把规范输入任何 AI 系统、也禁止用 AI 分析或提取。改读联盟公开材料；在环境 "rf design" 放行 www.uciexpress.org、uciexpress.org、hc2023.hotchips.org、www.hc2023.hotchips.org（用户批准）。
- 读的：Hot Chips 2023 UCIe 教程 "Electrical, Form-Factor, and Compliance"（30 页，slides 52–81）；UCIe 1.0 白皮书（2022-02，7 页，Table 1 是图片，渲染读）。两份都没有 AI 使用限制。
- 结果：16 条里 15 条值相同，改 spec（`VERIFIED`）；`ucie.standard.lane_repair` 的"x16 → x8"没找到，仍 survey，note 改了（`CHANGED`）。新增 `ucie.raw_ber_by_rate`、`ucie.advanced.spare_lanes_per_32`。
- 发现：眼罩（40 mV、0.75 / 0.65 UI）是无噪声、无抖动行为级模型下的**信道合规**眼罩；原始 BER 分速率，1e-27 只到先进 12 / 标准 8 Gb/s，之上 1e-15 加 CRC / 重传；迁入时说白皮书有"BER < 1e-27"，白皮书里没有；TX 0.4 V 是最小值；24 / 32 GT/s 前向时钟另有速率 / 4 一档；先进封装每 32 位 2 条备用。
- 引文里的句子都在幻灯片 / 白皮书文本层里逐字找到（白皮书一处"single-ended"在换行处被抽成"singleended"）。
- 共享表 102 条：spec 53、survey 40、derived 9。测试 80 个（78 通过，2 跳过）。d2d_link 需重新 pin，issue 待用户定。

## 2026-11-14 · 第 2 批再补：Henzler ISSCC 2008 的单次精度（feat/m2-batch2-tdc-henzler，未发布）

- PR #17 已合并（main `bb70a66`）。fmcw 报回 TDC 抖动决定鬼目标数，于是读 Wu 文 [35]：Henzler et al., ISSCC 2008 paper 30.5（3 页），用户从 Xplore 下载。
- 90 nm 局部无源插值 TDC：4 倍插值，分辨率 4.7 ps @ 1.2 V（3.9 ps @ 1.4 V），INL ±1.2、DNL ±0.6 LSB，180 MHz 时 3 mA、19 pJ/次。原文说比较器输入的 kT/C 噪声可忽略。
- **单次精度 0.7 LSB**：原文定义为反复测同一恒定间隔时输出码字的标准差（Fig. 30.5.4 标注、Fig. 30.5.6 对比表）。按秒 3.29 ps，建 derived 条目（`RECOMPUTE` 复算 0.7 × 4.7e-12）。原文还明说有限的单次精度给输出加了 dither，多次平均可降低量化误差，正是 fmcw 模型里抖动的角色。
- 限制写进 note：标准差里含码字离散化与片上表征单元产生起止脉冲的抖动，所以是上界量级；Sheppard 修正 √(0.7² − 1/12) 粗算噪声本身约 0.64 LSB ≈ 3.0 ps（近似，不登记）。结构与 Wu 2014 的延迟链 TDC 不同。对比表里 Staszewski 2006 那栏没有单次精度，与上一条的结论一致。
- 新文件 `data/tdc.yaml`（前缀 `tdc`，登记进 `FILE_PREFIXES` 与 AGENTS.md），没有库 vendor 它。共享表 100 条：spec 36、survey 55、derived 9。测试 80 个（78 通过，2 跳过）。
- 用户定：fmcw 暂不换 `tdc_jitter_s`，不开 issue（ROADMAP 第 2 项记下了日后开 issue 时要写的话）。

## 2026-11-14 · 验收 fmcw_radar#17：60 GHz 档的 TDC 分辨率改读本库（feat/accept-fmcw-17）

- PR #16 已合并（main `e49979f`），以它为 PIN 开了 fmcw [#17](https://github.com/alexyudragonsword-collab/fmcw_radar/issues/17)。fmcw 回报合并 `0d32179`（0.2.12，`ffc703e` 上的一个提交）。
- 复核：
  - 5 个 vendor 文件去掉出处头后与 `e49979f` 逐字节相同，`vendor_check --strict` 无 stale；
  - 它的测试 200 过 2 跳过；
  - 加载后 `60g_sensing.tdc_res_s` = 1.22e-11（spec，upstream 对），`77g_automotive.tdc_res_s` 仍 5e-12 assumed；来源计数 24 / 7 / 6 / 2，与回报一致。
- 指纹：`ffc703e` → `0d32179` 动了 720 / 2035（值的总数 1979 → 2035，多出的是新检出的鬼目标）。在 `ffc703e` 上只改这一个数，再用 `tools/export_lo_profile.py` 重新导出剖面：剖面与它提交的逐字节相同，2035 个值与 `0d32179` 逐位相同。它另改的 `lo.py` 只是文档字符串，示例 01 只是打印格式。
- 它报回的后果：1 ps 抖动在 12.2 ps 步长下只有 0.08 LSB，打不散量化，默认配置每帧 2.75 个鬼目标（原来 0）。所以 TDC 抖动的出处有分量了，ROADMAP 第 2 项加了候选原文（Wu 文 [35]，Henzler ISSCC 2008，题名写 0.7-LSB single-shot precision）。
- 登记 1 条引用（`consumers.yaml` 共 9 条）。fmcw 的验收快照换成 `0d32179` 那份（`ffc703e` 那份在 git 历史里）。共享表仍 98 条，测试 79 个（77 通过，2 跳过：多出的 2 个是新登记那条的两项检查）。

## 2026-11-14 · `adpll60.wu_jssc2014_tdc` 的分辨率改按秒记（feat/adpll60-tdc-res-seconds，未发布）

- PR #15 已合并（main `465152b`）。准备给 fmcw 开 issue 时发现：它的加载器要求本地值与 `upstream` 读到的值完全相等，而它的 `60g_sensing.tdc_res_s` 以秒为单位（5.0e-12）。本库条目原来是 `tdc_res_ps: 12.2`，它引用时得做换算，铁律 6 不许。
- 条目未发布、没人读，直接把字段改成 `tdc_res_s: 1.22e-11`（unit 跟着改为 s）。YAML 里 1.22e-11 与 12.2e-12 解析成同一个 double，fmcw 写哪种都能逐位相等。
- 共享表仍 98 条，测试 77 个（75 通过，2 跳过）。

## 2026-11-14 · 第 2 批收尾：Wu 文 [23] 也没有 TDC 抖动（feat/m2-batch2-tdc-ref23）

- PR #14 已合并（main `bc08b36`）。用户下了 Wu 文 [23]：Staszewski et al., TCAS-II 53(3) 2006，5 页，TI 的 90 nm GSM ADPLL 用的伪差分延迟链 TDC。
- 有的：分辨率 17–21 ps（1.3 V，15 片 × 工艺角，强弱角差 3 ps），DNL / INL < 0.7 LSB，0.01 ps/°C，5.3 mA（电源管理后 1.3 mA）。Fig. 15 读图：1.0 / 1.2 / 1.5 V 时约 34.5 / 22.4 / 15.4 ps。
- 没有的：TDC 自身的抖动。Table I 只比工艺、电源、功耗、面积、分辨率。"metastability resolution window is less than 1 ps" 是触发器的判决窗口，不是抖动，不能拿来当 `tdc_jitter_s`。
- 结论：两篇原文都只给分辨率。fmcw 的 `tdc_jitter_s`（1 ps）保持 assumed，不再找。`tdc_res_s` 有 Wu 2014 的 12.2 ps 可引。90 nm 这篇的数没有库要读，不建条目，只记在 `cairn/Reference/README.md`。
- 只改文档，共享表仍 98 条，测试 77 个（75 通过，2 跳过）。

## 2026-11-14 · 第 2 批：60 GHz ADPLL 的 TDC（feat/m2-batch2-tdc，未发布）

- PR #13 已合并（main `8c63b09`）。用户从 Xplore 下了 Wu、Staszewski、Long（JSSC 2014，16 页）。原文清单说 TU Delft 机构库有免费全文，实际只有元数据，已更正。
- VI.A：TDC（伪差分延迟链，Wu 文 [23]）平均分辨率 12.2 ps @ 1.2 V，随 PVT 自校准；100 MHz 参考。公式 ℒ = (2π)²/12 · (Δtres/TV)² / fR 是嵌入对象，渲染第 12 页读：60 GHz 下 −78 dBc/Hz（复算 −77.54）。实测带内 −77 dBc/Hz（约 1.5 MHz 带宽），原文说由 TDC 量化主导。分辨率降到 4 ps 可低 9.7 dB。
- **没有 TDC 自身的输入参考抖动**。−77 对 −78 只差 1 dB、都是整数 dB，推不出抖动的值，所以不建 derived。fmcw 的 `tdc_res_s`（占位 5 ps）有原文数 12.2 ps 可引，`tdc_jitter_s`（1 ps）仍没有出处。摘要的 590.2 fs 是合成器输出 10 kHz–10 MHz 的积分抖动，不是 TDC 的。
- 新文件 `data/adpll60.yaml`（前缀 `adpll60`，登记进 `FILE_PREFIXES` 与 AGENTS.md），没有库 vendor 它，不涉及重新 pin。
- 共享表 98 条：spec 35、survey 55、derived 8。测试 77 个（75 通过，2 跳过，多出的 1 个是新文件的 grep 守卫）。

## 2026-11-14 · 第 1 批（部分）：[9] Kuo、[11] Jin 对上原文（feat/m2-batch1-kuo-jin，未发布）

- PR #12 已合并（main `500710b`）。这两行在已读 5 篇的对比表里都没出现过，先读。
- [9] Kuo（MWCL 2009）：Table I This Work 的 1.8 V 一行是 30 / 10.3 / 13.8 / 12.6 %、178 mW，与 Asada 相同。2.4 V 是 31.3 / 11.7 / 16.2 / 14 %，3 V 是 32.4 / 12 / 18 / 15 %。Psat − P1dB 依次 3.5 / 4.5 / 6.0 dB，同一颗 PA 漏压越高压缩越平缓。2.4 V 的 PAE 正文写 15、表写 14。文本层丢了斜体符号，引文按渲染页补，逐段核过。
- [11] Jin（ESSCIRC 2007）：**不是 60 GHz 的数**。增益峰值 25 dB 在 52 GHz，60 GHz 时 11 dB（摘要写 10），-3 dB 带宽 46–53 GHz。Psat 8 / P1dB 5 dBm / PAE 7 % 是 48 GHz 的扫描，Fig. 9 只有 6 个点，读出的增益是 22 → 21 → 20 → 19 → 17.4 → 13 dB，从最低一点就在降，P1dB 5 dBm 在图上读不出来。Asada 的 110 mW 就是 1.5 V × 73 mA。
- 出处线索：Kuo 的 Table I 把 Tanomura 写成 15.2 / 10 / 11 / 8.2 / 150 mW / 1 V，与 Asada [13] 一字不差，Asada 那格 15.2 看来转抄自 Kuo。
- 剩 6 行（[5] [7] [8] [10] [12] [14]），在已读原文的对比表里都至少出现过一次且与 Asada 相符（Kuo 表写 [5] 1.2 V，Asada 写 1.0 V），优先级降到第 2、3 批之后。
- 共享表 97 条：spec 34、survey 55、derived 8；`pa60.yaml` 的 grep 计数 spec 12、derived 1。测试 76 个（74 通过，2 跳过）。

## 2026-11-14 · 第 1 批（部分）：[15] Martineau 对上原文（feat/m2-batch1-martineau，未发布）

- PR #11 已合并（main `31fe48b`）。用户下了 [15] Martineau（ISSCC 2010 paper 23.8，IEEE Xplore 5433879）。
- 对比表 Fig. 23.8.5 的 1.2 V 一列：增益 14.3、P1dB 11、Psat 16.6、PAE 4.9 %，与 Asada [15] 四格相同。1.8 V：15.5 / 11.5 / 18.1 / 3.6 %，直流 732 / 1504 mW。
- Psat − P1dB：1.2 V 5.6 dB，1.8 V 6.6 dB。**Fig. 23.8.4 扫到 Pin = 10 dBm 为止，两条 Pout 曲线到终点仍在上升**（1.2 V 时增益从 14.3 压到约 6.6 dB，读图），所以 Psat 是扫描终点，真实的差只会更大。原作者没说有异常，是 A 类 cascode 加合路损耗的平缓压缩。
- 对 mmw60 的含义：去掉作者自认偏置不当的 [1]（9.0 dB），表里最软的正常 PA 是 [15]，扫描范围内 5.6 dB（1.8 V 6.6 dB）。要到 TGad Rapp 的 9.5 dB，1.2 V 的 Psat 得到 20.5 dBm，而曲线末端每 dB 输入只涨约 0.2 dB（读图），不像能到。
- 题名是"18dBm"（1.8 V 的 18.1），Asada 参考文献表写成"18 dB"。重新取了 Asada 原文核对，是 Asada 的笔误，不是本库抄错。
- Martineau 的对比表旁证了 [10] [12] [14] 三行（[14] 增益 5.5，与 Asada 同）。剩 8 行里 [9]、[11] 在 5 篇原文的对比表里都没出现，建议下一步先下。
- 共享表 95 条：spec 32、survey 55、derived 8；`pa60.yaml` 的 grep 计数 spec 10、derived 1。测试 76 个（74 通过，2 跳过）。

## 2026-11-13 · 验收 mmw60_trx#25、fmcw_radar#15（feat/accept-mmw60-25-fmcw-15）

- PR #10 已合并（main `fff06a7`）。两边都回报了，在它们的 main 上独立复核。容器重建过，建了个 venv（numpy 2.5.4、scipy 1.18.1、itur 0.4.0）。
- mmw60（b16b6a0，pin 9a443ba）：
  - 8 个文件去掉两行出处头后与 pin 逐字节相同；`vendor_check --strict` 里 spec_sources 8 个都是 verbatim，`pa60.yaml` 报 stale pin，是 PR #10 造成的，属预期；
  - 指纹 97353e0 对 b16b6a0：69 个值逐位相同，两边都有一项因没装 numba 而报错，算相同；
  - `all_entries()` 130 条、未核实 42 条；它的 test_spec_sources / test_vendor_check 15 过 2 跳过。
- fmcw（ffc703e，pin dfaa36b，选 (a) 只算氧气）：
  - 4 个文件逐字节相同；它的 `__init__.py` 是自己写的，不在登记里；
  - 指纹 79d040a 对 ffc703e 动了 319 / 1979。**在 79d040a 上只改两个氧气数（15.0→14.651、0.4→0.091），1979 个值就与 ffc703e 逐位相同**，所以变化全部来自这两个数；
  - 全量 pytest 198 过 2 跳过（它的环境里是 200 过，跳过的 2 个要姊妹库）。
- 登记 3 条引用（`consumers.yaml` 8 条），fmcw 在 ffc703e 时的表加为 fixture，`test_consumers.py` 用它核对 8 条 `upstream:` 都已登记且值相等。
- **更正**（fmcw 指出）：上一条 LOG 里 77 GHz 总气体衰减"合计 0.348"，是 itur 把 `p` 当干空气压时的结果（总压 1023.2 hPa）。按总压 1013.25 读：氧气 0.0956、水汽 0.2485，合计 0.344。条目只登记干大气，数值不动；`atmosphere.yaml` 里那句 note 等这个文件下次改动时注明读法（ROADMAP）。
- 测试 76 个（74 通过，2 跳过）：多出 3 条登记各 2 个、新 fixture 1 个、fmcw 引用核对 1 个。

## 2026-11-13 · 第 1 批（部分）：Asada Table I 的 4 行对上原文（feat/m2-batch1-pa60-originals，未发布）

- PR #9 已合并（main `dfaa36b`）。fmcw [#15](https://github.com/alexyudragonsword-collab/fmcw_radar/issues/15) 提前开了，ROADMAP 原来写的是"等第 4 批齐了再开"，已改。#15 与 mmw60 #25 都还没回报。
- 用户从 IEEE Xplore 下了 [1] Chan、[2] Lai、[6] Law、[13] Tanomura（ISSCC 2009 / 2010 / 2010 / 2008）。Chan 与 Tanomura 的表格用嵌入字体，文本层是乱码，渲染 300 dpi 读。
- 12 格 P1dB / Psat / PAE 与 Asada 全部相同，Psat − P1dB 依次为 9.0 / 2.6 / 1.7 / 1.0 dB。不同的有三处：
  - [1] 的增益：原文表 15.8，Asada 写 16.0；
  - [13] 的增益：Asada 的 15.2 是 0.7 V 的线性增益，同一行另外三格是 1.0 V 的（1.0 V 线性增益是 14.3 ± 1.3）；
  - [2] 原文前后不一：正文 17.9 / 15.4 dBm、11.7 %，汇总表 17.7 / 15.1、11.1 %，Asada 抄的是汇总表。
- **[1] 的 9.0 dB 原作者自己归因于偏置不当造成的提前压缩**。它是 Table I 里唯一接近 TGad Rapp 9.5 dB 的一行；去掉它，最大是 [15] 的 5.6 dB（未读）。
- [13] 的 Psat 是"Output RF power"（扫到 Pin = 0 dBm 的最高输出），带 ±0.5 dB；60 GHz 正文给 P1dB 10.5、增益 13.3 dB 时输出 11.3，只差 0.8 dB。
- 新增 4 条 spec，`pa60.eumc2011_table1` 只改 note（`CHANGED` 登记一次替换，"本库"换成库名），值不动。
- 共享表 94 条：spec 31、survey 55、derived 8；账本 125 行。测试 68 个（66 通过，2 跳过）。
- 环境：容器里 pytest 的 uv 环境丢了 PyYAML，重装后测试才跑得起来。

## 2026-11-13 · 第 4 批（部分）：P.676 氧气衰减与行人 RCS（feat/m2-batch4-atmosphere-rcs，未发布）

- PR #8 合并为 0.3.0（main `9a443ba`），给 mmw60 开了 [#25](https://github.com/alexyudragonsword-collab/mmw60_trx/issues/25)：重新 pin，数值不变，示例 09 一行标签变。
- ITU-R P.676-13：Table 1 的 44 条谱线从文本层抽出；式 (5)–(9) 渲染原文第 7、10 页核对。按图 1 的干大气（1013.25 hPa、15 °C）逐线求和：60 GHz 14.651、峰值 15.06 @ 60.81 GHz、77 GHz 0.096、77.5 GHz 0.091 dB/km。itur 0.4.0（P.676-12）给 14.6511 / 15.0369 / 0.0962，一致。
- **fmcw 的 77 GHz"氧气 0.4 dB/km"是总气体衰减**：itur 标准大气下氧气 0.0975 加水汽 0.2505，合计 0.348。60 GHz 的"约 15"指峰值，60.0 GHz 处是 14.651。
- 湿空气有歧义：1013.25 hPa 是总压还是干空气压，原文没说。两种读法在 60 GHz 差 0.12 dB/km（14.50 对 14.62），所以只登记干大气。
- arXiv:1910.13706：77 GHz 行人同极化 −10…+5 dBsm、交叉极化约低 10 dB，是射线追踪仿真，登记为 `target_rcs.deep2019_pedestrian_77g`，note 写明仿真。fmcw 的 −10 dBsm 是这个范围的下端。
- 不升版本号：mmw60 vendor `__init__.py`，一升就又要它重新 pin，而 #25 还没做。账本新键记 `added=unreleased`，测试要求此时 CHANGELOG 有"未发布"一节。
- 共享表 90 条：spec 27、survey 55、derived 8。测试 68 个（66 通过，2 跳过）。

## 2026-11-13 · 0.3.0：TGad 评估方法学对上原文，退役别名（feat/0.3.0-tgad-em-verified）

- 原文怎么取到的：
  - Asada EuMC 2011：东工大实验室站点已迁到 www.ssc.p.isct.ac.jp，这个域名本来就在放行列表里，只是我先试了旧域名；
  - TGad EM：在环境 "rf design" 里放行了 mentor.ieee.org（用户批准），取到 802.11-09/0296r16（2010-01-20）与 r09。
- 9 条 `tgad_em.*` 由 survey 改为 spec，值一个不变。7 个参数与原文 3.2 节逐个相同；两个公式是 .doc 里嵌入的对象，转 PDF 渲染第 4–5 页读的。
- 顺带读到的新事实，新增 4 条 spec：TGad 的相噪参数（−90 dBc/Hz、1 MHz、100 MHz、−130）、相噪加在收发两侧、回退从 Psat 算、推荐回退 OFDM 8 dB / 单载波 0.5 dB。mmw60 的 `assumed.pn_apply_sides`、`assumed.pa_obo_reference` 一直标着"原文没说"，现在有原文可引了，要不要改由它定。
- 修订史：r09（2009）的 CMOS PA 是 g 5 / Asat 0.6 / s 0.71；r12（2009-11-19）"Modified CMOS PA model"改成现值；r11 把相噪改成单极点。
- Asada 的参考文献表：Table I 那 13 行的题名都读出来了（`cairn/Reference/README.md`），Table I 与 `pa60.eumc2011_table1` 逐格一致。[8] 的页码与 [7] 相同，应是原文笔误。
- 17 个别名退役（`retired=0.3.0`），前提已在 #23 验收时确认。
- 共享表 84 条：spec 23、survey 55、derived 6；`keys.lock` 101 行。
- 本环境实测：ROADMAP 原来写"脚本能自己取"的 mentor、eCFR 其实被拦，IEEE Xplore 返回 418、MDPI 返回 403。清单已按实测重写。

## 2026-11-13 · mmw60_trx 跟上 0.2.0，#23 验收关闭（feat/accept-mmw60-0.2.0）

- 回报：mmw60 PR #24，合并 `97353e0`，pin 到 `e573d4d`。本库在它的 main 上独立复核：
  - 8 个 vendored 文件与 PIN 逐字节相同；
  - 代码 / 测试 / 本地表 / 期望输出里的旧名从 42 / — / 4 / 4 处降到 0；
  - 指纹 68 / 68 逐位相同，对 b8fc55b 和 13024e0 都一致。
- 逐字段比对（旧名映射到新名后）：126 条只差 7 处，全是文字或值里出现的改名键名。
  - 文字 6 处：我们登记的 3 处，加上它本地表的 3 处；
  - 值 1 处：`assumed.pa60_surveyed_pick` 的 `rapp_p` 引用；读到的数不变。
- 它把 `DeprecatedKeyWarning` 设成了测试错误。非慢测试 199 通过、7 跳过（与回报一致）；受影响的 7 个测试文件 93 通过、2 跳过。
- 它多做的一处：垫片原来自己查合并表、不认 `aliases:`，只重新 pin 的话旧名会直接 KeyError，它补了 `_resolve`。
  - **更正**：这是迁移说明里给 mmw60 的垫片示例漏掉的，`survey()` 函数体照旧，不处理别名。
  - 读取器带 `table` 时的 `ref()` 也不认别名。已记进 ROADMAP，下次动 `reader.py` 时一起做。
- `consumers.yaml`：mmw60 的 pin 改到 `e573d4d`（at `97353e0`，issue #23）；fmcw、d2d 仍在 `d7b4d1e`。0.3.0 退役别名的前提已满足。

## 2026-11-13 · 0.2.0：17 个旧前缀键改名，旧名留别名（feat/0.2.0-rename）

- 合并为 main `e573d4d`（PR #5），即 0.2.0 的 PIN。已开 [mmw60_trx#23](https://github.com/alexyudragonsword-collab/mmw60_trx/issues/23)。
  按 mmw60 main `b8fc55b` 数过：读旧名的代码 42 处（13 个文件），本地表文字 4 处，期望输出 4 处（08 三处、09 一处）。
  issue 里建议它加 `filterwarnings = error::…DeprecatedKeyWarning` 守住没改完的旧名。
  更正：0.2.0 的 CHANGELOG 与 ROADMAP 写"示例 04 / 08 / 09"会变，实为 08 / 09（04 打印的 `derived.pa60_obo_at_evm_limit_db` 是 mmw60 本地键）。

- 用户确认了新名表（ROADMAP 里拟的那张），照表改了 17 个键，分布：energy 5、ieee80211 6、liu2025 3、frontend60 2、pa60 1。值、单位、标签都没变。
- 旧名写进各数据文件的 `aliases:`（since 0.2.0），读取时发 `DeprecatedKeyWarning`，返回的条目 `.key` 是新名。`keys.lock` 97 行：80 个活键，17 个 `aliased=0.2.0`。
- 条目里引用旧名的交叉引用有 3 处，跟着改（登记在 `CHANGED`）：一条 note、两条 cite（`derived.cfo_liu2025_hz` → `liu2025.cfo_from_ppm_hz`）。文件头里的前缀说明重写。
- `LEGACY_PREFIX_KEYS` 删掉，标签一律不许当前缀。新前缀 7 个，已登记在 `FILE_PREFIXES` 和 AGENTS 里。
- 版本号从 `reader.py` 挪到 `__init__.py`，`reader.py` 只差这一行。以后单纯升版本，不会再让只 vendor `reader.py` 的 fmcw / d2d 变成"需重新 pin"。
- 这次三个库都"需重新 pin"（`vendored:` 守卫要求 CHANGELOG 写明）：
  - mmw60：要改调用，示例 04 / 08 / 09 打印的键名会变，开 issue；
  - fmcw、d2d：读到的数不变，择机重新 pin，等里程碑 2 的 issue 一起做。
- 测试 66 个（64 通过，2 跳过）：新增一条，逐个检查 17 个别名会警告并解析到新键。
- **更正**：上一条（迁移验收）写的"测试 66 个（64 通过，2 跳过）"不对，应为 65 个（63 通过，2 跳过）——当时是数进度点数错了，这次用 `-o addopts=""` 拿到 pytest 的汇总行才核对出来。

## 2026-11-13 · 三个消费方的迁移验收通过，issue 关闭（feat/accept-migrations）

- 回报：mmw60 PR #22 → `b8fc55b`；fmcw PR #14 → `79d040a`（0.2.10）；d2d → `0cbd4e9`（0.16.0）。三个都是各自 main 的 HEAD。
- 本库独立复核（不只看回报）：
  - vendored 文件对 PIN 逐字节相同：mmw60 8 / 8、fmcw 2 / 2、d2d 3 / 3。fmcw、d2d 的 `__init__.py` 按说明是自己写的。
  - mmw60 本地表 62 条，grep 0 / 3 / 56 / 3，`audit_tags` 空，与共享表无交集。
  - fmcw 的 5 条 `upstream:` 与登记逐条一致，值相等。
- 指纹（我这边重录，与各自迁移前比）：mmw60 68 / 68、fmcw 1979 / 1979、d2d 3597 / 3597，全部逐位相同。mmw60 经垫片读出的 125 条 `repr` 逐条相同。
  - d2d 第一次只录到 3487 个：环境里缺 scikit-rf，Touchstone 用例被跳过。补装后两边都是 3597，与它的回报一致。
- 改了原计划：mmw60 / d2d 不按条连值登记（那是把 80 条数据抄一遍），改成 `consumers.yaml` 的 `vendored:` 按文件登记；文件在某个消费方的 pin 之后改了，CHANGELOG 要写"`<库>` 需重新 pin"。变异：改 `frontend60.yaml` 并提交，只有 mmw60、fmcw 两条变红（d2d 不读它）；补上两行后转绿。
- 删三份迁移说明，fmcw 的 14 条清单移进 ROADMAP。测试 66 个（64 通过，2 个因没有迁移说明而跳过）。
- 各库回报里的后续，归它们自己：mmw60 的 ROADMAP C11（3 条 survey 的标签）；mmw60 的 `test_entries_a_downstream_library_reads_*` 现在可以删了（fmcw 已迁）。本库下一步：0.2.0 改名。

## 2026-11-13 · 迁移改由各库的 issue 跟踪（feat/upstream-issues）

- PR #2 合并（main `bef20fb`；`src/spec_sources/` 与 PIN `d7b4d1e` 之间 diff 为空）。
- 用户定：不再由用户转话，直接在三个库开 issue。三个库原来都没有未关的 issue；格式照 mmw60_trx#14（跨库 issue 的先例）。
  - [mmw60_trx#21](https://github.com/alexyudragonsword-collab/mmw60_trx/issues/21)：只搬家，验收是指纹 68 / 68，加 `all_entries()` 125 条 repr 比对。
  - [fmcw_radar#13](https://github.com/alexyudragonsword-collab/fmcw_radar/issues/13)：5 条 `upstream:` 的对照表；验收指纹 1979 / 1979。
  - [d2d_link#1](https://github.com/alexyudragonsword-collab/d2d_link/issues/1)：别名表接住旧键名；写明唯一改动的 note；验收指纹 3345 / 3345。
- 每个 issue 都写了 PIN、要做的事、演练结果、`--siblings` 路径的坑、回报内容；按 mmw60 的规矩，由 spec_sources 验收后关。
- AGENTS"不改消费方的仓库"一条与 ROADMAP"报回上游"改成链 issue。

## 2026-11-13 · PR #1 合并；迁移说明回填 PIN，关掉开放问题 1（feat/m1-pin）

- PR #1 以合并提交 `d7b4d1eb510617d69784622c593c8ed31ab32b8b` 进 main（CI：lint、test 3.10 / 3.12 全绿）。三份迁移说明的 PIN 都填它（mmw60 6 处、fmcw 5 处、d2d 3 处）。
- 演练用的是 `59726b9`；它与 `d7b4d1e` 之间 `src/spec_sources/` 的 `git diff` 为空，演练结果（指纹 3345 / 1979 / 68 逐位相同等）对正式 PIN 照样成立。
- 开放问题 1 关掉：用户确认 3 条 survey（两条 clock_profile、dsp_ip）留在 mmw60。ROADMAP 里留了两条后续：mmw60 自己考虑这 3 条的标签（它们是模型输出，不是文献）；有库要 Wu 2019 的实测数时为论文单开条目。
- 17 个旧前缀键改名排期写进 ROADMAP：mmw60 迁完之后单独出 0.2.0，附拟定的新名表（动手前再确认）。
- 新守卫 `tests/test_migration_notes.py`：每份说明恰好一条完整 SHA 的 PIN、归属头都用它、三份一致、PIN 是 HEAD 的祖先（有历史时）。变异：放回 `<PIN>`、头里换成别的 SHA，都红。测试 63 个。

## 2026-11-13 · 里程碑 1：开库，三张表合成 80 条；三份迁移说明各演练一遍（feat/m1-shared-tables，0.1.0）

- 源：mmw60_trx@13024e0（125 条：spec 10 / survey 51 / assumed 56 / derived 8）、d2d_link@6789810（16 条 survey）、fmcw_radar@2e5cbb6（39 条，只登记 5 条引用）。三个检出的 HEAD 核过就是这三个 SHA。
- 迁入 **80 条**：mmw60 63（spec 10、survey 48、derived 5）+ d2d 16（加 `ucie.`）+ 新 derived 1（隔离度 40 − 20 = 20 dB）。按标签：spec 10、survey 64、derived 6、assumed 0。7 个领域文件。
- **和指令不一样**：指令写"spec 10 + survey 51 = 61 条"，实际只迁 48 条 survey。留下的 3 条按铁律 2 不进共享表：两条 clock_profile 的值是 mmw60 仓库里的文件名（x10 那条还用了它的 assumed 底噪），dsp_ip 那条是姊妹库的综合估计。理由在 `tests/test_extraction.py::MMW60_STAYS`（ROADMAP 开放问题 1）。
- derived 8 条：跟着走 5 条（cfo、k_threshold_stf、k_threshold_ltf_only 只用 liu2025.*；rapp_p1db_below_psat_db 只用 tgad_em.*；pa60_rapp_p_asada_eumc2011 用 pa60.asada_eumc2011 + tgad_em 的形状）；留下 3 条（用了 assumed.cr_rms_delay_ns、assumed.pa60_operating_rule，或是示例 03 的读数）。共享的 6 条在 `RECOMPUTE` 里只用共享条目复算：Rapp 闭式 p = 0.81 → 9.497 dB、p = 1.286 → 4.598 dB。
- grep 守卫查出两张源表数错：mmw60 第 636 行注释（spec 数 11 对 10），d2d 表头 + 一条 note（spec 数 2 对 0）。那条 note 是迁入条目唯一改了的字段（`CHANGED`）。
- mmw60 的 17 个 `survey.` / `derived.` 前缀键**没改名**：它的示例 04 / 08 / 09 打印键名，改名会让示例输出动；冻结成旧名，改名排进 ROADMAP。
- 测试 58 个（3.13 与 3.10 都绿），ruff 干净。变异检查：注释写进标签词、登记值 12 → 13（也试了只改 consumers.yaml 不改 CHANGELOG）、改名不留别名、留别名不记账本、derived 不写复算、未知字段——每种都红，还原后绿。
- **演练**（各库 pin 提交的临时 worktree，没推）：d2d 指纹 3345 / 3345 逐位相同，pytest 250 passed / 12 skipped；fmcw 1979 / 1979，197 passed / 2 skipped；mmw60 指纹 68 / 68，经垫片读出的 125 条旧条目 8 个字段逐条相同，pytest 199 passed / 6 skipped。三库 `vendor_check --strict` 里 spec_sources 的文件都 verbatim（mmw60 8 个、d2d 3 个、fmcw 2 个）。
- 演练查出、已写进说明与 ROADMAP 的：d2d / mmw60 的 `example_drift.spec_values` 按路径读表（d2d 的一条测试因此红过）；d2d 的 `_strip_header` 会吃掉 YAML 正文第一行注释；mmw60 / fmcw 的 `test_vendor_check` 写死了 pin；第一版 `audit_tags` 把 mmw60 值映射里的 `source` 键也报了——改成只报规则禁止的，共享表另有更严的测试。
- knowledge-vault 不在本会话里（指令：没有就跳过），没读。
- 下一步：用户合并后，把合并提交的完整 SHA 填进三份迁移说明的 `<PIN>`，按 mmw60 → fmcw → d2d 转给各库。
