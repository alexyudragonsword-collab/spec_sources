# 迁移说明：d2d_link（第 3 个）

把 `src/d2d_link/data/spec/ucie_survey.yaml` 的 16 条换成 vendored 的 spec_sources `data/ucie.yaml`（键名加了 `ucie.` 前缀）。`d2d_link/spec` 用别名表 `legacy_keys/d2d_link.yaml` 把它们按旧的裸键名接住，所以 `survey("reach_mm", "standard")`、`survey_tiered(...)`、报告里打印的键名全都照旧。只搬家，不动数：**指纹逐位不变**。

`<PIN>` = spec_sources main 上合并里程碑 1 的提交的完整 SHA（合并后由用户填）。

## 1. vendor 哪些文件

目标目录 `src/d2d_link/vendor/spec_sources/`，原样拷贝，前面两行头：

```
# Vendored from spec_sources@<PIN>: src/spec_sources/<相对路径>
# Adapted-copy policy: see src/d2d_link/vendor/__init__.py
```

| 文件 | 说明 |
|---|---|
| `reader.py` | 读取器 |
| `data/ucie.yaml` | 16 条，全是 survey |
| `legacy_keys/d2d_link.yaml` | 旧裸键名 → `ucie.` 键名，一一对应，顺序同原表 |
| `__init__.py` | d2d 的 `vendor_check` 跳过所有 `__init__.py`：写自己的（docstring 写明 pin），或原样拷 |

另外：

- **删** `src/d2d_link/data/spec/ucie_survey.yaml`；`model_presets.yaml`（`source: model` 的 30 条估计）不动，仍用 d2d 自己的 `load_survey(..., allowed=("model",))` 读——`model` 不是 spec_sources 的标签，那是 d2d 自己的取舍。
- `pyproject.toml` 的 package-data 加 `"vendor/spec_sources/data/*.yaml"`、`"vendor/spec_sources/legacy_keys/*.yaml"`。
- `tools/vendor_check.py` 只扫 `*.py`（第 176、254 行的 `VENDOR.rglob("*.py")`）：照 fmcw_radar 的写法加上 `*.yaml`，否则两个 YAML 不被核对。
- CI 的 vendor-drift：加 `repository: alexyudragonsword-collab/spec_sources`、`ref: <PIN>`、`path: _siblings/spec_sources` 与对应的 `--siblings`。

## 2. 垫片：`src/d2d_link/spec/__init__.py`

公开名字一个不少（`SpecNumber`、`survey`、`survey_tiered`、`tier_keys`、`all_entries`、`unverified`、`load_survey`、`SURVEY_FILE`、`SOURCES`、`preset`、`all_presets`、`preset_values`、`PRESETS_FILE`），`SpecNumber` 仍是 d2d 自己的类（`survey` / `spec` / `model`，`tag()`、`estimated`）。只改两处：

```python
VENDOR_DIR = Path(__file__).resolve().parents[1] / "vendor" / "spec_sources"
SURVEY_FILE = VENDOR_DIR / "data" / "ucie.yaml"


@lru_cache(maxsize=1)
def _table() -> dict[str, SpecNumber]:
    """spec_sources 的 ucie.* 条目，按旧的裸键名（legacy_keys/d2d_link.yaml，原表的顺序）。"""
    from ..vendor.spec_sources import reader as ss

    shared = ss.load_table(SURVEY_FILE)
    out = {}
    for old, new in ss.legacy_keys("d2d_link").items():
        e = shared[new]
        out[old] = SpecNumber(key=old, value=e.value, unit=e.unit, source=e.source, cite=e.cite,
                              note=e.note, quote=e.quote or "", section=e.section or "")
    return out
```

`quote` / `section` 在 spec_sources 缺省是 `None`，d2d 的是 `""`：上面换成 `""`，与原来逐字相同。`tier_keys`、`_range_entry`、`survey_tiered` 不改：它们按旧键名查，`rx_eye_width_ui@24-32` 的区间档照旧（表的顺序也照旧）。

16 条里只有一处字段变了：`ucie.rx_eye_width_ui@24-32` 的 note 里"改 source: spec 或删去"改成"改成 spec 标签或删去"（铁律 5：note 里不许写"标签词 + 冒号"，原表 `grep -c "source: spec"` 得 2、实际 0）。d2d 的代码不打印 note（`src/` 里没有 `.note` 的用法），输出不受影响。

## 3. 测试怎么调：`tests/test_spec_sources.py`

- `test_grep_lists_every_unverified_number`：grep 的是新的 `SURVEY_FILE`（vendored `ucie.yaml`），仍是 16，不用改；再加四个标签的守卫：`ss.audit_tags(spec.SURVEY_FILE) == []`。
- `test_data_ships_inside_the_package`：`spec.SURVEY_FILE.is_relative_to(PACKAGE_DIR / "vendor" / "spec_sources" / "data")`；pyproject 的正则加上 vendor 的两个 glob。
- `test_model_presets_are_tagged_and_grep_able` 里 `spec.load_survey(spec.SURVEY_FILE, allowed=("model",))` 仍报 "does not belong"，不改。
- 加一条：垫片的键就是旧键名——`list(spec.all_entries()) == list(ss.legacy_keys("d2d_link"))`，且每条 `spec.survey(old).value == ss.value(new)`。
- 其余（`test_package_lookup`、`test_targets_resolve_with_their_source`、`test_code_does_not_hardcode_the_table`、`test_tag_format`、`test_bundled_configs_stay_inside_the_survey_envelope`）不改。

## 4. 验收

1. `python tools/fingerprint.py record` 迁移前后逐位相同（0.65 UI、0.75 UI、40 mV、1e-27、25 mm……一个都不该动）。
2. 示例输出不动（键名、数值、单位、标签都没变）。
3. `python tools/vendor_check.py --strict` 绿。
4. `pytest` 与 `ruff check .` 绿。
