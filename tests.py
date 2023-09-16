#!/usr/bin/env python3

from __future__ import annotations

import sys
import shutil
import tempfile
import unittest
import subprocess
from pathlib import Path

TESTS = Path(__file__).parent / 'tests'
VALIDATE_GENERATED_FILES = Path(__file__).parent / 'validate-generated-files.py'

EXPECTED = [
    (TESTS / 'ok', 0),
    (TESTS / 'mismatch', 1),
    (TESTS / 'missing-generated', 1),
    (TESTS / 'error', 2),
]


class SnapshotTests(unittest.TestCase):
    maxDiff = None

    def assertProcessSnapshot(
        self,
        directory: Path,
        target_files: list[Path],
        exit_code: int,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            tmp_dir = Path(tmp_dir_name)
            shutil.copytree(directory, tmp_dir, dirs_exist_ok=True)

            script = tmp_dir / 'run.sh'

            result = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATE_GENERATED_FILES),
                    '--files',
                    *target_files,
                    '--',
                    'bash',
                    str(script),
                ],
                capture_output=True,
                text=True,
                cwd=tmp_dir,
            )

            expected_err = (directory / 'stderr.snap').read_text()
            self.assertEqual(expected_err, result.stderr, "Stderr snapshot is incorrect")

            expected_out = (directory / 'stdout.snap').read_text()
            self.assertEqual(expected_out, result.stdout, "Stdout snapshot is incorrect")

            self.assertEqual(exit_code, result.returncode, "Unexpected return code")

    def test_snapshot(self) -> None:
        for directory, exit_code in EXPECTED:
            with self.subTest(directory.name):
                self.assertProcessSnapshot(
                    directory,
                    [x.relative_to(directory) for x in directory.glob('*.out')],
                    exit_code,
                )

    def test_missing_original_file(self) -> None:
        self.assertProcessSnapshot(
            TESTS / 'missing-originals',
            [Path('missing.out')],
            exit_code=2,
        )


if __name__ == '__main__':
    unittest.main()
