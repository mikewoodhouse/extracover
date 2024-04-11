from datetime import datetime
from pathlib import Path

from app.ingest.classes import Match

count = 0

started = datetime.now()
print(datetime.now() - started, count)

for p in Path("matches").glob("**/*.json"):
    if "T20" in str(p):
        count += 1
        if count % 1_000 == 0:
            print(datetime.now() - started, count)
        try:
            m = Match.from_json(p.read_text())
        except Exception as e:
            print(p, e)
print(datetime.now() - started, count)
