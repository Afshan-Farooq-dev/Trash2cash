import sqlite3
import json
import sys

DB='e:/Updated FYP/Traffic/db.sqlite3'
try:
    conn=sqlite3.connect(DB)
    cur=conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables=[r[0] for r in cur.fetchall()]
    print(json.dumps(tables, indent=2))
except Exception as e:
    print('ERROR:', e)
    sys.exit(1)
finally:
    try:
        conn.close()
    except:
        pass
