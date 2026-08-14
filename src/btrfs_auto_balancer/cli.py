import argparse
import sys

from btrfs_auto_balancer.core import (
    EXIT_MISSING_BINARY,
    MissingBinaryError,
    get_btrfs_mounts,
    run_btrfs_balance,
)


def positive_int(value):
    """Argparse type accepting only integers greater than zero.

    Args:
        value: Raw argument string.
    """
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError(f"must be greater than zero: {value}")
    return number


def build_parser():
    """Return the argument parser for the btrfs-auto-balancer command."""
    parser = argparse.ArgumentParser(
        description="Run btrfs balance with countdown and display balance status."
    )
    parser.add_argument(
        "countdown",
        type=positive_int,
        help="Initial countdown value for dusage and musage.",
    )
    parser.add_argument(
        "count_down_step",
        type=positive_int,
        help="The step to decrement the countdown by each loop.",
    )
    parser.add_argument(
        "--drive_path",
        type=str,
        help=(
            "The drive path to balance (optional). If not provided, all Btrfs "
            "drives will be balanced."
        ),
    )
    return parser


def main(argv=None):
    """Balance one or all mounted btrfs filesystems.

    Args:
        argv: Argument list, defaults to sys.argv[1:].

    Returns:
        Process exit code.
    """
    args = build_parser().parse_args(argv)

    try:
        if args.drive_path:
            run_btrfs_balance(args.drive_path, args.countdown, args.count_down_step)
            return 0

        btrfs_mounts = get_btrfs_mounts()
        if not btrfs_mounts:
            print("No Btrfs filesystems found.")
            return 1

        for drive_path in btrfs_mounts:
            run_btrfs_balance(drive_path, args.countdown, args.count_down_step)
    except MissingBinaryError as error:
        print(f"Error: {error}", file=sys.stderr)
        return EXIT_MISSING_BINARY

    return 0
