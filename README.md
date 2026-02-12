# IPFinder - IP Lookup Tool

## Description

**IPFinder** is an advanced research tool for locating user IP addresses from log files. It's useful for analyzing past connections and identifying the IP address associated with a given username.

## Features

✅ **Flexible username search** - Searches for the username with multiple variants (uppercase, lowercase, mixed case, etc.)

✅ **Multi-format support** - Reads `.log`, `.log.gz`, and `latest.log` files

✅ **IP extraction** - Automatically extracts IP address and port from each connection found

✅ **Time parsing** - Retrieves the time of each connection

✅ **Ping validation** - Tests discovered IPs to verify which ones are accessible

✅ **Sorted results** - Displays connections sorted by file and time

✅ **Cross-platform** - Works on Windows and Linux/Mac

## Installation

No external dependencies required - uses only Python standard library.

```bash
python iplookup.py
```

## Usage

1. Place your `.log` or `.log.gz` files in the same directory as the script
2. Run the script:
   ```bash
   python iplookup.py
   ```
3. Enter the username to search for when prompted
4. The script will display:
   - Generated username variants
   - All connections found with IP, port, time, and source file
   - Ping test results on unique IPs

## Usage Example

```
Enter the username to search for: player123
→ Generated variants: player123, Player123, PLAYER123, 123REYALP, ...

All connections found for player123 (and variants):

- 14:32:05 | player123 | IP: 192.168.1.100:25565 | File: latest.log
  > [14:32:05] player123 joined the game / [192.168.1.100:25565]

=== Testing unique IPs found (ping) ===
192.168.1.100 : ❌ Does not respond
```

## How It Works

### 1. Variant Generation

The script automatically generates multiple username variants to improve discovery chances:

- Lowercase: `username`
- Uppercase: `USERNAME`
- Capitalized: `Username`
- Swapcase: `uSERNAME`
- Variants with extra 'x' if applicable

### 2. Log Extraction

Iterates through all `.log`, `.log.gz`, and `latest.log` files in the current directory and extracts lines containing:

- Time `[HH:MM:SS]`
- Username (or variant)
- IP address and port

### 3. Ping Test

Uses `ping` (system command) to verify if discovered IPs are currently accessible:

- **Windows**: `ping -n 1 -w 1000`
- **Linux/Mac**: `ping -c 1`

## Supported Log File Format

The script searches for the following pattern in logs:

```
[HH:MM:SS]...<username>.../<IP:PORT> or /[IP:PORT]
```

Example:

```
[14:32:05] User|player123 joined the game /[192.168.1.100:25565]
```

## Troubleshooting

**"No IP responds"**

- The user is in DHCP mode (dynamic IP)
- The computer is turned off
- A firewall blocks pings
- The IPs are invalid
- The user may have already changed IP

**"No connections found"**

- Check the username spelling
- Make sure `.log` files are in the current directory
- Verify that the log format matches the expected pattern

## Limitations

- IPs can be dynamic (change on restart)
- Some firewalls block pings (not 100% reliable)
- The log format must match the pattern recognized by the script

## License

Free to use for research and analysis.
