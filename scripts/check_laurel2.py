#!/usr/bin/env python3
import urllib.request, json, yaml, sys

with open('/data/data/com.termux/files/home/.config/gh/hosts.yml') as f:
    d = yaml.safe_load(f)
    TOKEN = d['github.com']['oauth_token']

def api(path):
    req = urllib.request.Request('https://api.github.com' + path,
        headers={'Authorization': 'Bearer ' + TOKEN})
    return json.loads(urllib.request.urlopen(req).read())

runs = api('/repos/criollojoel10/alarm-laurel_sprout/actions/runs?branch=main&per_page=2')
for r in runs['workflow_runs']:
    print(f"#{r['run_number']} {r['status']} {r.get('conclusion','?')}")
    if r.get('conclusion') == 'failure':
        jobs = api(f"/repos/criollojoel10/alarm-laurel_sprout/actions/runs/{r['id']}/jobs")
        for job in jobs['jobs']:
            for s in job['steps']:
                if s.get('conclusion') == 'failure':
                    print(f"  FAIL: {s['name']}")
            if job['conclusion'] == 'failure':
                log_url = job.get('logs_url', '')
                if log_url:
                    req2 = urllib.request.Request(log_url,
                        headers={'Authorization': 'Bearer ' + TOKEN})
                    try:
                        resp = urllib.request.urlopen(req2)
                        if resp.status in (301, 302):
                            req2 = urllib.request.Request(resp.headers.get('Location', ''))
                            resp = urllib.request.urlopen(req2)
                        data = resp.read().decode('utf-8','replace')
                        lines = data.split('\n')
                        count = 0
                        for line in reversed(lines):
                            l = line.strip()
                            if l:
                                print(f"  {l[:300]}")
                                count += 1
                                if count >= 50:
                                    break
                    except Exception as e:
                        print(f'  Error: {e}')
        break
