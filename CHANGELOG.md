# 变更记录 / Changelog

按版本记录。每条写**做了什么**和**为什么**；数字原值在 `cairn/LOG.md`。
下游重新 pin 时读这里：`consumers.yaml` 里登记的条目，数值或键名每变一次，这里就有一行 `` `<引用>` = <值> ``（铁律 4，`tests/test_consumers.py` 守着）。

## 未发布

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
