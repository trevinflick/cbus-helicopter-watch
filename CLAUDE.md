# CLAUDE.md

This is a fork of [plane-notify](https://github.com/Jxck-S/plane-notify),
sharing its hardened infrastructure with a sibling project (a private-jet
Bluesky tracker), but tracking a different fleet for a different purpose:
Columbus Division of Police's helicopters, posting when one is **circling**
an area. See [RESEARCH.md](RESEARCH.md) for the fleet-identification
evidence chain and current status.

## Operating principles for this fork

- This tracks **circling/loitering events only**, using publicly broadcast
  ADS-B data - not takeoff/landing (deliberately out of scope, see Phase 1
  notes below). Don't re-enable takeoff/landing posting on a helicopter
  config without discussing it first.
- Posts go out **in real time, no delay** - a deliberate choice (community
  situational awareness over operational-security caution), different from
  the jet-tracking sibling project's `DELAY_MINS`. Don't add a delay back in
  without discussing it; equally, don't assume this choice generalizes to
  any future aircraft tracked from this codebase.
- Every circling detection writes a row to the SQLite event log
  (`dataLog.py`) **regardless of whether any social channel is enabled** -
  this is intentional, so future analytics (frequency, duration, cost,
  per-neighborhood heatmaps) are a query problem against existing data, not
  a data-collection retrofit. Don't gate the DB write behind a channel's
  `ENABLE` flag.
- `configs/*.ini` is gitignored - real credentials must only ever live
  there, never in `*.ini.example` files or committed anywhere else.
- This fleet's ownership is **not** obscured by a trust/shell company (it's
  registered directly to the City of Columbus) - the identification bar here
  is "is this aircraft still actively flying for CPD," not "who really owns
  this," since the fleet is being actively modernized (Bell 505s added in
  2026, older airframes retired). Re-check RESEARCH.md's open items
  periodically rather than assuming the fleet list is static.

## Architecture

- **Entry point:** `__main__.py` - identical to the sibling jet-tracking
  project: reads `configs/mainconf.ini` + every `configs/*.ini` helicopter
  file, loops forever polling the data source, sleeping `[SLEEP] SLEEPSEC`
  seconds between cycles.
- **Event detection:** `planeClass.py`'s `Plane` class, same per-aircraft
  state machine as upstream. Circling detection is the part this fork
  actually relies on, and it has **replaced** upstream's "720 degrees of
  accumulated turning" rule with a loiter test in `loiter.py`: every
  position over the last `CIRCLING_WINDOW_MIN` (5) minutes within
  `CIRCLING_CENTROID_RADIUS_MI` (1.0) of their centroid, plus at least
  `CIRCLING_MIN_TURN_DEG` (180) of turning. At our ~30s sampling a
  helicopter can finish an orbit between samples, so accumulated turning is
  mostly noise, and upstream's 20-minute window let transit legs drag the
  centroid (and the posted neighborhood) across town. The centroid posted
  and stored is from the loiter window only. An event ends when the
  aircraft moves more than 2x the radius away or drops off the feed for 10
  minutes.
- **Data source:** `defAirplanesLive.py` - despite the name, now points at
  adsb.fi's open data API (airplanes.live started returning 403 and requires
  emailed approval). Free, no key, limited to 1 request/second, hence the 2s
  sleep per request. adsb.fi's terms require crediting them with a link,
  which is done via `[MAP] TEXT_CREDIT` and the Bluesky alt text.
- **Notification channels:** same `defX.py` pattern as upstream
  (`sendX(photo, message, config)`), but with one addition specific to this
  fork: each channel's circling dispatch checks `ENABLE_CIRCLING` instead of
  plain `ENABLE`, falling back to `ENABLE` if `ENABLE_CIRCLING` is absent
  (see `Plane._channel_enabled()`). This is what makes "post circling, not
  takeoff/landing" possible per-channel - the takeoff/landing dispatch block
  still checks plain `ENABLE`, which every helicopter config leaves `FALSE`.
- **Neighborhood lookup:** `defNeighborhood.py` reverse-geocodes a circling
  event's centroid into a Columbus neighborhood name via point-in-polygon
  against the city's "Columbus Communities" GeoJSON (auto-downloaded into
  `dependencies/`, same pattern as `airports.csv`). Falls back to the
  existing nearest-airport/heliport phrasing when a point falls outside all
  mapped boundaries.
- **Event log:** `dataLog.py` - a SQLite table (`circling_events`) written
  at the moment circling is detected and updated when it ends, independent
  of social posting. This is the foundation for the future
  frequency/duration/cost/heatmap analytics - see RESEARCH.md and the
  table schema comments for what's already captured.

## Adding/changing a notification channel

Same as upstream: add a `[X]` section to a helicopter's `.ini`, write
`defX.py` with `sendX(photo, message, config)`, wire it into the takeoff/
landing dispatch block (checking plain `ENABLE`) and the circling dispatch
block (checking via `Plane._channel_enabled('X', circling=True)`, not a raw
`ENABLE` check, to keep the circling-only posting model consistent).

## Running locally

```
pipenv install
cp configs/mainconf.ini.example configs/mainconf.ini
cp configs/heli1.ini.example configs/heli_n551cp.ini   # one per helicopter, see RESEARCH.md for ICAO hexes
# edit configs with real ICAO hexes/credentials, then:
pipenv run python __main__.py
```
