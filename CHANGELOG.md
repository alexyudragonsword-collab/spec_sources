# 变更记录 / Changelog

按版本记录。每条写**做了什么**和**为什么**；数字原值在 `cairn/LOG.md`。
下游重新 pin 时读这里：`consumers.yaml` 里登记的条目，数值或键名每变一次，这里就有一行 `` `<引用>` = <值> ``（铁律 4，`tests/test_consumers.py` 守着）。

## 未发布

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
