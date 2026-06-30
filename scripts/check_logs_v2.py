#!/usr/bin/env python3
import urllib.request, json, yaml, os, sys

with open('/data/data/com.termux/files/home/.config/gh/hosts.yml') as f:
    d = yaml.safe_load(f)
    TOKEN = d['github.com']['oauth_token']

def api(url):
    req = urllib.request.Request(url,
        headers={'Authorization': 'Bearer ' + TOKEN})
    return json.loads(urllib.request.urlopen(req).read())

# Get latest run
runs = api('https://api.github.com/repos/criollojoel10/alarm-laurel_sprout/actions/runs?branch=main&per_page=1')
r = runs['workflow_runs'][0]
print(f"#{r['run_number']} - {r['status']} - {r.get('conclusion','?')}")

# Get jobs
jobs = api(f"https://api.github.com/repos/criollojoel10/alarm-laurel_sprout/actions/runs/{r['id']}/jobs")
for job in jobs['jobs']:
    print(f"Job {job['id']}: {job['conclusion']}")
    
    if job['conclusion'] == 'failure':
        # Get logs directly with the raw URL pattern
        log_url = f"https://api.github.com/repos/criollojoel10/alarm-laurel_sprout/actions/jobs/{job['id']}/logs"
        
        req_log = urllib.request.Request(log_url,
            headers={'Authorization': 'Bearer ' + TOKEN,
                     'Accept': 'application/vnd.github.v3+json'})
        try:
            resp = urllib.request.urlopen(req_log)
            ct = resp.headers.get('Content-Type', '')
            print(f"Status: {resp.status}, CT: {ct}")
            
            if resp.status in (301, 302, 307):
                loc = resp.headers.get('Location', '')
                print(f"Redirect to: {loc}")
                if loc:
                    req2 = urllib.request.Request(loc)
                    resp = urllib.request.urlopen(req2)
                    data = resp.read().decode('utf-8', 'replace')
                else:
                    data = ''
            else:
                data = resp.read().decode('utf-8', 'replace')
            
            lines = data.split('\n')
            print(f"Total log lines: {len(lines)}")
            
            # Print last 50 non-empty
            count = 0
            for line in reversed(lines):
                if line.strip():
                    print(line[:300])
                    count += 1
                    if count >= 30:
                        break
                        
        except Exception as e:
            print(f"Log fetch error: {e}")
            pass
