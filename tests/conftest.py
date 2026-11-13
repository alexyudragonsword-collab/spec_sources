from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest
import yaml

from spec_sources import reader

REPO = Path(__file__).resolve().parents[1]
PACKAGE = REPO / "src" / "spec_sources"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
SIBLING_ROOTS = (Path("/home/user"), Path("/home/user/alexyudragonsword-collab"))

#: the source tables the entries came from: (repo, full SHA, path in that repo)
FIXTURE_FILES = {
    "mmw60_trx.survey.yaml": ("mmw60_trx", "13024e0b012923071d827cc557b0da5eb9a9b2aa",
                              "src/mmw60/data/spec/survey.yaml"),
    "d2d_link.ucie_survey.yaml": ("d2d_link", "6789810ccb6328324673222b2f64cc21f748451e",
                                  "src/d2d_link/data/spec/ucie_survey.yaml"),
    "fmcw_radar.sources.yaml": ("fmcw_radar", "2e5cbb61cef62819804fad89a197b0412b2eb84d",
                                "src/fmcw_radar/data/sources.yaml"),
    # not a source table: fmcw_radar's table when fmcw_radar#15 was accepted (its references, test_consumers.py)
    "fmcw_radar.sources.ffc703e.yaml": ("fmcw_radar", "ffc703ed2208ac5c5b59ac1666537520619125c5",
                                        "src/fmcw_radar/data/sources.yaml"),
}
#: 0.2.0 renamed mmw60_trx's 17 keys whose prefix was a tag (survey. / derived.), not a domain;
#: 0.3.0 retired the aliases (keys.lock: aliased=0.2.0 retired=0.3.0)
RENAMED_0_2_0 = {
    "survey.horowitz_mult32_pj": "horowitz2014.mult32_pj",
    "survey.horowitz_add32_pj": "horowitz2014.add32_pj",
    "survey.walden_fom_fj": "adc_survey.walden_fom_fj",
    "survey.walden_fom_range_fj": "adc_survey.walden_fom_range_fj",
    "survey.node_scale_45_to_7nm": "deepscale.node_scale_45_to_7nm",
    "survey.n_sd_11ac": "ieee80211ac.n_sd",
    "survey.n_sd_11be": "ieee80211be.n_sd",
    "survey.eht_tone_mapper_dtm": "ieee80211be.ldpc_tone_mapping_distance",
    "survey.ldpc_ppdu_encoding_thresholds": "ieee80211.ldpc_ppdu_encoding_thresholds",
    "survey.rx60_comm_iscas2015": "rx60.comm_iscas2015",
    "survey.dmg_sensitivity_assumptions": "dmg.sensitivity_assumptions",
    "survey.antenna60_okada2013_dbi": "antenna60.okada2013_dbi",
    "derived.cfo_liu2025_hz": "liu2025.cfo_from_ppm_hz",
    "derived.k_threshold_stf": "liu2025.k_threshold_stf",
    "derived.k_threshold_ltf_only": "liu2025.k_threshold_ltf_only",
    "derived.rapp_p1db_below_psat_db": "tgad_em.rapp_p1db_below_psat_db",
    "derived.pa60_rapp_p_asada_eumc2011": "pa60.asada_eumc2011_rapp_p",
}

_HEADER = re.compile(r"# fixture: (?P<repo>\S+)@(?P<sha>[0-9a-f]{40}) (?P<path>\S+)")
HEADER_LINES = 2


def fixture_text(name: str) -> str:
    """The source table as the commit holds it (the two header lines dropped)."""
    lines = (FIXTURES / name).read_text(encoding="utf-8").split("\n")
    return "\n".join(lines[HEADER_LINES:])


def fixture_header(name: str) -> dict:
    first = (FIXTURES / name).read_text(encoding="utf-8").split("\n", 1)[0]
    m = _HEADER.fullmatch(first)
    assert m, f"{name}: first line must be '# fixture: <repo>@<full sha> <path>'"
    return m.groupdict()


def fixture_entries(name: str) -> dict:
    return yaml.safe_load(fixture_text(name))["entries"]


def raw_entries() -> dict:
    """Every shared entry as its YAML mapping (no SpecNumber in between)."""
    out = {}
    for f in reader.data_files():
        out.update(yaml.safe_load(f.read_text(encoding="utf-8"))["entries"])
    return out


def sibling(repo: str) -> Path | None:
    for root in SIBLING_ROOTS:
        if (root / repo / ".git").exists():
            return root / repo
    return None


def git_show(repo: str, sha: str, path: str) -> str | None:
    root = sibling(repo)
    if root is None:
        return None
    r = subprocess.run(["git", "-C", str(root), "show", f"{sha}:{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


@pytest.fixture
def shared_tables(monkeypatch, tmp_path):
    """Point the reader at a scratch data directory; returns ``write(name, text)``."""
    data = tmp_path / "data"
    data.mkdir()
    monkeypatch.setattr(reader, "DATA_DIR", data)
    monkeypatch.setattr(reader, "_TABLE", None)
    monkeypatch.setattr(reader, "_ALIASES", None)

    def write(name: str, text: str) -> Path:
        p = data / name
        p.write_text(text, encoding="utf-8")
        reader._TABLE = None
        reader._ALIASES = None
        return p

    return write
