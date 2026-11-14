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
- 原文只给分辨率不给 TDC 自身的抖动。fmcw 若要 `tdc_jitter_s` 的出处，下一篇是 Wu 文的 [23]：📥 R. B. Staszewski, S. Vemulapalli, P. Vallur, J. Wallberg, P. T. Balsara, "1.3 V 20 ps Time-to-Digital Converter for Frequency Synthesis in 90-nm CMOS", IEEE TCAS-II 53(3), pp. 220–224, 2006（同一种伪差分延迟链 TDC；有没有抖动数要读了才知道）。

### 第 3 批 · UCIe 眼罩（d2d_link 的判定全悬在 0.65 UI 上）
- 📥 UCIe 规范 2.0 或 3.0（uciexpress.org，免费注册；3.0 加了 48 / 64 GT/s）。拿到它，其余 16 条 `ucie.*` 都能对原文核。
- 🌐 Hot Chips 2023 的 UCIe 教程 "Electrical Form Factor and Compliance"（www.hc2023.hotchips.org）。它写了 24–32 GT/s 的 40 mV / 0.65 UI，用来替代 ResearchGate 那篇二手转述（那篇不再找）。
- 可选 📥 D. Das Sharma et al., IEEE Trans. CPMT 2022。有了规范就用不着。

### 第 4 批 · fmcw_radar 的 9 条
- ~~✅ ITU-R P.676~~ 已读（见上表）。
- 📥 F. J. Harris, "On the use of windows for harmonic analysis with the discrete Fourier transform", Proc. IEEE 66(1), 1978：Table I，4 条窗函数主瓣宽度。
- 人体 RCS：arXiv 1910.13706 已读，但只有仿真。要实测值 📥 Belgiovane et al., IEEE Radar Conf. 2014（76–77 GHz 人体 RCS 实测），或 🌐 EC JRC 报告 JRC78619（publications.jrc.ec.europa.eu）。
- 车辆 RCS：🌐 NHTSA DOT HS 813 648（rosap.ntl.bts.gov，76–77 GHz，ISO 19206-3）；可选 📥 SAE 2021-01-5103。
- 角反射器：教科书公式，不用取。

### 第 5 批 · array_tx 的互耦（它的 ROADMAP A1）
array_tx 要的是面阵实测的复数 S 参数（.sNp），能读到的论文里都没有。下面两篇只给幅度，取了也只能把 −16 dB 从 assumed 升成 survey，相位仍然缺：
- 可选 📥 Int. J. Electron. Commun.（AEÜ，ScienceDirect S1434841126001263）。
- 🌐 美国专利 10910732（patents.google.com）。

### 第 6 批 · Halo_Serdes ROADMAP P3 #11 的 4 条条文
- 📥 IEEE 802.3dj：TDECQ 的前后抽头差、逐抽头 w(i)/w(0) 上下限；DR1 上限是否降到 3.0 dB。到 2025 年底还是草案；批准后走 GET 计划免费。
- 📥 IEEE 802.3db-2022：f_A（GET 计划免费）。
- 🌐 OIF-CEI-112G-LINEAR-PAM4 实施协议（www.oiforum.com，免费）：CTLE 档位表 Table 29-2 / 29-8。

### 第 7 批 · 其余 survey（mmw60_trx 带来的）
- 📥 X. Liu et al., "Wi-Fi 8: Embracing the Millimeter-Wave Era", IEEE Commun. Mag., Mar. 2025（刊出版；arXiv v1 / v2 已读）。
- 📥 K. Okada et al., "Full Four-Channel 6.3-Gb/s 60-GHz CMOS Transceiver With Low-Power Analog and Digital Baseband Circuitry", IEEE JSSC 48(1), 2013（`antenna60.okada2013_dbi`；东工大实验室站点上可能有，先在那里找）。
- 📥 "A 64 dB Gain 60 GHz Receiver with 7.1 dB Noise Figure for 802.11ad Applications in 90 nm CMOS", ISCAS 2015（`rx60.comm_iscas2015`）。
- 📥 M. Horowitz, "1.1 Computing's energy problem (and what we can do about it)", ISSCC 2014（`horowitz2014.*`）。
- 📥 S. Sarangi, B. Baas, "DeepScaleTool: A Tool for the Accurate Estimation of Technology Scaling in the Deep-Submicron Era", ISCAS 2021（`deepscale.*`）。
- 📥 IEEE 802.11-2020、802.11ax-2021、802.11ay-2021、802.11be（GET 计划，免费注册）：N_SD、LDPC 编码流程与音调映射距离、DMG 灵敏度表的前提、信道化。
- 🌐 47 CFR §15.255（www.ecfr.gov）：`fcc15255.*`。
- ✅ Murmann ADC survey（GitHub 仓库，git 克隆）：`adc_survey.*`。

## 合计

- 📥 要用户下载 27 篇：第 1 批 13 篇、UCIe 规范 1 篇、Harris 与人体 RCS 2 篇、802.3dj / 802.3db 2 篇、第 7 批 9 篇。另有 3 篇可选（Das Sharma、AEÜ、SAE）。2026-11-13 已下 4 篇（第 1 批 [1] [2] [6] [13]），2026-11-14 又下 1 篇（[15]），又下 2 篇（[9] [11]），还剩 20 篇。
- 🌐 放行站点后本库自己取 7 篇：TU Delft、Hot Chips、JRC、NHTSA、专利、OIF、eCFR。（TU Delft 那篇实为只有元数据，2026-11-14 由用户从 Xplore 下载）
- ✅ 已能取 3 篇（ITU-R P.676、arXiv 1910.13706 已读；剩 Murmann ADC survey）。

下载后把文件放进本目录，文件名用表里的编号或第一作者加年份（如 `asada_t1_01_chan_isscc2009.pdf`）。`*.pdf` / `*.doc` 不入库。
