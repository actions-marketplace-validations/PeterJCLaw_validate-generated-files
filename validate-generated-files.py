#!/usr/bin/env python3

"""
Utility to validate that generated files are up to date.

This is typically useful in contexts where, for one reason or another, generated
files are stored in a version control repository alongside their inputs.
"""

from __future__ import annotations

import sys
import difflib
import argparse
import subprocess
from pathlib import Path


def print_banner(text: str) -> None:
    print("--" * 25)
    print(text)
    print("--" * 25)


def main(args: argparse.Namespace) -> None:
    files: list[Path] = args.files

    originals = []
    for path in files:
        try:
            originals.append(path.read_bytes())
        except IOError:
            print(f"{path} could not be read.", file=sys.stderr)
            continue

    if len(originals) != len(files):
        exit(2)

    result = subprocess.run(args.command)
    if result.returncode:
        print("Command failed", file=sys.stderr)
        exit(2)

    mismatches = False
    for path, original_bytes in zip(files, originals):
        try:
            actual_bytes = path.read_bytes()
        except IOError:
            mismatches = True
            print_banner(f"{path} is missing after running command")
            continue

        try:
            original = original_bytes.decode()
            actual = actual_bytes.decode()

            diff = ''.join(difflib.unified_diff(
                original.splitlines(keepends=True),
                actual.splitlines(keepends=True),
                fromfile=f"{path} : original",
                tofile=f"{path} : generated",
            ))
            if diff:
                mismatches = True
                print_banner(str(path))
                print(diff, end='')

        except UnicodeDecodeError:
            if actual_bytes != original_bytes:
                mismatches = True
                print(f"Binary file {path} has changes")
                continue

    exit(1 if mismatches else 0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--files',
        type=Path,
        nargs=argparse.ONE_OR_MORE,
        required=True,
        help="The files to validate.",
    )
    parser.add_argument(
        'command',
        metavar='COMMAND_PART',
        type=Path,
        nargs=argparse.ONE_OR_MORE,
        help="The command to run which will produce the files.",
    )
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
