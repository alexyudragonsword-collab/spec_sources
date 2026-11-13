# 迁移说明：mmw60_trx（第 1 个）

把 `src/mmw60/data/spec/survey.yaml` 里关于外部世界的 63 条换成 vendored 的 spec_sources，`mmw60/spec.py` 留成薄垫片。只搬家，不动数：**指纹逐位不变**，示例输出不变（键名一个都没改）。

`<PIN>` = spec_sources main 上合并里程碑 1 的提交的完整 SHA（合并后由用户填）。

## 1. vendor 哪些文件

目标目录 `src/mmw60/vendor/spec_sources/`，每个文件原样拷贝，前面加两行头（YAML 也一样，`#` 注释）：

```
# Vendored from spec_sources@<PIN>: src/spec_sources/<相对路径>
# Adapted-copy policy: see src/mmw60/vendor/__init__.py
```

| 文件 | 说明 |
|---|---|
| `__init__.py`、`reader.py` | 读取器（只依赖 PyYAML，相对导入） |
| `data/liu2025.yaml`、`data/ieee80211.yaml`、`data/regulatory.yaml`、`data/frontend60.yaml`、`data/pa60.yaml`、`data/energy.yaml` | 64 条：从本库迁出的 63 条 + 新的 `isolation.tx_rx_tue2018_no_ebg_min_db` |

不拷 `data/ucie.yaml` 与 `legacy_keys/`。另外：

- `pyproject.toml` 的 package-data 加 `"vendor/spec_sources/data/*.yaml"`（装好的包也要找得到）。
- `src/mmw60/vendor/__init__.py` 的 Pins 节加一条 spec_sources @ `<PIN>`。
- `tools/vendor_check.py` 的 `vendored_files()` 现在只收 `*.py`：照 fmcw_radar 的写法加上 `VENDOR.rglob("*.yaml")`，否则 6 个数据文件不被核对。
- CI 的 vendor-drift 作业加一个 checkout（公开库，不要 token）：`repository: alexyudragonsword-collab/spec_sources`，`ref: <PIN>`，`path: _siblings/spec_sources`，命令行加 `--siblings spec_sources=${{ github.workspace }}/_siblings/spec_sources`。本地默认根 `/home/user` 下有 `spec_sources/` 即可。

## 2. 本地表：`src/mmw60/data/spec/survey.yaml`

删掉下面 63 条（按共享表的文件分组），留 62 条：assumed 56、derived 3、survey 3。漏删一条，垫片的 `merge_tables` 会报 `key '…' is in two tables`。

- `data/energy.yaml`（5）：`survey.horowitz_mult32_pj`、`survey.horowitz_add32_pj`、`survey.walden_fom_fj`、`survey.walden_fom_range_fj`、`survey.node_scale_45_to_7nm`
- `data/frontend60.yaml`（6，另一条是新的）：`rx60.comm_asada2011`、`survey.rx60_comm_iscas2015`、`rx60.radar_iwr6843`、`rx60.radar_iwr6843_fig7_2`、`isolation.tx_rx_tue2018`、`survey.antenna60_okada2013_dbi`
- `data/ieee80211.yaml`（17）：`tgad_em.pa_rapp_g`、`tgad_em.pa_rapp_asat`、`tgad_em.pa_rapp_p`、`tgad_em.pa_ampm_alpha`、`tgad_em.pa_ampm_beta`、`tgad_em.pa_ampm_q1`、`tgad_em.pa_ampm_q2`、`tgad_em.pa_model_shape`、`tgad_em.pn_model_shape`、`derived.rapp_p1db_below_psat_db`、`ieee80211ay.channel_centres_ghz`、`survey.n_sd_11ac`、`survey.n_sd_11be`、`survey.dmg_sensitivity_assumptions`、`dmg.rx_max_input_dbm`、`survey.eht_tone_mapper_dtm`、`survey.ldpc_ppdu_encoding_thresholds`
- `data/liu2025.yaml`（25）：`liu2025.*` 全部 22 条、`derived.cfo_liu2025_hz`、`derived.k_threshold_stf`、`derived.k_threshold_ltf_only`
- `data/pa60.yaml`（6）：`pa60.asada_eumc2011`、`pa60.wu_asscc2012`、`pa60.ning_elex2011`、`pa60.eumc2011_table1`、`pa60.wu_isscc2015`、`derived.pa60_rapp_p_asada_eumc2011`
- `data/regulatory.yaml`（4）：`fcc15255.eirp_avg_dbm`、`fcc15255.eirp_peak_dbm`、`fcc15255.band_low_hz`、`fcc15255.band_high_hz`

留下的 6 条非 assumed（理由在 spec_sources `tests/test_extraction.py::MMW60_STAYS`）：`derived.isi_beyond_gi_k16_db`（用 `assumed.cr_rms_delay_ns`）、`derived.pa60_obo_at_evm_limit_db`（用 `assumed.pa60_operating_rule`）、`derived.irr_after_cal_measured_db`（示例 03 的读数）、`survey.clock_profile_wu19`、`survey.clock_profile_wu19_x10`（值是本仓库 `data/clock_profiles/` 里的文件名）、`survey.dsp_ip_dpd_poly_p4`（姊妹库的综合估计）。

表头要改写：现在第 9–10 行写着 `"source: xxx"` 与 `grep -c "source: <标签>"`，含"标签词 + 冒号"，`audit_tags` 会报。第 636 行那条注释随 D4 节的 spec 条目一起走了（共享表的 `data/frontend60.yaml` 文件头里有改写后的版本）。表头写明：外部的数在 vendored spec_sources，这里只有本库的取舍、本库的产出与 3 条留下的 survey。

## 3. 垫片：`src/mmw60/spec.py`

公开名字一个不少：`SpecNumber`、`SOURCES`、`load_table`、`all_entries`、`survey`、`value`、`unverified`、`by_source`、`DATA_DIR`、`SURVEY_FILE`，以及 fig4 / LDPC / PER 门限那几组（`FIG4_FILE`、`LDPC_FILE`、`THRESHOLDS_FILE`、`fig4_readings`、`ldpc_document`、`ldpc_base_matrices`、`per_threshold_document`、`per_threshold_db`，**原样不动**）。加一个 `ref`。

```python
from .vendor import spec_sources as _shared
from .vendor.spec_sources import SOURCES, SpecNumber  # noqa: F401  (re-exported)

DATA_DIR = Path(__file__).resolve().parent / "data" / "spec"
SURVEY_FILE = DATA_DIR / "survey.yaml"     # 只剩本库的表：assumed 56、derived 3、survey 3
...

def load_table(path: Path = SURVEY_FILE) -> dict[str, SpecNumber]:
    return _shared.load_table(path)        # 默认参数保持原义：本地表


_TABLE: dict[str, SpecNumber] | None = None


def all_entries() -> dict[str, SpecNumber]:
    """vendored 的共享表 + 本库的表；同一个键出现两次是错误。"""
    global _TABLE
    if _TABLE is None:
        _TABLE = _shared.merge_tables(_shared.all_entries(), load_table())
    return _TABLE


def ref(reference: str):
    return _shared.ref(reference, all_entries())

# survey / value / unverified / by_source：函数体不变（都走 all_entries()）
```

`SpecNumber` 是 vendored 的那个类：字段名、顺序、默认值、校验信息与原来的逐字相同，`tests/test_spec_sources.py` 里按位置构造的用法不用改。合并后的表 126 条（125 + 新的隔离度 derived），每个旧键的 `value` 都与 13024e0 相同（数据是逐字迁的）。

## 4. 测试怎么调：`tests/test_spec_sources.py`

- `test_grep_lists_every_unverified_number`、`test_grep_lists_every_assumed_number`：`spec.unverified()` / `by_source()` 现在跨两张表，不能再和一个文件的 grep 比。换成每张表各自四个标签都数：
  ```python
  def test_grep_counts_every_tag_in_every_table():
      from mmw60.vendor import spec_sources as ss
      local = spec.load_table()
      for tag in spec.SOURCES:
          out = subprocess.run(["grep", "-c", f"source: {tag}", str(spec.SURVEY_FILE)], capture_output=True, text=True)
          assert int(out.stdout.strip() or 0) == sum(e.source == tag for e in local.values()), tag
      for f in [spec.SURVEY_FILE, *ss.data_files()]:
          assert ss.audit_tags(f) == [], f
  ```
- 加一条：本地表只剩该剩的——`{e.source for e in spec.load_table().values()} == {"assumed", "derived", "survey"}`，3 条 survey 正是上面那 3 条，且与共享表没有交集（`spec.all_entries()` 能建起来就说明没有）。
- `test_derived_entries_follow_their_formulas`、`test_every_entry_is_tagged_and_cited`、`test_spec_source_needs_a_quote_and_survey_needs_unverified`、`test_unknown_key_names_what_exists`、fig4 / LDPC 两条：不改。
- `test_entries_a_downstream_library_reads_keep_their_keys_fields_and_values`：守的东西搬到了 spec_sources（`consumers.yaml` + `tests/test_consumers.py`）。fmcw_radar 迁完（它不再 vendor 本库的表）之后删掉；在那之前留着，照样绿。
- 迁移前后各跑一次，核对每个旧键的值：
  ```python
  old = yaml.safe_load(subprocess.run(["git", "show", "13024e0:src/mmw60/data/spec/survey.yaml"], ...).stdout)["entries"]
  assert all(spec.value(k) == e["value"] for k, e in old.items())
  ```

## 5. 文档

- `AGENTS.md` 铁律 5：外部的数在 vendored spec_sources（`src/mmw60/vendor/spec_sources/data/`），本库自己的 assumed / derived 在 `data/spec/survey.yaml`；grep 守卫覆盖两边、四个标签。
- `cairn/spec-sources.md` 的"制度"一节同上；"本库定的假设清单"不变。
- `CHANGELOG.md` 一条：vendor spec_sources @ `<PIN>`，表从 125 条变成 62 条本地 + 64 条共享，指纹不变。

## 6. 验收

1. `python tools/fingerprint.py record` 迁移前后各一次，`compare` 逐位相同；提交信息不带 `(numbers-move`。
2. `examples/expected/` 不动（键名没改，04 / 08 / 09 打印的键名照旧）。
3. `python tools/vendor_check.py --strict` 绿，spec_sources 的 8 个文件都是 verbatim。
4. `pytest` 与 `ruff check .` 绿。
