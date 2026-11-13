"""Milestone 1 acceptance: every migrated entry equals its source table field
by field.  The source tables are in tests/fixtures/, each headed by its repo
and full SHA; where a sibling checkout is present the fixture is also
compared byte for byte with ``git show <sha>:<path>``."""
from __future__ import annotations

import collections

import pytest
from conftest import FIXTURE_FILES, RENAMED_0_2_0, fixture_entries, fixture_header, fixture_text, git_show, raw_entries

import spec_sources as ss

MMW60 = "mmw60_trx.survey.yaml"
D2D = "d2d_link.ucie_survey.yaml"

#: what stays in mmw60_trx's local table besides its 56 assumed entries, and why
#: (iron rule 2: a library's own choices and outputs stay with it; confirmed by the user 2026-11-13)
MMW60_STAYS = {
    "derived.isi_beyond_gi_k16_db": "uses assumed.cr_rms_delay_ns",
    "derived.pa60_obo_at_evm_limit_db": "uses assumed.pa60_operating_rule",
    "derived.irr_after_cal_measured_db": "mmw60_trx's own example 03 run, not an outside number",
    "survey.clock_profile_wu19": "names a file in mmw60_trx's tree (data/clock_profiles/)",
    "survey.clock_profile_wu19_x10": "names a file in mmw60_trx's tree; generated with its assumed floor and rejection",
    "survey.dsp_ip_dpd_poly_p4": "a sibling library's synthesis estimate, not a paper / datasheet / standard",
}
#: entries this library added (not in any source table)
NEW = {"isolation.tx_rx_tue2018_no_ebg_min_db",
       # 0.3.0, read in IEEE 802.11-09/0296r16 while verifying the tgad_em.* entries
       "tgad_em.pn_params", "tgad_em.pn_sides", "tgad_em.pa_backoff_definition", "tgad_em.pa_backoff_recommended_db",
       # milestone 2 batch 4, read in ITU-R P.676-13 and arXiv:1910.13706 (not migrated from a table)
       "itu_p676.oxygen_lines", "itu_p676.method", "itu_p676.figure1_conditions", "itu_p676.gamma_o_dry_sea_level",
       "itu_p676.gamma_o_dry_sea_level_peak", "target_rcs.deep2019_pedestrian_77g"}
#: migrated entries since read in the original (milestone 2): survey -> spec. Their value and unit
#: still equal the source table; tag, cite, note, quote and section are the verification's own.
VERIFIED = {k: "0.3.0 (IEEE 802.11-09/0296r16)" for k in (
    "tgad_em.pa_rapp_g", "tgad_em.pa_rapp_asat", "tgad_em.pa_rapp_p", "tgad_em.pa_ampm_alpha",
    "tgad_em.pa_ampm_beta", "tgad_em.pa_ampm_q1", "tgad_em.pa_ampm_q2", "tgad_em.pa_model_shape",
    "tgad_em.pn_model_shape")}
#: fields changed on the way in: {key: {field: (old text, new text)}}; each is
#: a replacement applied to the source's field and nothing else
CHANGED = {
    # iron rule 5: the note spelled the tag word with a colon (d2d_link's grep counted 0 spec lines as 1)
    "ucie.rx_eye_width_ui@24-32": {"note": ("改 source: spec 或删去", "改成 spec 标签或删去")},
    # 0.2.0: cross-references to renamed keys follow the rename
    "adc_survey.walden_fom_fj": {"note": ("survey.walden_fom_range_fj", "adc_survey.walden_fom_range_fj")},
    "liu2025.k_threshold_stf": {"cite": ("derived.cfo_liu2025_hz", "liu2025.cfo_from_ppm_hz")},
    "liu2025.k_threshold_ltf_only": {"cite": ("derived.cfo_liu2025_hz", "liu2025.cfo_from_ppm_hz")},
}


def _now(key: str) -> str:
    """A migrated key under its current name (0.2.0 renamed 17 of them; the old name is an alias)."""
    return RENAMED_0_2_0.get(key, key)


@pytest.mark.parametrize("name", sorted(FIXTURE_FILES))
def test_each_fixture_names_its_repo_and_full_sha(name):
    repo, sha, path = FIXTURE_FILES[name]
    assert fixture_header(name) == {"repo": repo, "sha": sha, "path": path}
    upstream = git_show(repo, sha, path)
    if upstream is None:
        pytest.skip(f"{repo} checkout with {sha[:7]} not present")
    assert fixture_text(name) == upstream


def _check_equal(new_key: str, src: dict, dst: dict):
    if new_key in VERIFIED:
        assert src["source"] == "survey" and dst["source"] == "spec" and dst["quote"] and dst["section"], new_key
        assert (dst["value"], dst["unit"]) == (src["value"], src["unit"]), new_key
        return
    changed = CHANGED.get(new_key, {})
    assert set(dst) == set(src), new_key
    for field in src:
        if field in changed:
            old, new = changed[field]
            assert old in src[field] and dst[field] == src[field].replace(old, new), (new_key, field)
        else:
            assert dst[field] == src[field], (new_key, field)


def test_mmw60_partition_is_explicit():
    src = fixture_entries(MMW60)
    tags = collections.Counter(e["source"] for e in src.values())
    assert len(src) == 125 and tags == {"spec": 10, "survey": 51, "assumed": 56, "derived": 8}
    assert set(MMW60_STAYS) <= set(src)
    stays = {k for k, e in src.items() if e["source"] == "assumed"} | set(MMW60_STAYS)
    moved = set(src) - stays
    assert collections.Counter(src[k]["source"] for k in moved) == {"spec": 10, "survey": 48, "derived": 5}
    assert collections.Counter(src[k]["source"] for k in stays) == {"assumed": 56, "survey": 3, "derived": 3}
    live = ss.all_entries()
    assert {_now(k) for k in moved} <= set(live) and not ({_now(k) for k in stays} & set(live))


def test_mmw60_entries_equal_the_source_field_by_field():
    src, dst = fixture_entries(MMW60), raw_entries()
    moved = [k for k, e in src.items() if e["source"] != "assumed" and k not in MMW60_STAYS]
    assert len(moved) == 63
    for k in moved:
        _check_equal(_now(k), src[k], dst[_now(k)])


def test_d2d_entries_equal_the_source_field_by_field_under_the_ucie_prefix():
    src, dst = fixture_entries(D2D), raw_entries()
    assert len(src) == 16 and {e["source"] for e in src.values()} == {"survey"}
    m = ss.legacy_keys("d2d_link")
    assert list(m) == list(src)                                  # every old key, in the source's order
    for old, new in m.items():
        assert new == f"ucie.{old}"
        _check_equal(new, src[old], dst[new])


def test_every_shared_entry_is_accounted_for():
    mmw = {_now(k) for k, e in fixture_entries(MMW60).items() if e["source"] != "assumed" and k not in MMW60_STAYS}
    ucie = set(ss.legacy_keys("d2d_link").values())
    assert set(ss.all_entries()) == mmw | ucie | NEW
    assert len(mmw) + len(ucie) + len(NEW) == 63 + 16 + 11 == 90
    assert set(CHANGED) <= set(ss.all_entries())


def test_the_source_tables_broke_the_grep_guard_and_the_audit_says_where():
    """Why iron rule 5 counts all four tags: mmw60_trx's comment at line 636 of
    its table read '(改成 source: spec ...)', so grep counted 11 spec lines for
    10 entries -- its guard counted only survey / assumed.  d2d_link's table
    did the same twice with no spec entry at all: its header comment and the
    note on the 24-32 GT/s eye width."""
    for name, tag, grep, real in ((MMW60, "spec", 11, 10), (D2D, "spec", 2, 0)):
        text = fixture_text(name)
        assert sum(f"source: {tag}" in line for line in text.splitlines()) == grep
        assert sum(e["source"] == tag for e in fixture_entries(name).values()) == real
    mmw_lines = fixture_text(MMW60).splitlines()
    assert "改成 source: spec" in mmw_lines[635]                 # line 636 of the source file
