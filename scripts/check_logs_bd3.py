#!/usr/bin/env python3
import json, sys, re, subprocess

with open('/data/data/com.termux/files/home/.config/gh/hosts.yml') as f:
    content = f.read()
    m = re.search(r'oauth_token:\s*(\S+)', content)
    if not m:
        print('ERROR: could not find token')
        sys.exit(1)
    TOKEN = m.group(1)

# First get the redirect URL
result = subprocess.run([
    'curl', '-s', '-o', '/dev/null', '-w', '%{redirect_url}',
    '-H', 'Authorization: Bearer ' + TOKEN,
    '-H', 'Accept: application/vnd.github.v3+json',
    '-L',
    'https://api.github.com/repos/criollojoel10/alarm-laurel_sprout/actions/jobs/84367100239/logs'
], capture_output=True, text=True, timeout=10)

if result.returncode != 0:
    print(f'curl error: {result.stderr}')
    sys.exit(1)

redirect_url = result.stdout.strip()
print(f'Redirect URL length: {len(redirect_url)}')
print(f'Redirect URL prefix: {redirect_url[:80]}...')

if not redirect_url or not redirect_url.startswith('http'):
    print(f'No redirect URL! stdout: "{result.stdout}"')
    # Try getting the response body instead
    result2 = subprocess.run([
        'curl', '-sSL',
        '-H', 'Authorization: Bearer ' + TOKEN,
        '-H', 'Accept: application/vnd.github.v3+json',
        'https://api.github.com/repos/criollojoel10/alarm-laurel_sprout/actions/jobs/84367100239/logs'
    ], capture_output=True, text=True, timeout=10)
    print(f'Response: {result2.stdout[:500]}')
else:
    # Download the first 100 lines from the redirect URL
    result2 = subprocess.run([
        'curl', '-s', '--max-time', '10',
        '-r', '0-500000',
        redirect_url
    ], capture_output=True, text=True, timeout=10)
    lines = result2.stdout.split('\n')
    print(f'Downloaded {len(lines)} lines')
    
# Search for boot-deploy lines
for i, line in enumerate(lines):
    if 'boot-deploy' in line:
        print(f'L{i}: {line[:250]}')

print('\n--- mkinitfs completed ---')
for i, line in enumerate(lines):
    if 'mkinitfs completed in' in line:
        for j in range(max(0,i-15), min(len(lines), i+8)):
            l = lines[j].strip()
            if l:
                print(f'L{j}: {l[:250]}')
        break
