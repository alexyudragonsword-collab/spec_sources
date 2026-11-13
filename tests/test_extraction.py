"""Milestone 1 acceptance: every migrated entry equals its source table field
by field.  The source tables are in tests/fixtures/, each headed by its repo
and full SHA; where a sibling checkout is present the fixture is also
compared byte for byte with ``git show <sha>:<path>``."""
from __future__ import annotations

import collections

import pytest
from conftest import FIXTURE_FILES, fixture_entries, fixture_header, fixture_text, git_show, raw_entries

import spec_sources as ss

MMW60 = "mmw60_trx.survey.yaml"
D2D = "d2d_link.ucie_survey.yaml"

#: what stays in mmw60_trx's local table besides its 56 assumed entries, and why
#: (iron rule 2: a library's own choices and outputs stay with it)
MMW60_STAYS = {
    "derived.isi_beyond_gi_k16_db": "uses assumed.cr_rms_delay_ns",
    "derived.pa60_obo_at_evm_limit_db": "uses assumed.pa60_operating_rule",
    "derived.irr_after_cal_measured_db": "mmw60_trx's own example 03 run, not an outside number",
    "survey.clock_profile_wu19": "names a file in mmw60_trx's tree (data/clock_profiles/)",
    "survey.clock_profile_wu19_x10": "names a file in mmw60_trx's tree; generated with its assumed floor and rejection",
    "survey.dsp_ip_dpd_poly_p4": "a sibling library's synthesis estimate, not a paper / datasheet / standard",
}
#: entries this library added (not in any source table)
NEW = {"isolation.tx_rx_tue2018_no_ebg_min_db"}
#: fields changed on the way in: {key: {field: (old text, new text)}}; each is
#: a replacement applied to the source's field and nothing else
CHANGED = {
    # iron rule 5: the note spelled the tag word with a colon (d2d_link's grep counted 0 spec lines as 1)
    "ucie.rx_eye_width_ui@24-32": {"note": ("改 source: spec 或删去", "改成 spec 标签或删去")},
}


@pytest.mark.parametrize("name", sorted(FIXTURE_FILES))
def test_each_fixture_names_its_repo_and_full_sha(name):
    repo, sha, path = FIXTURE_FILES[name]
    assert fixture_header(name) == {"repo": repo, "sha": sha, "path": path}
    upstream = git_show(repo, sha, path)
    if upstream is None:
        pytest.skip(f"{repo} checkout with {sha[:7]} not present")
    assert fixture_text(name) == upstream


def _check_equal(new_key: str, src: dict, dst: dict):
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
    assert moved <= set(live) and not (stays & set(live))


def test_mmw60_entries_equal_the_source_field_by_field():
    src, dst = fixture_entries(MMW60), raw_entries()
    moved = [k for k, e in src.items() if e["source"] != "assumed" and k not in MMW60_STAYS]
    assert len(moved) == 63
    for k in moved:
        _check_equal(k, src[k], dst[k])


def test_d2d_entries_equal_the_source_field_by_field_under_the_ucie_prefix():
    src, dst = fixture_entries(D2D), raw_entries()
    assert len(src) == 16 and {e["source"] for e in src.values()} == {"survey"}
    m = ss.legacy_keys("d2d_link")
    assert list(m) == list(src)                                  # every old key, in the source's order
    for old, new in m.items():
        assert new == f"ucie.{old}"
        _check_equal(new, src[old], dst[new])


def test_every_shared_entry_is_accounted_for():
    mmw = {k for k, e in fixture_entries(MMW60).items() if e["source"] != "assumed" and k not in MMW60_STAYS}
    ucie = set(ss.legacy_keys("d2d_link").values())
    assert set(ss.all_entries()) == mmw | ucie | NEW
    assert len(mmw) + len(ucie) + len(NEW) == 63 + 16 + 1 == 80
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
