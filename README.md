# Auto Btrfs Balancer

The Auto Btrfs Balancer is a Python script designed for automating the management of Btrfs filesystem balancing. It intelligently decrements usage thresholds while simultaneously providing real-time balance status updates. This tool simplifies the maintenance of Btrfs volumes by executing balance operations with dynamic parameters, ensuring efficient storage utilization and enhanced system performance.

## Features

- Automates Btrfs balance operations with dynamic decrementing usage thresholds.
- Provides real-time status updates on Btrfs balance operations.
- Simplifies Btrfs volume maintenance for improved storage utilization and system performance.
- Supports balancing operations on all mounted Btrfs filesystems if no specific drive path is provided.

## Requirements

- Python 3.x
- Btrfs file system
- Linux Operating System

## Usage

To use the Auto Btrfs Balancer, clone this repository to your local machine and run the script with the required arguments. Here is a basic example:

### Balancing a specific Btrfs drive:

```bash
python auto_btrfs_balancer.py <countdown> <count_down_step> --drive_path <drive_path>
```

### Balancing all mounted Btrfs drives:

```bash
python auto_btrfs_balancer.py <countdown> <count_down_step>
```

Replace `<countdown>`, `<count_down_step>`, and optionally `<drive_path>` with your specific parameters.

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/kevinveenbirkenbach/auto-btrfs-balancer.git
```

Navigate to the cloned directory and run the script as shown in the [Usage](#usage) section.

## Author

**Kevin Veen-Birkenbach**

- Email: [kevin@veen.world](mailto:kevin@veen.world)
- Website: [https://www.veen.world/](https://www.veen.world/)

## License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project was inspired by a conversation about automating Btrfs balance operations. For more context and the development background, you can refer to [this](https://chatgpt.com/share/27c9bf71-0f68-494c-8592-fc24e01b9997) and [this conversation](https://chat.openai.com/share/a12d8fdf-3adb-4533-9dcf-b71612e9af61).