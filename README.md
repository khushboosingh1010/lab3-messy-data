# Lab 3: Parsing Messy Health and Genomic Data

I used Python for the graduate version of this lab. I worked with both the sample CSV and the FASTA file. I compared regex parsing with AI-assisted extraction and made a sample table for analysis.

## How to run

Use Python 3.10 or newer. No extra packages or API keys are needed. Open a terminal in this folder and run:

```bash
python3 scripts/clean_regex.py
python3 scripts/materialize_ai.py
python3 scripts/compare.py
```

The first command reads both raw files and creates the regex outputs and the analytic sample table. The second saves the AI decisions recorded in the script as CSV files. It does not make a new AI call. The third compares the outputs by record ID and saves the differences and agreement counts.

## Files

| File | What it contains |
| --- | --- |
| `data/raw/messy_samples.csv` | The 60 original sample records |
| `data/raw/messy_sequences.fasta` | The 8 original sequences |
| `data/raw/SOURCE.md` | The instructor's information about the synthetic data |
| `scripts/clean_regex.py` | Regex parsing, checks, and the analytic table |
| `scripts/materialize_ai.py` | Recorded AI field decisions and CSV output |
| `scripts/compare.py` | Comparison by ID and field |
| `outputs/regex_samples.csv` | Sample results from the first regex parser |
| `outputs/regex_sequences.csv` | FASTA results from regex |
| `outputs/ai_samples.csv` | AI-assisted sample results |
| `outputs/ai_sequences.csv` | AI-assisted FASTA results |
| `outputs/analytic_samples.csv` | One row per sample, with reviewed birth dates |
| `outputs/differences.csv` | Every difference in the compared fields |
| `outputs/comparison_summary.json` | Agreement counts |
| `COMPARISON.md` | My comparison and readiness notes |
| `AI_USAGE.md` | AI help and prompts |

## Cleaning choices

Dates use `YYYY-MM-DD`. Sex uses `Male`, `Female`, or a blank value. I kept a flag to show whether a blank came from an empty field or an unknown value. Sites use `Site A`, `Site B`, and `Site C`. Glucose uses mg/dL. The conversion is mmol/L × 18.0182. I kept the original values and flags so the cleaning can be checked.

The first regex output keeps Python's default two-digit-year results, including six future birth dates, to show the problem in the comparison. The analytic table fixes those six dates using the possible birth years in the supplied generator and marks the correction. These dates would need confirmation if this were real data.

FASTA results keep both the header length and the counted sequence length. Missing header lengths stay blank. I did not change a sequence to make it match its header.

## Source and repository

These are instructor-created synthetic data, with no real patient information. I kept one copy of each raw dataset. The generator was used to understand the date formats and possible birth years; it is not needed to run the lab. The root `.gitignore` excludes common temporary and local files. Submit the link to the public GitHub repository after uploading this folder's contents.

During checking, the supplied generator reproduced the FASTA text but did not reproduce the uploaded sample CSV in this environment. I used the uploaded CSV as the input and did not replace it with generated data. The generator's birth-year range supports the century rule, but it is not a record-by-record answer key for this upload.
