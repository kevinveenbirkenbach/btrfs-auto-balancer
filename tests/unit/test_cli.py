import argparse
import unittest
from unittest import mock

from btrfs_auto_balancer.cli import main, positive_int


class TestPositiveInt(unittest.TestCase):
    def test_accepts_positive_values(self):
        self.assertEqual(positive_int("90"), 90)

    def test_rejects_zero_and_negatives(self):
        for value in ("0", "-1"):
            with (
                self.subTest(value=value),
                self.assertRaises(argparse.ArgumentTypeError),
            ):
                positive_int(value)


class TestMain(unittest.TestCase):
    def test_explicit_drive_path_skips_discovery(self):
        with (
            mock.patch("btrfs_auto_balancer.cli.get_btrfs_mounts") as mounts,
            mock.patch("btrfs_auto_balancer.cli.run_btrfs_balance") as balance,
        ):
            exit_code = main(["90", "10", "--drive_path", "/data"])

        mounts.assert_not_called()
        balance.assert_called_once_with("/data", 90, 10)
        self.assertEqual(exit_code, 0)

    def test_balances_every_discovered_mount(self):
        with (
            mock.patch("btrfs_auto_balancer.cli.get_btrfs_mounts") as mounts,
            mock.patch("btrfs_auto_balancer.cli.run_btrfs_balance") as balance,
        ):
            mounts.return_value = ["/", "/home"]
            exit_code = main(["90", "10"])

        self.assertEqual(
            [call.args for call in balance.call_args_list],
            [("/", 90, 10), ("/home", 90, 10)],
        )
        self.assertEqual(exit_code, 0)

    def test_missing_filesystems_exit_non_zero(self):
        with (
            mock.patch("btrfs_auto_balancer.cli.get_btrfs_mounts") as mounts,
            mock.patch("btrfs_auto_balancer.cli.run_btrfs_balance") as balance,
        ):
            mounts.return_value = []
            exit_code = main(["90", "10"])

        balance.assert_not_called()
        self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()
