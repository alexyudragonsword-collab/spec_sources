"""Iron rule 4: entries a downstream library reads are registered in
consumers.yaml, each registration resolves to its value, and CHANGELOG.md
names it -- so changing a registered number or key turns this red until the
registration and the CHANGELOG move with it."""
from __future__ import annotations

import re

import pytest
import yaml
from conftest import REPO, fixture_entries

import spec_sources as ss

FMCW = "fmcw_radar.sources.yaml"
REQUIRED = {"repo", "at", "local", "key", "value", "was"}
OPTIONAL = {"field", "select"}


def _registrations() -> list[dict]:
    doc = yaml.safe_load((REPO / "consumers.yaml").read_text(encoding="utf-8"))
    return doc["consumers"]


def _ref(r: dict) -> str:
    return r["key"] + (f"#{r['field']}" if r.get("field") else "") + (f"@{r['select']}" if r.get("select") else "")


def test_registrations_are_well_formed():
    regs = _registrations()
    assert len(regs) == 5
    for r in regs:
        assert REQUIRED <= set(r) <= REQUIRED | OPTIONAL, r
        assert re.fullmatch(r"[0-9a-f]{40}", r["at"]), r
        assert "select" not in r or "field" in r, r
    assert len({(r["repo"], r["local"]) for r in regs}) == len(regs)


@pytest.mark.parametrize("reg", _registrations(), ids=lambda r: f"{r['repo']}:{r['local']}")
def test_rule4_each_registration_resolves_to_its_value(reg):
    assert reg["key"] in ss.all_entries(), f"{reg['key']}: register a live key, not an alias"
    assert ss.ref(_ref(reg)) == reg["value"]


@pytest.mark.parametrize("reg", _registrations(), ids=lambda r: f"{r['repo']}:{r['local']}")
def test_rule4_changelog_names_each_registered_number(reg):
    line = f"`{_ref(reg)}` = {reg['value']}"
    assert line in (REPO / "CHANGELOG.md").read_text(encoding="utf-8"), f"CHANGELOG.md must say {line}"


def test_fmcw_references_are_all_registered_and_agree_with_its_table():
    """fmcw_radar@2e5cbb6 reads five numbers through ``upstream:``; each is
    registered, its value there equals the registration, and the old string is
    kept in ``was``.  Four old strings are already valid references once the
    repo prefix is dropped; the fifth (a subtraction) is not -- it reads the
    derived entry instead (iron rule 6)."""
    src = fixture_entries(FMCW)
    upstream = {k: e for k, e in src.items() if e.get("upstream")}
    regs = {r["local"]: r for r in _registrations() if r["repo"] == "fmcw_radar"}
    assert set(regs) == set(upstream)
    for local, r in regs.items():
        assert upstream[local]["upstream"] == r["was"] and upstream[local]["value"] == r["value"]
        assert r["at"] == "2e5cbb61cef62819804fad89a197b0412b2eb84d"
        old = r["was"].removeprefix("mmw60_trx:")
        if "-" in old.partition("#")[2]:
            with pytest.raises(ValueError, match="derived"):
                ss.ref(old)
            assert ss.survey(r["key"]).source == "derived"
        else:
            assert old == _ref(r) and ss.ref(old) == r["value"]


def test_fmcws_own_spec_and_survey_entries_are_listed_for_milestone_2():
    """Not migrated this round: the 14 spec / survey entries of fmcw_radar's
    table (5 of them the registered front-end figures, 9 its own: oxygen, RCS,
    window widths) are listed in its migration note."""
    src = fixture_entries(FMCW)
    own = [k for k, e in src.items() if e["source"] in ("spec", "survey")]
    assert len(own) == 14 and sum(bool(src[k].get("upstream")) for k in own) == 5
    note = (REPO / "cairn" / "migration-fmcw_radar.md").read_text(encoding="utf-8")
    for k in own:
        assert f"`{k}`" in note, k
