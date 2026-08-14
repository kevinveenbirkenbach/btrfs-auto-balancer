import subprocess
import time

BALANCE_POLL_SECONDS = 2
MIN_USAGE = 5

REQUIRED_BINARIES = ("findmnt", "btrfs")
EXIT_MISSING_BINARY = 127


class MissingBinaryError(RuntimeError):
    """A required external command is not installed.

    Args:
        binary: Name of the missing executable.
    """

    def __init__(self, binary):
        super().__init__(f"required command '{binary}' is not installed")
        self.binary = binary


def get_btrfs_mounts():
    """Return the mount points of all currently mounted btrfs filesystems."""
    try:
        result = subprocess.run(
            ["findmnt", "-t", "btrfs", "-o", "TARGET", "--noheadings", "-n", "-r"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as error:
        raise MissingBinaryError("findmnt") from error

    return [line for line in result.stdout.strip().split("\n") if line]


def balance_command(drive_path, usage):
    """Return the btrfs balance command for a given usage threshold.

    Args:
        drive_path: Mount point to balance.
        usage: Threshold passed as both -dusage and -musage.
    """
    return [
        "btrfs",
        "balance",
        "start",
        f"-dusage={usage}",
        f"-musage={usage}",
        drive_path,
    ]


def print_balance_status(drive_path):
    """Print allocation and balance status of the given mount point."""
    try:
        subprocess.run(["btrfs", "fi", "df", drive_path], check=False)
        subprocess.run(["btrfs", "balance", "status", drive_path], check=False)
    except FileNotFoundError as error:
        raise MissingBinaryError("btrfs") from error


def run_btrfs_balance(drive_path, countdown, count_down_step):
    """Balance a mount point repeatedly, lowering the usage threshold each round.

    Args:
        drive_path: Mount point to balance.
        countdown: Initial dusage/musage threshold.
        count_down_step: Amount subtracted from the threshold after each round.
    """
    if count_down_step <= 0:
        raise ValueError("count_down_step must be greater than zero")

    while countdown > MIN_USAGE:
        command = balance_command(drive_path, countdown)
        print(" ".join(command))

        try:
            process = subprocess.Popen(command)
        except FileNotFoundError as error:
            raise MissingBinaryError(command[0]) from error

        while process.poll() is None:
            print_balance_status(drive_path)
            time.sleep(BALANCE_POLL_SECONDS)

        countdown -= count_down_step
