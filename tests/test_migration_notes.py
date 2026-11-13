"""The migration notes (cairn/migration-<repo>.md) name one full-SHA pin, the
same in every note, and no placeholder is left.  A note is deleted once its
library has migrated (AGENTS.md); with none left this file tests nothing."""
from __future__ import annotations

import re
import subprocess

import pytest
from conftest import REPO

NOTES = sorted((REPO / "cairn").glob("migration-*.md"))
_PIN_LINE = re.compile(r"\*\*PIN = `([0-9a-f]{40})`\*\*")


def _pin(path) -> str:
    pins = _PIN_LINE.findall(path.read_text(encoding="utf-8"))
    assert len(pins) == 1, f"{path.name}: one '**PIN = `<full sha>`**' line"
    return pins[0]


@pytest.mark.parametrize("note", NOTES, ids=lambda p: p.name)
def test_each_note_names_one_full_sha_and_uses_it_throughout(note):
    text = note.read_text(encoding="utf-8")
    pin = _pin(note)
    assert "<PIN>" not in text
    for sha in re.findall(r"spec_sources@([0-9a-f]+)", text):     # every attribution header in the note
        assert sha == pin, f"{note.name}: header pins {sha}, the note's PIN is {pin}"


def test_every_note_pins_the_same_commit():
    assert len({_pin(n) for n in NOTES}) <= 1


def test_the_pin_is_in_this_repositorys_history_when_the_history_is_here():
    if not NOTES:
        pytest.skip("no migration note left")
    pin = _pin(NOTES[0])
    if subprocess.run(["git", "-C", str(REPO), "cat-file", "-e", f"{pin}^{{commit}}"], capture_output=True).returncode:
        pytest.skip("shallow checkout: the pinned commit is not here")
    r = subprocess.run(["git", "-C", str(REPO), "merge-base", "--is-ancestor", pin, "HEAD"], capture_output=True)
    assert r.returncode == 0, f"PIN {pin} is not an ancestor of HEAD"
