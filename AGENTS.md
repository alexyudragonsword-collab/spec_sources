# spec_sources 协作规则

> 本项目使用 Project Cairn：`AGENTS.md` 是规则与导航入口，`cairn/` 是项目知识/状态层。同目录 `CLAUDE.md` 只有一行 `@AGENTS.md`，使 Claude Code 读到同一份规则；Codex 直接读本文件。

## 项目一句话

带出处的规范 / 文献数字表 + 读取器 + 守卫，不做任何仿真。规范条文、论文与数据手册的数，以及只由它们推出的数，在这里各登记一次；mmw60_trx、fmcw_radar、d2d_link 等把 `src/spec_sources/` 按完整 SHA vendor 进去，按键读。

## Init 配置

- 毕业 provider：暂缓对接（首次毕业时再接知识库）
- 知识库索引 / 毕业目标：尚未配置

## 进入项目后的阅读顺序

1. 先读本文件。
2. 读根目录 `ROADMAP.md`（只写没做的，含"报回上游"节）。
3. 读 `cairn/LOG.md` 最新几条（新条目在顶部）。
4. 有进行中的迁移时读 `cairn/migration-<库>.md`（迁完验收后即删）；谁读了本库的什么在 `consumers.yaml`。

## 文档职责

| 文件 | 角色 | 维护方式 |
|---|---|---|
| `AGENTS.md` / `CLAUDE.md` | 规则与导航 / 单行存根 | 很少变 |
| `ROADMAP.md` | 待办与优先级 | 只写没做的；做完即删，在 CHANGELOG 与 LOG 记一笔 |
| `CHANGELOG.md` | 按版本的变更；下游重新 pin 时读它 | 每个版本一节；登记条目的改动逐条写 |
| `cairn/LOG.md` | 时间序日志，新条目在顶部 | 每条 ≤ 20 行，带条数与数字原值 |
| `cairn/migration-<库>.md` | 给消费方的迁移说明 | 那个库迁完后删，LOG 记一笔 |
| `cairn/Reference/` | 原文摘录与读书笔记（出版方 PDF 只放本地，`.gitignore`） | 按需创建，只追加 |

## 代码与数据的布局

- `src/spec_sources/reader.py`：读取器（`SpecNumber`、`SOURCES`、`load_table`、`all_entries`、`survey`、`value`、`unverified`、`by_source` 与 mmw60_trx 的 `mmw60.spec` 同名同义，外加 `ref`、`aliases`、`legacy_keys`、`merge_tables`、`audit_tags`）。`__init__.py` 只转出。
- `src/spec_sources/data/<领域>.yaml`：按**出处的领域**切，一个文件一组前缀；消费方只 vendor 它读的那几个文件。
  `data/liu2025.yaml`（liu2025.\*，Liu 2025 论文）· `data/ieee80211.yaml`（tgad_em.\*、ieee80211.\*、ieee80211ac / be / ay.\*、dmg.\*：802.11 条文、TGad 评估方法学、ITU-R M.2003）· `data/regulatory.yaml`（fcc15255.\*）· `data/frontend60.yaml`（rx60.\*、isolation.\*、antenna60.\*：60 GHz 前端测量值）· `data/pa60.yaml`（pa60.\*：60 GHz PA 测量值）· `data/energy.yaml`（horowitz2014.\*、adc_survey.\*、deepscale.\*：运算能耗、ADC FoM、工艺缩放）· `data/atmosphere.yaml`（itu_p676.\*：大气衰减）· `data/radar_targets.yaml`（target_rcs.\*：雷达目标 RCS）· `data/ucie.yaml`（ucie.\*）。
  新领域开新文件，并在 `tests/test_iron_rules.py::FILE_PREFIXES` 登记它的前缀。
- `src/spec_sources/legacy_keys/<库>.yaml`：某个消费方的旧键名 → 本库键名，给它的垫片用（现在只有 d2d_link）。
- `consumers.yaml`（根）：被下游读取的条目登记。`keys.lock`（根）：发布过的每个键的账本。
- `tests/fixtures/`：迁入时的源表原文件，文件头是库名与完整 SHA；只读。

## 项目铁律（每条都有测试守着）

1. **每条带 `source` ∈ {spec, survey, assumed, derived}**：spec 必须带 quote + section，survey 的 note 必须写"未核实"，cite 必填（`SpecNumber.__post_init__`，沿用 mmw60_trx；`test_reader.py::test_spec_number_refuses_*`、`test_iron_rules.py::test_rule1_*`）。
2. **只收关于外部世界的数**：规范条文、论文与数据手册的数，以及只由它们推出的 derived。某个库自己的取舍（mmw60_trx 的 assumed.\*）与它自己的产出（仿真读数、姊妹库的综合估计、指向它仓库里文件的条目）留在那个库，用本库的 `load_table` 读它本地的表。共享表里 assumed 为零；每条 derived 在 `test_iron_rules.py::RECOMPUTE` 里只用共享条目复算（`test_rule2_*`）。
3. **键名全局唯一，带领域前缀**（liu2025.、pa60.、rx60.、ucie.……）。改名或删除走弃用期：旧键写进数据文件的 `aliases:`（读取时 `DeprecatedKeyWarning`），`keys.lock` 补 `aliased=`，至少再过一个版本才能 `retired=`。标签（spec / survey / assumed / derived）不能当前缀：mmw60_trx 带来的 17 个这样的键 0.2.0 改名、0.3.0 退役了别名（`test_rule3_*`）。
4. **被下游读取的条目登记在 `consumers.yaml`**：在自己表里抄了数的引用按条登记（库、键、字段、值），改这些条目的数值或键名必须同时改登记，并在 CHANGELOG 写一行 `` `<引用>` = <值> ``；整份 vendor 的按文件登记（`vendored:`：库、pin、文件），这些文件在它的 pin 之后改了，CHANGELOG 写 `` `<库>` 需重新 pin ``（`test_consumers.py`）。
5. **grep 计数守卫覆盖全部四个标签**：对每个数据文件，`grep -c "source: <标签>"` 等于该标签的条目数；注释与说明（cite / note / quote / section / unit）里一律不写"标签词 + 冒号"（`audit_tags`，消费方的本地表也用它）。共享表更严：整个文件只有标签行带它，`grep -c "source:"` 等于条目数（`test_rule5_*` 跑真的 grep）。
6. **引用只做查找，不做计算**：`ref("<键>[#<字段>[@<轴>=<值>]]")`。差、比、换算都是本库一条 derived 条目，note 写公式（`test_reader.py::test_ref_*`、`test_consumers.py`）。

## 本仓库特有的硬规矩

- **`src/spec_sources/` 单独拷出去就要能用**：只依赖 PyYAML，只用相对导入，数据挨着代码找。消费方 vendor 它、pin 完整 SHA、过 `vendor_check --strict`（`test_vendored_copy.py` 从临时拷贝里 import 并运行）。
- **迁入的条目逐字段等于源表**；迁入时改过的字段列在 `tests/test_extraction.py::CHANGED`（每处只是一次替换）。核实后改成 spec 的条目列在 `VERIFIED`（值与单位仍等于源表）。原文清单与读书笔记在 `cairn/Reference/README.md`。
- **不改消费方的仓库**：需要它们做的写进 ROADMAP 的"报回上游"节，并在那个库开 issue（标题以"spec_sources 收件："开头；对方迁完在 issue 里回报，本库验收后关）。
- 提交信息写为什么，带实测数字。在 `feat/*` 分支上开 PR 合 main。

## 冲突仲裁

- 优先级：**原文 > 数据表与测试 > 知识专题文档 > LOG 历史**；规则层面的冲突由本文件裁定。

## 知识沉淀规则

- 每次实质性推进后，在 `cairn/LOG.md` 顶部加一条（摘要 + 指针，带条数）。修正过去的判断时追加更正说明，不要静默覆盖。
- 每个里程碑结束：CHANGELOG 一节、LOG 一条、ROADMAP 删掉做完的并加上过程中发现的问题（带复现方式和数字）。
