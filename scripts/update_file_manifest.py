#!/usr/bin/env python3
"""Rebuild FILE_MANIFEST.sha256 from tracked and non-ignored Git files."""
from pathlib import Path
import hashlib
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
try:
    raw = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root,
    )
except (subprocess.CalledProcessError, FileNotFoundError) as exc:
    print(f"Could not enumerate Git files: {exc}", file=sys.stderr)
    raise SystemExit(1)

paths = sorted(p for p in raw.decode("utf-8").split("\0") if p and p != "FILE_MANIFEST.sha256")
lines = []
for rel in paths:
    path = root / rel
    if path.is_file():
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {rel.replace(chr(92), '/')}")
(root / "FILE_MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Updated FILE_MANIFEST.sha256: {len(lines)} files")
