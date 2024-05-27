import subprocess
import time
import argparse

def get_btrfs_mounts():
    # Find all mounted btrfs filesystems using findmnt with proper formatting
    result = subprocess.run("findmnt -t btrfs -o TARGET --noheadings -n -r", shell=True, capture_output=True, text=True)
    btrfs_mounts = result.stdout.strip().split('\n')
    # Filter out any empty strings in case of extra newlines
    btrfs_mounts = [mount for mount in btrfs_mounts if mount]
    return btrfs_mounts

def run_btrfs_balance(drive_path, countdown, count_down_step):
    while countdown > 5:
        # Start the btrfs balance command in the background
        balance_cmd = f"btrfs balance start -dusage={countdown} -musage={countdown} {drive_path}"
        # Use Popen to start the command and allow the script to continue running
        print(balance_cmd)
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
    parser.add_argument("countdown", type=int, help="Initial countdown value for dusage and musage.")
    parser.add_argument("count_down_step", type=int, help="The step to decrement the countdown by each loop.")
    parser.add_argument("--drive_path", type=str, help="The drive path to balance (optional). If not provided, all Btrfs drives will be balanced.")

    args = parser.parse_args()
    
    if args.drive_path:
        # If drive_path is provided, run balance on it
        run_btrfs_balance(args.drive_path, args.countdown, args.count_down_step)
    else:
        # If drive_path is not provided, get all Btrfs mounts and run balance on each
        btrfs_mounts = get_btrfs_mounts()
        if not btrfs_mounts or btrfs_mounts == ['']:
            print("No Btrfs filesystems found.")
            exit(1)
        
        for drive_path in btrfs_mounts:
            run_btrfs_balance(drive_path, args.countdown, args.count_down_step)
