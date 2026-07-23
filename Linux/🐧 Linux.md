# 🐧 Linux — Complete Reference

> Everything you need to know about Linux — from concepts to commands to security.

---

# Table of Contents

- [[#What is Linux?]]
- [[#Linux Architecture]]
- [[#File System]]
- [[#Basic Commands]]
- [[#File Permissions]]
- [[#Users & Groups]]
- [[#Process Management]]
- [[#Package Management]]
- [[#Networking]]
- [[#Disk Management]]
- [[#Shell Scripting]]
- [[#Systemd & Services]]
- [[#Logs & Monitoring]]
- [[#SSH]]
- [[#Cron Jobs]]
- [[#Environment Variables]]
- [[#File Descriptors & Redirection]]
- [[#Compression & Archiving]]
- [[#Text Processing]]
- [[#Useful Commands]]
- [[#Troubleshooting]]
- [[#Security Hardening]]
- [[#Interview Questions]]
- [[#Practice Labs]]

---

# What is Linux?

Linux is an open-source, Unix-like operating system kernel first created by **Linus Torvalds** in 1991. The full OS (kernel + tools) is technically called **GNU/Linux**.

**Key traits:**

- Multiuser & multitasking
- Everything is a file (even devices)
- Case-sensitive file system
- Free & open source (GPL license)

**Used in:**

- Servers (90%+ of web servers run Linux)
- Cloud (AWS, GCP, Azure all run on Linux)
- DevOps & CI/CD pipelines
- Cybersecurity & penetration testing
- Android (Linux kernel underneath)
- Supercomputers (100% of Top500 run Linux)
- Embedded systems & IoT

**Popular distributions:**

|Distro|Based On|Use Case|
|---|---|---|
|Ubuntu|Debian|General purpose, beginner-friendly|
|Debian|—|Stable servers|
|CentOS Stream|RHEL|Enterprise-like, free|
|RHEL|—|Enterprise production|
|Arch Linux|—|Advanced users, rolling release|
|Kali Linux|Debian|Penetration testing|
|Alpine Linux|—|Containers, minimal footprint|
|Fedora|—|Cutting-edge, developer-focused|

---

# Linux Architecture

```text
┌─────────────────────────────┐
│          User Space          │
│  (Applications, Shell, GUI) │
├─────────────────────────────┤
│         System Calls         │
├─────────────────────────────┤
│           Kernel             │
│  (Process, Memory, FS, Net) │
├─────────────────────────────┤
│          Hardware            │
│  (CPU, RAM, Disk, Network)  │
└─────────────────────────────┘
```

## Components

|Component|Purpose|
|---|---|
|Kernel|Core of OS — manages hardware, memory, processes|
|Shell|Command interpreter (bash, zsh, sh, fish)|
|File System|Organizes and stores files (ext4, xfs, btrfs)|
|Processes|Running instances of programs|
|Daemons|Background services (e.g., sshd, nginx)|
|Device Drivers|Interface between kernel and hardware|

## Types of Shells

|Shell|Notes|
|---|---|
|bash|Default on most distros|
|zsh|Extended features, popular with Oh My Zsh|
|sh|POSIX-compliant, minimal|
|fish|User-friendly, auto-suggestions|

---

# File System

## Linux File System Hierarchy (FHS)

```
/
├── bin/        → Essential user binaries (ls, cp, mv)
├── sbin/       → System binaries (reboot, fdisk)
├── etc/        → Configuration files
├── home/       → User home directories
├── root/       → Root user's home
├── var/        → Variable data (logs, mail, spool)
├── tmp/        → Temporary files (cleared on reboot)
├── usr/        → User programs and libraries
│   ├── bin/
│   ├── lib/
│   └── local/
├── lib/        → Shared libraries
├── proc/       → Virtual FS for process info
├── sys/        → Virtual FS for kernel/hardware info
├── dev/        → Device files
├── mnt/        → Temporary mount points
├── media/      → Removable media (USB, CD)
├── opt/        → Optional/third-party software
└── boot/       → Bootloader files (GRUB, kernel)
```

## Important Directories

|Directory|Purpose|
|---|---|
|`/`|Root of the entire file system|
|`/home`|Regular user files|
|`/etc`|System-wide configurations|
|`/var/log`|Log files|
|`/tmp`|Temporary files|
|`/bin`, `/usr/bin`|User commands|
|`/sbin`, `/usr/sbin`|Admin commands|
|`/root`|Root user home|
|`/proc`|Running process info (virtual)|
|`/dev`|Hardware devices as files|

## File System Types

|FS Type|Notes|
|---|---|
|ext4|Default on Ubuntu/Debian|
|xfs|Default on RHEL/CentOS|
|btrfs|Snapshots, checksums|
|tmpfs|RAM-based, temporary|
|NFS|Network File System|

---

# Basic Commands

## Navigation

|Command|Purpose|
|---|---|
|`pwd`|Print current directory|
|`ls`|List files|
|`ls -la`|Long listing with hidden files|
|`ls -lh`|Human-readable sizes|
|`cd /path`|Change directory|
|`cd ~`|Go to home directory|
|`cd -`|Go to previous directory|

## File Operations

|Command|Purpose|
|---|---|
|`touch file.txt`|Create empty file|
|`mkdir dir`|Create directory|
|`mkdir -p a/b/c`|Create nested directories|
|`cp src dst`|Copy file|
|`cp -r src/ dst/`|Copy directory recursively|
|`mv src dst`|Move or rename|
|`rm file`|Remove file|
|`rm -rf dir/`|Remove directory (⚠️ use carefully)|
|`ln -s target link`|Create symbolic link|

## Viewing Files

|Command|Purpose|
|---|---|
|`cat file`|Print file content|
|`less file`|Page through content|
|`head -n 20 file`|First 20 lines|
|`tail -n 20 file`|Last 20 lines|
|`tail -f file`|Follow file in real-time|
|`wc -l file`|Count lines|

## Examples

```bash
# List all files including hidden
ls -la

# Create nested directories
mkdir -p projects/linux/scripts

# Follow a log file live
tail -f /var/log/syslog

# Copy entire directory
cp -r /etc/nginx /tmp/nginx-backup
```

---

# File Permissions

## Permission Structure

```
-rwxr-xr-x  1  user  group  4096  Jan 1  file.sh
│└──┴──┴──┘     │     │
│ u   g   o     │     └── Group owner
│               └──────── User owner
└─────────────────────── File type (- file, d dir, l link)

u = user (owner)
g = group
o = others
```

## Permission Types

|Symbol|Meaning|Numeric|
|---|---|---|
|`r`|read|4|
|`w`|write|2|
|`x`|execute|1|
|`-`|no permission|0|

## chmod — Numeric Mode

|Value|Permissions|
|---|---|
|777|rwxrwxrwx — everyone full access|
|755|rwxr-xr-x — owner full, others read+execute|
|644|rw-r--r-- — owner read/write, others read|
|600|rw------- — owner only read/write|
|400|r-------- — owner read only|

```bash
chmod 755 script.sh       # Set permissions numerically
chmod +x script.sh        # Add execute bit
chmod u+w,g-r file.txt   # Symbolic mode
chmod -R 755 /var/www/   # Recursive
```

## chown — Change Ownership

```bash
chown user file.txt           # Change owner
chown user:group file.txt     # Change owner + group
chown -R user:group /var/www  # Recursive
```

## Special Permissions

|Permission|Meaning|
|---|---|
|SUID (4xxx)|Run as file owner|
|SGID (2xxx)|Run as group owner|
|Sticky bit (1xxx)|Only owner can delete (used in /tmp)|

```bash
chmod 4755 /usr/bin/program   # Set SUID
chmod +t /tmp                 # Set sticky bit
```

---

# Users & Groups

## User Management

|Command|Purpose|
|---|---|
|`useradd username`|Create user|
|`useradd -m -s /bin/bash user`|Create user with home + shell|
|`passwd username`|Set password|
|`usermod -aG group user`|Add user to group|
|`userdel -r username`|Delete user + home dir|
|`id username`|Show user/group IDs|
|`whoami`|Current user|
|`su - username`|Switch user|
|`sudo command`|Run as root|

## Group Management

```bash
groupadd devops          # Create group
groupdel devops          # Delete group
usermod -aG devops loki  # Add loki to devops group
groups loki              # List groups for user
```

## Important Files

|File|Purpose|
|---|---|
|`/etc/passwd`|User accounts|
|`/etc/shadow`|Encrypted passwords|
|`/etc/group`|Group definitions|
|`/etc/sudoers`|Sudo permissions|

```bash
# View user entries
cat /etc/passwd | grep loki

# Edit sudoers safely
visudo
```

## sudoers Examples

```bash
# Give full sudo access
loki ALL=(ALL:ALL) ALL

# Allow specific command without password
loki ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
```

---

# Process Management

## Process States

```
Running → Sleeping → Stopped → Zombie
```

## Process Commands

|Command|Purpose|
|---|---|
|`ps aux`|All running processes|
|`ps -ef`|Full format listing|
|`top`|Live process monitor|
|`htop`|Interactive process monitor|
|`pgrep nginx`|Find PID by name|
|`kill PID`|Send signal to process|
|`kill -9 PID`|Force kill|
|`pkill nginx`|Kill by process name|
|`killall nginx`|Kill all instances|
|`nice -n 10 cmd`|Start with priority|
|`renice -n 5 PID`|Change priority|

## Background & Foreground

```bash
command &           # Run in background
jobs                # List background jobs
fg %1               # Bring job 1 to foreground
bg %1               # Send job 1 to background
nohup command &     # Run immune to hangup
disown %1           # Remove job from shell
```

## Process Signals

|Signal|Number|Meaning|
|---|---|---|
|SIGTERM|15|Graceful terminate (default)|
|SIGKILL|9|Force kill (can't be caught)|
|SIGHUP|1|Reload config|
|SIGSTOP|19|Pause process|
|SIGCONT|18|Resume process|

## Examples

```bash
ps aux | grep nginx          # Find nginx processes
kill -9 $(pgrep nginx)       # Kill all nginx by PID
top -u loki                  # Show processes for user loki
```

---

# Package Management

## Ubuntu / Debian (APT)

```bash
apt update                     # Refresh package lists
apt upgrade                    # Upgrade all packages
apt install nginx              # Install package
apt remove nginx               # Remove package
apt purge nginx                # Remove + config files
apt autoremove                 # Remove unused packages
apt search nginx               # Search packages
apt show nginx                 # Package details
dpkg -l                        # List installed packages
dpkg -i package.deb            # Install .deb file
```

## RHEL / CentOS (YUM / DNF)

```bash
dnf update                     # Update all packages
dnf install nginx              # Install
dnf remove nginx               # Remove
dnf search nginx               # Search
dnf info nginx                 # Package info
rpm -qa                        # List installed packages
rpm -ivh package.rpm           # Install .rpm file
```

## Snap & Flatpak (Universal)

```bash
snap install code              # Install VS Code via snap
flatpak install flathub app    # Flatpak install
```

---

# Networking

## IP & Interface

```bash
ip a                          # Show all interfaces & IPs
ip link show                  # Show link state
ip route                      # Show routing table
ip addr add 192.168.1.10/24 dev eth0  # Assign IP
hostname -I                   # Quick IP display
```

## Connectivity Testing

```bash
ping google.com               # ICMP ping
ping -c 4 8.8.8.8            # Ping 4 times
traceroute google.com         # Trace route
mtr google.com                # Live traceroute
curl ifconfig.me              # Get public IP
curl -I https://example.com   # HTTP headers only
wget https://example.com/file # Download file
```

## Ports & Sockets

```bash
ss -tulnp                    # Open ports + processes
netstat -tulnp               # Same (older tool)
nmap -sV 192.168.1.1        # Port scan target
lsof -i :80                  # What's using port 80
```

## DNS

```bash
nslookup google.com          # DNS lookup
dig google.com               # Detailed DNS info
dig google.com MX            # MX records
cat /etc/resolv.conf         # DNS server config
cat /etc/hosts               # Local hostname overrides
```

## Firewall (UFW & firewalld)

```bash
# UFW (Ubuntu)
ufw status
ufw enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw deny 23
ufw delete allow 80

# firewalld (RHEL/CentOS)
firewall-cmd --state
firewall-cmd --add-port=80/tcp --permanent
firewall-cmd --reload
```

## Network Config Files

|File|Purpose|
|---|---|
|`/etc/hosts`|Static hostname resolution|
|`/etc/resolv.conf`|DNS servers|
|`/etc/network/interfaces`|Interface config (Debian)|
|`/etc/netplan/`|Network config (Ubuntu 18+)|

---

# Disk Management

## Viewing Disk Info

```bash
df -h                    # Disk usage (human-readable)
df -hT                   # Include filesystem type
du -sh /var/log          # Size of a directory
du -sh /* | sort -rh    # Largest dirs from root
lsblk                    # List block devices
fdisk -l                 # Partition table info
blkid                    # UUID and FS type of devices
```

## Partitioning

```bash
fdisk /dev/sdb           # Partition disk (MBR)
gdisk /dev/sdb           # Partition disk (GPT)
parted /dev/sdb          # Partition tool
```

## Formatting & Mounting

```bash
mkfs.ext4 /dev/sdb1      # Format as ext4
mkfs.xfs /dev/sdb1       # Format as xfs

mount /dev/sdb1 /mnt/data         # Mount filesystem
umount /mnt/data                  # Unmount
mount -a                          # Mount all in /etc/fstab
```

## Persistent Mount (/etc/fstab)

```
# Device           Mount Point   FS     Options    Dump  Pass
UUID=abc123...     /mnt/data     ext4   defaults   0     2
```

## LVM (Logical Volume Manager)

```bash
# Create physical volume
pvcreate /dev/sdb

# Create volume group
vgcreate vg_data /dev/sdb

# Create logical volume
lvcreate -L 20G -n lv_data vg_data

# Format and mount
mkfs.ext4 /dev/vg_data/lv_data
mount /dev/vg_data/lv_data /mnt/data

# Extend volume
lvextend -L +10G /dev/vg_data/lv_data
resize2fs /dev/vg_data/lv_data
```

## Swap

```bash
swapon --show           # Show swap
free -h                 # Memory + swap
swapoff -a              # Disable all swap
swapon -a               # Enable all swap

# Create swap file
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
```

---

# Shell Scripting

## Script Basics

```bash
#!/bin/bash
# This is a comment

echo "Hello, Linux!"
```

## Variables

```bash
NAME="loki"
echo "Hello, $NAME"
echo "Home: $HOME"
echo "Script: $0"
echo "Args: $1 $2"
echo "All args: $@"
echo "Arg count: $#"
echo "Last exit code: $?"
echo "PID: $$"
```

## Conditionals

```bash
# if/elif/else
if [ "$1" == "hello" ]; then
  echo "Hello back!"
elif [ "$1" == "bye" ]; then
  echo "Goodbye!"
else
  echo "Unknown input"
fi

# File checks
[ -f file.txt ] && echo "File exists"
[ -d /etc ]     && echo "Directory exists"
[ -r file ]     && echo "Readable"
[ -z "$VAR" ]   && echo "Variable is empty"
[ -n "$VAR" ]   && echo "Variable is not empty"
```

## Loops

```bash
# for loop
for i in 1 2 3 4 5; do
  echo "Number: $i"
done

# for loop with range
for i in {1..10}; do
  echo "$i"
done

# while loop
count=1
while [ $count -le 5 ]; do
  echo "Count: $count"
  ((count++))
done

# Loop over files
for file in /etc/*.conf; do
  echo "$file"
done
```

## Functions

```bash
greet() {
  local name=$1
  echo "Hello, $name!"
}

greet "loki"
greet "world"
```

## Input / Exit Codes

```bash
read -p "Enter your name: " name
echo "Hello, $name"

exit 0   # Success
exit 1   # General error
```

## Example: Backup Script

```bash
#!/bin/bash

SRC="/home/loki"
DEST="/backup"
DATE=$(date +%Y-%m-%d)
FILENAME="backup-$DATE.tar.gz"

mkdir -p "$DEST"
tar -czf "$DEST/$FILENAME" "$SRC"

if [ $? -eq 0 ]; then
  echo "Backup successful: $DEST/$FILENAME"
else
  echo "Backup failed!"
  exit 1
fi
```

---

# Systemd & Services

## Service Management

```bash
systemctl start nginx          # Start service
systemctl stop nginx           # Stop service
systemctl restart nginx        # Restart service
systemctl reload nginx         # Reload config (no downtime)
systemctl status nginx         # Check status
systemctl enable nginx         # Start on boot
systemctl disable nginx        # Don't start on boot
systemctl is-active nginx      # Check if active
systemctl list-units --type=service  # All services
```

## Creating a Custom Service

```ini
# /etc/systemd/system/myapp.service

[Unit]
Description=My Custom App
After=network.target

[Service]
User=loki
WorkingDirectory=/home/loki/myapp
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload       # Reload systemd config
systemctl enable myapp
systemctl start myapp
```

## Targets (Runlevels)

|Target|Old Runlevel|Meaning|
|---|---|---|
|poweroff.target|0|Shutdown|
|rescue.target|1|Single user|
|multi-user.target|3|Multi-user CLI|
|graphical.target|5|GUI|
|reboot.target|6|Reboot|

---

# Logs & Monitoring

## Log Files

|File|Purpose|
|---|---|
|`/var/log/syslog`|General system messages|
|`/var/log/auth.log`|Authentication attempts|
|`/var/log/kern.log`|Kernel messages|
|`/var/log/dpkg.log`|Package installs (Debian)|
|`/var/log/nginx/access.log`|Nginx access|
|`/var/log/nginx/error.log`|Nginx errors|
|`/var/log/mysql/error.log`|MySQL errors|

## Viewing Logs

```bash
tail -f /var/log/syslog          # Follow in real-time
tail -n 100 /var/log/auth.log    # Last 100 lines
grep "Failed" /var/log/auth.log  # Filter errors
```

## journalctl (systemd logs)

```bash
journalctl                         # All logs
journalctl -u nginx                # Logs for nginx
journalctl -u nginx --since today  # Today only
journalctl -f                      # Follow live
journalctl -xe                     # Recent errors
journalctl --since "2024-01-01" --until "2024-01-02"
journalctl -p err                  # Error level only
```

## System Monitoring

```bash
top                     # Live processes
htop                    # Interactive (better top)
free -h                 # RAM usage
vmstat 1 5              # CPU/memory stats every 1s (5 times)
iostat -x 1             # Disk I/O stats
uptime                  # Load average
sar -u 1 5              # CPU usage history
dmesg | tail            # Kernel ring buffer
watch -n 2 df -h        # Auto-refresh disk usage
```

## Load Average (from uptime/top)

```
load average: 0.5, 1.2, 0.8
                │    │    └── 15 min avg
                │    └─────── 5 min avg
                └──────────── 1 min avg

Rule of thumb: value > number of CPUs = overloaded
```

---

# SSH

## Basic SSH

```bash
ssh user@ip                      # Connect
ssh user@ip -p 2222              # Custom port
ssh -i ~/.ssh/key.pem user@ip   # With private key
ssh -v user@ip                   # Verbose (debugging)
```

## SSH Key Setup

```bash
# Generate key pair
ssh-keygen -t rsa -b 4096 -C "your@email.com"

# Copy public key to server
ssh-copy-id user@ip

# Or manually
cat ~/.ssh/id_rsa.pub | ssh user@ip "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

## SCP — Secure Copy

```bash
scp file.txt user@ip:/home/user/          # Upload file
scp user@ip:/home/user/file.txt ./        # Download file
scp -r ./dir user@ip:/home/user/          # Upload directory
scp -P 2222 file.txt user@ip:/tmp/        # Custom port
```

## SSH Config File (~/.ssh/config)

```
Host myserver
    HostName 192.168.1.10
    User loki
    Port 22
    IdentityFile ~/.ssh/id_rsa

Host prod
    HostName prod.example.com
    User deploy
    Port 2222
```

```bash
ssh myserver    # Now use the alias
```

## SSH Tunneling

```bash
# Local port forwarding (access remote service locally)
ssh -L 8080:localhost:80 user@ip

# Remote port forwarding (expose local to remote)
ssh -R 9090:localhost:3000 user@ip

# SOCKS proxy
ssh -D 1080 user@ip
```

## SSH Hardening (/etc/ssh/sshd_config)

```
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
Port 2222
AllowUsers loki deploy
MaxAuthTries 3
```

```bash
systemctl restart sshd
```

---

# Cron Jobs

## Cron Syntax

```
* * * * *  command
│ │ │ │ │
│ │ │ │ └── Day of week (0-7, 0=Sunday)
│ │ │ └──── Month (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)
```

## Examples

```bash
# Edit crontab
crontab -e

# View crontab
crontab -l

# Remove crontab
crontab -r
```

```
# Run every minute
* * * * * /path/to/script.sh

# Run daily at 2:30 AM
30 2 * * * /home/loki/backup.sh

# Run every Sunday at midnight
0 0 * * 0 /scripts/weekly-cleanup.sh

# Run every 15 minutes
*/15 * * * * /scripts/check.sh

# Run at 9 AM on weekdays only
0 9 * * 1-5 /scripts/report.sh

# Run on the 1st of every month
0 0 1 * * /scripts/monthly.sh
```

## System-wide Cron Directories

|Directory|Frequency|
|---|---|
|`/etc/cron.hourly/`|Every hour|
|`/etc/cron.daily/`|Every day|
|`/etc/cron.weekly/`|Every week|
|`/etc/cron.monthly/`|Every month|

## Logging Cron Output

```bash
# Redirect output to log
0 2 * * * /home/loki/backup.sh >> /var/log/backup.log 2>&1
```

---

# Environment Variables

```bash
printenv                     # Print all env vars
echo $PATH                   # Print PATH
echo $HOME                   # Home directory
echo $USER                   # Current user
echo $SHELL                  # Current shell

# Set variable (current session only)
export MY_VAR="hello"

# Persist across sessions
echo 'export MY_VAR="hello"' >> ~/.bashrc
source ~/.bashrc

# Remove variable
unset MY_VAR
```

## Common Env Variables

|Variable|Purpose|
|---|---|
|`$PATH`|Directories to search for commands|
|`$HOME`|Current user's home|
|`$USER`|Current username|
|`$SHELL`|Current shell path|
|`$HOSTNAME`|Machine hostname|
|`$LANG`|Locale/language|
|`$EDITOR`|Default text editor|

## Adding to PATH

```bash
export PATH="$PATH:/usr/local/myapp/bin"

# Persist
echo 'export PATH="$PATH:/usr/local/myapp/bin"' >> ~/.bashrc
```

---

# File Descriptors & Redirection

## Descriptors

|FD|Name|Default|
|---|---|---|
|0|stdin|Keyboard|
|1|stdout|Terminal|
|2|stderr|Terminal|

## Redirection

```bash
command > file.txt        # stdout to file (overwrite)
command >> file.txt       # stdout to file (append)
command 2> errors.txt     # stderr to file
command 2>&1              # Merge stderr into stdout
command &> all.txt        # Both stdout+stderr to file
command < file.txt        # Read stdin from file
command1 | command2       # Pipe stdout to next command
```

## Examples

```bash
ls /nonexistent 2> /dev/null        # Suppress errors
ls /etc > list.txt 2>&1             # Capture everything
cat < /etc/hosts                    # Read from file
echo "hello" | tee output.txt       # Print + save
```

---

# Compression & Archiving

## tar

```bash
# Create archive
tar -czf archive.tar.gz /path/to/dir    # gzip compressed
tar -cjf archive.tar.bz2 /path/to/dir  # bzip2 compressed
tar -cf archive.tar /path/to/dir       # No compression

# Extract
tar -xzf archive.tar.gz                 # Extract gzip
tar -xjf archive.tar.bz2               # Extract bzip2
tar -xf archive.tar -C /destination/   # Extract to dir

# View contents
tar -tzf archive.tar.gz
```

## zip / gzip

```bash
zip -r archive.zip /path/to/dir    # Zip directory
unzip archive.zip                  # Unzip
gzip file.txt                      # Compress (replaces file)
gunzip file.txt.gz                 # Decompress
```

---

# Text Processing

## grep

```bash
grep "error" file.txt             # Search in file
grep -i "error" file.txt          # Case-insensitive
grep -r "error" /var/log/         # Recursive search
grep -n "error" file.txt          # Show line numbers
grep -v "info" file.txt           # Exclude matches
grep -c "error" file.txt          # Count matches
grep -E "error|fail" file.txt     # Extended regex
```

## awk

```bash
awk '{print $1}' file.txt          # Print first column
awk -F: '{print $1}' /etc/passwd   # Field separator :
awk 'NR==5' file.txt               # Print line 5
awk '{sum += $1} END {print sum}' file.txt  # Sum column
```

## sed

```bash
sed 's/old/new/' file.txt          # Replace first match
sed 's/old/new/g' file.txt         # Replace all matches
sed -i 's/old/new/g' file.txt      # In-place edit
sed -n '5,10p' file.txt            # Print lines 5–10
sed '/pattern/d' file.txt          # Delete matching lines
```

## sort, uniq, cut

```bash
sort file.txt                      # Sort alphabetically
sort -n file.txt                   # Numeric sort
sort -r file.txt                   # Reverse sort
sort file.txt | uniq               # Remove duplicates
sort file.txt | uniq -c            # Count duplicates
cut -d: -f1 /etc/passwd            # Cut field 1, delim :
```

---

# Useful Commands

## find

```bash
find / -name nginx.conf                    # Find by name
find /home -type f -name "*.log"           # Find log files
find /tmp -mtime +7                        # Files older than 7 days
find / -size +100M                         # Files larger than 100MB
find /etc -type f -perm 777               # World-writable files
find /home -user loki                     # Files owned by user
find / -name "*.conf" -exec grep "port" {} \;  # Search inside found files
```

## Other Handy Tools

```bash
which python3                 # Path of command
whereis nginx                 # Binary, source, man page
man ls                        # Manual for command
history                       # Command history
history | grep ssh            # Search history
!!                            # Repeat last command
!ssh                          # Repeat last ssh command
alias ll='ls -la'             # Create alias
xargs                         # Build commands from input
tee                           # Read stdin, write to stdout + file
tr 'a-z' 'A-Z'               # Translate characters
diff file1 file2              # Compare files
stat file.txt                 # Detailed file info
date                          # Current date/time
cal                           # Calendar
bc                            # Calculator
```

---

# Troubleshooting

## High CPU Usage

```bash
top                              # Live view
htop                             # Interactive
ps aux --sort=-%cpu | head       # Top CPU processes
uptime                           # Load average
```

## High Memory Usage

```bash
free -h                          # RAM overview
ps aux --sort=-%mem | head       # Top memory processes
cat /proc/meminfo                # Detailed memory info
```

## Disk Full

```bash
df -h                            # Disk usage
du -sh /* 2>/dev/null | sort -rh # Find largest dirs
find / -size +100M -type f       # Large files
journalctl --vacuum-size=500M    # Trim logs
```

## Service Not Starting

```bash
systemctl status nginx           # Check status
journalctl -u nginx -xe          # Detailed logs
nginx -t                         # Test config syntax
```

## Network Issues

```bash
ping 8.8.8.8                     # Check internet
ip a                             # Check IP config
ip route                         # Check default gateway
cat /etc/resolv.conf             # Check DNS
ss -tulnp                        # Check open ports
```

## Can't SSH

```bash
systemctl status sshd            # Is SSH running?
ss -tulnp | grep 22              # Is port 22 open?
cat /var/log/auth.log            # Auth failures
ufw status                       # Firewall rules
```

## Permission Denied

```bash
ls -la file                      # Check permissions
id                               # Your user/groups
stat file                        # Detailed info
sudo ls -la /root                # Use sudo if needed
```

---

# Security Hardening

## Essential Steps

1. **Keep system updated**

```bash
apt update && apt upgrade -y
unattended-upgrades             # Auto security patches
```

2. **Disable root SSH login**

```bash
# In /etc/ssh/sshd_config
PermitRootLogin no
PasswordAuthentication no
```

3. **Set up UFW firewall**

```bash
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

4. **Fail2Ban — block brute force**

```bash
apt install fail2ban
systemctl enable fail2ban
```

5. **Check for open ports**

```bash
ss -tulnp
```

6. **Monitor failed logins**

```bash
grep "Failed password" /var/log/auth.log
```

7. **Remove unnecessary packages**

```bash
apt autoremove
```

8. **File integrity monitoring (AIDE)**

```bash
apt install aide
aideinit
```

---

# Interview Questions

**Q: Difference between Linux and Unix?**

> Unix is proprietary (AIX, HP-UX, Solaris). Linux is open-source, inspired by Unix but written from scratch.

**Q: What is a process?**

> A running instance of a program. Has its own PID, memory space, file descriptors.

**Q: What is chmod 777?**

> Gives read, write, and execute to user, group, and others. Very insecure — avoid on production.

**Q: Difference between hard link and soft link?**

> Hard link: points to the same inode; survives original deletion. Soft link (symlink): points to filename/path; breaks if original is removed.

**Q: What is SSH?**

> Secure Shell — encrypted protocol for remote login and command execution. Runs on port 22.

**Q: What is the difference between process and thread?**

> A process has its own memory space. Threads share memory within a process. Threads are lighter.

**Q: What is a zombie process?**

> A process that has finished but its entry remains in the process table because the parent hasn't read its exit status.

**Q: What is /proc?**

> A virtual filesystem that exposes kernel and process info as files. e.g. `/proc/cpuinfo`, `/proc/meminfo`.

**Q: What happens when you type a command?**

> Shell reads input → looks in $PATH → finds binary → kernel fork() + exec() → new process runs.

**Q: Explain Linux boot process.**

> BIOS/UEFI → Bootloader (GRUB) → Kernel loads → initramfs → systemd (PID 1) → Targets → Login

**Q: What is the difference between `>` and `>>`?**

> `>` overwrites the file. `>>` appends to it.

**Q: What is an inode?**

> A data structure storing file metadata (permissions, owner, size, timestamps) but NOT the filename. Filenames are stored in directories.

**Q: What is LVM?**

> Logical Volume Manager — allows flexible disk management with volume groups and logical volumes. Supports resizing without downtime.

---

# Practice Labs

## Lab 1 — User & Group Management

```bash
# Create user and group, assign permissions
useradd -m -s /bin/bash devuser
groupadd devteam
usermod -aG devteam devuser
mkdir /shared
chown root:devteam /shared
chmod 770 /shared
```

## Lab 2 — Install & Manage Nginx

```bash
apt update
apt install nginx
systemctl enable nginx
systemctl start nginx
systemctl status nginx
curl localhost
```

## Lab 3 — Backup Shell Script

```bash
#!/bin/bash
DATE=$(date +%Y-%m-%d)
SRC="/home/loki"
DEST="/backup"
mkdir -p "$DEST"
tar -czf "$DEST/backup-$DATE.tar.gz" "$SRC"
echo "Done: $DEST/backup-$DATE.tar.gz"
```

## Lab 4 — System Resource Monitor Script

```bash
#!/bin/bash

echo "===== System Resource Monitor ====="
echo "Date: $(date)"
echo ""

echo "--- CPU Load ---"
uptime

echo ""
echo "--- Memory Usage ---"
free -h

echo ""
echo "--- Disk Usage ---"
df -h | grep -v tmpfs

echo ""
echo "--- Top 5 CPU Processes ---"
ps aux --sort=-%cpu | head -6

echo ""
echo "--- Top 5 Memory Processes ---"
ps aux --sort=-%mem | head -6

echo ""
echo "--- Open Ports ---"
ss -tulnp
```

## Lab 5 — Firewall Setup

```bash
# Reset and configure UFW from scratch
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp      # SSH
ufw allow 80/tcp      # HTTP
ufw allow 443/tcp     # HTTPS
ufw enable
ufw status verbose
```

## Lab 6 — Cron + Log Rotation

```bash
# Add a cron job that runs backup every day at 2 AM
crontab -e
# Add this line:
# 0 2 * * * /home/loki/backup.sh >> /var/log/backup.log 2>&1

# Check cron is running
systemctl status cron

# View the log
tail -f /var/log/backup.log
```

---

_Tags: #linux #devops #sysadmin #reference_```bash
#!/bin/bash
echo "=== System Report: $(date) ==="
echo ""
echo "--- CPU Load ---"
uptime

echo ""
echo "--- Memory ---"
free -h

echo ""
echo "--- Disk Usage ---"
df -h

echo ""
echo "--- Top 5 Processes by CPU ---"
ps aux --sort=-%cpu | head -6
```

## Lab 5 — Cron Job Setup

```bash
crontab -e

# Add:
# Backup daily at 2 AM
0 2 * * * /home/loki/backup.sh >> /var/log/backup.log 2>&1

# Verify
crontab -l
```

## Lab 6 — SSH Key Setup

```bash
ssh-keygen -t rsa -b 4096
ssh-copy-id user@192.168.1.10
ssh user@192.168.1.10
```

## Lab 7 — Firewall Setup

```bash
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 'Nginx Full'
ufw enable
ufw status verbose
```

---

# Learning Roadmap

```
Phase 1 — Foundations
  ├── Linux Basics & Navigation
  ├── File System & Permissions
  ├── Users & Groups
  └── Process Management

Phase 2 — Intermediate
  ├── Networking
  ├── Shell Scripting
  ├── Services & Systemd
  ├── Logs & Monitoring
  └── SSH & Security

Phase 3 — DevOps & Cloud
  ├── Docker & Containers
  ├── Git & Version Control
  ├── CI/CD Pipelines
  ├── Nginx / Apache
  └── Ansible (Automation)

Phase 4 — Advanced
  ├── Kubernetes
  ├── Cloud (AWS/GCP/Azure)
  ├── Terraform
  ├── Observability (Prometheus, Grafana)
  └── Linux Internals (Kernel, eBPF)
```

---

_Last updated: 2025 | Happy Learning! 🐧_

---

# 🚑 Real-World Scenarios

> **The shift from beginner to engineer:** Beginners know commands. Engineers know `problem → investigation → diagnosis → fix`.

---

## Scenario 1 — Port 80 Already in Use

### Symptoms

```
nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)
Job for nginx.service failed.
```

### Investigation

```bash
# Who is using port 80?
ss -tulnp | grep :80
lsof -i :80

# Sample output:
# LISTEN  0  128  0.0.0.0:80   users:(("apache2",pid=1234,...))
```

### Diagnosis

Apache2 is already bound to port 80. Two services can't share the same port.

### Fix

```bash
# Option A: Kill the conflicting service
systemctl stop apache2
systemctl disable apache2

# Option B: Kill by PID (last resort)
kill -9 1234

# Restart nginx
systemctl restart nginx
systemctl status nginx
```

---

## Scenario 2 — Disk Full, Server Won't Write Logs

### Symptoms

```
No space left on device
Application throwing write errors
Cron jobs silently failing
```

### Investigation

```bash
# Check overall disk usage
df -h

# Find the biggest directories
du -sh /* 2>/dev/null | sort -rh | head -20

# Find files larger than 500MB
find / -type f -size +500M 2>/dev/null

# Check if it's inodes (not space) that's full
df -i
```

### Diagnosis

```bash
# Common culprits:
# 1. Log files grown out of control
ls -lh /var/log/

# 2. Journal logs bloated
journalctl --disk-usage

# 3. Docker images/containers (if applicable)
docker system df
```

### Fix

```bash
# Trim journal logs
journalctl --vacuum-size=200M
journalctl --vacuum-time=7d

# Rotate and compress old logs
logrotate -f /etc/logrotate.conf

# Clear apt cache
apt clean

# Remove old Docker resources
docker system prune -f

# Tar and move old log files
tar -czf /backup/old-logs.tar.gz /var/log/old/
rm -rf /var/log/old/
```

---

## Scenario 3 — Service Crashes Immediately After Start

### Symptoms

```
systemctl start myapp
● myapp.service: Main process exited, code=exited, status=1
Active: failed
```

### Investigation

```bash
# Read the full error
systemctl status myapp -l

# Deep dive into logs
journalctl -u myapp -xe --no-pager

# Check if binary exists and is executable
ls -la /usr/bin/myapp
which myapp

# Check if it runs manually
/usr/bin/myapp --config /etc/myapp.conf
```

### Diagnosis (common causes)

```bash
# 1. Missing config file
ls /etc/myapp/

# 2. Wrong user in service file
cat /etc/systemd/system/myapp.service | grep User

# 3. Port already in use
ss -tulnp | grep <port>

# 4. Missing dependency
ldd /usr/bin/myapp | grep "not found"
```

### Fix

```bash
# Fix the config, then:
systemctl daemon-reload
systemctl start myapp
systemctl status myapp
```

---

## Scenario 4 — Cannot SSH Into Server

### Symptoms

```
ssh: connect to host 192.168.1.10 port 22: Connection refused
ssh: connect to host 192.168.1.10 port 22: Connection timed out
```

### Investigation

```bash
# From another machine or console:
# 1. Is the server reachable at all?
ping 192.168.1.10

# 2. Is sshd running?
systemctl status sshd

# 3. Is port 22 open?
ss -tulnp | grep :22

# 4. Is firewall blocking it?
ufw status
iptables -L -n | grep 22

# 5. Check auth logs
tail -50 /var/log/auth.log
```

### Diagnosis

```bash
# Common causes:
# - sshd crashed → restart it
# - Firewall rule blocking port 22 → open it
# - Wrong port in sshd_config
grep ^Port /etc/ssh/sshd_config

# - Server under brute force, fail2ban blocked your IP
fail2ban-client status sshd
```

### Fix

```bash
# Restart sshd
systemctl restart sshd

# Unban your own IP from fail2ban
fail2ban-client set sshd unbanip YOUR_IP

# Open port in UFW
ufw allow 22/tcp
ufw reload
```

---

## Scenario 5 — High CPU, Server Slow

### Symptoms

```
Server responding slowly
Load average: 15.2, 14.8, 13.1  (on 4-core server = overloaded)
```

### Investigation

```bash
# 1. Check load average (> num CPUs = overloaded)
uptime
nproc              # how many CPU cores?

# 2. Find the guilty process
top                # press P to sort by CPU
htop               # more visual
ps aux --sort=-%cpu | head -10

# 3. Check what the process is actually doing
strace -p PID      # syscalls being made
lsof -p PID        # files/ports it has open
```

### Diagnosis

```bash
# Is it a runaway process?
ps aux | grep defunct    # zombie processes

# Is it a fork bomb?
ps aux | wc -l           # how many processes total?

# Is it I/O wait? (wa% in top)
iostat -x 1 5
```

### Fix

```bash
# Kill runaway process gracefully first
kill -15 PID

# Force kill if needed
kill -9 PID

# If it keeps respawning, check cron and systemd
crontab -l
systemctl list-units --state=running
```

---

## Scenario 6 — Permission Denied Error

### Symptoms

```
bash: ./script.sh: Permission denied
open("/var/data/file", O_RDWR) = -1 EACCES
```

### Investigation

```bash
# Check permissions on the file
ls -la script.sh

# Check your current user and groups
id
whoami

# Check parent directory permissions too
ls -la /path/to/

# Check if there's a mount option blocking execute
mount | grep noexec
```

### Diagnosis & Fix

```bash
# Missing execute bit
chmod +x script.sh

# Wrong ownership
chown loki:loki script.sh

# Wrong directory permissions
chmod 755 /path/to/dir/

# Filesystem mounted with noexec
# remount without noexec (check /etc/fstab)
mount -o remount,exec /mountpoint
```

---

## Scenario 7 — OOM Killer Killed Your App

### Symptoms

```
App suddenly died with no error
No crash log
Systemd shows: Main process exited
```

### Investigation

```bash
# Check kernel OOM logs
dmesg | grep -i "out of memory"
dmesg | grep -i "oom"

# Check journal around the time it died
journalctl -u myapp --since "1 hour ago"

# Check current memory
free -h
cat /proc/meminfo
```

### Diagnosis

The Linux kernel killed your process because RAM was exhausted. OOM Killer picks the "least important" process — often your app.

### Fix

```bash
# Short term: free memory
sync && echo 3 > /proc/sys/vm/drop_caches

# Check what's eating RAM
ps aux --sort=-%mem | head -10

# Long term options:
# 1. Add more RAM
# 2. Add swap space
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# 3. Set OOM score for your app (lower = less likely to be killed)
echo -500 > /proc/PID/oom_score_adj

# 4. Tune app memory limits via systemd
# In service file:
# MemoryLimit=512M
```

---

## 🔎 Universal Debugging Workflow

When something breaks, follow this order — don't panic, don't guess:

```
1. READ the error message carefully
      ↓
2. CHECK logs (journalctl, /var/log/)
      ↓
3. CHECK process state (systemctl status, ps)
      ↓
4. CHECK ports & network (ss, ping, curl)
      ↓
5. CHECK permissions (ls -la, id)
      ↓
6. CHECK disk & memory (df -h, free -h)
      ↓
7. REPRODUCE the issue manually
      ↓
8. FIX root cause (not just symptoms)
      ↓
9. VERIFY fix + monitor
```

---

# 🥾 Linux Boot Process

Understanding boot = understanding how everything starts.

```
Power On
    ↓
BIOS / UEFI
    ↓
Bootloader (GRUB)
    ↓
Kernel
    ↓
initramfs
    ↓
systemd (PID 1)
    ↓
Targets (runlevels)
    ↓
Services start
    ↓
Login prompt
```

---

## Stage 1 — BIOS / UEFI

- **BIOS** (legacy) or **UEFI** (modern) — firmware stored in ROM on motherboard
- Runs POST (Power-On Self Test) — checks hardware
- Looks for bootable device (disk, USB, network)
- Loads the bootloader from MBR (BIOS) or EFI partition (UEFI)

|BIOS|UEFI|
|---|---|
|Legacy, 16-bit|Modern, 32/64-bit|
|MBR partition table|GPT partition table|
|Max 2TB disk|Max 9.4 ZB disk|
|No Secure Boot|Supports Secure Boot|

---

## Stage 2 — GRUB (Bootloader)

- **GRUB2** = Grand Unified Bootloader (most Linux distros)
- Lives in `/boot/grub/`
- Shows boot menu (choose kernel or OS)
- Loads the kernel + initramfs into memory

```bash
# GRUB config
cat /boot/grub/grub.cfg
ls /boot/                         # see kernels available

# Update GRUB after config change
update-grub                       # Debian/Ubuntu
grub2-mkconfig -o /boot/grub2/grub.cfg   # RHEL/CentOS
```

---

## Stage 3 — Kernel

- Kernel image (`vmlinuz`) decompresses itself into RAM
- Initializes CPU, memory, hardware drivers
- Mounts root filesystem (read-only initially)
- Starts the first process: **initramfs → then systemd**

```bash
uname -r              # Current kernel version
ls /boot/vmlinuz*     # Available kernels
cat /proc/version     # Kernel info
dmesg | head -50      # Kernel boot messages
```

---

## Stage 4 — initramfs

- **Initial RAM Filesystem** — temporary root filesystem loaded into RAM
- Contains just enough drivers and tools to mount the real root filesystem
- Once real `/` is mounted, initramfs is discarded
- Handles: LUKS encryption, LVM, RAID during boot

```bash
# View initramfs contents
lsinitramfs /boot/initrd.img-$(uname -r)
```

---

## Stage 5 — systemd (PID 1)

- **systemd** is the first real process (PID 1)
- Replaces the old `init` (SysV init)
- Reads unit files, resolves dependencies
- Starts services in parallel for fast boot

```bash
ps -p 1                     # Confirm PID 1 is systemd
systemd-analyze             # Total boot time
systemd-analyze blame       # Which service was slowest?
systemd-analyze critical-chain   # Boot dependency chain
```

---

## Stage 6 — Targets (Runlevels)

|Target|Old Runlevel|When|
|---|---|---|
|`sysinit.target`|—|Hardware init|
|`basic.target`|—|Basic system|
|`multi-user.target`|3|Normal CLI boot|
|`graphical.target`|5|GUI boot|
|`rescue.target`|1|Emergency mode|

```bash
# Current default target
systemctl get-default

# Change default
systemctl set-default multi-user.target

# Boot into rescue mode now
systemctl isolate rescue.target
```

---

# ⚙️ Linux Kernel Concepts

> These are what power Docker, Kubernetes, and performance tuning. Understand them — don't just memorize them.

---

## System Calls (syscalls)

- The **only** way user programs talk to the kernel
- User space can't directly access hardware — it asks the kernel via syscalls
- Examples: `read()`, `write()`, `fork()`, `exec()`, `open()`, `socket()`

```bash
# Trace syscalls a process makes
strace ls /etc

# Count syscalls by type
strace -c ls /etc

# Attach to running process
strace -p PID
```

```
User Program (e.g. nginx)
    ↓  [syscall: write()]
Kernel
    ↓
Hardware (disk, network card)
```

---

## Namespaces

- **Namespaces isolate resources** — what a process can see
- This is **how containers work** — each container gets its own namespaces

|Namespace|Isolates|
|---|---|
|`pid`|Process IDs|
|`net`|Network interfaces, routes|
|`mnt`|Filesystem mounts|
|`uts`|Hostname|
|`ipc`|Inter-process communication|
|`user`|User/group IDs|
|`cgroup`|cgroup root|

```bash
# View namespaces of a process
ls -la /proc/PID/ns/

# Create a new network namespace
ip netns add mynet
ip netns list
ip netns exec mynet bash    # run shell in that namespace
```

---

## cgroups (Control Groups)

- **cgroups limit and account for resource usage** per process group
- CPU, memory, disk I/O, network bandwidth can all be capped
- This is **how Docker enforces memory limits** (`docker run -m 512m`)

```bash
# View cgroup hierarchies
ls /sys/fs/cgroup/

# Check cgroup for a process
cat /proc/PID/cgroup

# systemd sets cgroups automatically
# Set memory limit in a service file:
# MemoryMax=512M
# CPUQuota=50%

# Check systemd slice usage
systemd-cgtop
```

---

## Linux Scheduler

- Decides which process runs on CPU at any moment
- Default: **CFS (Completely Fair Scheduler)**
- Uses `nice` values and priority to decide

```
nice range: -20 (highest priority) to +19 (lowest)
Default:     0
```

```bash
# Run with lower priority (be nice to others)
nice -n 10 ./backup.sh

# Change priority of running process
renice -n 5 -p PID

# View priorities in top/htop
# NI column = nice value, PR column = actual priority
```

---

## Memory Management

```
Virtual Memory
    ↓
Page Table (kernel maps virtual → physical)
    ↓
Physical RAM
    ↓ (if RAM full)
Swap Space (on disk)
```

```bash
# View memory map of a process
cat /proc/PID/maps
pmap -x PID

# Check page faults
/usr/bin/time -v ./program      # "Major page faults"

# Transparent huge pages (performance tuning)
cat /sys/kernel/mm/transparent_hugepage/enabled

# Check swap usage
swapon --show
vmstat -s | grep swap
```

---

# 🌐 Deep Networking

---

## TCP vs UDP

|Feature|TCP|UDP|
|---|---|---|
|Connection|Yes (3-way handshake)|No (connectionless)|
|Reliability|Guaranteed delivery|Best effort|
|Order|Ordered|Not ordered|
|Speed|Slower|Faster|
|Use cases|HTTP, SSH, FTP, databases|DNS, video streaming, gaming|

---

## TCP 3-Way Handshake

```
Client                Server
  │                     │
  │──── SYN ───────────►│   "I want to connect"
  │                     │
  │◄─── SYN-ACK ────────│   "Ok, I'm ready"
  │                     │
  │──── ACK ───────────►│   "Great, let's go"
  │                     │
  │══════ DATA ══════════│   Connection established
```

```bash
# Watch TCP connections live
watch -n 1 ss -tn

# See connection states
ss -tn state established
ss -tn state time-wait

# Capture TCP handshake
tcpdump -i eth0 host google.com -n
```

## TCP Connection States

|State|Meaning|
|---|---|
|LISTEN|Waiting for incoming connections|
|SYN_SENT|Client sent SYN|
|ESTABLISHED|Connection active|
|TIME_WAIT|Waiting after close (2 MSL)|
|CLOSE_WAIT|Remote closed, local hasn't yet|
|FIN_WAIT|Local closing|

---

## Common Port Numbers

|Port|Protocol|Service|
|---|---|---|
|22|TCP|SSH|
|25|TCP|SMTP|
|53|TCP/UDP|DNS|
|80|TCP|HTTP|
|443|TCP|HTTPS|
|3306|TCP|MySQL|
|5432|TCP|PostgreSQL|
|6379|TCP|Redis|
|8080|TCP|HTTP Alt|
|27017|TCP|MongoDB|

---

## DNS Resolution Flow

```
Browser: "what is the IP of google.com?"
    ↓
1. Check local cache (browser cache)
    ↓
2. Check /etc/hosts
    ↓
3. Check /etc/resolv.conf → ask DNS resolver (e.g. 8.8.8.8)
    ↓
4. Resolver checks its cache
    ↓
5. Ask Root DNS servers (.)
    ↓
6. Ask TLD servers (.com)
    ↓
7. Ask Authoritative nameserver (google.com)
    ↓
8. Returns: 142.250.67.46
    ↓
Browser connects to 142.250.67.46:443
```

```bash
# Full DNS trace
dig +trace google.com

# Check what resolver is being used
cat /etc/resolv.conf

# Test specific DNS server
dig @8.8.8.8 google.com

# Reverse lookup (IP → hostname)
dig -x 8.8.8.8
nslookup 8.8.8.8
```

---

## NAT (Network Address Translation)

```
Private Network: 192.168.1.0/24
    ↓
Router/NAT device (public IP: 203.0.113.5)
    ↓
Internet

# Your private IP (192.168.1.10) appears as 203.0.113.5 to the internet
```

- **SNAT** (Source NAT): change source IP (for outbound traffic)
- **DNAT** (Destination NAT): change destination IP (for port forwarding)
- **Masquerade**: SNAT where public IP is dynamic

```bash
# View NAT rules
iptables -t nat -L -n -v

# Add port forwarding (DNAT)
iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.10:8080
```

---

## Subnetting Basics

```
IP Address:  192.168.1.100
Subnet Mask: 255.255.255.0  = /24

Network:     192.168.1.0
Broadcast:   192.168.1.255
Usable hosts: 192.168.1.1 - 192.168.1.254 (254 hosts)
```

|CIDR|Subnet Mask|Hosts|
|---|---|---|
|/8|255.0.0.0|~16M|
|/16|255.255.0.0|~65K|
|/24|255.255.255.0|254|
|/28|255.255.255.240|14|
|/30|255.255.255.252|2|
|/32|255.255.255.255|1 (host only)|

```bash
# Show routing table
ip route show

# Add a static route
ip route add 10.0.0.0/8 via 192.168.1.1

# Check which route a packet will take
ip route get 8.8.8.8
```

---

## Packet Flow Through Kernel

```
Incoming packet
    ↓
Network card (NIC)
    ↓
Kernel network stack
    ↓
iptables/netfilter (PREROUTING)
    ↓
Routing decision
    ↓
iptables (INPUT / FORWARD)
    ↓
Socket buffer
    ↓
Application (nginx, sshd...)
```

---

# 🗄️ File System Internals

---

## What is an Inode?

Every file has **two parts**:

1. **Filename** → stored in the directory
2. **Inode** → stores everything else about the file

```
Directory entry:
  "nginx.conf" → inode 48291

Inode 48291:
  - File type: regular file
  - Permissions: 644
  - Owner UID: 0 (root)
  - Group GID: 0 (root)
  - Size: 4096 bytes
  - Timestamps: atime, mtime, ctime
  - Block pointers: [block 1, block 2, ...]
  (NOT the filename)
```

```bash
ls -li file.txt         # Show inode number
stat file.txt           # Full inode info
df -i                   # Inode usage per filesystem
```

---

## Hard Links vs Soft Links

```
Hard Link:
  file.txt ──────────────┐
                          ├──► Inode 48291 ──► data blocks
  hardlink.txt ──────────┘

Soft Link (Symlink):
  symlink.txt ──► "file.txt" ──► Inode 48291 ──► data blocks
```

||Hard Link|Soft Link|
|---|---|---|
|Points to|Inode|File path|
|Works after original deleted?|✅ Yes|❌ No (dangling link)|
|Cross filesystem?|❌ No|✅ Yes|
|Can link directories?|❌ No|✅ Yes|
|Shows with `ls -l`|`file.txt`|`link -> file.txt`|

```bash
# Create hard link
ln file.txt hardlink.txt

# Create soft link
ln -s /etc/nginx/nginx.conf nginx.conf

# Find dangling symlinks
find /etc -xtype l 2>/dev/null
```

---

## Journaling

- **Without journaling**: if power fails mid-write → filesystem corruption
- **With journaling**: changes are first written to a **journal (log)**, then to disk
- If power fails → replay journal on next boot → no corruption

|Filesystem|Journaling|
|---|---|
|ext4|✅ Yes|
|xfs|✅ Yes|
|btrfs|✅ (COW-based)|
|ext2|❌ No|
|fat32|❌ No|

---

## Mount Points

```
/           ← root filesystem (on /dev/sda1)
├── /boot   ← can be separate partition (/dev/sda2)
├── /home   ← can be separate disk (/dev/sdb1)
├── /tmp    ← can be tmpfs (RAM)
└── /mnt/nas ← network filesystem (NFS)
```

```bash
# View what's mounted
mount
cat /proc/mounts

# Mount types
mount -t ext4 /dev/sdb1 /mnt/data      # Physical disk
mount -t tmpfs tmpfs /tmp              # RAM-based
mount -t nfs 192.168.1.5:/share /mnt  # Network

# /etc/fstab — auto-mount on boot
UUID=abc123  /data  ext4  defaults,noatime  0  2
```

---

## ext4 Internals (Brief)

```
Disk
└── Superblock (filesystem metadata)
    └── Block Groups
        ├── Block Bitmap (which blocks are free)
        ├── Inode Bitmap (which inodes are free)
        ├── Inode Table (actual inodes)
        └── Data Blocks (file contents)
```

```bash
# View ext4 superblock info
tune2fs -l /dev/sda1

# Check and repair filesystem (unmounted)
fsck.ext4 /dev/sdb1

# View filesystem info
dumpe2fs /dev/sda1 | head -50
```

---

# 🔐 Security — Deep Dive

---

## Principle of Least Privilege

> Every user, process, and service should have **only the permissions it needs** — nothing more.

```bash
# BAD: Running nginx as root
User=root

# GOOD: Running nginx as dedicated user
User=nginx
Group=nginx

# Check what a service runs as
ps aux | grep nginx
```

---

## File Ownership Risks

```bash
# World-writable files = anyone can modify = huge risk
find / -perm -0002 -type f 2>/dev/null

# SUID programs run as their owner (often root) — audit these
find / -perm -4000 -type f 2>/dev/null

# Files with no owner (orphaned) — sign of deleted user
find / -nouser 2>/dev/null

# Config files should NOT be world-readable
chmod 640 /etc/myapp/config.yml
```

---

## sudo Misuse & Risks

```bash
# Dangerous: giving full sudo with NOPASSWD
loki ALL=(ALL) NOPASSWD: ALL    ← never do this

# Safe: allow only specific commands
loki ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx

# See who has sudo
cat /etc/sudoers
ls /etc/sudoers.d/

# Check sudo log
grep sudo /var/log/auth.log
journalctl | grep sudo
```

---

## SSH Brute Force Protection

```bash
# See failed SSH attempts
grep "Failed password" /var/log/auth.log | tail -20
grep "Invalid user" /var/log/auth.log | tail -20

# Count by IP (find who's attacking)
grep "Failed password" /var/log/auth.log | \
  awk '{print $(NF-3)}' | sort | uniq -c | sort -rn | head

# Install and configure fail2ban
apt install fail2ban

cat /etc/fail2ban/jail.local
# [sshd]
# enabled = true
# maxretry = 3
# bantime = 3600
# findtime = 600

systemctl restart fail2ban

# Check banned IPs
fail2ban-client status sshd
```

---

## SELinux Basics (RHEL/CentOS)

- **Security-Enhanced Linux** — mandatory access control on top of standard Unix permissions
- Even root can be restricted by SELinux policy

```bash
# Check SELinux mode
getenforce             # Enforcing / Permissive / Disabled
sestatus

# Modes:
# Enforcing  = actively blocking policy violations
# Permissive = logging only, not blocking
# Disabled   = off

# Temporarily switch to permissive (for debugging)
setenforce 0

# Check if SELinux is blocking something
ausearch -m avc -ts recent
grep "denied" /var/log/audit/audit.log

# See security context of files
ls -Z /var/www/html/

# Set correct context for nginx web files
chcon -Rt httpd_sys_content_t /var/www/html/
restorecon -Rv /var/www/html/

# Persistent config: /etc/selinux/config
SELINUX=enforcing
```

---

## AppArmor Basics (Ubuntu/Debian)

- Similar to SELinux but profile-based and simpler
- Restricts what files and capabilities a program can access

```bash
# Check AppArmor status
apparmor_status
aa-status

# Profiles location
ls /etc/apparmor.d/

# Modes: enforce / complain / disabled
aa-enforce /etc/apparmor.d/usr.sbin.nginx
aa-complain /etc/apparmor.d/usr.sbin.nginx    # log only

# Check AppArmor denials
dmesg | grep apparmor
grep "apparmor" /var/log/syslog
```

---

# 📦 How Package Management Actually Works

```
Developer writes code
    ↓
Packages code + metadata into .deb / .rpm
    ↓
Uploads to repository server
    ↓
Your package manager fetches package list
    ↓
You run: apt install nginx
    ↓
apt downloads nginx + all dependencies
    ↓
dpkg installs each .deb in correct order
    ↓
Binary lands in /usr/bin/
Config lands in /etc/
Service file in /etc/systemd/system/
```

---

## Repository System

```bash
# Where apt looks for packages
cat /etc/apt/sources.list
ls /etc/apt/sources.list.d/

# Format of a repo line:
# deb https://repo.example.com/ubuntu focal main restricted

# Add a new repository
add-apt-repository ppa:nginx/stable

# Import a GPG key (for repo authentication)
curl -fsSL https://nginx.org/keys/nginx_signing.key | apt-key add -

# Update package index from all repos
apt update
```

---

## Dependency Resolution

```bash
# See what a package depends on
apt depends nginx
dpkg -I nginx.deb                    # .deb package info

# See what depends on a package (reverse)
apt rdepends nginx

# Install package without recommended
apt install --no-install-recommends nginx

# Simulate install (don't actually install)
apt install --dry-run nginx

# Why is a package installed?
apt-mark showmanual | grep nginx     # manually installed
```

---

## Package Pinning & Holds

```bash
# Hold a package at current version (don't upgrade)
apt-mark hold nginx
apt-mark showhold

# Unhold
apt-mark unhold nginx

# Install specific version
apt install nginx=1.18.0-0ubuntu1
```

---

# 🐳 How Docker Uses Linux

> Docker is NOT magic. It's Linux kernel features packaged into a developer-friendly tool.

```
docker run -d --memory=512m --cpus=1 nginx
           ↓
Linux Kernel Features:
  ├── namespaces  → isolation
  ├── cgroups     → resource limits
  ├── OverlayFS   → layered filesystems
  └── seccomp     → syscall filtering
```

---

## Namespaces — Container Isolation

Each container gets its own set of namespaces:

|Namespace|What container sees|
|---|---|
|`pid`|Its own process tree (PID 1 = container init)|
|`net`|Its own network interfaces (eth0, lo)|
|`mnt`|Its own filesystem view|
|`uts`|Its own hostname|
|`ipc`|Isolated IPC|
|`user`|Can have "root" inside without being real root|

```bash
# See container namespaces
docker inspect <container> | grep -i pid
ls -la /proc/<container-pid>/ns/

# The container's PID 1 from host perspective
docker top mycontainer
```

---

## cgroups — Resource Limits

```bash
# Docker uses cgroups to enforce limits
docker run -m 512m --cpus=1 nginx

# Where it shows up on the host
cat /sys/fs/cgroup/memory/docker/<container-id>/memory.limit_in_bytes
cat /sys/fs/cgroup/cpu/docker/<container-id>/cpu.cfs_quota_us

# systemd slice for docker
systemd-cgtop | grep docker
```

---

## Union Filesystem (OverlayFS)

```
Container layers (read-only):
  ┌────────────────────────┐  ← Layer 3: COPY index.html
  ├────────────────────────┤  ← Layer 2: RUN apt install nginx
  ├────────────────────────┤  ← Layer 1: FROM ubuntu:22.04
  └────────────────────────┘

Container writable layer:
  ┌────────────────────────┐  ← Layer 4: Your writes (ephemeral)
```

- Each `RUN`, `COPY`, `ADD` in Dockerfile = new layer
- Layers are shared between containers using same base image → saves disk
- Write to a file in a running container = **copy-on-write** to writable layer

```bash
# See image layers
docker history nginx

# Where layers are stored on host
ls /var/lib/docker/overlay2/

# Check container's filesystem on host
docker inspect mycontainer | grep MergedDir
```

---

## Kernel Sharing

```
Host Machine
├── Linux Kernel (shared by everyone)
├── Container A (nginx) ← its own namespaces + cgroups
├── Container B (mysql) ← its own namespaces + cgroups
└── Container C (app)  ← its own namespaces + cgroups

vs VMs:
Host Machine
├── Hypervisor
├── VM1: Full Linux kernel + OS
├── VM2: Full Linux kernel + OS
└── VM3: Full Linux kernel + OS  ← much heavier
```

Implications:

- Containers share kernel → **can't run Windows containers on Linux kernel**
- Containers are lighter (no full OS per container)
- A kernel vulnerability affects all containers on that host

---

## seccomp — Syscall Filtering

```bash
# Docker blocks ~44 dangerous syscalls by default
# Example: containers can't use reboot(), mount(), etc.

# See the default seccomp profile
docker info | grep seccomp

# Run without seccomp (dangerous)
docker run --security-opt seccomp=unconfined nginx

# Check what syscalls a process uses
strace -c -p PID
```

---

## Docker Networking (Linux Under the Hood)

```
Container eth0
    ↓
veth pair (virtual ethernet)
    ↓
docker0 bridge (172.17.0.1)
    ↓
iptables NAT rules (masquerade)
    ↓
Host eth0
    ↓
Internet
```

```bash
# See Docker bridge on host
ip a show docker0

# See veth pairs
ip link show type veth

# Docker's iptables rules
iptables -t nat -L DOCKER -n
iptables -L DOCKER -n

# Container's network namespace
docker inspect <container> | grep NetworkMode
```

---

_Last updated: 2025 | Real Linux. Real Engineering. 🐧_