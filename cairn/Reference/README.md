# cairn/Reference：原文清单

这里放原文的读书笔记和待取清单。出版方的 PDF / .doc 只放本地，不入库（`.gitignore`）。

标记：📥 要用户下载（IEEE Xplore 对脚本返回空页；标准与 UCIe 规范要注册账号）· 🌐 免费，放行括号里的站点后本库自己取 · ✅ 本会话已能直接取。站点通不通是 2026-11-13 在环境 "rf design" 里实测的。

## 已读（本库取到原文）

| 文献 | 从哪里取 | 读了什么、落到哪里 |
|---|---|---|
| E. Perahia (Intel), "TGad Evaluation Methodology", IEEE 802.11-09/0296r16, 2010-01-20（另取 r09 对照） | mentor.ieee.org（2026-11-13 放行） | 3.2 Hardware impairments：9 条 `tgad_em.*` 由 survey 改为 spec（0.3.0），值不变；新增 `tgad_em.pn_params`、`pn_sides`、`pa_backoff_definition`、`pa_backoff_recommended_db`。公式是 .doc 里嵌入的公式对象，转成 PDF 后渲染第 4–5 页读的 |
| Recommendation ITU-R P.676-13 (08/2022), "Attenuation by atmospheric gases and related effects" | www.itu.int | Annex 1：Table 1（44 条氧气谱线）与式 (1)–(9) → `itu_p676.*`。式子在文本层里丢了 θ，渲染第 7、10 页读的。用 itur 0.4.0 独立核对过干大气结果 |
| Y. Deep et al., "Polarimetric Radar Cross-Sections of Pedestrians at Automotive Radar Frequencies", arXiv:1910.13706v1, 2019 | arxiv.org | III.B 与图 4：77 GHz 行人同极化 RCS −10…+5 dBsm（射线追踪仿真）→ `target_rcs.deep2019_pedestrian_77g` |
| H. Asada et al., "A 60 GHz CMOS Power Amplifier Using Capacitive Cross-Coupling Neutralization with 16 % PAE", EuMC 2011 | www.ssc.p.isct.ac.jp（东工大并入科学东京后的实验室站点，已放行） | 参考文献表（下面第 1 批的 13 篇）；Table I 的 14 行与 `pa60.eumc2011_table1` 逐格一致 |
| Table I [1] Chan et al., ISSCC 2009 paper 22.4 | 用户从 IEEE Xplore 下载（2026-11-13），`asada_t1_01_chan_isscc2009.pdf` | Fig. 22.4.5 对比表（嵌入字体，渲染读）：增益 15.8、P1dB 2.5、Psat 11.5、PAE 11 % → `pa60.chan_isscc2009`。Asada 写增益 16.0。正文：P1dB 偏低"may be due to premature compression caused by non-optimal biasing" |
| Table I [2] Lai, Valdes-Garcia, ISSCC 2010 paper 23.6 | 同上，`asada_t1_02_lai_isscc2010.pdf` | 正文 61.5 GHz、1.0 V：Psat 17.9、OP1dB 15.4、PAE 11.7 %；自己的汇总表 Fig. 23.6.7：17.7 / 15.1 / 11.1 %。Asada 抄汇总表，四格相同 → `pa60.lai_isscc2010`（两套都记） |
| Table I [6] Law, Pham, ISSCC 2010 paper 23.7 | 同上，`asada_t1_06_law_isscc2010.pdf` | Fig. 23.7.6：P1dB 18.2、Max. Pout 19.9、PAE 14.2 %、增益 20.6，与 Asada 四格相同；正文取整为 +18 / 20 → `pa60.law_isscc2010` |
| Table I [13] Tanomura et al., ISSCC 2008 paper 31.1 | 同上，`asada_t1_13_tanomura_isscc2008.pdf` | Fig. 31.1.6（嵌入字体，渲染读）60–64 GHz、1.0 V：Output RF power 11.0 ± 0.5、P-1dB 10.0 ± 0.5、PAE > 8.2 %、线性增益 14.3 ± 1.3。Asada 的 P1dB / Psat / PAE 是这三格，增益 15.2 却是正文 0.7 V、60 GHz 的线性增益 → `pa60.tanomura_isscc2008` |
| Table I [15] Martineau et al., ISSCC 2010 paper 23.8 | 用户从 IEEE Xplore 下载（2026-11-14），`asada_t1_15_martineau_isscc2010.pdf` | Fig. 23.8.5 两列 This work：1.2 V 增益 14.3、P1dB 11、Psat 16.6、PAE 4.9 %，与 Asada 四格相同；1.8 V 15.5 / 11.5 / 18.1 / 3.6 %。Fig. 23.8.4 扫到 Pin = 10 dBm 时 Pout 仍在上升，Psat 是扫描终点 → `pa60.martineau_isscc2010` |
| Table I [9] Kuo et al., IEEE MWCL 19(1) 2009 | 用户从 IEEE Xplore 下载（2026-11-14），`asada_t1_09_kuo_mwcl2009.pdf` | Table I This Work 三行：1.8 V 30 / 10.3 / 13.8 / 12.6 %、178 mW，与 Asada 相同；2.4 V 31.3 / 11.7 / 16.2 / 14 %；3 V 32.4 / 12 / 18 / 15 %。文本层丢了斜体符号，按渲染页补 → `pa60.kuo_mwcl2009` |
| Table I [11] Jin et al., ESSCIRC 2007 | 同上，`asada_t1_11_jin_esscirc2007.pdf` | 增益峰值 25 dB @ 52 GHz、60 GHz 时 11 dB（摘要写 10），-3 dB 带宽 46–53 GHz；Psat 8、P1dB 5 dBm、PAE 7 % 是 48 GHz 的功率扫描（Fig. 9，只有 6 个点）；1.5 V、73 mA。Asada 四格都在原文里，但不是 60 GHz 的 → `pa60.jin_esscirc2007` |
| 第 2 批 W. Wu, R. B. Staszewski, J. R. Long, IEEE JSSC 49(5) 2014 | 用户从 IEEE Xplore 下载（2026-11-14），`wu_jssc2014_adpll.pdf` | VI.A：TDC 平均分辨率 12.2 ps（1.2 V），100 MHz 参考，带内相噪公式（嵌入对象，渲染第 12 页读）给 −78 dBc/Hz，实测 −77 dBc/Hz（约 1.5 MHz 环路带宽），由 TDC 量化主导。**没有给 TDC 自身的抖动** → `adpll60.wu_jssc2014_tdc` |
| 第 2 批 Wu 文 [23]：R. B. Staszewski, S. Vemulapalli, P. Vallur, J. Wallberg, P. T. Balsara, IEEE TCAS-II 53(3) 2006, pp. 220–224 | 用户从 IEEE Xplore 下载（2026-11-14），`staszewski_tcas2_2006_tdc.pdf` | 90 nm、GSM 用的伪差分延迟链 TDC：分辨率 17–21 ps（1.3 V，随工艺角），DNL / INL < 0.7 LSB，0.01 ps/°C，5.3 mA（加电源管理 1.3 mA）@ 1.3 V；Fig. 15 分辨率随电压从 1.0 V 约 34.5 ps 降到 1.5 V 约 15.4 ps（读图）。**也没有 TDC 自身的抖动**：Table I 只比工艺、电源、功耗、面积、分辨率；最接近的是"metastability resolution window is less than 1 ps"，那是触发器的判决窗口，不是抖动。没有库读这些数，不建条目 |
| 第 2 批 Wu 文 [35]：S. Henzler, S. Koeppe, W. Kamp, H. Mulatz, D. Schmitt-Landsiedel, ISSCC 2008 paper 30.5, pp. 548–549 | 用户从 IEEE Xplore 下载（2026-11-14），`henzler_isscc2008_tdc.pdf` | 90 nm 局部无源插值 TDC：分辨率 4.7 ps（1.2 V）/ 3.9 ps（1.4 V），INL ±1.2、DNL ±0.6 LSB，19 pJ/次。**单次精度 0.7 LSB**（Fig. 30.5.4 与对比表；定义为反复测同一间隔时输出码字的标准差）≈ 3.29 ps → `tdc.henzler_isscc2008`、`tdc.henzler_isscc2008_single_shot_s`。对比表里 Staszewski 2006 那栏没有单次精度，Dudek 2000 的 Vernier 是 0.7 LSB（30 ps） |

## 待取清单（按里程碑 2 的顺序）

### 第 1 批 · 60 GHz PA（决定 mmw60_trx 同台表每格的 MCS）

`tgad_em.*` 已核实。剩下的是 `pa60.eumc2011_table1` 里 Asada 转引的 13 行，要逐行对原文。全部 📥，8 篇是 ISSCC 文摘。✅ 是已读（2026-11-13，见上面"已读"表）：

| Table I 行 | 文献 | Psat − P1dB / Psat |
|---|---|---|
| ✅ [1] | W. L. Chan, J. R. Long, M. Spirito, J. J. Pekarik, "A 60 GHz-Band 1V 11.5 dBm Power Amplifier with 11 % PAE in 65 nm CMOS", ISSCC 2009, pp. 380–381 | **9.0 dB（最大）** / 11.5 dBm |
| ✅ [2] | J. Lai, A. Valdes-Garcia, "A 1 V 17.9 dBm 60 GHz Power Amplifier in Standard 65 nm CMOS", ISSCC 2010, pp. 424–425 | 2.6 / **17.7 dBm（65 nm 最高）** |
| [5] | T. Suzuki, Y. Kawano, M. Sato, T. Hirose, K. Joshin, "60 and 77 GHz Power Amplifiers in Standard 90 nm CMOS", ISSCC 2008, pp. 562–563 | 2.4 / 10.6 |
| ✅ [6] | C. Y. Law, A. Pham, "A High-Gain 60 GHz Power Amplifier with 20 dBm Output Power in 90 nm CMOS", ISSCC 2010, pp. 426–428 | 1.7 / **19.9 dBm（最高）** |
| [7] | N. Kurita, H. Kondoh, "60 GHz and 80 GHz Wide Band Power Amplifier MMICs in 90 nm CMOS Technology", RFIC 2009, pp. 39–42 | 3.8 / 12.6 |
| [8] | M. Bohsali, A. Niknejad, "Current Combining 60 GHz CMOS Power Amplifiers", RFIC 2009（Asada 写的页码 39–42 与 [7] 相同，应是笔误，以 Xplore 为准） | 2.1 / 14.2 |
| ✅ [9] | J. L. Kuo, Z. M. Tsai, K. Y. Lin, H. Wang, "A 50 to 70 GHz Power Amplifier Using 90 nm CMOS Technology", IEEE MWCL vol. 19 no. 1, Jan. 2009, pp. 45–47 | 3.5 / 13.8 |
| [10] | D. Dawn et al., "60 GHz CMOS Power Amplifier with 20-dB Gain and 12 dBm Psat", IMS 2009, pp. 537–540 | 3.8 / 12.0 |
| ✅ [11] | Y. Jin, E. A. Rivero, M. A. T. Sanduleanu, J. R. Long, "A Millimeter-Wave Power Amplifier with 25 dB Power Gain and +8 dBm Saturated Output Power", ESSCIRC 2007, pp. 276–279 | 3.0 / 8.0 |
| [12] | S. Pinel et al., "A 90 nm CMOS 60 GHz Radio", ISSCC 2008, pp. 130–131 | 3.3 / 8.4 |
| ✅ [13] | M. Tanomura et al., "TX and RX Front-Ends for 60 GHz Band in 90 nm Standard Bulk CMOS", ISSCC 2008, pp. 558–559 | **1.0 dB（最小）** / 11.0 |
| [14] | D. Chowdhury, P. Reynaert, A. M. Niknejad, "A 60 GHz 1 V +12.3 dBm Transformer-Coupled Wideband PA in 90 nm CMOS", ISSCC 2008, pp. 560–561 | 3.3 / 12.3 |
| ✅ [15] | B. Martineau et al., "A 53-to-68 GHz 18 dB Power Amplifier with an 8-Way Combiner in Standard 65 nm CMOS", ISSCC 2010, pp. 428–429（原题是 "18dBm"，Asada 写成 18 dB） | 5.6 / 16.6 |

**先下 4 篇**：[1]、[13]（Psat − P1dB 的两端）和 [6]、[2]（Psat 的两端）。表的分布（中位 3.3 dB）就是靠这几行撑起来的。[1] 和 [11] 出自 TU Delft 的 Long 组，机构库里可能有免费全文。

**2026-11-13 补记**：这 4 篇已读，P1dB / Psat / PAE 与 Asada 逐格相同，只有 [1]、[13] 的增益不同（见上表）。顺带得到的：
- [8] 的页码：Lai 与 Law 的参考文献都写 Bohsali, Niknejad, RFIC 2009, pp. 31–34，Asada 的 39–42 是笔误。
- 这 4 篇的对比表也转引了别的行，与 Asada 对得上：[5] Suzuki 8.3 / 8.2 / 10.6（Law 表，PAE 一格空）；[7] Kurita 10 / 8.8 / 12.6 / 6.9（Law 表）；[8] Bohsali 4.4 / 12.1 / 14.2 / 5.8（Law 表；Lai 表的增益是 4.5）；[12] Pinel 17 / 5.1 / 8.4 / 5.8（Chan 表）；[14] Chowdhury P1dB 9.0、Psat 12.3、PAE 8.8（Chan、Law 两表），增益两表都是 5.6，Asada 写 5.5。这些是二手对二手，不算核实，那几行仍要读原文。
- 下一篇建议 [15] Martineau：去掉 [1] 以后，它的 5.6 dB 是 Psat − P1dB 的最大一格。

**2026-11-14 补记**：[15] 已读，四格与 Asada 相同（1.2 V 一列），见上表。顺带得到的：
- Asada 参考文献表把 [15] 的题名写成 "18 dB"，原题是 "18dBm"（1.8 V 时的 Psat 18.1）。
- Martineau 的对比表也转引了别的行：[10] Dawn 20 / 8.2 / 12 / 9 与 Asada 相同；[12] Pinel 相同；[14] Chowdhury 的增益写 5.5，与 Asada 相同（Chan、Law 两表写 5.6）；[13] Tanomura 增益写 14.3（1.0 V 的值），Asada 写 15.2。仍是二手对二手。
- 剩下 8 行里，[9] Kuo（MWCL 2009）与 [11] Jin（ESSCIRC 2007）是 5 篇原文的对比表都没有转引的两行，连二手的旁证都没有；下一步建议先下这两篇。[11] 出自 TU Delft 的 Long 组，机构库里可能有免费全文。

**2026-11-14 再补记**：[9]、[11] 已读（见上表）。顺带得到的：
- [11] 不是 60 GHz 的数：Asada 把 52 GHz 的峰值增益与 48 GHz 的功率扫描列进 60 GHz 的对比表。
- Kuo 的 Table I 把 Tanomura 写成 15.2 / 10 / 11 / 8.2 / 150 mW / 1 V，与 Asada [13] 一行完全相同，Asada 那格 15.2 看来是从这里转抄的。Kuo 表里 Suzuki 的电压是 1.2 V，Asada 写 1.0 V（二手对二手，待读 [5] 原文）。Kuo 表还列了 Jin 2008 JSSC 期刊版：51.2 GHz 19.5 / 3.1 / 8.2 dBm、60 GHz 增益 10.3、PAE 4.2 %、150 mW、2 V，与 ESSCIRC 版不同。
- 剩下 6 行（[5] [7] [8] [10] [12] [14]）在已读原文的对比表里都至少出现过一次且与 Asada 相符（[5] 的电压除外），核实的紧迫性低了。

MDPI 那篇 22 nm PA（Georgakopoulos et al., "A 60-GHz Current Combining Class-AB Power Amplifier in 22 nm FD-SOI CMOS", Microwave 2026）**不取**：它只有版图后仿真，查到的内容里也没有 OFDM 的 EVM，给不了 mmw60 想要的 OFDM 工作点。

### 第 2 批 · TDC 抖动（fmcw_radar 的 1 ps 占位）
- ✅ W. Wu, R. B. Staszewski, J. R. Long, "A 56.4-to-63.4 GHz Multi-Rate All-Digital Fractional-N PLL for FMCW Radar Applications in 65 nm CMOS", IEEE JSSC 49(5), pp. 1081–1096, 2014, doi 10.1109/JSSC.2014.2301764。~~TU Delft 机构库有免费全文（repository.tudelft.nl）~~；**更正（2026-11-14）**：那条记录只有元数据，没有全文。用户从 Xplore 下了，已读（见上面"已读"表）。
- 原文只给分辨率不给 TDC 自身的抖动。fmcw 若要 `tdc_jitter_s` 的出处，下一篇是 Wu 文的 [23]：📥 R. B. Staszewski, S. Vemulapalli, P. Vallur, J. Wallberg, P. T. Balsara, "1.3 V 20 ps Time-to-Digital Converter for Frequency Synthesis in 90-nm CMOS", IEEE TCAS-II 53(3), pp. 220–224, 2006（同一种伪差分延迟链 TDC；有没有抖动数要读了才知道）。**2026-11-14 补记**：[23] 已读（见上面"已读"表），也没有抖动数。两篇都只给分辨率，`tdc_jitter_s` 在读得到的原文里找不到出处，不再找。**2026-11-14 再补记**：fmcw 在 #17 里报回鬼目标数随抖动剧变（1 / 3 ps → 每帧 2.75 / 0.16 个），于是又读了 Wu 文 [35] Henzler ISSCC 2008（见"已读"表）：它给的单次精度 0.7 LSB × 4.7 ps ≈ 3.29 ps 是能找到的唯一一个 TDC 自身随机误差的量级，但结构不同、且含离散化与测试脉冲的抖动。JSSC 2008 的期刊版（"A Local Passive Time Interpolation Concept ..."，Xplore 4550638）没读。

### 第 3 批 · UCIe 眼罩（d2d_link 的判定全悬在 0.65 UI 上）
- ~~📥 UCIe 规范 2.0 或 3.0（uciexpress.org，免费注册；3.0 加了 48 / 64 GT/s）。拿到它，其余 16 条 `ucie.*` 都能对原文核。~~ **不能用（2026-11-14）**：规范下载页的最终用户许可协议第 (ii) 款禁止把规范（全部或部分）"upload, submit, transmit, disclose, provide access to, or otherwise input ... into any artificial-intelligence, machine-learning, large-language-model, generative-AI, or similar automated system"，包括用它 "analyze, evaluate, interpret, transform, ... extract from"。用户不要把规范发给 Claude。
- ✅ Hot Chips 2023 的 UCIe 教程 "Electrical, Form-Factor, and Compliance"（slides 52–81，hc2023.hotchips.org，放行后本库自己取，本地 `ucie_hc2023_electrical.pdf`）：slide 53 速率 / BER 表 / reach，54 宽度与前向时钟，56 TX 摆幅最小 0.4 V，57 时钟频率表，60 每 32 位 2 条备用，61 信道眼罩，69 电气汇总，71 两种封装对照。没有 AI 使用限制的字样。
- ✅ UCIe 1.0 白皮书 "Building an open chiplet ecosystem"（D. Das Sharma，2022-02，www.uciexpress.org/ucie-resources，本地 `ucie_wp2022_1.0.pdf`）：Table 1（速率、宽度、凸点间距、reach、FIT 期望约 1e-10）与"spare lanes / width degradation"一段。**没有"BER < 1e-27"这句**，迁入时的 cite 有误。同页另有 1.1、2.0、4.0 规范的白皮书，取了没读。
- 可选 📥 D. Das Sharma et al., IEEE Trans. CPMT 2022：标准封装降宽是否到 x8 只剩它可查。

### 第 4 批 · fmcw_radar 的 9 条
- ~~✅ ITU-R P.676~~ 已读（见上表）。
- ✅ F. J. Harris, "On the use of windows for harmonic analysis with the discrete Fourier transform", Proc. IEEE 66(1), pp. 51–83, 1978（2026-11-14 用户从 Xplore 下载，本地 `harris_procieee1978_windows.pdf`，33 页；文字层是 OCR，表要渲染出来读）：Table I（p. 55）的矩形、Hann（α = 2）、Hamming、Exact Blackman、Blackman 五行；DFT-even 的定义在 Sec. II（p. 52），Blackman 系数式 (31) 与"相干增益就是 a0"在 Sec. V-E（pp. 63–64） → `harris1978.*`。数值复算：前三行相符（Hamming 扇贝损失差 0.03 dB），Blackman 的 3-dB / 6-dB 宽偏大约 2 %，Exact Blackman 一行与原文的系数不符。可选 📥 A. H. Nuttall, "Some windows with very good sidelobe behavior", IEEE Trans. ASSP 29(1), 1981：讨论过 Harris 的这几族余弦和窗，是否勘误了这几行没读。
- 人体 RCS：arXiv 1910.13706 已读，但只有仿真。要实测值 📥 Belgiovane et al., IEEE Radar Conf. 2014（76–77 GHz 人体 RCS 实测），或 🌐 EC JRC 报告 JRC78619（publications.jrc.ec.europa.eu）。
- ✅ 车辆 RCS：NHTSA DOT HS 813 648（rosap.ntl.bts.gov，2026-11-14 放行后取到，本地 `nhtsa_dot_hs_813648.pdf`，65 页）。两颗 76–77 GHz 雷达（Bosch、Continental），ISO 19206-3:2021 的方法；Table 8（车尾固定角：P_FAR 20、ΔP 10、D_FAR 40 m、K_DEC 0.013）、Table 9（30 m 一周的上下界）是转引 ISO 的；实测的乘用车都在界内，报告不给单车的 RCS 数 → `target_rcs.iso19206_3_car_*`。标定用的两个三面角反射器在 77 GHz 是 10 与 −3.6 dBsm（Eravant SAJ-043-S1、SAJ-020-S1-1.97）。可选 📥 SAE 2021-01-5103、ISO 19206-3 原文（要购买）。
- ✅ 角反射器：A. W. Doerry, "Reflectors for SAR Performance Testing", Sandia SAND2008-0396（www.osti.gov，2026-11-14 放行后取到，本地 `doerry_sand2008_0396.pdf`，57 页）：式 1 / 4 / 7（三角形、方形、四分之一圆），Table 1 复核到 0.1 dB 以内 → `target_rcs.trihedral_peak`。2014 年有第二版（SAND2014-0882），没读。

### 第 5 批 · array_tx 的互耦（它的 ROADMAP A1）
array_tx 要的是面阵实测的复数 S 参数（.sNp），能读到的论文里都没有。下面两篇只给幅度，取了也只能把 −16 dB 从 assumed 升成 survey，相位仍然缺：
- 可选 📥 Int. J. Electron. Commun.（AEÜ，ScienceDirect S1434841126001263）。
- 🌐 美国专利 10910732（patents.google.com）。

### 第 6 批 · Halo_Serdes ROADMAP P3 #11 的 4 条条文
- 📥 IEEE 802.3dj：TDECQ 的前后抽头差、逐抽头 w(i)/w(0) 上下限；DR1 上限是否降到 3.0 dB。到 2025 年底还是草案；批准后走 GET 计划免费。
- 📥 IEEE 802.3db-2022：f_A（GET 计划免费）。
- 🌐 OIF-CEI-112G-LINEAR-PAM4 实施协议（www.oiforum.com，免费）：CTLE 档位表 Table 29-2 / 29-8。

### 第 7 批 · 其余 survey（mmw60_trx 带来的）
- ✅ X. Liu et al., "Wi-Fi 8: Embracing the Millimeter-Wave Era", IEEE Commun. Mag. 63(3), pp. 69–75, Mar. 2025（刊出版，doi 10.1109/MCOM.002.2400059；2026-11-15 用户从 Xplore 下载，本地 `liu_commag2025_wifi8.pdf`，7 页，文字层可用、两张表渲染核对过）：TABLE 1（p. 72）、Simulation Configuration 与 TABLE 2（p. 73）、Simulation Results（pp. 73–74）、Discussion（p. 74）→ `liu2025.*` 21 条改 spec（3 条改了值），新收 4 条。mmw60_trx 在本库 #26 里请求。
- ✅ IEEE 802.15-06-0477-01-003c，Choi et al.（NICT、NEC、NTT、Panasonic），"RF impairment models for 60GHz-band SYS/PHY simulation"，2006-11（mentor.ieee.org 公开，本地 `ieee802_15_06_0477r1_rf_impairment.pdf`，17 页；Liu 的 [15]）：slide 5 修正 Rapp（无参数）、slide 9 相噪模型（−87 dBc/Hz、1 MHz、100 MHz）、slide 10 四档示例、slide 15 转引 802.11n 比较准则 IM1 / IM4 → `tg3c.*`。
- ✅ IEEE 802.15-06-0396-01-003c，Choi et al.（NICT、NEC、NTT），"Behavioral model of 60GHz-band power amplifier for SYS/PHY evaluation"，2006-09（mentor.ieee.org 公开，本地 `ieee802_15_06_0396r1_pa_model.pdf`，15 页）：slide 10 NEC GaAs pHEMT PA 的 Ghorbani 参数（印的公式分子少了指数）、slide 8 输入 P1dB −11 dBm → `tg3c.pa_ghorbani_nec_gaas`。
- 📥 K. Okada et al., "Full Four-Channel 6.3-Gb/s 60-GHz CMOS Transceiver With Low-Power Analog and Digital Baseband Circuitry", IEEE JSSC 48(1), 2013（`antenna60.okada2013_dbi`；2026-11-16 查过实验室网站 www.ssc.p.isct.ac.jp/publication/，只有题录、没有 PDF；东工大实验室站点上可能有，先在那里找）。
- 📥 "A 64 dB Gain 60 GHz Receiver with 7.1 dB Noise Figure for 802.11ad Applications in 90 nm CMOS", ISCAS 2015（`rx60.comm_iscas2015`）。
- 📥 M. Horowitz, "1.1 Computing's energy problem (and what we can do about it)", ISSCC 2014（`horowitz2014.*`）。
- 📥 S. Sarangi, B. Baas, "DeepScaleTool: A Tool for the Accurate Estimation of Technology Scaling in the Deep-Submicron Era", ISCAS 2021（`deepscale.*`）。
- ~~📥 IEEE 802.11-2020、802.11ax-2021、802.11ay-2021、802.11be（GET 计划，免费注册）~~ **不能用（2026-11-16）**：用户下载 IEEE 802.11-2024（已并入 11ay 等 7 个修正案）后，许可条款禁止把它输入 AI 系统，与 UCIe 规范同类。不读标准，也别请用户发；GET 计划里的其它 IEEE 标准（802.3dj / db 等）下载前同样先看条款。做法改为读 mentor.ieee.org 上的公开提案与厂商公开资料，再请用户对照标准核对（用户只说哪几行对不上，不把标准内容发过来）。
- ✅ #29 读的公开文件（2026-11-16，本地 PDF）：
  - IEEE 802.11-10/0433r2，TGad 采纳的完整提案规范文本（335 页，`ieee802_11_10_0433r2_tgad_cp_spec.pdf`）：21.3.3.8 灵敏度表与前提、21.3.4 Table 67、21.5 / 21.6 的 MCS、导频、SC 块、EVM。EVM 后来改过。
  - R&S 白皮书 1MA220_3e（2017-11，`rs_1ma220_3e_80211ad.pdf`）：Table 4-1 DMG 发射 EVM 与灵敏度（转引 802.11-2016 第 20 章）。
  - TGay：11-17/0597r1 OFDM 信号参数、11-17/0628r1 单信道导频序列、11-17/0909r0 OFDM MCS、11-15/1358r9 SFD（SC 的 GI 与 MCS）、11-18/0713r3 SC 性能要求（EVM）、11-18/1152r0 OFDM 性能要求（EVM）；采纳动议见 11-17/0186r37（各有本地 PDF，文件名以 `ieee802_11_` 开头）。都没有 AI 使用限制的字样。
  → `dmg.*`、`edmg.*`，并把 `ieee80211ay.channel_centres_ghz`、`dmg.sensitivity_assumptions` 改成 spec。
- ✅ #33 读的公开文件（2026-11-16，mentor.ieee.org）：TGad 11-10/0433r2（21.3.8 LDPC 矩阵、21.3.9 扰码、21.4 控制 PHY、21.5 / 21.6 编码流程、21.10.4 PHY 特性、7.2.1.16–18 SS 帧；公式是嵌入图片，从 docx 的 wmf 渲染出来读）；REVmc 11-16/0233r0（扩展 SC MCS、7/8 打孔）；TGay 11-16/1495r1（7/8 打孔的是前 48 个校验位）、SFD 11-15/1358r9（6.3.6 LDPC、6.9.1 Short SSW）、17/1061r1（1344 码长 7/8，动议 #264）、17/0214r1（EDMG SC 编码，动议 #178）、17/0018（Short SSW 文本，已进 SFD）→ #33 的 12 条，用户核对一致。
- ✅ 第 7 批读的 802.11 公开文件（2026-11-16，mentor.ieee.org）：TGn 联合提案 11-05/1102r4（Table 1 的 N_SD、4.3.3.4 LDPC PPDU 编码流程，步骤 (d) 是公式图）、TGac 框架 11-09/0992r21、TGax 11-15/0330r5（OFDMA 数字学）与框架 11-15/0132r17（Table 6 D_TM）、TGbe 框架 11-19/1262r23（Nsd_total 表、D_TM）→ `ieee80211ac.n_sd`、`ieee80211be.n_sd`、`ieee80211be.ldpc_tone_mapping_distance`、`ieee80211.ldpc_ppdu_encoding_thresholds`，用户对照标准核对一致。
- ✅ 47 CFR §15.255（www.ecfr.gov，2026-11-16 放行后读 2026-11-12 版的现行条文，该节最近修订 2023-08-23）→ `fcc15255.*`。(c)(2) 有雷达类器件的限值（ROADMAP）。
- ✅ Murmann ADC survey（github.com/bmurmann/ADC-survey，BSD-3，提交 00b4b85，`xls/ADCsurvey_rev20260801.xlsx`）：≥ 40 GS/s、4–7 nm 的 6 行时间交织 SAR → `adc_survey.ti_sar_ge40gs_4to7nm`，两条统计由它复算。
- ✅ arXiv:2309.16813v1（Liu 2025 的预印本 v1）第 V 节：'the specified PER (10−2 )' → `liu2025.per_target`。

## 合计

- 📥 要用户下载 27 篇：第 1 批 13 篇、UCIe 规范 1 篇、Harris 与人体 RCS 2 篇、802.3dj / 802.3db 2 篇、第 7 批 9 篇。另有 3 篇可选（Das Sharma、AEÜ、SAE）。2026-11-13 已下 4 篇（第 1 批 [1] [2] [6] [13]），2026-11-14 又下 1 篇（[15]），又下 2 篇（[9] [11]），又下 1 篇（Harris），2026-11-15 又下 1 篇（Liu 刊出版），还剩 18 篇（含因许可不能用的 UCIe 规范）。
- 🌐 放行站点后本库自己取 7 篇：TU Delft、Hot Chips、JRC、NHTSA、专利、OIF、eCFR。（TU Delft 那篇实为只有元数据，2026-11-14 由用户从 Xplore 下载）
- ✅ 已能取 3 篇（ITU-R P.676、arXiv 1910.13706 已读；剩 Murmann ADC survey）。

下载后把文件放进本目录，文件名用表里的编号或第一作者加年份（如 `asada_t1_01_chan_isscc2009.pdf`）。`*.pdf` / `*.doc` 不入库。

## 2026-11-16 · IEEE Xplore 的许可：本地的 12 篇 Xplore 原文已删

- 查许可时发现 IEEE Xplore 的使用条款限制 AI：个人 / 访客用户不得把 Xplore 内容直接或间接上传给 AI 工具；机构订阅不得把授权内容与 AI 工具结合使用（简短的学术引用除外），有的机构协议另许把少量文献交给不训练的 AI 工具做摘要；也不得把内容存放在 AI 工具里。**这是几次搜索结果的一致说法，条款原文没读到**：ieeexplore.ieee.org 的条款页对本环境返回 418，转述它的几个图书馆页面不在网络白名单里。
- 用户决定删掉本地副本。删了这 12 篇（`cairn/Reference/` 里的 PDF、会话上传目录里的原件、scratchpad 里由它们渲染的页面与抽出的文字，按哈希复查容器里没有剩下的）：第 1 批 Asada 表 [1] Chan、[2] Lai、[6] Law、[9] Kuo、[11] Jin、[13] Tanomura、[15] Martineau；第 2 批 Wu JSSC 2014、Staszewski TCAS-II 2006、Henzler ISSCC 2008；Harris Proc. IEEE 1978；Liu ComMag 2025。上面各行写的"本地 `…pdf`"已不在。
- 由它们建的条目不动：只有数值和简短引文。
- 还标 📥 的都在 Xplore 上：第 1 批 Asada 表 [5] [7] [8] [10] [12] [14]，第 7 批 Horowitz ISSCC 2014、ISCAS 2015 接收机、Okada JSSC 2013、DeepScaleTool ISCAS 2021，可选的 Das Sharma CPMT 2022。**不再请用户下载发来**；怎么取待用户定（公开版本加用户核对，或留 survey）。DeepScaleTool 有作者的 arXiv 预印本（2102.10195）与 GPLv3 的工具本身（SourceForge），不经 Xplore。Horowitz 能搜到的全文副本（gwern.net、一个大学的 restricted 目录）不是作者或 IEEE 授权的发布，不用。
- 不受影响的：mentor.ieee.org 的 802 工作组公开文件、Asada EuMC 2011（实验室网站）、arXiv、ITU-R、eCFR、NHTSA、Sandia、R&S、UCIe 联盟的公开材料、Murmann 的 GitHub。
- ✅ DeepScaleTool（2026-11-16，不经 Xplore）：作者预印本 arXiv:2102.10195v1（CC BY 4.0，6 页；正文只有 130 → 45 nm 等几个例子，Fig. 2 是工具截图、Fig. 3 是以 65 nm 为 1 的曲线）与工具本身 sourceforge.net/projects/deepscaletool 的 `DeepScaleTool/DeepScaleTool.xlsm`（GPLv3，2021-03-03，33 581 字节，sha256 561a3f8f…958df8）。能量倍数在 VBA 宏 `Sub Energy()` 里，用 olevba 当文本读出、没有执行 → `deepscale.energy_by_node`、`deepscale.node_scale_45_to_7nm`。两个文件放在 scratchpad，没放进本目录（`.xlsm` 不在 `.gitignore` 里）。

## 2026-11-17 · 用户发来 10 篇 IEEE Xplore 原文

- 上一节定的默认做法是不发 Xplore 原文；用户随后上传了 10 篇，经询问确认其许可允许交给本库读。读完删掉了本地副本：会话上传目录里的 10 个 PDF、scratchpad 里抽出的文字与渲染图。
- ✅ M. Horowitz，ISSCC 2014 1.1，doi 10.1109/ISSCC.2014.6757323：Figure 1.1.9（编码字体，渲染）→ `horowitz2014.*`。
- ✅ Asada Table I 的其余 6 行 → `pa60.suzuki_isscc2008`（[5]，doi …4523307）、`pa60.kurita_rfic2009`（[7]，doi 10.1109/RFIC.2009.5135485）、`pa60.bohsali_rfic2009`（[8]，…5135483）、`pa60.dawn_ims2009`（[10]，doi 10.1109/MWSYM.2009.5165752）、`pa60.pinel_isscc2008`（[12]，…4523091）、`pa60.chowdhury_isscc2008`（[14]，…4523306）。上面 [5] 那行"电压 1.0 V 对 1.2 V"的疑问：原文是 1.2 V。
- ✅ J. Luo 等，ISCAS 2015，doi 10.1109/ISCAS.2015.7169168 → `rx60.comm_iscas2015`（作者这次读到了：清华微电子所）。
- ✅ K. Okada 等，JSSC 48(1) 2013，doi 10.1109/JSSC.2012.2218066 → `antenna60.okada2013_dbi`。
- ✅ D. Das Sharma、G. Pasdast，IEEE Trans. CPMT 12(9) 2022，pp. 1423–1431，doi 10.1109/TCPMT.2022.3207195：II.A 'the advanced package supports spare lanes to handle faulty lanes (including clock, valid, and sideband) whereas the standard package supports width degradation to handle failures'；高级模块 'allocates two redundant bumps for every 32 data signals to repair'。没有写标准封装降到 x8 → `ucie.standard.lane_repair` 仍是 survey。
- DOI 取自各 PDF 的元数据（Subject 字段）。

## 2026-11-17 · #43：控制 PHY 的码字、EDMG 前导、OFDM 调制映射（mentor.ieee.org 公开文件）

- ✅ TGad 11-10/0433r2 21.4.3.3.2 Encoder（#33 时已下载；公式图 image103–117 渲染出来读）→ `dmg.control_phy_encoding`。
- ✅ TGay 11-17/1806r3 "30.12.3 TXTIME Calculation"：30.12.3.2（EDMG 控制模式）、30.12.3.3（EDMG SC）、30.12.3.5（非 EDMG 控制模式）、30.12.3.6（非 EDMG SC），公式图渲染出来读 → `dmg.sc_ppdu_chips`、`edmg.sc_siso_preamble`，并更正 `dmg.control_phy`、`dmg.phy_timing` 的前导（控制 STF 6400、SC STF 2176 码片）。
- ✅ 11-17/0277r0（EDMG 控制模式数据域）、11-17/1040r0（控制模式 PPDU 发送，动议 #245）→ `edmg.control_mode_encoding`。
- ✅ 11-17/1170r2（30.6.7.4 调制映射，动议 #275）、11-17/0870r3（30.6.7.2）、11-17/1568r0（30.6.8，动议 #328）、11-18/0331r2（DCM 改名）、11-18/0332r4（CID 1536、1537）→ `edmg.ofdm_modulation_mapping`。
- ✅ 11-17/0018r0、11-17/1586r1（Short SSW 例子，动议 #339）、11-19/0043r3（对 D2.2 的意见处理）、动议 #168 → 更正 `edmg.short_ssw` 的位宽。
- 没有：Short SSW 的 PPDU 类型与 MCS；EDMG OFDM 16 / 64-QAM 的交织置换；EDMG OFDM 的填充规则。TGay 2017–2019 年的文件目录（mentor 上约 1860 份）按标题筛过一遍。
- 用户 2026-11-17 对照 IEEE 802.11-2024 核对：后来的公开文件与标准一致（#33 时取自 0433r2 / 2015 年 SFD 的三处因此更正）。


## 2026-11-18 · #48：EDMG OFDM 包的训练场、DMG CEF、hFilt、Golay（mentor.ieee.org 公开文件）

- ✅ TGay 11-17/1806r3 30.12.3.4（EDMG OFDM 的 TXTIME，公式图 image47–55 渲染出来读）→ `edmg.ofdm_ppdu_ncb1`。
- ✅ 11-17/0596r0 "30.6.3 OFDM EDMG-CEF Definition"（动议 #219）：30.6.3.2 与 30.11 的 16 张序列表（前 8 张是 i_STS 1–8 的左半，后 8 张右半），公式图渲染出来读 → `edmg.ofdm_cef_ncb1`（只收 i_STS = 1）。
- ✅ 11-17/0546r0 "EDMG-STF for OFDM in single channel"（动议 #209），同样的排法 → `edmg.ofdm_stf_ncb1`（只收 i_STS = 1）。
- ✅ 11-17/1404r2（OFDM 前导与导频的意见处理，动议 #313）：对 EDMG-STF / EDMG-CEF 没有改动。
- ✅ TGad 11-10/0433r2（#33 时已下载）21.3.6.2 与图 134 / 135、21.3.6.3 与 21.3.6.3.1、21.9 与 Table 83–88 → `dmg.cef_golay_layout`、`dmg.ofdm_preamble_hfilt`、`dmg.golay_sequences`。
- 动议编号查自 11-17/0186r37（TGay 动议汇编，本地）。
- 没有：DMG SC / 控制 PHY 前导 STF 的最终组成（只有长度 2176 / 6400）；"数据信道用 EDMG-CEF 估"与"EDMG OFDM 包的 L-CEF 用 OFDM 排法"的原句（用户对照标准确认标准里有）。
- 用户 2026-11-18 对照 IEEE 802.11-2024 核对 N1–N6，一致。

## 2026-11-18 · #50：47 CFR §15.255(c)(2) 的雷达限值（eCFR）

- ✅ 47 CFR §15.255，eCFR 2026-11-16 版（该节最近修订仍是 2023-08-23，与 2026-11-16 读的 2026-11-12 版逐字节相同）：(b)(3)、(c)(2)(i)–(v)、(c)(3)、(c)(4)、(f)、(h)、(i) → `fcc15255.radar_*`（10 条）。eCFR 的 versioner API 现在要求响应压缩（curl 加 `--compressed`）。
- ✅ 47 CFR §15.3 Definitions（2023-08-23 版，即现行）：(l) Field disturbance sensor 的定义（雷达是它的一例）。没有 indoor / outdoor、fixed、vehicular 的定义。
- 没有读：§15.35(b)(c)（(c)(4) 说它们不适用于 (c)(2)、(3)）、§2.947 与它认可的测量规程（(i) 指向它们）。fmcw_radar 说这次不用去读。

## 2026-11-25 · #54：FCC 23-35（60 GHz 雷达规则）、47 CFR §2.1；TGbf 文件清单

- ✅ FCC 23-35，Report and Order，ET Docket No. 21-264，2023-05-18 通过、05-19 发布（docs.fcc.gov/public/attachments/FCC-23-35A1.pdf，41 页；Federal Register 88 FR 47384，2023-07-24，FR 文号 2023-15367，生效 2023-08-23，即 eCFR §15.255 的最近修订）。读了第 1–3、17–25、37、41–46、49–50、60–62 段，以及 Appendix B 里 §15.255(c)(2)(iv) 的条文。用于 #54 第二组的答复，不建条目。
- ✅ 47 CFR §2.1 Definitions（eCFR，该节最近修订 2026-02-13）：Radar、Radiodetermination 的定义（现行文本把 retransmitted 拼成 "retrainsmitted"，照录）。
- 读不到：Federal Register 的全文页（跳到 unblock.federalregister.gov 反爬页；API 的元数据能读）；FCC KDB 的检索（apps.fcc.gov/oetcf/kdb 的检索结果页返回 503）。
- TGbf（802.11bf）在 mentor 的文件清单 2020–2025 共 3105 个文件（含各版本，00bf 组 2247 个），DMG / EDMG 感知相关的约 110 个（SFD 11-21/0504r12、PDT、CC40 / LB272 / LB276 / LB281 / SA 投票的意见处理）；动议汇编 11-20/1874r96、11-23/0410r96。按 jcas60 的限制只读这些公开文件，不读标准与草案正文。

## 2026-11-25 · #54 第二部分：TGbf（802.11bf）与 TGay 的 TRN（mentor.ieee.org 公开文件）

- ✅ TGbf：SFD 11-21/0504r12；采纳的 PDT 与意见处理 22/0243r6、22/0295r5、22/0370r3、22/0947r3、22/0966r1、22/1112r1、22/1523r3、22/1524r4、22/1830r3、22/1915r5、22/2058r0、22/2073r2、23/0702r1、23/0751r1、23/1081r3、23/1082r1、23/0896r3、23/1544r2、23/2008r3、24/1351r2 等；提案 22/0799r1、22/0464r6、22/0781r2（未采纳）作对照；动议汇编 11-20/1874r96、11-23/0410r96 → `ieee80211bf.*`（5 条）。下载与文字稿在本会话的 scratchpad（i54/bf），不入库。
- ✅ TGay：17/0430r0（动议 #189，TRN 子字段与 TRN_BL）、17/0007r1（#152 采纳第 11–15 页；第 3、9 页描述 11ad 的 TRN / AGC）、17/0213r0（#179）、17/1806r3（#392，T_TRN 公式图渲染）、TGad 10/0433r2 21.8.2.2 → `dmg.trn_field`、`edmg.trn_field`。
- 没有：802.11bf 的标准与各版草案（许可禁止输入 AI，没有读）；单站是否要求全双工；DMG 感知只限 2.16 GHz 的明文；信道聚合时的感知；采纳文本里指明估信道用哪一段的句子。
- 用户 2026-11-25 对照 IEEE 802.11bf 与 802.11-2024 核对 S1–S7，一致。

## 2026-11-25 · #57：DMG Golay 序列的定稿版（TGay SFD）、双站 PPDU

- ✅ TGay SFD 11-15/1358r9（本地 PDF）6.10 Golay sequences：6.10.2 的 D_K、NOTE 2（i = 1 的 Ga / Gb 64、128 等于 20.11 的 DMG 序列）、Table 30 第 1 行的 W_K、Table 33、34、39、40 的 i = 1 序列（规范性的表；本库解析后与递推逐位相同）→ 更正 `dmg.golay_sequences`。0433r2 的 128 / 64 长 D / W 与表是 2010 年的旧版。
- ✅ TGad 11-12/0213r0（CID 6001，2012）：只把 Gu / Gv 的"complementary Golay"措辞删掉（它们不是互补对），与本库 #48 时算出的"只周期互补"一致；不涉及 D / W。TGad 2009–2012 文件清单 942 个，按标题筛 Golay / 序列 / 前导，没有别的改序列的文件。
- ✅ TGbf 22/0327r1（动议 #87，双站的 BRP 帧序）、SFD 21/0504r12 动议 #45、#46 → `ieee80211bf.dmg_bistatic_ppdu`；22/0132r6（#92）、22/1915r5（#221）、23/1081r3（#358）→ `ieee80211bf.dmg_monostatic_ppdu` 的补充；17/0430r0（TGay #189）→ `edmg.trn_field` 的旋转与第 1 流。
- 没有：DMG 定稿的 Ga32 / Gb32；EDMG TRN 的 π/2 旋转从哪个 n 起算。

## 2026-11-26 · #59：60 GHz 接收机压缩、长 Golay 对、BRP 帧

- ✅ M. Spasaro et al., IMS 2022 作者稿 arXiv:2406.12115（CC BY-NC-ND 4.0）：IV.A 与 Fig. 5(b)（渲染后按像素读图）→ `rx60.amp_spasaro2024_compression`。
- ✅ J. Moody, S. Lepanowski, T. Forbes（Sandia），SAND2025-02836C，OSTI 3022982 全文：Abstract、III 与 Fig. 7(b)（读图）→ `rx60.rx_moody2023_compression`。同一工作的摘要 OSTI 2004749 写 IP1dB −20.4 dBm（不一致，按全文）。
- ✅ Infineon BGT60TR13C Datasheet V2.4.9（2023-11-21）Table 55 → `rx60.radar_bgt60tr13c`。另读了英飞凌 BGT60UTR11AIP / ATR24C / CUTR13AIP / ATR24AIP 与 TI 多颗 60 / 77 GHz 雷达芯片的数据手册：都只有 P1dB，没有曲线与 IIP3，未建条目。
- 读不到：www.mdpi.com（403）、research.tue.nl（Cloudflare）、www.mouser.com（拒绝）；代理不放行 analog.com 等。MDPI 上有几篇 60 GHz 接收前端 / LNA 的论文（Electronics 14(10):2091、14(14):2819、13(21):4285，Applied Sciences 12(9):4468）没能读。
- ✅ TGay SFD 15/1358r9 Table 41–44、17/0430r0 新 Table 2 → `edmg.golay_sequences_long`。
- ✅ TGad 10/1291r2（D1.0 PHY CR：CID 508 STF 15 → 17 段、CID 1097 BRP 数据域至少 18 SC 块）、10/0833r2、10/0887r2、10/0944r1、11/0592r0（Gu512 改法被拒）、12/0213r0、10/0439r1（2010 年 STF 15 段的演示稿）；TGay 18/0400r0（#408）、17/0007r1、17/1674r0；TGbf 22/1495r6、22/2073r2、23/0896r3 → `ieee80211bf.dmg_bistatic_ppdu` 的更正与补充。
- 没有：L-STF 17 段的构成；BRP 帧的 MAC 头字节数与整帧长度；BRPIFS 从 20 µs 改到别的值的文件（公开材料只在两处提到 44 µs）。
