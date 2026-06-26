import json
import os
import sqlite3
import threading
import time

DB_PATH = os.environ.get("HELI_DB_PATH", "./state/events.sqlite")
_lock = threading.Lock()

def _connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS circling_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            icao TEXT NOT NULL,
            reg TEXT,
            started_ts INTEGER NOT NULL,
            ended_ts INTEGER,
            duration_sec INTEGER,
            centroid_lat REAL,
            centroid_lon REAL,
            neighborhood TEXT,
            trace_json TEXT,
            alt_ft INTEGER,
            posted INTEGER NOT NULL DEFAULT 0,
            post_uri TEXT
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_circling_icao_started ON circling_events(icao, started_ts)")
    return conn

def record_circling_start(icao, reg, centroid_lat, centroid_lon, neighborhood, trace, alt_ft):
    """Writes a new circling_events row at the moment circling is detected, independent of
    whether any notification channel is enabled. Returns the row id to thread through
    record_circling_end/record_post_uri."""
    with _lock:
        conn = _connect()
        try:
            cur = conn.execute(
                "INSERT INTO circling_events (icao, reg, started_ts, centroid_lat, centroid_lon, neighborhood, trace_json, alt_ft) VALUES (?,?,?,?,?,?,?,?)",
                (icao, reg, int(time.time()), centroid_lat, centroid_lon, neighborhood, json.dumps(trace), alt_ft),
            )
            conn.commit()
            return cur.lastrowid
        finally:
            conn.close()

def record_circling_end(event_id, ended_ts=None):
    if event_id is None:
        return
    ended_ts = ended_ts if ended_ts is not None else int(time.time())
    with _lock:
        conn = _connect()
        try:
            conn.execute(
                "UPDATE circling_events SET ended_ts = ?, duration_sec = ? - started_ts WHERE id = ?",
                (ended_ts, ended_ts, event_id),
            )
            conn.commit()
        finally:
            conn.close()

def record_post_uri(event_id, post_uri):
    if event_id is None or post_uri is None:
        return
    with _lock:
        conn = _connect()
        try:
            conn.execute("UPDATE circling_events SET posted = 1, post_uri = ? WHERE id = ?", (post_uri, event_id))
            conn.commit()
        finally:
            conn.close()
