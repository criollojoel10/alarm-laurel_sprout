#!/usr/bin/env python3
import json, sys, re, subprocess

with open('/data/data/com.termux/files/home/.config/gh/hosts.yml') as f:
    content = f.read()
    m = re.search(r'oauth_token:\s*(\S+)', content)
    if not m:
        print('ERROR: could not find token')
        sys.exit(1)
    TOKEN = m.group(1)

result = subprocess.run([
    'curl', '-sSL',
    '-H', 'Authorization: Bearer ' + TOKEN,
    '-H', 'Accept: application/vnd.github.v3+json',
    'https://api.github.com/repos/criollojoel10/alarm-laurel_sprout/actions/jobs/84367100239/logs'
], capture_output=True, text=True, timeout=20)

lines = result.stdout.split('\n')

# Search for boot-deploy lines
for i, line in enumerate(lines):
    if 'boot-deploy' in line:
        print(f'L{i}: {line[:250]}')

# Find mkinitfs completed line
for i, line in enumerate(lines):
    if 'mkinitfs completed in' in line:
        print(f'\n--- Around mkinitfs completed ---')
        for j in range(max(0,i-15), min(len(lines), i+8)):
            l = lines[j].strip()
            if l:
                print(f'L{j}: {l[:250]}')
        break
