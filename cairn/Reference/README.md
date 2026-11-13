# cairn/Reference：原文清单

这里放原文的读书笔记和待取清单。出版方的 PDF / .doc 只放本地，不入库（`.gitignore`）。

标记：📥 要用户下载（IEEE Xplore 对脚本返回空页；标准与 UCIe 规范要注册账号）· 🌐 免费，放行括号里的站点后本库自己取 · ✅ 本会话已能直接取。站点通不通是 2026-11-13 在环境 "rf design" 里实测的。

## 已读（本库取到原文）

| 文献 | 从哪里取 | 读了什么、落到哪里 |
|---|---|---|
| E. Perahia (Intel), "TGad Evaluation Methodology", IEEE 802.11-09/0296r16, 2010-01-20（另取 r09 对照） | mentor.ieee.org（2026-11-13 放行） | 3.2 Hardware impairments：9 条 `tgad_em.*` 由 survey 改为 spec（0.3.0），值不变；新增 `tgad_em.pn_params`、`pn_sides`、`pa_backoff_definition`、`pa_backoff_recommended_db`。公式是 .doc 里嵌入的公式对象，转成 PDF 后渲染第 4–5 页读的 |
| H. Asada et al., "A 60 GHz CMOS Power Amplifier Using Capacitive Cross-Coupling Neutralization with 16 % PAE", EuMC 2011 | www.ssc.p.isct.ac.jp（东工大并入科学东京后的实验室站点，已放行） | 参考文献表（下面第 1 批的 13 篇）；Table I 的 14 行与 `pa60.eumc2011_table1` 逐格一致 |

## 待取清单（按里程碑 2 的顺序）

### 第 1 批 · 60 GHz PA（决定 mmw60_trx 同台表每格的 MCS）

`tgad_em.*` 已核实。剩下的是 `pa60.eumc2011_table1` 里 Asada 转引的 13 行，要逐行对原文。全部 📥，8 篇是 ISSCC 文摘：

| Table I 行 | 文献 | Psat − P1dB / Psat |
|---|---|---|
| [1] | W. L. Chan, J. R. Long, M. Spirito, J. J. Pekarik, "A 60 GHz-Band 1V 11.5 dBm Power Amplifier with 11 % PAE in 65 nm CMOS", ISSCC 2009, pp. 380–381 | **9.0 dB（最大）** / 11.5 dBm |
| [2] | J. Lai, A. Valdes-Garcia, "A 1 V 17.9 dBm 60 GHz Power Amplifier in Standard 65 nm CMOS", ISSCC 2010, pp. 424–425 | 2.6 / **17.7 dBm（65 nm 最高）** |
| [5] | T. Suzuki, Y. Kawano, M. Sato, T. Hirose, K. Joshin, "60 and 77 GHz Power Amplifiers in Standard 90 nm CMOS", ISSCC 2008, pp. 562–563 | 2.4 / 10.6 |
| [6] | C. Y. Law, A. Pham, "A High-Gain 60 GHz Power Amplifier with 20 dBm Output Power in 90 nm CMOS", ISSCC 2010, pp. 426–428 | 1.7 / **19.9 dBm（最高）** |
| [7] | N. Kurita, H. Kondoh, "60 GHz and 80 GHz Wide Band Power Amplifier MMICs in 90 nm CMOS Technology", RFIC 2009, pp. 39–42 | 3.8 / 12.6 |
| [8] | M. Bohsali, A. Niknejad, "Current Combining 60 GHz CMOS Power Amplifiers", RFIC 2009（Asada 写的页码 39–42 与 [7] 相同，应是笔误，以 Xplore 为准） | 2.1 / 14.2 |
| [9] | J. L. Kuo, Z. M. Tsai, K. Y. Lin, H. Wang, "A 50 to 70 GHz Power Amplifier Using 90 nm CMOS Technology", IEEE MWCL vol. 19 no. 1, Jan. 2009, pp. 45–47 | 3.5 / 13.8 |
| [10] | D. Dawn et al., "60 GHz CMOS Power Amplifier with 20-dB Gain and 12 dBm Psat", IMS 2009, pp. 537–540 | 3.8 / 12.0 |
| [11] | Y. Jin, E. A. Rivero, M. A. T. Sanduleanu, J. R. Long, "A Millimeter-Wave Power Amplifier with 25 dB Power Gain and +8 dBm Saturated Output Power", ESSCIRC 2007, pp. 276–279 | 3.0 / 8.0 |
| [12] | S. Pinel et al., "A 90 nm CMOS 60 GHz Radio", ISSCC 2008, pp. 130–131 | 3.3 / 8.4 |
| [13] | M. Tanomura et al., "TX and RX Front-Ends for 60 GHz Band in 90 nm Standard Bulk CMOS", ISSCC 2008, pp. 558–559 | **1.0 dB（最小）** / 11.0 |
| [14] | D. Chowdhury, P. Reynaert, A. M. Niknejad, "A 60 GHz 1 V +12.3 dBm Transformer-Coupled Wideband PA in 90 nm CMOS", ISSCC 2008, pp. 560–561 | 3.3 / 12.3 |
| [15] | B. Martineau et al., "A 53-to-68 GHz 18 dB Power Amplifier with an 8-Way Combiner in Standard 65 nm CMOS", ISSCC 2010, pp. 428–429 | 5.6 / 16.6 |

**先下 4 篇**：[1]、[13]（Psat − P1dB 的两端）和 [6]、[2]（Psat 的两端）。表的分布（中位 3.3 dB）就是靠这几行撑起来的。[1] 和 [11] 出自 TU Delft 的 Long 组，机构库里可能有免费全文。

MDPI 那篇 22 nm PA（Georgakopoulos et al., "A 60-GHz Current Combining Class-AB Power Amplifier in 22 nm FD-SOI CMOS", Microwave 2026）**不取**：它只有版图后仿真，查到的内容里也没有 OFDM 的 EVM，给不了 mmw60 想要的 OFDM 工作点。

### 第 2 批 · TDC 抖动（fmcw_radar 的 1 ps 占位）
- 🌐 W. Wu, R. B. Staszewski, J. R. Long, "A 56.4-to-63.4 GHz Multi-Rate All-Digital Fractional-N PLL for FMCW Radar Applications in 65 nm CMOS", IEEE JSSC 49(5), pp. 1081–1096, 2014, doi 10.1109/JSSC.2014.2301764。TU Delft 机构库有免费全文（repository.tudelft.nl）；不放行就 📥 从 Xplore 下。

### 第 3 批 · UCIe 眼罩（d2d_link 的判定全悬在 0.65 UI 上）
- 📥 UCIe 规范 2.0 或 3.0（uciexpress.org，免费注册；3.0 加了 48 / 64 GT/s）。拿到它，其余 16 条 `ucie.*` 都能对原文核。
- 🌐 Hot Chips 2023 的 UCIe 教程 "Electrical Form Factor and Compliance"（www.hc2023.hotchips.org）。它写了 24–32 GT/s 的 40 mV / 0.65 UI，用来替代 ResearchGate 那篇二手转述（那篇不再找）。
- 可选 📥 D. Das Sharma et al., IEEE Trans. CPMT 2022。有了规范就用不着。

### 第 4 批 · fmcw_radar 的 9 条
- ✅ ITU-R P.676（www.itu.int）：两条氧气衰减。
- 📥 F. J. Harris, "On the use of windows for harmonic analysis with the discrete Fourier transform", Proc. IEEE 66(1), 1978：Table I，4 条窗函数主瓣宽度。
- 人体 RCS：✅ arXiv 1910.13706（行人在汽车雷达频段的极化 RCS）先读；不够再 📥 Belgiovane et al., IEEE Radar Conf. 2014（76–77 GHz 人体 RCS 实测），或 🌐 EC JRC 报告 JRC78619（publications.jrc.ec.europa.eu）。
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

- 📥 要用户下载 27 篇：第 1 批 13 篇、UCIe 规范 1 篇、Harris 与人体 RCS 2 篇、802.3dj / 802.3db 2 篇、第 7 批 9 篇。另有 3 篇可选（Das Sharma、AEÜ、SAE）。
- 🌐 放行站点后本库自己取 7 篇：TU Delft、Hot Chips、JRC、NHTSA、专利、OIF、eCFR。
- ✅ 已能取 3 篇。

下载后把文件放进本目录，文件名用表里的编号或第一作者加年份（如 `asada_t1_01_chan_isscc2009.pdf`）。`*.pdf` / `*.doc` 不入库。
