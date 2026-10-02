"""Compare cleaned fields by ID and write actual disagreements."""
import csv
import json
from clean_regex import OUT

def read(name):
    with (OUT / name).open(newline='') as f:
        return list(csv.DictReader(f))

def main():
    summary = {}
    differences = []
    for kind, key, fields in [
        ('samples', 'sample_id', ['patient_name','dob','sex','enrollment_site','glucose_mg_dl','notes']),
        ('sequences', 'sequence_id', ['organism','gene','declared_length','actual_length','note','sequence'])
    ]:
        regex = read(f'regex_{kind}.csv')
        ai = read(f'ai_{kind}.csv')
        left = {r[key]:r for r in regex}
        right = {r[key]:r for r in ai}
        assert len(left) == len(regex) and len(right) == len(ai), 'Duplicate IDs'
        assert set(left) == set(right), 'IDs do not align'
        counts = {f:0 for f in fields}
        for ident, r in left.items():
            for field in fields:
                if r[field] != right[ident][field]:
                    counts[field] += 1
                    differences.append(dict(dataset=kind, record_id=ident, field=field,
                                            regex_value=r[field], ai_value=right[ident][field]))
        total = len(left) * len(fields)
        summary[kind] = dict(records=len(left), fields_compared=fields,
                             cells_compared=total, matching_cells=total-sum(counts.values()),
                             differences_by_field=counts)
    with (OUT / 'differences.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['dataset','record_id','field','regex_value','ai_value'])
        w.writeheader()
        w.writerows(differences)
    (OUT / 'comparison_summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
