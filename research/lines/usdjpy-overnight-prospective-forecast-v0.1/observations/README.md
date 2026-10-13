# USD/JPY Live Market State Journal

This directory stores append-only point-in-time observations under `OBS-USDJPY-LIVE-STATE-001-v01`.

## Operating cadence

Default:

- 08:30 JST — MORNING_STATE
- 15:00 JST — TOKYO_CLOSE_STATE
- 21:30 JST — PRE_FORECAST_STATE
- EVENT_DRIVEN when a material event occurs
- MANUAL for explicit ad-hoc checks

## File naming

Use:

`YYYYMMDDTHHMMSS+0900_<CHECKPOINT_TYPE>.json`

Example:

`20261005T083000+0900_MORNING_STATE.json`

Never replace an older state file.

Corrections are new files with `checkpoint_type = CORRECTION` and `corrects_state_id` set.

## Scientific boundary

These files are observations, not scored forecast results.

They may motivate a separately versioned challenger but cannot rewrite:

- frozen weekly forecasts;
- frozen overnight forecasts;
- historical source snapshots;
- prior journal entries.

For scored forecasts, trace any material journal fact back to the underlying point-in-time source artifact.
