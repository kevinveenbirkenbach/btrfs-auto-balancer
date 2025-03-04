# Btrfs Auto Balancer (btrfsauba)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org)
[![GitHub stars](https://img.shields.io/github/stars/kevinveenbirkenbach/btrfs-auto-balancer.svg?style=social)](https://github.com/kevinveenbirkenbach/btrfs-auto-balancer/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/kevinveenbirkenbach/btrfs-auto-balancer.svg?style=social)](https://github.com/kevinveenbirkenbach/btrfs-auto-balancer/network)

**Btrfs Auto Balancer** is a Python utility that automates the balancing process for Btrfs filesystems. It dynamically adjusts usage thresholds while providing real-time status updates, ensuring efficient storage utilization and improved system performance on your Linux system. ⚙️💾

## 🎯 Purpose

Btrfs Auto Balancer simplifies Btrfs volume maintenance by automating the balance process. It dynamically decrements usage thresholds (for both data and metadata) and displays real-time status updates during balancing operations. Whether you're managing a single drive or all mounted Btrfs filesystems, this tool helps keep your system optimized.

## 🚀 Features

- **Dynamic Balancing:** Automatically decrements disk usage thresholds during balancing operations. 🔄
- **Real-Time Monitoring:** Continuously displays current Btrfs filesystem status and balance progress. 📊
- **Multi-Drive Support:** Balances a specific drive if provided, or processes all mounted Btrfs volumes if no drive is specified. 💻
- **Flexible Parameters:** Easily adjust initial thresholds and decrement steps to suit your system's needs. 🔧

## 🛠 Requirements

- **Python 3.x** 🐍
- **Btrfs Filesystem** 🗄️
- **Linux Operating System** 🐧

## 📥 Installation

You can install **Btrfs Auto Balancer** using [Kevin's Package Manager](https://github.com/kevinveenbirkenbach/package-manager) with the alias **btrfsauba**:

```bash
pkgman install btrfsauba
```

Alternatively, clone the repository directly:

```bash
git clone https://github.com/kevinveenbirkenbach/auto-btrfs-balancer.git
cd auto-btrfs-balancer
```

## 🚀 Usage

### Balancing a Specific Btrfs Drive

```bash
sudo btrfsauba <countdown> <count_down_step> --drive_path <drive_path>
```

### Balancing All Mounted Btrfs Drives

```bash
sudo btrfsauba <countdown> <count_down_step>
```

Replace `<countdown>` with the initial usage threshold (for both data and metadata), `<count_down_step>` with the decrement step for each balance iteration, and optionally `<drive_path>` with the specific mount point you wish to balance.

## 📜 License

This project is licensed under the GNU Affero General Public License v3.0. See the [LICENSE](./LICENSE) file for details.

## 👨‍💻 Author

Developed by **Kevin Veen-Birkenbach**  
- Email: [kevin@veen.world](mailto:kevin@veen.world)  
- Website: [https://www.veen.world/](https://www.veen.world/)

---

Happy balancing! ⚖️💡
