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
