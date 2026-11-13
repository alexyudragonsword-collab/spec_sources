# spec_sources

带出处的规范 / 文献数字表 + 读取器 + 守卫，不做任何仿真。

```python
from spec_sources import survey, value, ref

value("liu2025.carrier_hz")                                   # 73.44e9
survey("rx60.radar_iwr6843").source                           # 'spec'（带 quote 与 section）
ref("rx60.radar_iwr6843_fig7_2#p1db_inband_dbm@gain_db=40")   # -34.0
```

- 每条带 `source`（spec / survey / assumed / derived），表在 `src/spec_sources/data/<领域>.yaml`。
- 对每个表、每个标签，`grep -c "source: <标签>"` 恰好等于该标签的条目数。
- 消费方把 `src/spec_sources/` 拷进自己的 `vendor/`、pin 完整 SHA；只依赖 PyYAML。
- 规则见 `AGENTS.md`；被下游读取的条目见 `consumers.yaml`；迁移说明见 `cairn/migration-*.md`。

```
pip install -e ".[test,dev]"
pytest && ruff check .
```
