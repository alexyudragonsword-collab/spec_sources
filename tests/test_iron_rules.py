"""The iron rules (AGENTS.md) over the real tables, one test group each.

Rule 4 (consumers.yaml) is tests/test_consumers.py; rule 6's grammar is in
tests/test_reader.py, its use by consumers in tests/test_consumers.py."""
from __future__ import annotations

import math
import random
import re
import statistics
import subprocess

import pytest
from conftest import PACKAGE, RENAMED_0_2_0, REPO

import spec_sources as ss

DATA_FILES = [f.name for f in ss.data_files()]


# ------------------------------------------------------------------- rule 1: every entry tagged, and what a tag needs
def test_rule1_every_entry_is_tagged_cited_and_complete():
    table = ss.all_entries()
    assert len(table) == 187
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
_CODE_RATE = {"1/2": 1 / 2, "5/8": 5 / 8, "3/4": 3 / 4, "13/16": 13 / 16, "7/8": 7 / 8}


def _edmg_ofdm_rates(v) -> dict:
    """Per-stream EDMG OFDM rates, NCB = 1: N_SD x N_BPSC x R / T_SYM, T_SYM = (N_DFT + GI samples) / Fs."""
    p, m = v("edmg.ofdm_params"), v("edmg.ofdm_mcs")
    out = {"mcs": m["mcs"]}
    for gi in ("short", "normal", "long"):
        n_gi = round(p[f"gi_{gi}_s"] * p["fs_hz"])
        out[f"{gi}_gi_mbps"] = [p["n_sd"] * b * _CODE_RATE[c] * p["fs_hz"] / (p["n_dft"] + n_gi) / 1e6
                                for b, c in zip(m["n_bpsc"], m["code_rate"], strict=True)]
    return out


def _edmg_sc_rates(v) -> dict:
    """Per-stream EDMG SC rates, NCB = 1: chip rate x (block - GI) / block x N_CBPS x R / repetition."""
    p, m = v("edmg.sc_params"), v("edmg.sc_mcs")
    out = {"mcs": m["mcs"]}
    for gi in ("short", "normal", "long"):
        keep = (p["block_chips"] - p[f"gi_{gi}_chips"]) / p["block_chips"]
        out[f"{gi}_gi_mbps"] = [p["chip_rate_hz"] * keep * b * _CODE_RATE[c] / r / 1e6
                                for b, c, r in zip(m["n_cbps"], m["code_rate"], m["repetition"], strict=True)]
    return out


RECOMPUTE = {
    # DMG control PHY data rate (#33): DBPSK spread by Ga32, effective code rate 1/2
    "dmg.control_phy_rate_bps": (
        lambda v: v("dmg.control_phy")["chip_rate_hz"] / v("dmg.control_phy")["spreading_factor"]
        * v("dmg.control_phy")["effective_code_rate"], 1e-6),
    # Murmann ADC survey, the six >= 40 GS/s 4-7 nm TI-SAR rows: median and range of FOMW_hf (batch 7)
    "adc_survey.walden_fom_fj": (lambda v: statistics.median(v("adc_survey.ti_sar_ge40gs_4to7nm")["fomw_hf_fj"]), 1e-9),
    "adc_survey.walden_fom_range_fj": (
        lambda v: [min(v("adc_survey.ti_sar_ge40gs_4to7nm")["fomw_hf_fj"]),
                   max(v("adc_survey.ti_sar_ge40gs_4to7nm")["fomw_hf_fj"])], 1e-9),
    # DeepScaleTool: energy at 7 nm over energy at 45 nm, kept to 4 digits
    "deepscale.node_scale_45_to_7nm": (
        lambda v: v("deepscale.energy_by_node")["energy_rel_65nm"][v("deepscale.energy_by_node")["node_nm"].index(7)]
        / v("deepscale.energy_by_node")["energy_rel_65nm"][v("deepscale.energy_by_node")["node_nm"].index(45)], 5e-5),
    # EDMG single-channel data rates per spatial stream (#29), rounded to 0.01 Mbps in the table
    "edmg.ofdm_rate_mbps": (_edmg_ofdm_rates, 0.006),
    "edmg.sc_rate_mbps": (_edmg_sc_rates, 0.006),
    # ISO 19206-3 rear band, far range: its lower edge
    "target_rcs.iso19206_3_car_rear_far_lower_dbsm": (
        lambda v: v("target_rcs.iso19206_3_car_rear")["p_far_dbsm"]
        - v("target_rcs.iso19206_3_car_rear")["half_width_db"], 1e-12),
    # single-shot precision in seconds: LSB count times the resolution
    "tdc.henzler_isscc2008_single_shot_s": (
        lambda v: v("tdc.henzler_isscc2008")["single_shot_precision_lsb"] * v("tdc.henzler_isscc2008")["res_s"], 1e-16),
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
        if isinstance(want, dict):                          # a table: compare column by column
            assert set(got) == set(want), key
            for col in want:
                assert got[col] == pytest.approx(want[col], abs=tol), (key, col)
            continue
        assert got == pytest.approx(want, abs=tol), key


def test_rule2_the_rapp_closed_form_matches_the_other_end():
    """The same closed form, read the other way: the measured-shape p gives back
    Asada's 4.6 dB and TGad EM's p = 0.81 its 9.5 dB (both the entries' own text)."""
    assert _rapp_gap_db(1.286) == pytest.approx(4.60, abs=0.005)
    assert _rapp_gap_db(0.81) == pytest.approx(9.5, abs=0.05)


# ------------------------------------------------------------------- rule 3: global keys with a domain prefix
#: which domain prefixes each table may hold (AGENTS.md has the same table)
FILE_PREFIXES = {
    "adpll60.yaml": {"adpll60"},
    "atmosphere.yaml": {"itu_p676"},
    "energy.yaml": {"horowitz2014", "adc_survey", "deepscale"},
    "frontend60.yaml": {"rx60", "isolation", "antenna60"},
    "ieee802153c.yaml": {"tg3c"},
    "ieee80211.yaml": {"tgad_em", "ieee80211", "ieee80211ac", "ieee80211be", "ieee80211ay", "ieee80211bf", "dmg",
                       "edmg"},
    "liu2025.yaml": {"liu2025"},
    "pa60.yaml": {"pa60"},
    "radar_targets.yaml": {"target_rcs"},
    "regulatory.yaml": {"fcc15255"},
    "tdc.yaml": {"tdc"},
    "ucie.yaml": {"ucie"},
    "windows.yaml": {"harris1978"},
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
    assert {t: len(ss.by_source(t)) for t in ss.SOURCES} == {"spec": 169, "survey": 2, "assumed": 0, "derived": 16}


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


def test_the_ldpc_tables_agree_with_each_other():
    """#33: the EDMG lifting matrices have -1 exactly where the DMG base matrices have a zero block, and
    the 672-bit rate-7/8 matrix is rows 1+3 and 2+4 of the DMG rate-3/4 matrix (two documents, six years apart)."""
    base, lift = ss.value("dmg.ldpc_matrices"), ss.value("edmg.ldpc_1344_lifting")
    pairs = [(r, r) for r in ("r1_2", "r5_8", "r3_4", "r13_16")] + [("r3_4", "r7_8_on_r3_4")]
    for b, lft in pairs:
        for row_b, row_l in zip(base[b], lift[lft], strict=True):
            assert [x == -1 for x in row_b] == [y == -1 for y in row_l], (b, lft)
    r34, r78 = base["r3_4"], ss.value("edmg.ldpc_672_r7_8")["rows"]
    for row, (i, j) in zip(r78, ((2, 0), (3, 1)), strict=True):
        assert row == [[x for x in (r34[i][c], r34[j][c]) if x != -1] for c in range(16)]


# PyYAML resolves floats by YAML 1.1: 1e-06 with no decimal point stays a string ('1e-06'), 1.0e-06 is a float.
_EXPONENT_TEXT = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)[eE][+-]?\d+$")


def _strings(v):
    if isinstance(v, str):
        yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from _strings(x)
    elif isinstance(v, list):
        for x in v:
            yield from _strings(x)


def test_no_number_in_exponent_form_was_read_as_text():
    """dmg.phy_timing shipped rifs_s: 1e-06 and four more like it, which PyYAML read as strings."""
    bad = [(k, s) for k, e in ss.all_entries().items() for s in _strings(e.value) if _EXPONENT_TEXT.match(s)]
    assert bad == []


def test_the_dmg_preambles_follow_their_chip_counts():
    """#43: both preamble lengths in dmg.phy_timing are their STF + CEF chips at 1.76 GHz, kept to 1 ns, and the
    chip counts agree wherever two entries carry the same field (17/1806r3 restates them for every mode)."""
    timing, cphy, sc = ss.value("dmg.phy_timing"), ss.value("dmg.control_phy"), ss.value("dmg.sc_ppdu_chips")
    rate = cphy["chip_rate_hz"]
    assert sc["chip_rate_hz"] == rate
    assert timing["control_preamble_s"] == pytest.approx((cphy["stf_chips"] + cphy["cef_chips"]) / rate, abs=0.5e-9)
    assert timing["data_preamble_s"] == pytest.approx((sc["l_stf_chips"] + sc["l_cef_chips"]) / rate, abs=0.5e-9)
    edmg_sc, edmg_c = ss.value("edmg.sc_siso_preamble"), ss.value("edmg.control_mode_encoding")
    assert [edmg_sc[f] for f in ("l_stf_chips", "l_cef_chips", "l_header_chips")] == \
        [sc[f] for f in ("l_stf_chips", "l_cef_chips", "l_header_chips")]
    assert (edmg_c["l_stf_chips"], edmg_c["l_cef_chips"]) == (cphy["stf_chips"], cphy["cef_chips"])
    assert ss.value("dmg.control_phy_encoding")["trn_chips_per_trn_len"] == sc["trn_chips_per_trn_len"]


def _control_codewords(length: int, extra_octets: int) -> list[int]:
    """Data bits per LDPC codeword of a control mode PPDU: 88 in the first, the rest shared out (0433r2, 17/0277r0)."""
    rest = (length + extra_octets) * 8
    n_cw = 1 + math.ceil(rest / 168)
    l_dpcw = math.ceil(rest / (n_cw - 1))
    return [88] + [l_dpcw] * (n_cw - 2) + [rest - (n_cw - 2) * l_dpcw]


def test_the_control_phy_codeword_split_reproduces_its_example_and_its_closed_form():
    """#43: 0433r2's example (Length 120 -> 7 codewords of 88, 152, ..., 152 bits) and 17/1806r3's closed form
    (Length + 5)*8 + 168*N_CW, for every allowed Length; likewise (Length + 14)*8 for the EDMG control mode."""
    enc = ss.value("dmg.control_phy_encoding")
    cws = _control_codewords(enc["example_length"], -6)
    assert len(cws) == enc["example_n_cw"] and cws[1] == enc["example_l_dpcw"] and cws[-1] == enc["example_l_dplcw"]
    lo, hi = enc["length_octets"]
    for length in range(lo, hi + 1):
        for extra, header in ((-6, 5), (3, 14)):
            cws = _control_codewords(length, extra)
            assert all(0 < c <= enc["max_data_bits_per_cw"] for c in cws), (length, extra)
            assert sum(c + enc["parity_bits_per_cw"] for c in cws) == (length + header) * 8 + 168 * len(cws)


def test_the_short_ssw_field_widths_decode_the_published_example():
    """#43: 17/1586r1's 48-bit example (LSB first) splits back into the values it lists only with the widths in
    edmg.short_ssw (Packet Type 1 bit, RF Chain ID 3 bits); every format is 48 bits."""
    ssw = ss.value("edmg.short_ssw")
    for fmt in ("itxss_su", "itxss_mu", "rtxss"):
        assert sum(ssw[f"{fmt}_field_bits"]) == ssw["packet_bits"]
        assert len(ssw[f"{fmt}_field_bits"]) == len(ssw[f"{fmt}_field_names"])
    bits = "000101010001000000011111100000110101101000000111"
    want = {"Packet Type": 0, "Direction": 0, "Addressing Mode": 0, "Source AID": 0x15, "Destination AID": 1,
            "CDOWN": 0x3F, "RF Chain ID": 3, "Short Scrambled BSSID": 0x02D, "Unassociated": 0, "FCS": 0xE}
    got, i = {}, 0
    for width, name in zip(ssw["itxss_su_field_bits"], ssw["itxss_su_field_names"], strict=True):
        got[name] = int(bits[i:i + width][::-1], 2)
        i += width
    assert got == want


def _parity_rows(base: list[list[int]], z: int) -> list[int]:
    """Rows of the binary parity-check matrix as ints (bit j = column j): -1 is a zero block, s >= 0 the
    identity cyclically shifted by s."""
    rows = []
    for block_row in base:
        for r in range(z):
            rows.append(sum(1 << (c * z + (r + s) % z) for c, s in enumerate(block_row) if s != -1))
    return rows


def test_the_rho2_codeword_is_well_defined_by_the_rate_half_matrix():
    """#43: for rho = 2, 0433r2 encodes (168 data bits, 168 zeros) with the rate-1/2 code and then replaces
    bits 169..336 (the zeros) with data XOR PN, keeping all 336 parity bits. That needs 2*L_Z = 336 to be the
    rate-1/2 code's information length and its parity columns to be invertible, so (data, zeros, parity) is
    unique; checked on dmg.ldpc_matrices, then one codeword is built and checked against H."""
    enc, mats = ss.value("dmg.data_encoding"), ss.value("dmg.ldpc_matrices")
    z, n = mats["z"], enc["l_cw"]
    assert n == mats["n"] == 16 * z
    l_z = n // (2 * 2)                                   # L_Z = L_CW / (2 rho), rho = 2
    assert l_z == 168 and "L_Z = L_CW/(2 rho) = 168" in enc["sc_rho2_codeword"]
    rows = _parity_rows(mats["r1_2"], z)
    k = n - len(rows)
    assert k == 2 * l_z == 336
    # solve H_p p = H_s s over GF(2) for s = (random data, zeros); bit n of a row holds the right-hand side
    data = random.Random(43).getrandbits(l_z)
    aug = [(row >> k) | ((bin(row & ((1 << k) - 1) & data).count("1") & 1) << (n - k)) for row in rows]
    piv_rows, r = [], 0
    for col in range(n - k):
        piv = next((i for i in range(r, len(aug)) if aug[i] >> col & 1), None)
        assert piv is not None, f"parity column {col} is dependent"
        aug[r], aug[piv] = aug[piv], aug[r]
        for i in range(len(aug)):
            if i != r and aug[i] >> col & 1:
                aug[i] ^= aug[r]
        piv_rows.append(r)
        r += 1
    parity = sum((aug[i] >> (n - k) & 1) << col for col, i in enumerate(piv_rows))
    c = data | (parity << k)                             # (b_1..b_168, 168 zeros, p_1..p_336)
    assert all(bin(row & c).count("1") % 2 == 0 for row in rows)



# ------------------------------------------------------------------- #48: the OFDM training fields
_TONE = {"0": 0, "+1": 1, "-1": -1, "+j": 1j, "-j": -1j}


def _tones(field: dict) -> dict[int, complex]:
    """k -> value of an EDMG OFDM training field laid out as [left 176, 0, 0, 0, right 176]."""
    left, right = ([_TONE[t] for t in field[f].split()] for f in ("seq1_left", "seq1_right"))
    values = left + [0, 0, 0] + right
    ks = range(field["k_first"], field["k_last"] + 1)
    assert len(values) == len(ks)
    return dict(zip(ks, values, strict=True))


def test_the_edmg_ofdm_training_fields_fill_the_ofdm_tones():
    """#48: EDMG-CEF covers k = -177..177 with only the three DC tones empty, so it has N_ST - N_DC = 352 unit
    tones; EDMG-STF uses every 4th tone (88), so its period is N_DFT/4 = 128 samples and 30 periods are the 3840
    samples 17/1806r3 gives the field; one EDMG-CEF symbol is N_DFT plus the long GI, two of them for one stream;
    the parts sent at 1.76 GHz are the DMG / EDMG SC ones."""
    ofdm, ppdu = ss.value("edmg.ofdm_params"), ss.value("edmg.ofdm_ppdu_ncb1")
    cef, stf = ss.value("edmg.ofdm_cef_ncb1"), ss.value("edmg.ofdm_stf_ncb1")
    for field in (cef, stf):
        assert (field["k_first"], field["k_last"]) == (-ofdm["n_sr"], ofdm["n_sr"])
    c = _tones(cef)
    assert len(c) == ofdm["n_st"] and [k for k, x in c.items() if not x] == [-1, 0, 1] and ofdm["n_dc"] == 3
    assert cef["n_tone"] == "N_ST - N_DC" and sum(1 for x in c.values() if x) == ofdm["n_st"] - ofdm["n_dc"] == 352
    assert all(abs(x) == 1 for x in c.values() if x)
    s = _tones(stf)
    used = [k for k, x in s.items() if x]
    assert len(used) == stf["n_tone"] == 88 and all(k % 4 == 0 and abs(s[k]) == 1 for k in used)
    period = ofdm["n_dft"] // 4
    assert period / ofdm["fs_hz"] == pytest.approx(stf["period_s"], abs=0.005e-9)
    assert stf["n_periods"] * period == ppdu["edmg_stf_samples"] == 3840
    assert ppdu["edmg_stf_samples"] / ppdu["fs_hz"] == pytest.approx(stf["duration_s"], abs=0.5e-9)
    assert ppdu["fs_hz"] == ofdm["fs_hz"]
    gi = dict(zip(ppdu["gi_order"], ppdu["n_gi"], strict=True))
    assert gi == {name: round(ofdm[f"gi_{name}_s"] * ofdm["fs_hz"]) for name in ppdu["gi_order"]}
    assert ppdu["edmg_cef_samples_per_symbol"] == ofdm["n_dft"] + gi[cef["gi"]] == 704
    assert ss.ref("edmg.ofdm_ppdu_ncb1#n_edmg_cef_symbols@n_sts=1") == cef["n_symbols_nsts1"] \
        == len(cef["p_matrix_nsts1"]) == 2
    sc, edmg_sc = ss.value("dmg.sc_ppdu_chips"), ss.value("edmg.sc_siso_preamble")
    assert [ppdu[f] for f in ("l_stf_chips", "l_cef_chips", "l_header_chips", "chip_rate_hz")] == \
        [sc[f] for f in ("l_stf_chips", "l_cef_chips", "l_header_chips", "chip_rate_hz")]
    assert ppdu["edmg_header_a_chips"] == edmg_sc["otherwise_edmg_header_a_chips"]


def _golay(d: list[int], w: list[int]) -> tuple[list[int], list[int]]:
    """0433r2 21.9: A_0 = B_0 = delta, A_k(n) = W_k A_{k-1}(n) + B_{k-1}(n - D_k), B_k(n) = W_k A_{k-1}(n) -
    B_{k-1}(n - D_k), kept on 0 <= n < 2^K (D_1 can exceed 2^1, only the last pair fits in 2^k)."""
    size = 2 ** len(d)
    a = [1] + [0] * (size - 1)
    b = a[:]
    for dk, wk in zip(d, w, strict=True):
        late = [0] * dk + b[:size - dk]
        a, b = [wk * x + y for x, y in zip(a, late, strict=True)], [wk * x - y for x, y in zip(a, late, strict=True)]
    return a, b


def _acf(x: list[int], lag: int, periodic: bool = False) -> int:
    n = len(x)
    if periodic:
        return sum(x[i] * x[(i + lag) % n] for i in range(n))
    return sum(x[i] * x[i + lag] for i in range(n - lag))


def test_the_golay_tables_are_their_recursion_reversed_and_complementary():
    """#48, corrected in #57: each table is the 21.9 recursion with its own D_k, W_k, read backwards (Ga128(n)
    = A_7(128 - n) with the tables indexed from 1), and each pair is complementary: the two aperiodic
    autocorrelations cancel at every nonzero lag. 128 and 64 are the TGay SFD's i = 1 pairs, which it says
    equal the DMG ones; 32 is still 0433r2's (unverified, its own entry)."""
    for key, n in (("dmg.golay_sequences", 128), ("dmg.golay_sequences", 64), ("dmg.golay_sequences_32", 32)):
        g = ss.value(key)
        a, b = _golay(g[f"d_{n}"], g[f"w_{n}"])
        ga, gb = g[f"ga{n}"], g[f"gb{n}"]
        assert len(ga) == len(gb) == n and ga == a[::-1] and gb == b[::-1]
        assert all(_acf(ga, lag) + _acf(gb, lag) == 0 for lag in range(1, n))
        assert f"Ga{n}(n) = A_{len(g[f'd_{n}'])}({n} - n)" in g["reversal"]
    corrected = ss.value("dmg.golay_sequences")
    assert (corrected["d_128"], corrected["w_128"]) == ([1, 8, 2, 4, 16, 32, 64], [-1, -1, -1, -1, 1, -1, -1])
    assert ss.survey("dmg.golay_sequences_32").source == "survey" and "ga32" not in corrected


def test_the_dmg_cef_is_built_from_the_golay_tables():
    """#48: Gu512 and Gv512 are spelled out of Ga128 / Gb128; both end with -Ga128, the end of the STF, so every
    512-chip block is preceded by its own cyclic prefix and the closing 128 chips are a cyclic suffix, and the two
    are periodically complementary. Both orders fill the 1152 CEF chips, the OFDM order swaps the SC one."""
    g, lay = ss.value("dmg.golay_sequences"), ss.value("dmg.cef_golay_layout")
    part = {"+Ga128": g["ga128"], "-Ga128": [-x for x in g["ga128"]],
            "+Gb128": g["gb128"], "-Gb128": [-x for x in g["gb128"]]}
    gu = [x for name in lay["gu512"] for x in part[name]]
    gv = [x for name in lay["gv512"] for x in part[name]]
    blocks = {"Gu512": gu, "Gv512": gv, "Gu128": gu[:128], "Gv128": gv[:128]}
    assert gu[:128] == gv[:128] == part["-Gb128"]
    assert lay["gu128"].endswith("-Gb128") and lay["gv128"].endswith("-Gb128")
    assert gu[-128:] == gv[-128:] == part["-Ga128"]
    for order in (lay["sc_order"], lay["ofdm_order"]):
        assert sum(len(blocks[b]) for b in order) == lay["cef_chips"] == ss.value("dmg.sc_ppdu_chips")["l_cef_chips"]
    assert lay["ofdm_order"][:2] == lay["sc_order"][1::-1] and lay["ofdm_order"][2] == "Gu128"
    assert all(_acf(gu, lag, periodic=True) + _acf(gv, lag, periodic=True) == 0 for lag in range(1, 512))
    assert any(_acf(gu, lag) + _acf(gv, lag) for lag in range(1, 512))      # not aperiodically complementary


def test_the_ofdm_preamble_filter_is_symmetric_and_centred_on_its_delay():
    """#48: hFilt has 73 integer taps, is symmetric with its peak 256 at h36, which is why 0433r2 takes sample
    2n - 36; 3/2 is the OFDM to SC rate ratio of dmg.phy_params."""
    f, dmg = ss.value("dmg.ofdm_preamble_hfilt"), ss.value("dmg.phy_params")
    h = f["coefficients"]
    assert len(h) == f["n_taps"] == 73 and all(isinstance(x, int) for x in h)
    assert h == h[::-1] and f["delay_half_samples"] == (len(h) - 1) // 2 == 36 and max(h) == h[36] == 256
    assert dmg["fs_ofdm_hz"] / dmg["chip_rate_hz"] == f["upsample"] / f["downsample"] == 1.5
    assert f["normalized_norm"] == "sqrt(3)" and math.sqrt(sum(x * x for x in h)) == pytest.approx(428.679, abs=5e-4)


# ------------------------------------------------------------------- #50: the radar tiers of 47 CFR 15.255(c)(2)
def _quoted(x: float, unit: str, quote: str) -> bool:
    """x as the eCFR prints it (57, 57.0, 61.56; a minus sign or a hyphen) followed by unit."""
    forms = {f"{x:g}", f"{x:.1f}", f"{x:.2f}"}
    return any(f"{s}{unit}" in quote or f"{s.replace('-', '−')}{unit}" in quote for s in forms)


def test_the_fcc_radar_tiers_sit_in_the_band_and_quote_their_own_numbers():
    """#50: every (c)(2) tier (and (b)(3), which (c)(2) offers as one) is a sub-band of 57-71 GHz whose band
    edges and dBm limits are in its own quote; off-time limits count runs of at least 2 ms over any 33 ms
    window; only the default tier has a conducted limit, the others operate 'without being subject to a
    transmitter conducted output power limit'."""
    table = ss.all_entries()
    lo, hi = ss.value("fcc15255.band_low_hz"), ss.value("fcc15255.band_high_hz")
    tiers = {k: e for k, e in table.items() if k.startswith("fcc15255.radar_") and "band_low_hz" in e.value}
    assert len(tiers) == 9
    default = tiers["fcc15255.radar_default"].value
    assert (default["band_low_hz"], default["band_high_hz"]) == (lo, hi)
    for k, e in tiers.items():
        v = e.value
        assert lo <= v["band_low_hz"] < v["band_high_hz"] <= hi, k
        assert any(_quoted(v["band_low_hz"] / 1e9, f"-{b}", e.quote)
                   for b in (f"{v['band_high_hz'] / 1e9:g}", f"{v['band_high_hz'] / 1e9:.1f}")), k
        for field in (f for f in v if f.endswith("_dbm")):
            assert _quoted(v[field], " dBm", e.quote), (k, field)
        assert ("peak_conducted_dbm" in v) == (k == "fcc15255.radar_default"), k
        if "off_time_sum_min_s" in v:
            assert (v["off_time_window_s"], v["off_time_min_run_s"]) == (0.033, 0.002), k
            assert v["off_time_sum_min_s"] < v["off_time_window_s"], k
            assert "off-times of at least two milliseconds" in e.quote, k
            window = " milliseconds within any contiguous interval of 33 milliseconds"
            assert _quoted(v["off_time_sum_min_s"] * 1e3, window, e.quote), k
    assert _quoted(tiers["fcc15255.radar_61_61p5"].value["max_bandwidth_hz"] / 1e6, " MHz bandwidth or less",
                   tiers["fcc15255.radar_61_61p5"].quote)
    assert _quoted(tiers["fcc15255.radar_uav_60_64"].value["max_height_agl_m"], " meters",
                   tiers["fcc15255.radar_uav_60_64"].quote)
    mode = table["fcc15255.radar_mode_switch"]
    assert mode.value == {"modes_at_once": 1, "min_dwell_s": 0.033}
    assert "only one mode at any time and does so for at least 33 milliseconds" in mode.quote


# ------------------------------------------------------------------- #54: 802.11bf sensing and the TRN fields
def _golay_part(g: dict, name: str) -> list[int]:
    """'+Ga128', '-Gb64' (an '_N' already substituted by the caller) -> the signed sequence from
    dmg.golay_sequences."""
    sign, seq = (1 if name[0] == "+" else -1), name[1:].lower()
    return [sign * x for x in g[seq]]


def test_the_dmg_trn_field_is_4992_chips_and_its_ce_is_the_sc_cef():
    """#54: a DMG TRN_LEN unit is 4 AGC subfields of five Ga64, the CE subfield and 4 TRN subfields of
    [Ga128 -Gb128 Ga128 Gb128 Ga128]: 1280 + 1152 + 2560 = 4992 chips, the TRN chips per TRN_LEN that
    17/1806r3 gives (dmg.sc_ppdu_chips); the CE subfield is the SC packet's CEF chip for chip (Gu512, Gv512,
    Gv128 from dmg.cef_golay_layout)."""
    g, trn, lay = ss.value("dmg.golay_sequences"), ss.value("dmg.trn_field"), ss.value("dmg.cef_golay_layout")
    agc = [x for n in trn["agc_subfield_sc"] for x in _golay_part(g, n)] * trn["agc_subfields_per_trn_len"]
    ce = [x for n in trn["ce_subfield"] for x in _golay_part(g, n)]
    sub = [x for n in trn["trn_subfield"] for x in _golay_part(g, n)]
    assert (len(agc), len(ce), len(sub)) == (1280, 1152, 640)
    total = len(agc) + len(ce) + trn["trn_subfields_per_trn_len"] * len(sub)
    assert total == trn["chips_per_trn_len"] == ss.value("dmg.sc_ppdu_chips")["trn_chips_per_trn_len"] == 4992
    gu = [x for n in lay["gu512"] for x in _golay_part(g, n)]
    gv = [x for n in lay["gv512"] for x in _golay_part(g, n)]
    sc_cef = {"Gu512": gu, "Gv512": gv, "Gu128": gu[:128], "Gv128": gv[:128]}
    assert ce == [x for b in lay["sc_order"] for x in sc_cef[b]]
    assert [n.replace("a64", "b64") for n in trn["agc_subfield_sc"]] == trn["agc_subfield_control"]
    e = ss.survey("dmg.trn_field")
    spelled = lambda seq: "[" + " ".join(n.lstrip("+") for n in seq) + "]"     # noqa: E731 -- the quotes' spelling
    assert spelled(trn["trn_subfield"]) in e.quote and spelled(trn["agc_subfield_sc"]) in e.quote
    assert spelled(trn["agc_subfield_control"]) in e.quote


def test_the_edmg_trn_and_sync_lengths_follow_trn_bl():
    """#54: the EDMG basic TRN subfield is six Golay sequences of TRN_BL x N_CB, so at N_CB = 1, one TX
    chain, TRN_BL = 128 it is 768 chips, the TRN_BASIC_LENGTH formula with N_TRN = 1; the multistatic Sync
    subfield is 18 of the same sequences, 2304 chips; the Golay tables of that length are complementary."""
    g, trn = ss.value("dmg.golay_sequences"), ss.value("edmg.trn_field")
    ms = ss.value("ieee80211bf.edmg_multistatic_ppdu")
    bl = ss.ref("edmg.trn_field#trn_bl@trn_seq_length=normal")
    assert bl == 128 and trn["trn_bl"] == [128, 256, 64] and trn["golay_length"] == ms["golay_length"] == "TRN_BL*N_CB"
    basic = [x for n in trn["basic_subfield"] for x in _golay_part(g, n.replace("_N", str(bl)))]
    n_trn = ss.ref("edmg.trn_field#n_trn@tx_chains_max=2")
    assert len(basic) == 6 * bl * n_trn == 768 and trn["basic_length"] == "6*TRN_BL*N_TRN"
    assert trn["n_trn"] == [1, 2, 4] and trn["unit_p"] == [0, 1, 2, 4] and trn["unit_m_max"] == 16
    assert ms["golay_per_sync_subfield"] * bl == 2304
    as_quoted = "[" + ", ".join(n.lstrip("+").replace("_N", "iN") for n in trn["basic_subfield"]) + "]"
    assert f"TRNibasic = {as_quoted}" in ss.survey("edmg.trn_field").quote
    ga, gb = g[f"ga{bl}"], g[f"gb{bl}"]
    assert all(_acf(ga, lag) + _acf(gb, lag) == 0 for lag in range(1, bl))


def test_the_dmg_sensing_schedule_swapped_its_interval_widths_and_counts_in_microseconds():
    """#54: the SA ballot (24/1351r2) swapped the Interburst / Intraburst Interval widths of D0.3
    (22/1830r3) and made the unit a microsecond; the subelement keeps its length. The sensing types table
    has one row per type, and the wide multistatic channels are whole 2.16 GHz channels."""
    s = ss.value("ieee80211bf.dmg_sensing_scheduling")
    i, j = s["field"].index("interburst_interval"), s["field"].index("intraburst_interval")
    swapped = list(s["d0_3_octets"])
    swapped[i], swapped[j] = swapped[j], swapped[i]
    assert s["octets"] == swapped and sum(s["octets"]) == 11
    assert ss.ref("ieee80211bf.dmg_sensing_scheduling#octets@field=intraburst_interval") == 1
    assert s["time_unit_s"] == 1e-06 and s["unit"][:3] == ["us"] * 3
    e = ss.survey("ieee80211bf.dmg_sensing_scheduling")
    assert "Octets 1 1 4 1 2 1 1 1 1" in e.quote and "in units of microsecond" in e.quote
    t = ss.value("ieee80211bf.dmg_sensing_types")
    assert {len(t[f]) for f in ("type", "transmitter", "receiver", "coordinated_by")} == {6}
    bw = ss.value("ieee80211bf.dmg_sensing_bandwidth")
    centres = ss.value("ieee80211ay.channel_centres_ghz")
    spacing = round(centres[1] - centres[0], 6)
    assert spacing == 2.16
    assert [round(n * spacing, 6) for n in bw["multistatic_sync_trn_channels"]] == bw["multistatic_channel_ghz"]


# ------------------------------------------------------------------- #59: long Golay pairs, RX compression, BRP timing
def test_the_long_edmg_golay_pairs_are_their_recursion_reversed_and_complementary():
    """#59: the stream-1 pairs of length 256 and 512 are the 21.9 recursion with the TGay SFD's D_k, W_k read
    backwards (they equal the SFD's tables 41-44), and each pair is complementary."""
    g = ss.value("edmg.golay_sequences_long")
    for n in (256, 512):
        a, b = _golay(g[f"d_{n}"], g[f"w_{n}"])
        ga, gb = g[f"ga{n}"], g[f"gb{n}"]
        assert len(ga) == len(gb) == n and ga == a[::-1] and gb == b[::-1]
        assert all(_acf(ga, lag) + _acf(gb, lag) == 0 for lag in range(1, n))
        assert f"Ga{n}(n) = A_{len(g[f'd_{n}'])}({n} - n)" in g["reversal"]
    assert g["d_256"] == [1, 8, 2, 4, 16, 32, 64, 128] and g["d_512"] == g["d_256"] + [256]


def _interp(xs: list[float], ys: list[float], x: float) -> float:
    i = next(k for k in range(1, len(xs)) if xs[k] >= x)
    return ys[i - 1] + (ys[i] - ys[i - 1]) * (x - xs[i - 1]) / (xs[i] - xs[i - 1])


def test_the_rx_compression_curves_fall_and_agree_with_their_stated_p1db():
    """#59: the two read-off curves only fall with input power, and at the IP1dB each paper states, the gain
    read off the figure is 1 dB below the small-signal value to within the reading error (0.1 dB)."""
    for key, field, small_signal in (("rx60.amp_spasaro2024_compression", "gt_db", None),
                                     ("rx60.rx_moody2023_compression", "conversion_gain_db", None)):
        v = ss.value(key)
        x, y = v["pin_dbm"], v[field]
        assert x == sorted(x) and all(b <= a for a, b in zip(y, y[1:], strict=False)), key
        g0 = y[0] if small_signal is None else small_signal
        compression = g0 - _interp(x, y, v["ip1db_dbm"])
        assert compression == pytest.approx(1.0, abs=0.1), (key, compression)
    moody = ss.value("rx60.rx_moody2023_compression")
    assert moody["conversion_gain_db"][0] - moody["gain_at_ip1db_db"] == pytest.approx(1.0)
    bgt = ss.value("rx60.radar_bgt60tr13c")
    assert bgt["rx_p1db_dbm_min"] < bgt["rx_p1db_dbm_typ"] and bgt["tx_rx_isolation_db_typ"] == 50.0


def test_the_bistatic_brp_exchange_separates_sifs_from_brpifs():
    """#59: BRP frames of the same STA are SIFS apart, the other STA answers within BRPIFS (#57 had only
    BRPIFS); an SC BRP packet's data field is at least 18 SC blocks."""
    v = ss.value("ieee80211bf.dmg_bistatic_ppdu")
    assert (v["same_sta_spacing"], v["reply_spacing"]) == ("SIFS", "BRPIFS")
    assert "SIFS between" in v["spacing"] and "BRPIFS" in v["spacing"]
    assert v["min_data_sc_blocks"] == 18 and v["first_brp_mcs"] == 0
    e = ss.survey("ieee80211bf.dmg_bistatic_ppdu")
    assert "All BRP frames transmitted by the initiator shall be separated by SIFS" in e.quote
    assert "is 18 SC blocks" in e.quote and "DMG Sensing Request frames" in e.quote


def test_brpifs_is_the_44_us_the_public_drafts_quote():
    """#59: dmg.phy_timing had BRPIFS 20 us from 0433r2 Table 90; TGad SB001 (D5.0) and TGay 17/0418r1 both say
    44 us, and the user confirmed 44 against the standard.  The old Table 90 cell is no longer quoted."""
    e = ss.survey("dmg.phy_timing")
    assert e.value["brpifs_s"] == pytest.approx(44e-6, rel=1e-12)
    assert "BRPIFS (44 us)" in e.quote and "BRPIFS=44 us" in e.quote and "aBRPIFS 20usec" not in e.quote
    assert e.value["sifs_s"] < e.value["brpifs_s"]

