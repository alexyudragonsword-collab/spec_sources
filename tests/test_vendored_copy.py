"""``src/spec_sources/`` copied out on its own works: a consumer vendors it
under its own package (attribution header on every file, the way its
``vendor_check --strict`` wants), imports it from there and reads the
tables -- without the original package ever being imported."""
from __future__ import annotations

import ast
import json
import shutil
import subprocess
import sys
from pathlib import Path

from conftest import PACKAGE

import spec_sources as ss

PIN = "0" * 40     # a consumer writes the full SHA it pins
#: what the reader may import: the standard library and PyYAML, nothing else
ALLOWED_IMPORTS = {"__future__", "re", "warnings", "dataclasses", "pathlib", "yaml"}


def _package_files() -> list[Path]:
    return sorted(p for p in PACKAGE.rglob("*") if p.is_file() and "__pycache__" not in p.parts)


def _vendor(root: Path, only: set[str] | None = None) -> Path:
    """Copy the package to ``root/consumer_pkg/vendor/spec_sources`` with a
    two-line attribution header on every file."""
    dest = root / "consumer_pkg" / "vendor" / "spec_sources"
    for p in _package_files():
        rel = p.relative_to(PACKAGE).as_posix()
        if only is not None and rel not in only:
            continue
        out = dest / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        header = (f"# Vendored from spec_sources@{PIN}: src/spec_sources/{rel}\n"
                  "# Adapted-copy policy: see src/consumer_pkg/vendor/__init__.py\n")
        out.write_text(header + p.read_text(encoding="utf-8"), encoding="utf-8")
    for d in (root / "consumer_pkg", root / "consumer_pkg" / "vendor"):
        (d / "__init__.py").write_text("", encoding="utf-8")
    return dest


_PROBE = r"""
import json, sys, warnings
sys.path.insert(0, sys.argv[1])
warnings.simplefilter("error")
from consumer_pkg.vendor import spec_sources as s
assert "spec_sources" not in sys.modules, "the original package was imported"
out = {"file": s.__file__, "n": len(s.all_entries()),
       "tags": {t: len(s.by_source(t)) for t in s.SOURCES},
       "audit": [p for f in s.data_files() for p in s.audit_tags(f)]}
if "ucie.raw_ber_target" in s.all_entries():
    out["ucie"] = s.value(s.legacy_keys("d2d_link")["raw_ber_target"])
if "rx60.radar_iwr6843_fig7_2" in s.all_entries():
    out["ref"] = s.ref("rx60.radar_iwr6843_fig7_2#p1db_inband_dbm@gain_db=40")
print(json.dumps(out))
"""


def _probe(root: Path) -> dict:
    r = subprocess.run([sys.executable, "-c", _PROBE, str(root)], capture_output=True, text=True, cwd=root)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def test_the_whole_package_works_from_a_temporary_copy(tmp_path):
    dest = _vendor(tmp_path)
    out = _probe(tmp_path)
    assert Path(out["file"]).resolve().is_relative_to(dest.resolve())
    assert out["n"] == len(ss.all_entries()) == 95
    assert out["tags"] == {t: len(ss.by_source(t)) for t in ss.SOURCES}
    assert out["audit"] == []                         # the attribution headers do not break the grep guard
    assert out["ucie"] == 1.0e-27 and out["ref"] == -34.0


def test_a_consumer_may_copy_only_the_tables_it_reads(tmp_path):
    """d2d_link's cut: the reader, its table and its old-key map."""
    _vendor(tmp_path, only={"__init__.py", "reader.py", "data/ucie.yaml", "legacy_keys/d2d_link.yaml"})
    out = _probe(tmp_path)
    assert out["n"] == 16 and out["tags"]["survey"] == 16 and out["ucie"] == 1.0e-27 and "ref" not in out


def test_the_copy_survives_being_moved(tmp_path):
    """Nothing in the package remembers where it was: copy, then move the copy."""
    _vendor(tmp_path / "a")
    shutil.move(str(tmp_path / "a"), str(tmp_path / "b"))
    assert _probe(tmp_path / "b")["n"] == 95


def test_the_reader_imports_only_the_standard_library_and_pyyaml():
    for p in PACKAGE.glob("*.py"):
        for node in ast.walk(ast.parse(p.read_text(encoding="utf-8"))):
            if isinstance(node, ast.ImportFrom):
                assert node.level == 1 or node.module.split(".")[0] in ALLOWED_IMPORTS, (p.name, node.module)
            elif isinstance(node, ast.Import):
                assert all(a.name.split(".")[0] in ALLOWED_IMPORTS for a in node.names), p.name
