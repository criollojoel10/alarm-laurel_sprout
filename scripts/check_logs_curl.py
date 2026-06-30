#!/usr/bin/env python3
import json, sys, re, subprocess

with open('/data/data/com.termux/files/home/.config/gh/hosts.yml') as f:
    content = f.read()
    m = re.search(r'oauth_token:\s*(\S+)', content)
    if not m:
        print('ERROR: could not find token')
        sys.exit(1)
    TOKEN = m.group(1)

def run_cmd(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

# Get job logs using curl
result = subprocess.run([
    'curl', '-sSL',
    '-H', 'Authorization: Bearer ' + TOKEN,
    '-H', 'Accept: application/vnd.github.v3+json',
    'https://api.github.com/repos/criollojoel10/alarm-laurel_sprout/actions/jobs/84367100239/logs'
], capture_output=True, text=True)

data = result.stdout
if result.returncode != 0:
    print('curl failed:', result.stderr)

# Check if it's a redirect (HTML or JSON with message)
lines = data.split('\n')
print(f'Total lines: {len(lines)}')
print('Last 40 non-empty lines:')
count = 0
for line in reversed(lines):
    if line.strip():
        print(line[:300])
        count += 1
        if count >= 40:
            break
