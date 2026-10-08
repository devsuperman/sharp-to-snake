# sync_positions.py -- uploads raw tracker pings to the tracking API
# written in 2019 by someone who left the company. DO NOT TOUCH, it works.
# usage: python sync_positions.py pings.csv
#
# NOTE FOR THE COURSE: this file is deliberately bad. It is the thing you will migrate.
# Do not "fix" it: the tests in tests/test_legacy_characterization.py pin its behaviour.
import csv
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timedelta

API_URL = os.environ.get("TRACKING_API", "http://localhost:8080/api/positions")
TOKEN = os.environ.get("TRACKING_TOKEN")
BATCH = 50
sent = 0
errors = 0


def load(path):
    rows = []
    seen = []
    with open(path) as f:
        for r in csv.DictReader(f):
            try:
                lat = float(r["lat"])
                lon = float(r["lon"])
                speed = float(r["speed_kmh"])
                t = datetime.strptime(r["timestamp"], "%d/%m/%Y %H:%M:%S") + timedelta(hours=3)
            except:
                continue
            if lat == 0 and lon == 0:
                continue
            if speed > 200:
                continue
            dev = r["device_id"].strip().upper()
            key = dev + r["timestamp"]
            if key in seen:
                continue
            seen.append(key)
            rows.append(
                {
                    "device": dev,
                    "ts": t.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "lat": lat,
                    "lon": lon,
                    "speed": speed,
                }
            )
    return rows


def post(batch):
    global sent, errors
    for i in range(3):
        try:
            req = urllib.request.Request(
                API_URL,
                data=json.dumps(batch).encode(),
                headers={"Authorization": "Token " + TOKEN, "Content-Type": "application/json"},
            )
            r = urllib.request.urlopen(req)
            if r.status == 200:
                sent += len(batch)
                return True
        except:
            errors += 1
            time.sleep(1)
    return False


def run(path):
    rows = load(path)
    batch = []
    for r in rows:
        batch.append(r)
        if len(batch) == BATCH:
            if not post(batch):
                print("FAILED batch")
            batch = []
    print("sent", sent, "errors", errors)
    return 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1]))
