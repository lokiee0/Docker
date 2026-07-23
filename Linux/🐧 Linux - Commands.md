# 🐧 Linux — Commands Reference

> All essential Linux commands in one place. Use this as your daily cheat sheet.

---

## 📑 Table of Contents

- [[#Navigation]]
- [[#File Operations]]
- [[#Viewing Files]]
- [[#File Permissions]]
- [[#Users & Groups]]
- [[#Process Management]]
- [[#Package Management]]
- [[#Networking]]
- [[#Disk Management]]
- [[#SSH & SCP]]
- [[#Systemd & Services]]
- [[#Logs]]
- [[#Cron]]
- [[#Text Processing]]
- [[#Compression]]
- [[#Redirection & Pipes]]
- [[#Environment Variables]]
- [[#Find & Search]]
- [[#Quick Cheat Sheet]]

---

## Navigation

| Command | Purpose |
|---|---|
| `pwd` | Print current directory |
| `ls` | List files |
| `ls -la` | Long listing with hidden files |
| `ls -lh` | Human-readable sizes |
| `cd /path` | Change directory |
| `cd ~` | Go to home directory |
| `cd -` | Go to previous directory |
| `tree` | Visual directory tree |

---

## File Operations

| Command | Purpose |
|---|---|
| `touch file.txt` | Create empty file |
| `mkdir dir` | Create directory |
| `mkdir -p a/b/c` | Create nested directories |
| `cp src dst` | Copy file |
| `cp -r src/ dst/` | Copy directory recursively |
| `mv src dst` | Move or rename |
| `rm file` | Remove file |
| `rm -rf dir/` | Remove directory ⚠️ |
| `ln -s target link` | Create symbolic link |

---

## Viewing Files

| Command | Purpose |
|---|---|
| `cat file` | Print file content |
| `less file` | Page through content |
| `head -n 20 file` | First 20 lines |
| `tail -n 20 file` | Last 20 lines |
| `tail -f file` | Follow file in real-time |
| `wc -l file` | Count lines |
| `stat file` | Detailed file info |
| `diff file1 file2` | Compare two files |

---

## File Permissions

| Command | Purpose |
|---|---|
| `chmod 755 file` | Set permissions numerically |
| `chmod +x file` | Add execute bit |
| `chmod -R 755 dir/` | Recursive permissions |
| `chown user file` | Change owner |
| `chown user:group file` | Change owner + group |
| `chown -R user:group dir/` | Recursive ownership |
| `umask` | Show default permission mask |

```
Permission values:
  r = 4   w = 2   x = 1
  755 → rwxr-xr-x
  644 → rw-r--r--
  600 → rw-------
```

---

## Users & Groups

| Command | Purpose |
|---|---|
| `whoami` | Current user |
| `id` | User + group IDs |
| `useradd -m -s /bin/bash user` | Create user |
| `passwd username` | Set password |
| `usermod -aG group user` | Add user to group |
| `userdel -r username` | Delete user + home |
| `groupadd devops` | Create group |
| `groups user` | List user's groups |
| `su - username` | Switch user |
| `sudo command` | Run as root |
| `visudo` | Edit sudoers safely |

---

## Process Management

| Command | Purpose |
|---|---|
| `ps aux` | All running processes |
| `top` | Live process monitor |
| `htop` | Interactive monitor |
| `pgrep nginx` | Find PID by name |
| `kill PID` | Graceful stop |
| `kill -9 PID` | Force kill |
| `pkill nginx` | Kill by name |
| `nice -n 10 cmd` | Start with priority |
| `renice -n 5 PID` | Change priority |
| `command &` | Run in background |
| `jobs` | List background jobs |
| `fg %1` | Bring job to foreground |
| `nohup command &` | Run immune to hangup |

---

## Package Management

### APT (Ubuntu/Debian)

| Command | Purpose |
|---|---|
| `apt update` | Refresh package lists |
| `apt upgrade` | Upgrade all packages |
| `apt install nginx` | Install package |
| `apt remove nginx` | Remove package |
| `apt purge nginx` | Remove + config files |
| `apt autoremove` | Remove unused packages |
| `apt search nginx` | Search packages |
| `dpkg -l` | List installed packages |
| `dpkg -i pkg.deb` | Install .deb file |

### DNF (RHEL/CentOS)

| Command | Purpose |
|---|---|
| `dnf update` | Update all |
| `dnf install nginx` | Install |
| `dnf remove nginx` | Remove |
| `rpm -qa` | List installed |
| `rpm -ivh pkg.rpm` | Install .rpm |

---

## Networking

| Command | Purpose |
|---|---|
| `ip a` | Show interfaces & IPs |
| `ip route` | Show routing table |
| `hostname -I` | Quick IP display |
| `ping -c 4 8.8.8.8` | Ping 4 times |
| `traceroute google.com` | Trace route |
| `curl ifconfig.me` | Get public IP |
| `curl -I https://site.com` | HTTP headers only |
| `wget https://url/file` | Download file |
| `ss -tulnp` | Open ports + processes |
| `nmap -sV 192.168.1.1` | Port scan |
| `lsof -i :80` | What's using port 80 |
| `dig google.com` | DNS lookup |
| `nslookup google.com` | DNS lookup (simple) |

### UFW Firewall

| Command | Purpose |
|---|---|
| `ufw status` | Show rules |
| `ufw enable` | Enable firewall |
| `ufw allow 22/tcp` | Allow SSH |
| `ufw deny 23` | Block port |
| `ufw delete allow 80` | Remove rule |

---

## Disk Management

| Command | Purpose |
|---|---|
| `df -h` | Disk usage |
| `du -sh /var/log` | Size of directory |
| `du -sh /* \| sort -rh` | Largest dirs |
| `lsblk` | List block devices |
| `fdisk -l` | Partition table |
| `mount /dev/sdb1 /mnt` | Mount filesystem |
| `umount /mnt` | Unmount |
| `mkfs.ext4 /dev/sdb1` | Format as ext4 |
| `swapon --show` | Show swap |
| `free -h` | Memory + swap |

---

## SSH & SCP

| Command | Purpose |
|---|---|
| `ssh user@ip` | Connect |
| `ssh user@ip -p 2222` | Custom port |
| `ssh -i key.pem user@ip` | With private key |
| `ssh-keygen -t rsa -b 4096` | Generate key pair |
| `ssh-copy-id user@ip` | Copy public key to server |
| `scp file.txt user@ip:/path/` | Upload file |
| `scp user@ip:/path/file ./` | Download file |
| `scp -r ./dir user@ip:/path/` | Upload directory |

---

## Systemd & Services

| Command | Purpose |
|---|---|
| `systemctl start nginx` | Start service |
| `systemctl stop nginx` | Stop service |
| `systemctl restart nginx` | Restart |
| `systemctl reload nginx` | Reload config |
| `systemctl status nginx` | Check status |
| `systemctl enable nginx` | Start on boot |
| `systemctl disable nginx` | Don't start on boot |
| `systemctl list-units --type=service` | All services |
| `systemctl daemon-reload` | Reload systemd config |

---

## Logs

| Command | Purpose |
|---|---|
| `tail -f /var/log/syslog` | Follow system log |
| `tail -n 100 /var/log/auth.log` | Last 100 lines |
| `grep "Failed" /var/log/auth.log` | Filter log |
| `journalctl -u nginx` | Service logs |
| `journalctl -f` | Follow live |
| `journalctl -xe` | Recent errors |
| `journalctl -p err` | Error level only |
| `journalctl --vacuum-size=500M` | Trim log size |

---

## Cron

```
* * * * *  command
│ │ │ │ └── Day of week (0-7)
│ │ │ └──── Month (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)
```

| Command | Purpose |
|---|---|
| `crontab -e` | Edit crontab |
| `crontab -l` | View crontab |
| `crontab -r` | Remove crontab |

```bash
30 2 * * *     /home/loki/backup.sh    # Daily at 2:30 AM
*/15 * * * *   /scripts/check.sh       # Every 15 minutes
0 9 * * 1-5    /scripts/report.sh      # Weekdays at 9 AM
0 0 * * 0      /scripts/weekly.sh      # Every Sunday midnight
```

---

## Text Processing

| Command | Purpose |
|---|---|
| `grep "error" file` | Search in file |
| `grep -i "error" file` | Case-insensitive |
| `grep -r "error" /var/log/` | Recursive |
| `grep -n "error" file` | Show line numbers |
| `grep -v "info" file` | Exclude matches |
| `grep -E "error\|fail" file` | Extended regex |
| `awk '{print $1}' file` | Print first column |
| `awk -F: '{print $1}' /etc/passwd` | Custom delimiter |
| `sed 's/old/new/g' file` | Replace all |
| `sed -i 's/old/new/g' file` | In-place edit |
| `sort file` | Sort alphabetically |
| `sort -n file` | Numeric sort |
| `sort file \| uniq` | Remove duplicates |
| `cut -d: -f1 /etc/passwd` | Cut field |

---

## Compression

| Command | Purpose |
|---|---|
| `tar -czf out.tar.gz /dir` | Create gzip archive |
| `tar -xzf archive.tar.gz` | Extract gzip |
| `tar -xf archive.tar -C /dest/` | Extract to dir |
| `tar -tzf archive.tar.gz` | View contents |
| `zip -r out.zip /dir` | Zip directory |
| `unzip archive.zip` | Unzip |
| `gzip file.txt` | Compress file |
| `gunzip file.txt.gz` | Decompress |

---

## Redirection & Pipes

| Operator | Purpose |
|---|---|
| `>` | Redirect stdout (overwrite) |
| `>>` | Redirect stdout (append) |
| `2>` | Redirect stderr |
| `2>&1` | Merge stderr into stdout |
| `&>` | Both stdout + stderr |
| `<` | Read stdin from file |
| `\|` | Pipe output to next command |

```bash
command > file.txt          # Save output
command >> file.txt         # Append output
command 2>/dev/null         # Suppress errors
command &> all.txt          # Capture everything
cmd1 | cmd2 | cmd3          # Chain commands
echo "hello" | tee out.txt  # Print + save
```

---

## Environment Variables

| Command | Purpose |
|---|---|
| `printenv` | Print all env vars |
| `echo $PATH` | Print PATH |
| `export MY_VAR="hello"` | Set variable |
| `unset MY_VAR` | Remove variable |
| `source ~/.bashrc` | Reload shell config |

```bash
# Persist variable across sessions
echo 'export MY_VAR="hello"' >> ~/.bashrc
source ~/.bashrc

# Add to PATH
export PATH="$PATH:/usr/local/myapp/bin"
```

---

## Find & Search

| Command | Purpose |
|---|---|
| `find / -name nginx.conf` | Find by name |
| `find /home -type f -name "*.log"` | Find log files |
| `find /tmp -mtime +7` | Files older than 7 days |
| `find / -size +100M` | Files larger than 100MB |
| `find /etc -perm 777` | World-writable files |
| `which python3` | Path of command |
| `whereis nginx` | Binary + man page |
| `locate file.txt` | Fast file search (uses db) |

---

## ⚡ Quick Cheat Sheet

```bash
# ── Navigation ───────────────────────────────────────
pwd                        # Where am I?
ls -la                     # List all files
cd /path                   # Go to path
cd ~                       # Go home

# ── Files ────────────────────────────────────────────
touch file.txt             # Create file
mkdir -p a/b/c             # Create nested dirs
cp -r src/ dst/            # Copy directory
mv old new                 # Move / rename
rm -rf dir/                # Delete directory ⚠️

# ── Permissions ──────────────────────────────────────
chmod 755 file             # rwxr-xr-x
chmod +x script.sh         # Make executable
chown user:group file      # Change ownership

# ── Processes ────────────────────────────────────────
ps aux                     # All processes
kill -9 PID                # Force kill
top / htop                 # Live monitor

# ── Services ─────────────────────────────────────────
systemctl start nginx      # Start
systemctl status nginx     # Check
systemctl enable nginx     # Auto-start on boot

# ── Networking ───────────────────────────────────────
ip a                       # Show IPs
ss -tulnp                  # Open ports
ping -c 4 8.8.8.8         # Test connectivity
curl ifconfig.me           # Public IP

# ── Disk ─────────────────────────────────────────────
df -h                      # Disk usage
du -sh /var/log            # Dir size
lsblk                      # Block devices

# ── Logs ─────────────────────────────────────────────
tail -f /var/log/syslog    # Follow system log
journalctl -u nginx -f     # Follow service log

# ── Search ───────────────────────────────────────────
grep -r "error" /var/log/  # Search in files
find / -name "*.conf"      # Find files

# ── Cleanup ──────────────────────────────────────────
apt autoremove             # Remove unused packages
journalctl --vacuum-size=500M  # Trim logs
docker system prune        # Clean Docker (if installed)
```

---

_Tags: #linux #devops #commands #cheatsheet_
