import subprocess
import time
import argparse

def run_btrfs_balance(drive_path, countdown, count_down_step):
    while countdown > 5:
        # Start the btrfs balance command in the background
        balance_cmd = f"btrfs balance start -dusage={countdown} -musage={countdown} {drive_path}"
        # Use Popen to start the command and allow the script to continue running
        balance_process = subprocess.Popen(balance_cmd, shell=True)
        
        # Continuously display the status of the balancing until the balance command finishes
        while balance_process.poll() is None:  # poll() returns None while the process is running
            subprocess.run(f"btrfs fi df {drive_path}", shell=True)
            subprocess.run(f"btrfs balance status {drive_path}", shell=True)
            time.sleep(2)  # Wait for 2 seconds before showing the next status
        
        # Update countdown for the next iteration
        countdown -= count_down_step

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run btrfs balance with countdown and display balance status.")
    parser.add_argument("drive_path", type=str, help="The drive path to balance.")
    parser.add_argument("countdown", type=int, help="Initial countdown value for dusage and musage.")
    parser.add_argument("count_down_step", type=int, help="The step to decrement the countdown by each loop.")

    args = parser.parse_args()

    run_btrfs_balance(args.drive_path, args.countdown, args.count_down_step)
