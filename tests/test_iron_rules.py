"""The iron rules (AGENTS.md) over the real tables, one test group each.

Rule 4 (consumers.yaml) is tests/test_consumers.py; rule 6's grammar is in
tests/test_reader.py, its use by consumers in tests/test_consumers.py."""
from __future__ import annotations

import math
import re
import subprocess

import pytest
from conftest import PACKAGE, RENAMED_0_2_0, REPO

import spec_sources as ss

DATA_FILES = [f.name for f in ss.data_files()]


# ------------------------------------------------------------------- rule 1: every entry tagged, and what a tag needs
def test_rule1_every_entry_is_tagged_cited_and_complete():
    table = ss.all_entries()
    assert len(table) == 94
    for key, e in table.items():
        assert e.source in ss.SOURCES and e.cite, key
        if e.source == "spec":
            assert e.quote and e.section, key
        if e.source == "survey":
            assert "未核实" in e.note, key
        if e.source == "derived":
            assert e.note, f"{key}: a derived entry's note says how it was computed"


# ------------------------------------------------------------------- rule 2: only numbers about the outside world
def test_rule2_no_library_choices_in_the_shared_tables():
    assert ss.by_source("assumed") == {}
    assert not [k for k in ss.all_entries() if k.startswith("assumed.")]


def _rapp_gap_db(p: float) -> float:
    """Psat − P1dB (dB) of the modified Rapp AM/AM G(A) = gA / (1 + (gA/Asat)^(2p))^(1/(2p))
    (tgad_em.pa_model_shape): independent of g and Asat.  At 1 dB compression
    u = gA/Asat = (10^(p/10) − 1)^(1/(2p)), so P1dB = Asat² u² 10^(−0.1) and Psat = Asat²."""
    u = (10 ** (p / 10) - 1) ** (1 / (2 * p))
    return 1.0 - 20 * math.log10(u)


def _solve_p(gap_db: float) -> float:
    lo, hi = 0.3, 10.0                                   # the gap falls monotonically with p
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if _rapp_gap_db(mid) > gap_db else (lo, mid)
    return 0.5 * (lo + hi)


def _p676_gamma_o(v, f_ghz: float) -> float:
    """ITU-R P.676-13 Annex 1, oxygen / dry-air branch (itu_p676.method), from the
    shared Table 1 (itu_p676.oxygen_lines) at Figure 1's dry atmosphere."""
    c = v("itu_p676.figure1_conditions")
    T = c["t_c"] + 273.15
    th = 300.0 / T
    e = c["rho_dry_g_m3"] * T / 216.7
    p = c["p_hpa"] - e
    n = 0.0
    for f0, a1, a2, a3, a4, a5, a6 in v("itu_p676.oxygen_lines")["rows"]:
        s = a1 * 1e-7 * p * th ** 3 * math.exp(a2 * (1 - th))
        df = a3 * 1e-4 * (p * th ** (0.8 - a4) + 1.1 * e * th)
        df = math.sqrt(df * df + 2.25e-6)
        dl = (a5 + a6 * th) * 1e-4 * (p + e) * th ** 0.8
        n += s * f_ghz / f0 * ((df - dl * (f0 - f_ghz)) / ((f0 - f_ghz) ** 2 + df * df)
                               + (df - dl * (f0 + f_ghz)) / ((f0 + f_ghz) ** 2 + df * df))
    d = 5.6e-4 * (p + e) * th ** 0.8
    nd = f_ghz * p * th ** 2 * (6.14e-5 / (d * (1 + (f_ghz / d) ** 2))
                                + 1.4e-12 * p * th ** 1.5 / (1 + 1.9e-5 * f_ghz ** 1.5))
    return 0.1820 * f_ghz * (n + nd)


def _p676_points(v):
    return [_p676_gamma_o(v, f) for f in v("itu_p676.gamma_o_dry_sea_level")["f_ghz"]]


def _p676_peak(v):
    best = max((_p676_gamma_o(v, 50 + i * 0.01), 50 + i * 0.01) for i in range(2001))
    return [round(best[1], 2), best[0]]


def _cfo(v):
    return (v("liu2025.xo_ppm_tx") + v("liu2025.xo_ppm_rx")) * 1e-6 * v("liu2025.carrier_hz")


#: every derived entry recomputed from shared entries only (``v`` is the shared
#: reader's value()): a derived entry that needs a library's own choice cannot
#: be written here, so it cannot live in the shared tables.  (value, abs tolerance)
RECOMPUTE = {
    "liu2025.cfo_from_ppm_hz": (lambda v: _cfo(v), 1.0),
    # 312.5 kHz: the 802.11 (VHT, 20 MHz) subcarrier spacing; L-STF repeats every 4 subcarriers
    "liu2025.k_threshold_stf": (lambda v: 2 * _cfo(v) / (4 * 312.5e3), 0.01),
    "liu2025.k_threshold_ltf_only": (lambda v: _cfo(v) / v("liu2025.ltf_capture_hz"), 0.05),
    "tgad_em.rapp_p1db_below_psat_db": (lambda v: _rapp_gap_db(v("tgad_em.pa_rapp_p")), 0.05),
    "pa60.asada_eumc2011_rapp_p": (
        lambda v: _solve_p(v("pa60.asada_eumc2011")["psat_dbm"] - v("pa60.asada_eumc2011")["p1db_dbm"]), 0.001),
    "itu_p676.gamma_o_dry_sea_level": (_p676_points, 0.0005),
    "itu_p676.gamma_o_dry_sea_level_peak": (_p676_peak, 0.005),
    "isolation.tx_rx_tue2018_no_ebg_min_db": (
        lambda v: v("isolation.tx_rx_tue2018")["with_ebg_db"] - v("isolation.tx_rx_tue2018")["improvement_max_db"],
        0.0),
}


def test_rule2_every_derived_entry_follows_its_formula_from_shared_entries():
    assert set(RECOMPUTE) == set(ss.by_source("derived"))
    for key, (f, tol) in RECOMPUTE.items():
        got, want = f(ss.value), ss.value(key)
        if key == "itu_p676.gamma_o_dry_sea_level":
            want = want["db_per_km"]
        elif key == "itu_p676.gamma_o_dry_sea_level_peak":
            want = [want["f_ghz"], want["db_per_km"]]
        assert got == pytest.approx(want, abs=tol), key


def test_rule2_the_rapp_closed_form_matches_the_other_end():
    """The same closed form, read the other way: the measured-shape p gives back
    Asada's 4.6 dB and TGad EM's p = 0.81 its 9.5 dB (both the entries' own text)."""
    assert _rapp_gap_db(1.286) == pytest.approx(4.60, abs=0.005)
    assert _rapp_gap_db(0.81) == pytest.approx(9.5, abs=0.05)


# ------------------------------------------------------------------- rule 3: global keys with a domain prefix
#: which domain prefixes each table may hold (AGENTS.md has the same table)
FILE_PREFIXES = {
    "atmosphere.yaml": {"itu_p676"},
    "energy.yaml": {"horowitz2014", "adc_survey", "deepscale"},
    "frontend60.yaml": {"rx60", "isolation", "antenna60"},
    "ieee80211.yaml": {"tgad_em", "ieee80211", "ieee80211ac", "ieee80211be", "ieee80211ay", "dmg"},
    "liu2025.yaml": {"liu2025"},
    "pa60.yaml": {"pa60"},
    "radar_targets.yaml": {"target_rcs"},
    "regulatory.yaml": {"fcc15255"},
    "ucie.yaml": {"ucie"},
}


def test_rule3_every_key_has_its_tables_domain_prefix():
    assert set(DATA_FILES) == set(FILE_PREFIXES)
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    for f in ss.data_files():
        assert f"data/{f.name}" in agents, f"AGENTS.md must describe data/{f.name}"
        for key in ss.load_table(f):
            assert ss.KEY_PATTERN.fullmatch(key), key
            prefix = key.split(".", 1)[0]
            assert prefix in FILE_PREFIXES[f.name], (f.name, key)
            assert prefix not in ss.SOURCES, f"{key}: a tag is not a domain prefix"


def test_rule3_keys_are_unique_across_tables():
    per_file = [set(ss.load_table(f)) for f in ss.data_files()]
    assert sum(len(s) for s in per_file) == len(set().union(*per_file)) == len(ss.all_entries())


def _version(v: str) -> tuple[int, ...]:
    return tuple(int(x) for x in v.split("."))


def _ledger() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for line in (REPO / "keys.lock").read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        key, *attrs = line.split()
        assert key not in out, f"keys.lock lists {key} twice"
        out[key] = dict(a.split("=", 1) for a in attrs)
        assert set(out[key]) <= {"added", "aliased", "retired"} and "added" in out[key], line
    return out


def test_rule3_a_published_key_never_disappears_without_its_alias_period():
    """keys.lock is append-only: every key ever published.  A live key is in it
    plainly; a renamed one is an alias in the data and marked aliased=; an
    alias can go only a later version (retired= after aliased=)."""
    ledger, live, alias = _ledger(), ss.all_entries(), ss.aliases()
    now = _version(ss.__version__)
    assert set(live) <= set(ledger), f"add to keys.lock: {sorted(set(live) - set(ledger))}"
    for key, a in ledger.items():
        if a["added"] == "unreleased":
            assert "## 未发布" in (REPO / "CHANGELOG.md").read_text(encoding="utf-8"), key
        else:
            assert _version(a["added"]) <= now, key
        if key in live:
            assert set(a) == {"added"}, f"{key} is live: no aliased= / retired="
        elif key in alias:
            assert "aliased" in a and "retired" not in a, key
            assert _version(a["aliased"]) <= now and alias[key].since == a["aliased"], key
        else:
            assert "aliased" in a and "retired" in a, f"{key} vanished without an alias period"
            assert _version(a["aliased"]) < _version(a["retired"]) <= now, key


def test_version_is_one_number_everywhere():
    pyproject = (REPO / "pyproject.toml").read_text(encoding="utf-8")
    assert f'version = "{ss.__version__}"' in pyproject
    assert f"## {ss.__version__}" in (REPO / "CHANGELOG.md").read_text(encoding="utf-8")


# ------------------------------------------------------------------- rule 5: grep counts all four tags
@pytest.mark.parametrize("name", DATA_FILES)
def test_rule5_grep_counts_every_tag_exactly(name):
    path = PACKAGE / "data" / name
    entries = ss.load_table(path)
    for tag in ss.SOURCES:
        out = subprocess.run(["grep", "-c", f"source: {tag}", str(path)], capture_output=True, text=True)
        assert int(out.stdout.strip() or 0) == sum(e.source == tag for e in entries.values()), (name, tag)
    assert ss.audit_tags(path) == []
    # the shared tables are stricter than audit_tags: the word with a colon only on tag lines, nowhere else
    out = subprocess.run(["grep", "-c", "source:", str(path)], capture_output=True, text=True)
    assert int(out.stdout.strip()) == len(entries), name


def test_rule5_holds_over_the_whole_data_directory():
    """The four counts over every table at once, the way a reader runs them by hand."""
    files = [str(f) for f in ss.data_files()]
    for tag in ss.SOURCES:
        out = subprocess.run(["grep", "-h", "-c", f"source: {tag}", *files], capture_output=True, text=True)
        assert sum(int(n) for n in out.stdout.split()) == len(ss.by_source(tag)), tag
    assert {t: len(ss.by_source(t)) for t in ss.SOURCES} == {"spec": 31, "survey": 55, "assumed": 0, "derived": 8}


def test_rule5_no_tag_spelling_outside_tag_lines_anywhere_in_the_package():
    """Besides the tables: the old-key maps, which are YAML a reader may grep too."""
    for p in (PACKAGE / "legacy_keys").glob("*.yaml"):
        assert not re.search(r"source:", p.read_text(encoding="utf-8")), p.name


def test_rule3_the_0_2_0_renames_were_retired_in_0_3_0():
    """The 17 keys renamed in 0.2.0 kept their old names as aliases for one
    version; 0.3.0 retired them (no consumer reads an old name: mmw60_trx#23).
    The ledger keeps every old name with aliased=0.2.0 retired=0.3.0, and an
    old name now reads as an unknown key."""
    ledger = _ledger()
    assert ss.aliases() == {}
    for old, new in RENAMED_0_2_0.items():
        assert ledger[old] == {"added": "0.1.0", "aliased": "0.2.0", "retired": "0.3.0"}, old
        assert new in ss.all_entries() and old not in ss.all_entries()
        with pytest.raises(KeyError):
            ss.survey(old)
