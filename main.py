#!/usr/bin/env python3
"""Fortune Cookie for the Liquidated Trader entry (make.fun).

Writes a single original fortune-cookie line for a crypto trader who
has just been liquidated, to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR
/entry.txt when the harness sets it). Stdlib only; no network, no files
read, no secrets.

The line: the market ate the trader's margin and left only crumbs —
and the cookie's turn is that crumbs, properly savoured, are a feast.
Fortune voice up front, the loss in the first clause, the punchline in
the last word; rueful and warm, never cruel, and no liquidation pun.
"""

import os
import sys

MAX_CHARS = 160
MAX_WORDS = 20

FORTUNE = (
    "The market ate your margin and left you the crumbs; "
    "chew them slowly, for crumbs, properly savored, are a feast."
)


def validate(text: str) -> str:
    """Return the stripped line, enforcing the gate's rules."""
    text = text.strip()
    if not text:
        raise ValueError("fortune is empty")
    if len(text) > MAX_CHARS:
        raise ValueError(f"fortune is {len(text)} chars, must be 1-{MAX_CHARS}")
    if len(text.split()) > MAX_WORDS:
        raise ValueError(f"fortune is {len(text.split())} words, must be 1-{MAX_WORDS}")
    if "\n" in text:
        raise ValueError("fortune must be a single line")
    return text


def write_entry(text: str, out_dir: str) -> str:
    """Write the fortune to entry.txt inside out_dir; return the path."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    # Re-read what landed on disk and make sure it is exactly the
    # validated line — a partial write must fail loudly, not silently.
    with open(path, "r", encoding="utf-8") as f:
        if f.read() != text:
            raise ValueError("entry.txt on disk does not match the fortune")
    return path


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    text = validate(FORTUNE)
    path = write_entry(text, out_dir)
    print(text)
    print(f"wrote {len(text)} chars to {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
