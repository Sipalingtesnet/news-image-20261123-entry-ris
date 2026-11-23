#!/usr/bin/env python3
"""Copy the repo's entry.png to the output directory, verifying its sha256.

Stdlib only, no network. Writes to MAKEFUN_OUTPUT_DIR (or /output) as
entry.png. Exits 0 on success.
"""
import hashlib
import os
import shutil
import sys

REPO_ENTRY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
EXPECTED_SHA = "16f545c95a6a5f1e4762963adce077052341cc91deb190e75e0610d2a701c76d"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")

    actual = sha256(REPO_ENTRY)
    if actual != EXPECTED_SHA:
        print("sha256 mismatch: expected %s got %s" % (EXPECTED_SHA, actual))
        sys.exit(1)

    shutil.copyfile(REPO_ENTRY, out_path)
    print(actual)
    sys.exit(0)


if __name__ == "__main__":
    main()