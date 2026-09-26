"""Circling/loiter detection over a helicopter's recent position traces.

A trace is (unix_ts, lat, lon, track_change_deg). The aircraft counts as circling when,
over the last window_sec seconds, every position stays within radius_mi of the group's
centroid and it has turned at least min_turn_deg in total. This replaces upstream's
"720 degrees of accumulated turning anywhere in a 20 minute window" check: at our ~30-70s
sampling a helicopter can complete an orbit between samples, so accumulated turning is
mostly aliasing noise, and a 20 minute window let transit legs drag the centroid (and the
posted neighborhood) away from where the helicopter was actually orbiting.
"""
from geopy.distance import geodesic


def recent_traces(traces, now, window_sec):
    return [t for t in traces if now - t[0] <= window_sec]


def detect_loiter(traces, now, window_sec, radius_mi, min_turn_deg):
    """Returns (centroid_lat, centroid_lon, window_traces) if circling, else None."""
    window = recent_traces(traces, now, window_sec)
    # Need enough samples, covering most of the window, to call it sustained.
    if len(window) < 4 or window[-1][0] - window[0][0] < window_sec * 0.6:
        return None
    centroid_lat = sum(t[1] for t in window) / len(window)
    centroid_lon = sum(t[2] for t in window) / len(window)
    if any(geodesic((t[1], t[2]), (centroid_lat, centroid_lon)).mi > radius_mi for t in window):
        return None
    if sum(abs(t[3]) for t in window) < min_turn_deg:
        return None
    return centroid_lat, centroid_lon, window
