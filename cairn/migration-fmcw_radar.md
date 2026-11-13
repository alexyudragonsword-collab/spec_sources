# 迁移说明：fmcw_radar（第 2 个）

fmcw_radar 现在 vendor 了 mmw60_trx@ef0f00c 的 `spec.py` + `data/spec/survey.yaml`，用 5 条 `upstream: "mmw60_trx:<条目>#<字段>"` 读其中的数，自己解析 `@gain_db=40` 选择子和 `#a-b` 减法。迁移后改读 vendored 的 spec_sources：引用统一成读取器的 `ref()`，减法换成 spec_sources 的一条 derived。只搬家，不动数：**指纹逐位不变**。

`<PIN>` = spec_sources main 上合并里程碑 1 的提交的完整 SHA（合并后由用户填）。

## 1. vendor 哪些文件

目标目录 `src/fmcw_radar/vendor/spec_sources/`，原样拷贝，前面两行头：

```
# Vendored from spec_sources@<PIN>: src/spec_sources/<相对路径>
# Adapted-copy policy: see src/fmcw_radar/vendor/__init__.py
```

| 文件 | 说明 |
|---|---|
| `reader.py` | 读取器 |
| `data/frontend60.yaml` | 7 条：两颗接收机、雷达芯片的表与 Fig. 7-2、收发隔离与它的 derived、封装天线 |
| `__init__.py` | fmcw 的 `vendor_check` 把各包的 `__init__.py` 当成本库自己的、不核对：写自己的（docstring 写明 pin），里面 `from .reader import ref, survey, value, all_entries, audit_tags, data_files`；或原样拷 spec_sources 的也行 |

另外：

- **删** `vendor/mmw60/spec.py` 与 `vendor/mmw60/data/spec/survey.yaml`。**留** `vendor/mmw60/data/clock_profiles/pllsim_wu19_x10_60p48g_floor150.yaml`（LO 剖面，不是规范数字，仍 pin 在 mmw60_trx@ef0f00c），`vendor/mmw60/__init__.py` 的说明改成"只有 LO 剖面"。
- `pyproject.toml` 的 package-data：`"vendor/mmw60/data/spec/*.yaml"` 换成 `"vendor/spec_sources/data/*.yaml"`。
- `src/fmcw_radar/vendor/__init__.py` 的 Pins 节：mmw60 一条只剩剖面文件；加 spec_sources @ `<PIN>`。
- CI 的 vendor-drift：加 `repository: alexyudragonsword-collab/spec_sources`、`ref: <PIN>`、`path: _siblings/spec_sources` 与对应的 `--siblings`；mmw60_trx 那个 checkout 留着（剖面文件）。`tools/vendor_check.py` 已经核对 YAML，不用改。

## 2. 垫片：`src/fmcw_radar/sources.py` 与 `data/sources.yaml`

`data/sources.yaml` 里 5 条的 `upstream:` 改写（`value`、`cite`、`quote`、`section`、`note` 不动——这张表要能单独读）：

| 本库条目 | 原来 | 改成 |
|---|---|---|
| `60g_sensing.tx_power_dbm` | `mmw60_trx:rx60.radar_iwr6843#tx_power_dbm` | `spec_sources:rx60.radar_iwr6843#tx_power_dbm` |
| `60g_sensing.nf_db` | `mmw60_trx:rx60.radar_iwr6843#nf_db` | `spec_sources:rx60.radar_iwr6843#nf_db` |
| `60g_sensing.p1db_oob_dbm` | `mmw60_trx:rx60.radar_iwr6843#p1db_in_oob_dbm` | `spec_sources:rx60.radar_iwr6843#p1db_in_oob_dbm` |
| `60g_sensing.p1db_inband_dbm` | `mmw60_trx:rx60.radar_iwr6843_fig7_2#p1db_inband_dbm@gain_db=40` | `spec_sources:rx60.radar_iwr6843_fig7_2#p1db_inband_dbm@gain_db=40` |
| `60g_sensing.tx_rx_isolation_db` | `mmw60_trx:isolation.tx_rx_tue2018#with_ebg_db-improvement_max_db` | `spec_sources:isolation.tx_rx_tue2018_no_ebg_min_db` |

前四条只换了库名前缀，语法就是 `ref()` 的；第五条的减法在 spec_sources 是一条 derived（40 − 20 = 20 dB，note 写公式）。表头"upstream 一栏"那段说明同步改写（不要写成"标签词 + 冒号"）。

`upstream_value` 只剩查找：

```python
def upstream_value(ref: str) -> float:
    """The number ``ref`` names in spec_sources (``spec_sources:<reference>``; the
    reader's ref(): ``<key>[#<field>[@<axis>=<value>]]``, lookup only)."""
    repo, _, rest = ref.partition(":")
    if repo != "spec_sources" or not rest:
        raise ValueError(f"upstream {ref!r}: expected 'spec_sources:<reference>'")
    from .vendor.spec_sources import ref as lookup

    try:
        return float(lookup(rest))
    except KeyError as e:                       # keep this module's contract: a bad reference is a ValueError
        raise ValueError(f"upstream {ref!r}: {e}") from e
```

解析 `@` 与 `-` 的分支删掉。`load_sources` 里"不等就拒绝加载"的核对不动。

## 3. 测试怎么调：`tests/test_sources.py`（fmcw 的来源守卫）

- `test_sourced_front_end_figures_are_the_sibling_tables`：`from fmcw_radar.vendor.mmw60 import spec` 换成 `from fmcw_radar.vendor import spec_sources as ss`；`e.upstream.startswith("spec_sources:")`；`ss.value("rx60.radar_iwr6843")` 等照旧；隔离度改成 `ss.value("isolation.tx_rx_tue2018_no_ebg_min_db") == 20.0 == iso["with_ebg_db"] - iso["improvement_max_db"]`；`upstream_value("spec_sources:rx60.radar_iwr6843_fig7_2#p1db_inband_dbm@gain_db=48") == -42.0`。坏引用的清单换成 `"polar_tx:x#y"`、`"mmw60_trx:rx60.radar_iwr6843#nf_db"`（旧库名）、`"spec_sources:rx60.radar_iwr6843_fig7_2#p1db_inband_dbm@gain_db=41"`、`"spec_sources:isolation.tx_rx_tue2018#with_ebg_db-improvement_max_db"`（减法被拒），都 `pytest.raises(ValueError)`。
- `test_in_band_compression_follows_the_gain`：同样换 import。
- 加一条：vendored 的表四个标签都数得准——`for f in ss.data_files(): assert ss.audit_tags(f) == []`。
- `test_grep_lists_every_sourced_number`（数本库自己的表）不改。
- 以后新加 `upstream:` 要报回 spec_sources，登记进它的 `consumers.yaml`（spec_sources 看不到这张表）。

## 4. 验收

1. `python tools/fingerprint.py record` 迁移前后逐位相同；5 个数照旧是 12.0 / 12.0 / −12.0 / −34.0 / 20.0 dB(m)。
2. `python tools/vendor_check.py --strict` 绿：spec_sources 的 `reader.py` 与 `data/frontend60.yaml` verbatim，mmw60 只剩剖面文件。
3. `pytest` 与 `ruff check .` 绿。

## 5. 里程碑 2 再迁的 14 条（本轮只列清单）

fmcw_radar@2e5cbb6 自己表里 spec / survey 共 14 条：

- 已登记的 5 条前端数（spec；数已经在 spec_sources，迁移后这 5 条的 `upstream:` 就是登记）：`60g_sensing.tx_power_dbm`、`60g_sensing.nf_db`、`60g_sensing.p1db_oob_dbm`、`60g_sensing.p1db_inband_dbm`、`60g_sensing.tx_rx_isolation_db`。
- 只在 fmcw 的 9 条 survey（里程碑 2 迁进 spec_sources 并核实，fmcw 改成引用）：
  - 大气：`oxygen.60g_db_per_km`、`oxygen.77g_db_per_km`（ITU-R P.676）
  - RCS：`rcs.human_dbsm`、`rcs.car_dbsm`、`rcs.corner_reflector_dbsm`
  - 窗函数主瓣宽度：`window.rect_3db_bins`、`window.hann_3db_bins`、`window.hamming_3db_bins`、`window.blackman_3db_bins`（Harris 1978 Table I）

另外 25 条 assumed（前端占位、77 GHz 一档）是 fmcw 自己的取舍，留在 fmcw。
