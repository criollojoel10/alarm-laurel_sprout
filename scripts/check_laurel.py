#!/usr/bin/env python3
import urllib.request, json, yaml, sys

with open('/data/data/com.termux/files/home/.config/gh/hosts.yml') as f:
    d = yaml.safe_load(f)
    TOKEN = d['github.com']['oauth_token']

def api(path):
    req = urllib.request.Request('https://api.github.com' + path,
        headers={'Authorization': 'Bearer ' + TOKEN})
    return json.loads(urllib.request.urlopen(req).read())

r = api('/repos/criollojoel10/alarm-laurel_sprout/actions/runs?branch=main&per_page=1')
r = r['workflow_runs'][0]
print(f"# Run #{r['run_number']} - {r['status']} - {r.get('conclusion','?')}")

j = api('/repos/criollojoel10/alarm-laurel_sprout/actions/runs/' + str(r['id']) + '/jobs')
for job in j['jobs']:
    print(f"  Job {job['id']}: {job['conclusion']}")
    for s in job['steps']:
        if s.get('conclusion') not in ('success', 'skipped', None):
            print(f"    FAIL #{s['number']}: {s['name']}")
    if job['conclusion'] == 'failure':
        print("  --- LOGS ---")
        log_url = job.get('logs_url', '')
        if log_url:
            req2 = urllib.request.Request(log_url,
                headers={'Authorization': 'Bearer ' + TOKEN})
            resp = urllib.request.urlopen(req2)
            if resp.status in (301, 302):
                log_url2 = resp.headers.get('Location', '')
                req2 = urllib.request.Request(log_url2)
                resp = urllib.request.urlopen(req2)
            data = resp.read().decode('utf-8','replace')
            lines = data.split('\n')
            print(f"  Total lines: {len(lines)}")
            count = 0
            for line in reversed(lines):
                l = line.strip()
                if l:
                    print(f"  {l[:300]}")
                    count += 1
                    if count >= 50:
                        break
        break
