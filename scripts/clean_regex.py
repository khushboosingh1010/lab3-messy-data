"""Regex parsing with explicit quality flags; Python standard library only."""
import csv
import re
from datetime import datetime, date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs'
OUT.mkdir(exist_ok=True)

def write(name, rows):
    with (OUT / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def raw_samples():
    with (ROOT / 'data/raw/messy_samples.csv').open(newline='') as f:
        return list(csv.DictReader(f))

def fasta():
    records = []
    for line in (ROOT / 'data/raw/messy_sequences.fasta').read_text().splitlines():
        if line.startswith('>'):
            records.append([line[1:], ''])
        elif line.strip():
            records[-1][1] += line.strip().upper()
    return records

def sample_row(raw, dob, sex, site, sid):
    flags = []
    if not dob:
        flags.append('unparsed_date')
    elif dob > '2026-10-02':
        flags.append('future_dob')
    if re.fullmatch(r'\d{2}\.\d{2}\.\d{2}', raw['dob']):
        flags.append('two_digit_year_review')
    if not sex:
        flags.append('sex_missing' if not raw['sex'] else 'sex_unknown')
    value = raw['glucose_value']
    match = re.fullmatch(r'(\d+(?:\.\d+)?)(\*)?', value.strip())
    unit = raw['glucose_unit'].lower()
    glucose = ''
    if match and unit in ('mg/dl', 'mmol/l'):
        glucose = round(float(match[1]) * (18.0182 if unit == 'mmol/l' else 1), 3)
        if match[2]:
            flags.append('asterisk_annotation')
        if unit == 'mmol/l' and float(match[1]) > 30:
            flags.append('source_value_unit_review')
    else:
        flags.append('glucose_missing_or_unparsed')
    if raw['notes']:
        flags.append('source_note_review')
    return dict(sample_id=sid, patient_name=raw['patient_name'].title(), dob=dob,
                sex=sex, enrollment_site=site, glucose_mg_dl=glucose,
                raw_dob=raw['dob'], raw_sex=raw['sex'],
                raw_glucose_value=value, raw_glucose_unit=raw['glucose_unit'],
                notes=raw['notes'], quality_flags=';'.join(flags))

def sequence_row(header, sequence, sid, organism, gene, declared, note):
    flags = []
    if declared == '':
        flags.append('header_length_missing')
    elif int(declared) != len(sequence):
        flags.append('header_length_mismatch')
    if not re.fullmatch('[ACGT]+', sequence):
        flags.append('non_acgt_sequence')
    return dict(sequence_id=sid, organism=organism, gene=gene,
                declared_length=declared, actual_length=len(sequence), note=note,
                sequence=sequence, raw_header=header, quality_flags=';'.join(flags))

def main():
    rows = []
    formats = [(r'\d{4}-\d{2}-\d{2}', '%Y-%m-%d'),
               (r'\d{2}/\d{2}/\d{4}', '%m/%d/%Y'),
               (r'\d{2}-[A-Za-z]{3}-\d{4}', '%d-%b-%Y'),
               (r'\d{2}\.\d{2}\.\d{2}', '%m.%d.%y')]
    for r in raw_samples():
        dob = ''
        for pattern, fmt in formats:
            if re.fullmatch(pattern, r['dob']):
                try:
                    dob = datetime.strptime(r['dob'], fmt).date().isoformat()
                except ValueError:
                    pass
                break
        sex = {'m':'Male','male':'Male','f':'Female','female':'Female'}.get(r['sex'].lower(), '')
        site = re.sub(r'[\s_-]', '', r['enrollment_site']).lower()
        site = {'sitea':'Site A','siteb':'Site B','sitec':'Site C'}.get(site, '')
        sid = re.fullmatch(r'[sS]-?(\d+)', r['sample_id'])
        rows.append(sample_row(r, dob, sex, site, f'S{int(sid[1]):04d}'))
    write('regex_samples.csv', rows)
    analytic = []
    for r in rows:
        a = {k:r[k] for k in ('sample_id','glucose_mg_dl','dob','sex','enrollment_site','notes','quality_flags')}
        # Review step based on the supplied generator's birth-year range.
        # Preserve the original parser result separately for comparison.
        if 'future_dob' in a['quality_flags'] and re.fullmatch(r'\d{2}\.\d{2}\.\d{2}', r['raw_dob']):
            a['dob'] = str(int(a['dob'][:4]) - 100) + a['dob'][4:]
            a['quality_flags'] = a['quality_flags'].replace('future_dob', 'dob_century_reviewed')
        analytic.append(a)
    write('analytic_samples.csv', analytic)
    sequences = []
    for h, s in fasta():
        ident = re.match(r'(?:sample|seq)[_-]?(\d+)', h, re.I)
        gene = re.search(r'\b(BRCA1|TP53|EGFR)\b', h)
        organism = 'Homo sapiens' if re.search(r'Homo[ _]sapiens|H\.?sapiens', h, re.I) else ''
        length = re.search(r'(?:len(?:gth)?\s*[=:]\s*|[;]\s*)(\d+)\s*(?:bp)?', h, re.I)
        note = re.search(r'note\s*[=:]\s*([^|;]+)', h)
        sequences.append(sequence_row(h, s, f'sample_{int(ident[1]):03d}', organism,
                                      gene[1] if gene else '', int(length[1]) if length else '',
                                      note[1] if note else ''))
    write('regex_sequences.csv', sequences)

if __name__ == '__main__':
    main()
