# Research: Identifying the Columbus Division of Police helicopter fleet

Last updated: 2026-06-26

This is a living document, same purpose as the sibling jet-tracking project's
`RESEARCH.md` - record the identification evidence chain and update it as the
fleet changes (CPD has been actively modernizing this fleet in 2025-2026).

## Why this project

Columbus Division of Police operates an aviation unit (~21 pilots, ~5,000
calls for service a year, ~$2.1M/year in maintenance/fuel/insurance per
[WOSU](https://www.wosu.org/politics-government/2025-06-24/columbus-to-purchase-two-new-helicopters-for-6-million-while-other-cities-buy-cheaper-drones))
flying daily patrol over the city. Unlike the jet-tracking project, this
fleet's purpose for tracking isn't "where did a person go" - it's "is a
police helicopter circling/loitering over a neighborhood right now," a
police-air-support transparency signal, with an eventual goal of
frequency/duration/cost/per-neighborhood analytics.

## Fleet identification

Unlike the jet-tracking project, ownership here is **not** obscured by a
trust/shell company - everything is registered directly to a real government
entity, so this was a direct FAA registry lookup by known N-number rather
than a multi-step disambiguation problem.

**Starting point (public sources):**
- [helis.com's CPD fleet roster](https://www.helis.com/database/sqd/Columbus-Police-Department/cn)
  listed N551CP, N552CP, N553CP, N554CP, N556CP, N557CP, N558CP, N559CP
  across MD500E/MD530F and (historically) OH-58A Kiowa airframes, the
  Kiowas now written off/cancelled.
- News coverage ([Bell Newsroom](https://news.bellflight.com/en-CA/252269-columbus-division-of-police-adds-two-bell-505s-to-aviation-section/),
  [WOSU](https://www.wosu.org/politics-government/2025-06-24/columbus-to-purchase-two-new-helicopters-for-6-million-while-other-cities-buy-cheaper-drones))
  confirmed two new Bell 505s were added to the fleet around early-to-mid
  2026, but didn't name their N-numbers directly.

**FAA registry lookup (2026-06-26), `registry.faa.gov/database/ReleasableAircraft.zip`
-> `MASTER.txt`, looked up directly by each candidate N-number (no
disambiguation needed - contrast with the jet project's trust-company
problem):**

| N-Number | ICAO24 Hex | Registrant | Model | Notes |
|---|---|---|---|---|
| N551CP | `A70362` | CITY OF COLUMBUS | MD Helicopters 369FF (MD530F) | |
| N552CP | `A70719` | CITY OF COLUMBUS OHIO | Bell 505 | One of the two new Bell 505s - identified via FAA model code `1182166` = Bell Textron Canada 505, not from a secondary source |
| N553CP | `A70AD0` | CITY OF COLUMBUS DIVISION OF POLICE | MD Helicopters 369FF (MD530F) | |
| N556CP | `A715F5` | CITY OF COLUMBUS | MD Helicopters 369FF (MD530F) | |
| N557CP | `A719AC` | CITY OF COLUMBUS | MD Helicopters 369FF (MD530F) | |
| N559CP | `A7211A` | CITY OF COLUMBUS OHIO | Bell 505 | The second new Bell 505 |

**Excluded:** `N558CP` - the FAA registry currently shows this N-number
registered to **Civil Air Patrol**, not CPD. helis.com's historical record
shows N558CP was a CPD MD500E/MD530F, but N-numbers get recycled after
cancellation (helis.com separately notes an earlier N558CP, an OH-58A Kiowa,
was "w/o unk; canc Jan00 as destroyed") - the current live FAA registrant is
authoritative over a possibly-stale third-party roster page. If CPD's
MD530F that used to carry N558CP is still flying, it's now under a different
N-number not yet identified - worth re-checking if a 7th active airframe is
suspected.

**Sanity checks performed:**
- Registrant addresses for both Bell 505s (N552CP, N559CP) and N551CP read
  "77 N FRONT ST FL 5TH, COLUMBUS, OH" and "120 MARCONI BLVD, COLUMBUS, OH"
  respectively - both are genuine City of Columbus government addresses
  (City Hall and the Public Safety building area), not a coincidental
  same-name match.
- Confirmed the FAA model-code field for each (`3030002` = MD Helicopters
  369FF, `1182166` = Bell Textron Canada 505) matches the expected airframe
  types from news coverage.

## ADS-B visibility

`N551CP` has a real, dated [FlightAware tracklog](https://www.flightaware.com/live/flight/N551CP/history/20260116/0530Z/OH52/OH52/tracklog)
from a January 2026 flight, round-trip from an identifier "OH52" (likely
their home heliport - a state-assigned identifier pattern typical of small
fields/heliports not in the main ICAO system). This confirms the fleet does
broadcast position data capturable by public ADS-B trackers like
airplanes.live, the same source already proven working for the jet-tracking
project. No CPD helicopter was airborne during a live spot-check on
2026-06-26 (4-5 aircraft total within 15nm of downtown Columbus, none CPD) -
expected, since this fleet flies on-call/patrol rather than continuously.

## Neighborhood data (for circling-location messages and future analytics)

The City of Columbus publishes an official neighborhood/community boundary
dataset, "Columbus Communities," as GeoJSON via
[opendata.columbus.gov](https://opendata.columbus.gov/datasets/columbus-communities/about).
Used for reverse-geocoding a circling event's centroid into a neighborhood
name - see `defNeighborhood.py`.

## Open items to revisit

- [ ] Re-run this FAA lookup periodically (e.g. after local news of a fleet
      change) - this is an actively modernizing fleet, not a static target.
- [ ] If a 7th active airframe is ever suspected (the N558CP gap above),
      look it up by serial number continuity rather than N-number guessing.
- [ ] `N554CP` (per helis.com, active May 2008-2017, no end-of-life noted)
      wasn't included above - the FAA registry should be re-checked for it
      specifically if it's still believed active; omitted here because no
      recent news/roster source described it as currently in service.
