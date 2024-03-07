import subprocess
import time
import argparse

def run_btrfs_balance(drive_path, countdown, count_down_step):
    while countdown > 5:
        # Start the btrfs balance command in the background
        balance_cmd = f"btrfs balance start -dusage={countdown} -musage={countdown} {drive_path} &"
        subprocess.run(balance_cmd, shell=True)
        
        # Wait a bit for the balance command to start before querying the status
        time.sleep(2)
        
        # Display the status of the balancing
        for _ in range(5):  # Adjustable based on how often you want to show the status
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
