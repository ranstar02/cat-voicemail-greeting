#!/usr/bin/env python3
"""cat-voicemail-greeting: write one original funny cat voicemail greeting.

The greeting is fixed in this file. The program is fully deterministic:
no randomness, no network, no clock, no secrets, and no input besides
the output directory. Two runs produce byte-identical output.
"""

import os

GREETING = (
    "Hi, it's Biscuit. I'm in the box your bed came in. "
    "Leave a message after the beep \u2014 "
    "I'll knock it off the counter too."
)

MAX_LEN = 120


def output_path():
    """Where entry.txt goes: MAKEFUN_OUTPUT_DIR when the grader sets it,
    /output otherwise (the sandbox mount)."""
    base = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(base, "entry.txt")


def validate(text):
    """Enforce the competition gate before writing anything."""
    if not text or not text.strip():
        raise ValueError("greeting must not be empty")
    if text != text.strip():
        raise ValueError("greeting must not start or end with whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("greeting must be a single line")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        raise ValueError("greeting must not contain control characters")
    if len(text) > MAX_LEN:
        raise ValueError(
            "greeting must be at most %d characters, got %d"
            % (MAX_LEN, len(text))
        )


def main():
    validate(GREETING)
    path = output_path()
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(GREETING)

    # Read it back and confirm the file holds exactly the greeting.
    with open(path, "r", encoding="utf-8") as handle:
        stored = handle.read()
    if stored != GREETING:
        raise ValueError("verification failed: file differs from GREETING")
    if "\n" in stored or "\r" in stored:
        raise ValueError("verification failed: file is not a single line")

    print("%d characters" % len(GREETING))
    print(GREETING)


if __name__ == "__main__":
    main()
