import unittest
from unittest import mock

from btrfs_auto_balancer.core import (
    REQUIRED_BINARIES,
    MissingBinaryError,
    balance_command,
    get_btrfs_mounts,
    print_balance_status,
    run_btrfs_balance,
)


class TestGetBtrfsMounts(unittest.TestCase):
    def test_parses_one_mount_per_line(self):
        with mock.patch("btrfs_auto_balancer.core.subprocess.run") as run:
            run.return_value.stdout = "/\n/home\n"
            self.assertEqual(get_btrfs_mounts(), ["/", "/home"])

    def test_no_mounts_yields_empty_list(self):
        with mock.patch("btrfs_auto_balancer.core.subprocess.run") as run:
            run.return_value.stdout = "\n"
            self.assertEqual(get_btrfs_mounts(), [])


class TestMissingBinaries(unittest.TestCase):
    def test_declares_every_external_command_the_package_calls(self):
        self.assertEqual(set(REQUIRED_BINARIES), {"findmnt", "btrfs"})

    def test_missing_findmnt_is_reported(self):
        with mock.patch("btrfs_auto_balancer.core.subprocess.run") as run:
            run.side_effect = FileNotFoundError

            with self.assertRaises(MissingBinaryError) as caught:
                get_btrfs_mounts()

        self.assertEqual(caught.exception.binary, "findmnt")

    def test_missing_btrfs_in_status_is_reported(self):
        with mock.patch("btrfs_auto_balancer.core.subprocess.run") as run:
            run.side_effect = FileNotFoundError

            with self.assertRaises(MissingBinaryError) as caught:
                print_balance_status("/data")

        self.assertEqual(caught.exception.binary, "btrfs")

    def test_missing_btrfs_in_balance_is_reported(self):
        with mock.patch("btrfs_auto_balancer.core.subprocess.Popen") as popen:
            popen.side_effect = FileNotFoundError

            with self.assertRaises(MissingBinaryError) as caught:
                run_btrfs_balance("/data", 90, 10)

        self.assertEqual(caught.exception.binary, "btrfs")


class TestBalanceCommand(unittest.TestCase):
    def test_sets_both_usage_thresholds(self):
        self.assertEqual(
            balance_command("/data", 75),
            ["btrfs", "balance", "start", "-dusage=75", "-musage=75", "/data"],
        )


class TestRunBtrfsBalance(unittest.TestCase):
    def _run(self, countdown, step):
        with (
            mock.patch("btrfs_auto_balancer.core.subprocess.Popen") as popen,
            mock.patch("btrfs_auto_balancer.core.print_balance_status"),
            mock.patch("btrfs_auto_balancer.core.time.sleep"),
        ):
            popen.return_value.poll.return_value = 0
            run_btrfs_balance("/data", countdown, step)
        return [call.args[0] for call in popen.call_args_list]

    def test_counts_down_to_the_minimum_usage(self):
        commands = self._run(20, 5)

        self.assertEqual(
            [command[3] for command in commands],
            ["-dusage=20", "-dusage=15", "-dusage=10"],
        )

    def test_threshold_at_or_below_minimum_does_nothing(self):
        self.assertEqual(self._run(5, 1), [])

    def test_zero_step_is_rejected(self):
        with self.assertRaises(ValueError):
            run_btrfs_balance("/data", 90, 0)

    def test_polls_until_the_balance_process_exits(self):
        with (
            mock.patch("btrfs_auto_balancer.core.subprocess.Popen") as popen,
            mock.patch("btrfs_auto_balancer.core.print_balance_status") as status,
            mock.patch("btrfs_auto_balancer.core.time.sleep"),
        ):
            popen.return_value.poll.side_effect = [None, None, 0]
            run_btrfs_balance("/data", 10, 5)

        self.assertEqual(status.call_count, 2)


if __name__ == "__main__":
    unittest.main()
