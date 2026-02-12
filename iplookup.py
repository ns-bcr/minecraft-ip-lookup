import gzip
import os
import re
import platform
import subprocess
import itertools

def generate_variants(pseudo):
    base = pseudo
    variants = set()
    variants.add(base)
    variants.add(base.lower())
    variants.add(base.upper())
    variants.add(base.capitalize())
    variants.add(base.swapcase())
    if base.endswith('x'):
        variants.add(base + 'x')
        variants.add(base.capitalize() + 'x')
        variants.add(base.upper() + 'X')
    if base.endswith('xx'):
        variants.add(base + 'x')
    if len(base) > 1:
        variants.add(base[0].upper() + base[1:])
        variants.add(base[:-1] + base[-1].upper())
    return list({v for v in variants if v})

def read_log(filename):
    if filename.endswith('.gz'):
        with gzip.open(filename, 'rt', encoding='utf-8', errors='ignore') as f:
            return f.readlines()
    else:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            return f.readlines()

def extract_ips_from_log(lines, pseudos):
    pseudos_regex = '|'.join(map(re.escape, pseudos))
    pattern = re.compile(
        r"\[(\d{2}:\d{2}:\d{2})\].*?\b(" + pseudos_regex + r")\b.*?/\[?([0-9]{1,3}(?:\.[0-9]{1,3}){3})\:(\d{1,5})\]?"
    )
    result = []
    for line in lines:
        match = pattern.search(line)
        if match:
            hour, pseudo, ip, port = match.groups()
            result.append({
                "hour": hour,
                "pseudo": pseudo,
                "ip": ip,
                "port": port,
                "raw": line.strip()
            })
    return result

def ping_ip(ip):
    system = platform.system().lower()
    count_flag = '-n' if system == 'windows' else '-c'
    try:
        result = subprocess.run(
            ["ping", count_flag, "1", "-w", "1000", ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False

def main():
    pseudo = input("Enter the username to search for: ").strip()
    variants = generate_variants(pseudo)
    print(f"→ Generated variants: {', '.join(variants)}")

    log_dir = "."
    log_files = [f for f in os.listdir(log_dir) if f.endswith('.log') or f.endswith('.log.gz') or f == "latest.log"]

    all_results = []
    for filename in sorted(log_files):
        try:
            lines = read_log(filename)
            res = extract_ips_from_log(lines, variants)
            for entry in res:
                entry['file'] = filename
            all_results.extend(res)
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    all_results.sort(key=lambda x: (x['file'], x['hour']))

    if all_results:
        print(f"\nAll connections found for {pseudo} (and variants):\n")
        for entry in all_results:
            print(f"- {entry['hour']} | {entry['pseudo']} | IP: {entry['ip']}:{entry['port']} | File: {entry['file']}\n  > {entry['raw']}")
        unique_ips = list(dict.fromkeys(x['ip'] for x in all_results))  # Order of appearance

        print(f"\n=== Testing unique IPs found (ping) ===")
        for ip in unique_ips:
            if ping_ip(ip):
                print(f"Found! {ip} (✅ Responds to ping)")
                break
            else:
                print(f"{ip} : ❌ Does not respond")
        else:
            print("No IP responds (◡ ︵ ◡ ), the user's box is probably in dynamic mode or turned off.")
            print("End of search.")
    else:
        print("No connections found for this username (or variants).")

if __name__ == "__main__":
    main()
