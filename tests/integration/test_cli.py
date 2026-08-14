import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"

FINDMNT_STUB = "#!/bin/sh\nexit 0\n"


def run_cli(*args, path_prefix=None, path=None):
    """Run 'python -m btrfs_auto_balancer' with the working tree on PYTHONPATH.

    Args:
        args: Command line arguments for the CLI.
        path_prefix: Directory prepended to PATH, used to stub out findmnt.
        path: Replacement PATH, used to hide findmnt and btrfs entirely.
    """
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC_DIR)
    if path is not None:
        env["PATH"] = str(path)
    if path_prefix:
        env["PATH"] = f"{path_prefix}{os.pathsep}{env['PATH']}"
    return subprocess.run(
        [sys.executable, "-m", "btrfs_auto_balancer", *args],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


class TestCli(unittest.TestCase):
    def test_help_exits_zero(self):
        result = run_cli("--help")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("btrfs balance", result.stdout)

    def test_zero_step_is_rejected(self):
        result = run_cli("90", "0")

        self.assertEqual(result.returncode, 2)
        self.assertIn("must be greater than zero", result.stderr)

    def test_missing_arguments_are_rejected(self):
        result = run_cli("90")

        self.assertEqual(result.returncode, 2)
        self.assertIn("count_down_step", result.stderr)

    def test_missing_findmnt_fails_cleanly(self):
        with tempfile.TemporaryDirectory() as empty:
            result = run_cli("90", "10", path=empty)

        self.assertEqual(result.returncode, 127)
        self.assertIn("required command 'findmnt' is not installed", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_missing_btrfs_fails_cleanly(self):
        with tempfile.TemporaryDirectory() as empty:
            result = run_cli("90", "10", "--drive_path", "/data", path=empty)

        self.assertEqual(result.returncode, 127)
        self.assertIn("required command 'btrfs' is not installed", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_reports_when_no_btrfs_filesystem_exists(self):
        with tempfile.TemporaryDirectory() as stub_dir:
            findmnt = os.path.join(stub_dir, "findmnt")
            with open(findmnt, "w") as handle:
                handle.write(FINDMNT_STUB)
            os.chmod(findmnt, 0o755)

            result = run_cli("90", "10", path_prefix=stub_dir)

        self.assertEqual(result.returncode, 1)
        self.assertIn("No Btrfs filesystems found.", result.stdout)


if __name__ == "__main__":
    unittest.main()
