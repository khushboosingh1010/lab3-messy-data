# My Lab 3 comparison

## What I compared

I worked with all 60 sample records and all 8 sequences. For the samples, I compared patient name, birth date, sex, site, glucose in mg/dL, and notes. For FASTA, I compared organism, gene, header length, actual length, note, and sequence. The comparison script matches records by ID. It does not count the raw fields or quality flags as separate agreement checks.

## Agreement and differences

| Dataset | Records | Matching field values | Different field values |
| --- | ---: | ---: | ---: |
| Samples | 60 | 354 of 360 (98.3%) | 6 |
| Sequences | 8 | 48 of 48 (100%) | 0 |

All six sample differences were birth dates: S0003, S0011, S0014, S0025, S0026, and S0043. Names, sex, sites, glucose, and notes matched. All compared FASTA fields matched, including the missing header lengths and the re-sequenced note for sample_007.

I would not treat these percentages as proof that everything is correct. The AI script and regex script share the glucose conversion and sequence-counting code. Those matches show consistent output, but they do not independently test those steps. Both methods can also agree on a source value that needs review.

## Specific problems and edge cases

**1. S0003: the birth date `11.24.53`.** The first regex parser returned `2053-11-24`. The AI extraction returned `1953-11-24`. The regex matched the format, but Python's default short-year rule interpreted 53 as 2053. The supplied generator starts birth dates in 1950 and adds at most 25,000 days, so 1953 fits that range. The same issue affected five other records. The regex flags the future dates; the analytic table changes these six centuries and records the review. For real records, I would confirm the century instead of relying on this synthetic-data rule.

**2. sample_003: header length versus actual length.** The header says `length=150bp`, but the sequence has 157 bases. Both methods kept 150 as the declared length, counted 157 as the actual length, and flagged the mismatch. Extracting the header alone would miss this problem. I cannot tell from this file whether the sequence or the header should change.

**3. sample_005: another length mismatch.** Its header says `130 bp`, but the sequence has 144 bases. Both methods found this. The header has no `len=` key, so a regex that only searched for that key would miss the stated length. Missing lengths, such as `len:NA` in sample_008, stay blank rather than being replaced with a guessed header value.

**4. S0039: `241.2*` with unit mmol/L.** Both methods remove the star from the numeric value but keep an annotation flag. The stated-unit conversion gives 4345.990 mg/dL. That result is unusually high and needs source review. The generator randomly assigns units without changing the numeric scale, which helps explain the problem in this synthetic file. I still kept the stated unit rather than silently treating it as mg/dL. All 13 mmol/L records are flagged for value/unit review.

The AI extraction handled the short-year century issue better with the generator as context. Both methods handled the mixed IDs, sex codes, site spellings, header styles, and missing lengths. The actual-length check was useful, but it came from shared deterministic code rather than an AI judgment.

## Time, effort, and which approach I would trust

I did not record separate times, so I cannot give a fair number of minutes for each method. AI made it easier to draft the extraction decisions and explain the unusual records. Regex required clear rules for each format, but those rules can be inspected and run again. Both approaches needed checking; I cannot claim one was faster to get right from a measured test.

For a real dataset, I would use a reviewed script for repeatable cleaning and AI to help identify unusual cases. I would check dates, units, and sequence lengths against the source before analysis. I would not accept an AI answer just because it looks reasonable.

## Graduate addendum: samples × features × metadata

I made `outputs/analytic_samples.csv` from the regex sample output, with the six century corrections described above. It has 60 rows, one per sample, and 7 columns. `sample_id` is the row key, `glucose_mg_dl` is the numeric feature, and birth date, sex, site, notes, and quality flags are metadata. There is no separate metadata file to join; the original sample file already contains those fields.

| sample_id | glucose_mg_dl | dob | sex | enrollment_site |
| --- | ---: | --- | --- | --- |
| S0001 | 145.9 | 1962-07-09 | Female | Site B |
| S0002 | 146.1 | 1974-12-16 | Male | Site C |
| S0003 | 84.2 | 1953-11-24 | Female | Site B |

The file also contains `notes` and `quality_flags`. Blank sex values are kept for all 18 missing or unknown records, with flags showing the reason. No sample is dropped.

Glucose is in one unit and dates use one format, but CSV does not enforce types, so I would load glucose as numeric and birth date as a date before modeling. I still need to confirm the flagged glucose units, short-year dates, stars, and re-draw notes, and choose how to handle missing or unknown sex. This table has a useful analysis shape, but it is not ready for modeling without those decisions.
