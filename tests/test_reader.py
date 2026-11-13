"""The reader: mmw60_trx's public names and behaviour, plus ref(), aliases and
the strict loader (iron rules 1, 3 and 6 at the mechanism level)."""
from __future__ import annotations

import dataclasses
import warnings

import pytest

import spec_sources as ss
from spec_sources import reader

#: mmw60_trx's ``mmw60.spec`` public names its shim re-exports (the superset rule)
MMW60_NAMES = ("SpecNumber", "SOURCES", "load_table", "all_entries", "survey", "value", "unverified", "by_source")


def test_public_names_are_a_superset_of_mmw60_spec():
    for name in MMW60_NAMES + ("ref",):
        assert hasattr(ss, name), name
        assert name in ss.__all__, name
    assert ss.SOURCES == ("spec", "survey", "assumed", "derived")


def test_spec_number_has_mmw60s_fields_in_its_order():
    """The shim builds SpecNumbers positionally in places (mmw60 tests do):
    same field names, order and defaults."""
    fields = dataclasses.fields(ss.SpecNumber)
    assert [f.name for f in fields] == ["key", "value", "unit", "source", "cite", "note", "quote", "section"]
    assert [f.default for f in fields[5:]] == ["", None, None]


# ------------------------------------------------------------------- iron rule 1: the tag and what it needs
def test_spec_number_refuses_what_rule_1_forbids():
    with pytest.raises(ValueError, match="quoted"):
        ss.SpecNumber("x.a", 1, "u", "spec", "cite")
    with pytest.raises(ValueError, match="quoted"):
        ss.SpecNumber("x.a", 1, "u", "spec", "cite", quote="text")             # a quote without its section
    with pytest.raises(ValueError, match="source"):
        ss.SpecNumber("x.a", 1, "u", "rumour", "cite")
    with pytest.raises(ValueError, match="未核实"):
        ss.SpecNumber("x.a", 1, "u", "survey", "cite", note="read somewhere")
    with pytest.raises(ValueError, match="cite"):
        ss.SpecNumber("x.a", 1, "u", "derived", "")
    ok = ss.SpecNumber("x.a", 1, "u", "spec", "cite", quote="the text", section="3.1")
    assert ok.verified and ok.tag() == "1 u (source: spec)"
    assert not ss.survey("liu2025.carrier_hz").verified


def test_loader_refuses_duplicate_keys_unknown_fields_and_missing_values(shared_tables):
    good = '  a.x:\n    value: 1\n    unit: u\n    source: derived\n    cite: "f"\n'
    p = shared_tables("t.yaml", "entries:\n" + good + good)
    with pytest.raises(Exception, match="duplicate key"):
        ss.load_table(p)
    p = shared_tables("t.yaml", "entries:\n" + good.replace("cite:", "upstream: z\n    cite:"))
    with pytest.raises(ValueError, match="unknown fields"):
        ss.load_table(p)
    p = shared_tables("t.yaml", "entries:\n  a.x:\n    unit: u\n    source: derived\n    cite: f\n")
    with pytest.raises(ValueError, match="needs a value"):
        ss.load_table(p)
    p = shared_tables("t.yaml", "entries:\n" + good + "extra: 1\n")
    with pytest.raises(ValueError, match="unknown top-level"):
        ss.load_table(p)
    p = shared_tables("t.yaml", "entries:\n" + good.replace("derived", "survey"))
    with pytest.raises(ValueError, match="未核实"):
        ss.load_table(p)


def test_a_key_in_two_tables_is_an_error(shared_tables):
    e = '  a.x:\n    value: 1\n    source: derived\n    cite: "f"\n'
    shared_tables("one.yaml", "entries:\n" + e)
    shared_tables("two.yaml", "entries:\n" + e)
    with pytest.raises(ValueError, match="two tables"):
        ss.all_entries()
    with pytest.raises(ValueError, match="two tables"):
        ss.merge_tables(ss.load_table(reader.DATA_DIR / "one.yaml"), ss.load_table(reader.DATA_DIR / "two.yaml"))


def test_lookup_names_what_exists_and_filters_by_tag():
    with pytest.raises(KeyError, match="liu2025.carrier_hz"):
        ss.survey("liu2025.nonexistent")
    assert ss.value("liu2025.carrier_hz") == 73.44e9
    assert ss.unverified() == ss.by_source("survey")
    assert ss.by_source("assumed") == {}
    with pytest.raises(ValueError, match="source must be one of"):
        ss.by_source("rumour")


# ------------------------------------------------------------------- iron rule 6: a reference is a lookup
def test_ref_forms():
    assert ss.ref("liu2025.carrier_hz") == 73.44e9                                        # the whole value
    assert ss.ref("ucie.rx_eye_width_ui@24-32") == 0.65                                   # '@' in a key: no selector
    assert ss.ref("rx60.radar_iwr6843#tx_power_dbm") == 12.0                              # a field
    assert ss.ref("rx60.radar_iwr6843_fig7_2#p1db_inband_dbm@gain_db=40") == -34.0       # a point of a curve
    assert ss.ref("rx60.radar_iwr6843_fig7_2#p1db_inband_dbm@gain_db=48.0") == -42.0
    assert ss.ref("rx60.radar_iwr6843_fig7_2#nf_db@gain_db=30") == 15.6
    assert ss.ref("rx60.radar_iwr6843_fig7_2#nf_db@gain_db=3e1") == 15.6                 # YAML 1.1 reads 3e1 as text
    assert ss.ref("liu2025.table1_scs_hz#8") == 2.5e6                                     # a numeric field name
    assert ss.ref("pa60.wu_asscc2012#vpa_1v0") == {"psat_dbm": 13.2, "p1db_dbm": 10.2, "pae_peak": 0.150}


def test_ref_refuses_arithmetic_and_bad_lookups():
    with pytest.raises(ValueError, match="derived"):
        ss.ref("isolation.tx_rx_tue2018#with_ebg_db-improvement_max_db")                # fmcw_radar's old subtraction
    with pytest.raises(ValueError, match="derived"):
        ss.ref("isolation.tx_rx_tue2018#with_ebg_db*2")
    with pytest.raises(KeyError, match="no point|matches 0"):
        ss.ref("rx60.radar_iwr6843_fig7_2#p1db_inband_dbm@gain_db=41")
    with pytest.raises(KeyError, match="no field"):
        ss.ref("rx60.radar_iwr6843#nope")
    with pytest.raises(KeyError, match="no axis"):
        ss.ref("rx60.radar_iwr6843_fig7_2#p1db_inband_dbm@gain=40")
    with pytest.raises(ValueError, match="not a mapping"):
        ss.ref("liu2025.carrier_hz#x")
    with pytest.raises(ValueError, match="selector"):
        ss.ref("rx60.radar_iwr6843_fig7_2#p1db_inband_dbm@gain_db")
    with pytest.raises(ValueError, match="lists"):
        ss.ref("rx60.radar_iwr6843#nf_db@tx_power_dbm=12")
    with pytest.raises(KeyError):
        ss.ref("mmw60_trx:rx60.radar_iwr6843#nf_db")                                    # the repo prefix is gone


def test_ref_reads_a_consumers_merged_table():
    local = {"loc.a": ss.SpecNumber("loc.a", {"g": [1, 2], "y": [5, 6]}, "", "assumed", "this library")}
    table = ss.merge_tables(ss.all_entries(), local)
    assert ss.ref("loc.a#y@g=2", table) == 6 and ss.ref("liu2025.packet_bytes", table) == 4096
    with pytest.raises(KeyError):
        ss.ref("loc.b", table)
    with pytest.raises(ValueError, match="two tables"):
        ss.merge_tables(table, {"liu2025.packet_bytes": ss.survey("liu2025.packet_bytes")})


# ------------------------------------------------------------------- iron rule 3: renames go through an alias
_LIVE = '  a.new:\n    value: 7\n    unit: u\n    source: derived\n    cite: "f"\n'


def test_an_alias_resolves_with_a_warning(shared_tables):
    shared_tables("a.yaml", "entries:\n" + _LIVE + 'aliases:\n  a.old: {to: a.new, since: "0.2.0", note: "renamed"}\n')
    with pytest.warns(ss.DeprecatedKeyWarning, match="a.old.*0.2.0.*a.new"):
        e = ss.survey("a.old")
    assert e.key == "a.new" and e.value == 7
    with pytest.warns(ss.DeprecatedKeyWarning):
        assert ss.value("a.old") == 7
    with pytest.warns(ss.DeprecatedKeyWarning):
        assert ss.ref("a.old") == 7
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert ss.value("a.new") == 7                                                     # the live key is silent
    assert ss.aliases()["a.old"] == ss.Alias("a.old", "a.new", "0.2.0", "renamed")
    assert "a.old" not in ss.all_entries()


@pytest.mark.parametrize("aliases, match", [
    ('  a.new: {to: a.new, since: "0.2.0"}\n', "also a live key"),
    ('  a.old: {to: a.gone, since: "0.2.0"}\n', "not a live key"),
    ('  a.old: {to: a.new}\n', "needs 'to' and 'since'"),
])
def test_a_bad_alias_is_refused(shared_tables, aliases, match):
    shared_tables("a.yaml", "entries:\n" + _LIVE + "aliases:\n" + aliases)
    with pytest.raises(ValueError, match=match):
        ss.aliases()


# ------------------------------------------------------------------- iron rule 5: the grep guard, as a function
def test_audit_tags_flags_a_comment_and_a_note_that_spell_the_tag(shared_tables):
    clean = shared_tables("ok.yaml", "# a header without the tag word\nentries:\n" + _LIVE)
    assert ss.audit_tags(clean) == []
    bad = shared_tables("bad.yaml", "# was changed to source: spec\nentries:\n" + _LIVE.replace(
        'cite: "f"', 'cite: "f"\n    note: "becomes source: spec once read"'))
    problems = ss.audit_tags(bad)
    assert any("bad.yaml:1:" in p for p in problems) and any("bad.yaml:8:" in p for p in problems)
    assert any("grep -c 'source: spec' = 2, entries = 0" in p for p in problems)


def test_audit_tags_allows_a_source_key_inside_a_value_but_not_in_prose(shared_tables):
    """mmw60_trx's assumed.pa60_surveyed_pick has ``value: {source: "pa60...", ...}``:
    a mapping key, breaks no count (its dry run found it).  The same word in a
    note, or ``source: <tag>`` anywhere but a tag line, is flagged."""
    data_key = _LIVE.replace("value: 7", 'value: {source: "pa60.asada_eumc2011", p: 1}')
    assert ss.audit_tags(shared_tables("ok.yaml", "entries:\n" + data_key)) == []
    in_note = _LIVE.replace('cite: "f"', 'cite: "f"\n    note: "its source: the datasheet"')
    assert len(ss.audit_tags(shared_tables("note.yaml", "entries:\n" + in_note))) == 1
    tag_value = _LIVE.replace("value: 7", "value: {source: spec}")
    assert any("grep -c 'source: spec' = 1, entries = 0" in p
               for p in ss.audit_tags(shared_tables("tag.yaml", "entries:\n" + tag_value)))
    inline = _LIVE.replace("value: 7", "value: 7   # was source: x")
    assert len(ss.audit_tags(shared_tables("inline.yaml", "entries:\n" + inline))) == 1


def test_legacy_keys_are_one_to_one_onto_live_keys():
    m = ss.legacy_keys("d2d_link")
    assert len(m) == 16 and len(set(m.values())) == 16
    assert all(new == f"ucie.{old}" and new in ss.all_entries() for old, new in m.items())
    with pytest.raises(FileNotFoundError):
        ss.legacy_keys("no_such_repo")
