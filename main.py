"""Print the funniest autocorrect fail (one line, under 200 chars).

Reads entry.txt next to this file, self-checks it against the gate
(single line, single sentence, under 200 characters), verifies a
write-then-read-back round trip in a temp file, and prints only the
entry to stdout. Standard library only; deterministic.
"""

import os
import re
import sys
import tempfile

MAX_CHARS = 200


def load_entry():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "entry.txt"), encoding="utf-8") as f:
        return f.read().strip()


def self_check(entry):
    assert "\n" not in entry, "entry must be a single line"
    assert len(entry) < MAX_CHARS, "entry must be under 200 characters"
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", entry) if s]
    assert len(sentences) == 1, "entry must be exactly one sentence"
    assert entry, "entry must not be empty"


def round_trip(entry):
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", suffix=".txt", delete=False
    ) as tmp:
        tmp.write(entry)
        path = tmp.name
    try:
        with open(path, encoding="utf-8") as f:
            assert f.read() == entry, "write/read-back mismatch"
    finally:
        os.unlink(path)


def main():
    entry = load_entry()
    self_check(entry)
    round_trip(entry)
    print(entry)
    return 0


if __name__ == "__main__":
    sys.exit(main())
