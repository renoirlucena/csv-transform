# csv-transform

Small Python script I wrote to clean up messy customer CSV exports. It normalizes names, fixes phone numbers, dedupes rows, and writes a clean file out.

Built it to solve a real problem at the time. Nothing exciting, just useful.

## What it does

- Trims and title-cases first / last names
- Adds country and area codes to mobile numbers based on city + state lookup
- Drops duplicate phone numbers
- Outputs a tidy `display_name` column

## Run it

```bash
python csv-transform.py
```

Expects three files in `data/`:

- `input_data.csv` — raw export
- `ddd_data.csv` — city / state / area code lookup
- `output_data.csv` — written by the script

## Notes

Single file, no dependencies beyond the standard library. Easy to fork and adapt.
