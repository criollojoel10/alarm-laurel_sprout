import urllib.request, json, sys, os

TOKEN = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('GH_TOKEN', '')

# Get job details first  
req = urllib.request.Request(
    'https://api.github.com/repos/criollojoel10/alarm-laurel_sprout/actions/jobs/84354651974',
    headers={'Authorization': f'Bearer {TOKEN}', 'Accept': 'application/vnd.github.v3+json'}
)
d = json.loads(urllib.request.urlopen(req).read())
logs_url = d.get('logs_url', '')
print(f'logs_url: {logs_url}')

if not logs_url:
    logs_url = 'https://api.github.com/repos/criollojoel10/alarm-laurel_sprout/actions/jobs/84354651974/logs'

if logs_url:
    log_req = urllib.request.Request(logs_url, headers={
        'Authorization': f'Bearer {TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    })
    try:
        resp = urllib.request.urlopen(log_req)
        data = resp.read().decode('utf-8', 'replace')
        lines = data.split('\n')
        print(f'Total log lines: {len(lines)}')
        count = 0
        for line in reversed(lines):
            if line.strip():
                print(line[:250])
                count += 1
                if count >= 50:
                    break
    except Exception as e:
        print(f'Error: {e}')
