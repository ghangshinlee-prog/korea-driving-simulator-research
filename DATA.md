# Data Availability

The raw eye-tracking data are **not committed** (human-subjects records held
under the original lab/IRB terms). The pipeline reads from `$DATA_DIR`.

| File (under `$DATA_DIR`) | Content |
|---|---|
| `vision_workload_events.tsv` | Fixation/saccade events: pupil diameter, fixation duration/location, saccade velocity & amplitude, with participant, age group, gender, road segment, scenario |

## Study design
- **Apparatus:** UC-win/Road driving simulator + Tobii Pro Glasses eye-tracker.
- **Measures developed (M.S. thesis):** pupil diameter, Index of Cognitive
  Activity (ICA), fixation duration, saccade velocity/amplitude.
- **Participants:** 66 drivers, age groups 30s / 40s / 50s, both genders.

## Published study (not in this repo)
The black-ice warning-sign experiment is published open-access:
Lee, G., Hwang, S., & Lee, D. (2022). *Improvements of Warning Signs for Black
Ice Based on Driving Simulator Experiments.* IJERPH 19(12), 7549.
https://doi.org/10.3390/ijerph19127549

## Included here
- M.S. thesis PDF (`docs/`)
- Analysis pipeline (`analysis/`)
- Derived, aggregated result tables (`results/`) — no individual raw records
- Generated figures (`figures/`)
