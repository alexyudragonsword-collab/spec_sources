# Project Cairn 日志

本文件按倒序记录实质性进展 —— 最新条目在本行正下方。每条保持简短（摘要 + 指针），
结论沉淀进 `cairn/<topic>.md`。

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
