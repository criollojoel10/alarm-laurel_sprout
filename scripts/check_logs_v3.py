#!/usr/bin/env python3
import urllib.request, json, yaml, os, sys

with open('/data/data/com.termux/files/home/.config/gh/hosts.yml') as f:
    d = yaml.safe_load(f)
    TOKEN = d['github.com']['oauth_token']

def api(url):
    req = urllib.request.Request(url,
        headers={'Authorization': 'Bearer ' + TOKEN})
    resp = urllib.request.urlopen(req)
    ct = resp.headers.get('Content-Type', '')
    if 'application/json' in ct:
        return json.loads(resp.read())
    else:
        return resp.read().decode('utf-8','replace')

# Get latest run 
runs_data = api('https://api.github.com/repos/criollojoel10/alarm-laurel_sprout/actions/runs?branch=main&per_page=1')
r = runs_data['workflow_runs'][0]
print(f"#{r['run_number']} - {r.get('conclusion','?')}")

# Get jobs
jobs = api(f"https://api.github.com/repos/criollojoel10/alarm-laurel_sprout/actions/runs/{r['id']}/jobs")
for job in jobs['jobs']:
    print(f"Job {job['id']}: {job['conclusion']}")
    if job['conclusion'] == 'failure':
        log_url = job.get('logs_url', '')
        print(f"logs_url: {log_url}")
        
        if not log_url:
            print("No logs_url from API, using constructed URL")
            log_url = f"https://api.github.com/repos/criollojoel10/alarm-laurel_sprout/actions/jobs/{job['id']}/logs"
        
        # Use curl approach instead
        print("Trying with urllib...")
        try:
            req = urllib.request.Request(log_url,
                headers={'Authorization': 'Bearer ' + TOKEN,
                         'Accept': 'application/vnd.github.v3+json'})
            resp = urllib.request.urlopen(req)
            print(f"Status: {resp.status}")
            
            # Follow redirect manually
            if resp.status in (301, 302, 307, 303):
                loc = resp.headers.get('Location', '')
                print(f"Location: {loc[:100] if loc else 'none'}")
                if loc:
                    req2 = urllib.request.Request(loc)
                    resp = urllib.request.urlopen(req2, timeout=30)
                    data = resp.read().decode('utf-8', 'replace')
                else:
                    data = resp.read().decode('utf-8', 'replace')
            else:
                data = resp.read().decode('utf-8', 'replace')
            
            lines = data.split('\n')
            print(f"Total: {len(lines)}")
            for line in reversed(lines):
                if line.strip():
                    print(line[:300])
                    break
                    
        except Exception as e:
            print(f"Error: {e}")
            # Try with Accept: application/vnd.github.v3.raw
            print("Trying with v3.raw accept...")
            try:
                req = urllib.request.Request(log_url,
                    headers={'Authorization': 'Bearer ' + TOKEN,
                             'Accept': 'application/vnd.github.v3.raw'})
                resp = urllib.request.urlopen(req)
                if resp.status in (301, 302, 307, 303):
                    loc = resp.headers.get('Location', '')
                    print(f"Location: {loc[:100] if loc else 'none'}")
                    if loc:
                        req2 = urllib.request.Request(loc)
                        resp = urllib.request.urlopen(req2, timeout=30)
                        data = resp.read().decode('utf-8', 'replace')
                    else:
                        data = ''
                else:
                    data = resp.read().decode('utf-8', 'replace')
                lines = data.split('\n')
                print(f"Total lines: {len(lines)}")
                count = 0
                for line in reversed(lines):
                    if line.strip():
                        print(line[:300])
                        count += 1
                        if count >= 30:
                            break
            except Exception as e2:
                print(f"Error2: {e2}")
