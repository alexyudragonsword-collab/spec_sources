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
       "itu_p676.gamma_o_dry_sea_level_peak", "target_rcs.deep2019_pedestrian_77g",
       # milestone 2 batch 1, read in four of the originals Asada's Table I quotes (rows [1], [2], [6], [13])
       "pa60.chan_isscc2009", "pa60.lai_isscc2010", "pa60.law_isscc2010", "pa60.tanomura_isscc2008",
       "pa60.martineau_isscc2010", "pa60.kuo_mwcl2009", "pa60.jin_esscirc2007",
       # milestone 2 batch 2, read in Wu, Staszewski, Long, JSSC 2014 (not migrated from a table)
       "adpll60.wu_jssc2014_tdc", "tdc.henzler_isscc2008", "tdc.henzler_isscc2008_single_shot_s",
       # milestone 2 batch 3, read in the UCIe consortium's Hot Chips 2023 tutorial
       "ucie.raw_ber_by_rate", "ucie.advanced.spare_lanes_per_32",
       # milestone 2 batch 4, read in NHTSA DOT HS 813 648 (ISO 19206-3 boundaries) and Sandia SAND2008-0396
       "target_rcs.iso19206_3_car_rear", "target_rcs.iso19206_3_car_30m",
       "target_rcs.iso19206_3_car_rear_far_lower_dbsm", "target_rcs.trihedral_peak",
       # milestone 2 batch 4, read in Harris, Proc. IEEE 1978, Table I
       "harris1978.rect", "harris1978.hann", "harris1978.hamming", "harris1978.exact_blackman",
       "harris1978.blackman",
       # issue #26 (mmw60_trx): Liu 2025's journal version and the two IEEE 802.15 documents its [15] points to
       "liu2025.table1_idft_period_s", "liu2025.table1_idft_size", "liu2025.cfo_algorithm_statement",
       "liu2025.mlo_bf_training_statement", "tg3c.pn_model", "tg3c.pn_psd0_examples_dbchz",
       "tg3c.pa_modified_rapp_shape", "tg3c.pa_ghorbani_nec_gaas",
       # issue #29 (mmw60_trx): DMG / EDMG PHY from public TGad / TGay contributions and R&S 1MA220
       "dmg.phy_params", "dmg.sc_mcs", "dmg.ofdm_mcs", "dmg.tx_evm_db", "dmg.rx_sensitivity_dbm",
       "edmg.ofdm_params", "edmg.ofdm_pilot_tones_ncb1", "edmg.ofdm_pilot_values_ncb1", "edmg.ofdm_mcs",
       "edmg.ofdm_rate_mbps", "edmg.sc_params", "edmg.sc_mcs", "edmg.sc_mcs_variants", "edmg.sc_rate_mbps",
       # batch 7: the six Murmann-survey rows the two adc_survey statistics are recomputed from
       "adc_survey.ti_sar_ge40gs_4to7nm",
       # issue #33 (mmw60_trx): DMG / EDMG LDPC codes, encoding, extended SC MCS, control PHY and sector sweep
       "dmg.ldpc_matrices", "dmg.data_encoding", "dmg.sc_mcs_extended", "dmg.ldpc_r7_8_punctured",
       "dmg.control_phy", "dmg.control_phy_rate_bps", "dmg.phy_timing", "dmg.ssw_frame",
       "edmg.ldpc_672_r7_8", "edmg.ldpc_1344_lifting", "edmg.sc_encoding", "edmg.short_ssw",
       # the per-node energy table in DeepScaleTool's own file the 45 -> 7 nm ratio is recomputed from
       "deepscale.energy_by_node",
       # milestone 2 batch 1, the last six rows of Asada's Table I read in their originals (2026-11-17)
       "pa60.suzuki_isscc2008", "pa60.kurita_rfic2009", "pa60.bohsali_rfic2009", "pa60.dawn_ims2009",
       "pa60.pinel_isscc2008", "pa60.chowdhury_isscc2008",
       # issue #43 (mmw60_trx): control PHY codewords, DMG / EDMG preamble chips, EDMG control mode, OFDM mapping
       "dmg.control_phy_encoding", "dmg.sc_ppdu_chips", "edmg.sc_siso_preamble", "edmg.control_mode_encoding",
       "edmg.ofdm_modulation_mapping"}
#: migrated entries since read in the original (milestone 2): survey -> spec. Their value and unit
#: still equal the source table; tag, cite, note, quote and section are the verification's own.
VERIFIED = {k: "0.3.0 (IEEE 802.11-09/0296r16)" for k in (
    "tgad_em.pa_rapp_g", "tgad_em.pa_rapp_asat", "tgad_em.pa_rapp_p", "tgad_em.pa_ampm_alpha",
    "tgad_em.pa_ampm_beta", "tgad_em.pa_ampm_q1", "tgad_em.pa_ampm_q2", "tgad_em.pa_model_shape",
    "tgad_em.pn_model_shape")}
# milestone 2 batch 3: read in the UCIe consortium's public Hot Chips 2023 tutorial and 2022 white paper
VERIFIED.update({k: "0.4.0 (Hot Chips 2023 UCIe tutorial; UCIe white paper 2022)" for k in (
    "ucie.data_rates_gtps", "ucie.forwarded_clock", "ucie.raw_ber_target", "ucie.raw_ber_with_retry",
    "ucie.rx_eye_height_mv", "ucie.rx_eye_width_ui", "ucie.rx_eye_width_ui@24-32", "ucie.tx_swing_vpp",
    "ucie.standard.bump_pitch_um", "ucie.standard.reach_mm", "ucie.standard.module_width_lanes",
    "ucie.advanced.bump_pitch_um", "ucie.advanced.reach_mm", "ucie.advanced.module_width_lanes",
    "ucie.advanced.lane_repair")})
# issue #26: read in Liu 2025's journal version (IEEE Commun. Mag. 63(3), 2025); the source table read arXiv v1 / v2
VERIFIED.update({k: "issue #26 (Liu 2025, IEEE Commun. Mag. 63(3))" for k in (
    "liu2025.mcs_list", "liu2025.ppdu_format", "liu2025.channel_model", "liu2025.antennas", "liu2025.carrier_hz",
    "liu2025.packet_bytes", "liu2025.xo_ppm_tx", "liu2025.xo_ppm_rx", "liu2025.cfo_max_hz", "liu2025.stf_capture_hz",
    "liu2025.ltf_capture_hz", "liu2025.scs_threshold_hz", "liu2025.k_threshold", "liu2025.pn_f_pole_hz",
    "liu2025.pn_f_zero_hz", "liu2025.pn_psd0_dbchz", "liu2025.pa_obo_db", "liu2025.mmwave_spectrum_ghz")})
# issue #29: read in public IEEE 802.11 contributions (the standard itself may not be input to AI);
# the user checked them against IEEE 802.11-2024
VERIFIED.update({k: "issue #29 (TGay 11-17/0597r1; TGad 11-10/0433r2)" for k in (
    "ieee80211ay.channel_centres_ghz", "dmg.sensitivity_assumptions")})
# batch 7: eCFR (47 CFR 15.255), arXiv v1 of Liu 2025, and public IEEE 802.11 contributions (TGn / TGac / TGax / TGbe)
_BATCH7 = "batch 7 (eCFR; arXiv:2309.16813v1; IEEE 802.11-05/1102r4, 09/0992r21, 15/0330r5, 15/0132r17, 19/1262r23)"
VERIFIED.update({k: _BATCH7 for k in (
    "fcc15255.band_low_hz", "fcc15255.band_high_hz", "fcc15255.eirp_avg_dbm", "fcc15255.eirp_peak_dbm",
    "liu2025.per_target", "ieee80211ac.n_sd", "ieee80211be.n_sd", "ieee80211be.ldpc_tone_mapping_distance",
    "ieee80211.ldpc_ppdu_encoding_thresholds")})
# the IEEE Xplore originals the user downloaded and confirmed their licence lets spec_sources read (2026-11-17)
VERIFIED.update({k: "Xplore originals, 2026-11-17 (Horowitz ISSCC 2014; Luo ISCAS 2015; Okada JSSC 2013)" for k in (
    "horowitz2014.mult32_pj", "horowitz2014.add32_pj", "rx60.comm_iscas2015", "antenna60.okada2013_dbi")})
#: migrated entries read in the original, which disagrees with the source table: survey -> spec, and the
#: value (or unit) changed to the original's -- {key: {field: (source value, value now)}}
CORRECTED = {
    # issue #26: the journal's Table 1 bases all three columns on 802.11ac (arXiv's 16x column was 802.11be)
    "liu2025.table1_scs_hz": {"value": ({4: 1.25e6, 8: 2.5e6, 16: 1.25e6}, {4: 1.25e6, 8: 2.5e6, 16: 5.0e6})},
    "liu2025.table1_bandwidth_hz": {"value": (
        {4: [80e6, 160e6, 320e6, 640e6], 8: [160e6, 320e6, 640e6, 1280e6], 16: [320e6, 640e6, 1280e6, 2560e6, 5120e6]},
        {4: [80e6, 160e6, 320e6, 640e6], 8: [160e6, 320e6, 640e6, 1280e6], 16: [320e6, 640e6, 1280e6, 2560e6]})},
    # issue #26: the journal tracks the phase at the receiver; arXiv said no estimation / compensation for CFO and PN
    # batch 7: recomputed from the six rows of the Murmann survey; Halo_Serdes had rounded the median 70.8 to 70
    "adc_survey.walden_fom_fj": {"value": (70.0, 70.815)},
    "adc_survey.walden_fom_range_fj": {"value": ([38.4, 120.2], [38.36, 120.19])},
    # recomputed from DeepScaleTool's per-node energy table, 0.11 / 0.63; Halo_Serdes had kept 3 digits
    "deepscale.node_scale_45_to_7nm": {"value": (0.175, 0.1746)},
    "liu2025.receiver_cfo_statement": {"value": (
        "refrained from using estimation and compensation algorithms for CFO and PN",
        "refrained from using estimation and compensation algorithms for CFO and used phase tracking"
        " only on the receiving end")},
}
#: fields changed on the way in: {key: {field: (old text, new text)}}; each is
#: a replacement applied to the source's field and nothing else
CHANGED = {
    # iron rule 5: the note spelled the tag word with a colon (d2d_link's grep counted 0 spec lines as 1)
    "ucie.rx_eye_width_ui@24-32": {"note": ("改 source: spec 或删去", "改成 spec 标签或删去")},
    # 0.2.0: cross-references to renamed keys follow the rename
    "liu2025.k_threshold_stf": {"cite": ("derived.cfo_liu2025_hz", "liu2025.cfo_from_ppm_hz")},
    "liu2025.k_threshold_ltf_only": {"cite": ("derived.cfo_liu2025_hz", "liu2025.cfo_from_ppm_hz")},
    # milestone 2 batch 1: four of the 13 quoted rows read in their originals; the note says which and what differs
    # (and names the library instead of the migrated "本库")
    # milestone 2 batch 3: still survey (the x8 is in neither public source); the note says what was read
    "ucie.standard.lane_repair": {"note": (
        "未核实:标准封装靠降宽度修复,先进封装靠备用 lane;本库两种都做成配置项。",
        "未核实:标准封装靠降宽度修复、没有备用 lane，已见联盟白皮书（'the standard pac"
        "kage supports width degradation to handle failures"
        "'）与 Hot Chips 2023 教程（'Width degrade for Standard "
        "pkg'）；降到 x8 这一点两者都没写，所以仍标 survey。本库两种修复都做成配置项。")},
    "pa60.eumc2011_table1": {"note": (
        "表里其他各行是它转引的、本库没有读各自的原文；用来看量级与分布，不用作基准档。"
        "14 行的 Psat 8–19.9 dBm（中位 12.45），Psat − P1dB 1.0–9.0 dB（中位 3.3），"
        "只有 [1] 一行（9.0 dB）接近 11ad 评估方法学那颗 Rapp 的 9.5 dB。",
        "表里其他各行是它转引的。spec_sources 读了全部 13 行的原文（里程碑 2 第 1 批；7 "
        "行在 2026-11-13–14，[5] [7] [8] [10] [12] [14] 在 2026-1"
        "1-17）：[1] pa60.chan_isscc2009、[2] pa60.lai_isscc2010"
        "、[5] pa60.suzuki_isscc2008、[6] pa60.law_isscc2010、[7"
        "] pa60.kurita_rfic2009、[8] pa60.bohsali_rfic2009、[9]"
        " pa60.kuo_mwcl2009、[10] pa60.dawn_ims2009、[11] pa60."
        "jin_esscirc2007、[12] pa60.pinel_isscc2008、[13] pa60."
        "tanomura_isscc2008、[14] pa60.chowdhury_isscc2008、[15"
        "] pa60.martineau_isscc2010。P1dB、Psat 13 行都与原文相同；峰值 P"
        "AE 除 [5] 外都相同，[5] 的 5.0 % 原文里没有（Suzuki 没给效率，Asada 那行"
        "的 1.0 V 原文是 1.2 V）。增益有几格要注意：[1] 原文表是 15.8（这里 16.0）；["
        "13] 的 15.2 是原文 0.7 V 时 60 GHz 的线性增益，同一行另外三格是 1.0 V 的"
        "（1.0 V 线性增益 14.3），这格看来转抄自 [9] 的对比表；[8] 的 4.4 是正文的 S2"
        "1，原文汇总表的功率增益是 4.2；[14] 的 5.5 是图上的标注，正文的 S21 是 5.6。[1"
        "1] 四格都在原文里，但不是 60 GHz 的：增益是 52 GHz 的峰值，功率是 48 GHz 的，"
        "60 GHz 时增益只有 11 dB。用来看量级与分布，不用作基准档。14 行的 Psat 8–19.9"
        " dBm（中位 12.45），Psat − P1dB 1.0–9.0 dB（中位 3.3）。只有 [1]"
        " 一行（9.0 dB）接近 11ad 评估方法学那颗 Rapp 的 9.5 dB，而原作者自己把这颗 P"
        "A 的 P1dB 偏低归于各级偏置不当造成的提前压缩（pa60.chan_isscc2009）；去掉这一"
        "行，最大是 [15] 的 5.6 dB，而它的 Psat 是功率扫描终点（Pin = 10 dBm）的输"
        "出、曲线仍在上升，真实的差只会更大，同一颗 PA 在 1.8 V 时是 6.6 dB（pa60.mart"
        "ineau_isscc2010）。")},
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
    if new_key in CORRECTED:
        assert src["source"] == "survey", new_key
        assert dst["source"] == "derived" or (dst["source"] == "spec" and dst["quote"] and dst["section"]), new_key
        for field in ("value", "unit"):
            if field in CORRECTED[new_key]:
                old, new = CORRECTED[new_key][field]
                assert src[field] == old and dst[field] == new and new != old, (new_key, field)
            else:
                assert dst[field] == src[field], (new_key, field)
        return
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
    assert len(mmw) + len(ucie) + len(NEW) == 63 + 16 + 79 == 158
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
