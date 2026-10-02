"""Serialize ChatGPT's recorded field decisions; does not call an AI API.

Date/sex/site and header decisions below were extracted separately from the
raw text. Shared helpers only format rows, convert units, and calculate flags.
"""
from clean_regex import raw_samples, fasta, sample_row, sequence_row, write

# Order matches the 60 source records. Blank sex means missing or unknown.
# Short years use the generator's possible birth-year range (1950–2018).
DECISIONS = '''
1962-07-09,Female,B
1974-12-16,Male,C
1953-11-24,Female,B
1957-02-27,Female,B
1997-12-02,Male,B
1968-12-05,Female,C
1969-09-04,,A
1999-08-20,Female,C
1995-07-19,Male,C
1951-10-01,Female,C
1961-07-09,Male,A
1996-06-07,,A
1952-10-26,Female,B
1958-09-12,Female,B
1998-02-11,Male,B
1958-05-15,,B
2015-07-16,,A
1957-03-10,Female,B
2000-09-16,Male,A
2000-07-05,Female,B
2004-11-16,Male,C
2006-11-25,,A
1999-06-30,Male,A
1953-07-31,Female,C
1965-11-19,Male,A
1953-06-22,Female,A
1956-03-24,Female,C
1988-12-26,Female,B
2009-08-04,Female,C
1984-01-06,Male,B
1995-11-11,Male,C
1992-08-17,,B
2012-06-07,Male,B
1995-04-15,,A
1956-12-13,Female,A
1987-04-21,,C
2015-11-28,,A
1997-12-02,,B
1980-04-12,Male,C
2008-06-21,Male,A
1965-01-20,Male,A
2006-04-10,Female,C
1951-02-19,,A
1998-04-13,,B
1984-01-01,Male,B
1967-02-21,Female,C
1977-06-21,,B
1978-04-23,Male,A
1966-02-05,Male,C
2001-07-02,,B
2011-08-02,Male,A
1989-09-20,,A
1999-07-10,Male,A
2006-01-28,,A
2011-10-14,,A
2010-06-30,Male,B
1986-08-20,Female,C
1972-08-23,Female,C
1968-04-06,Male,A
1970-02-27,,A
'''.strip().splitlines()

HEADERS = [
    ('sample_001', 'Homo sapiens', 'BRCA1', 120, ''),
    ('sample_002', 'Homo sapiens', 'TP53', '', ''),
    ('sample_003', 'Homo sapiens', 'EGFR', 150, ''),
    ('sample_004', 'Homo sapiens', 'BRCA1', '', ''),
    ('sample_005', 'Homo sapiens', 'TP53', 130, ''),
    ('sample_006', 'Homo sapiens', 'EGFR', '', ''),
    ('sample_007', 'Homo sapiens', 'BRCA1', '', 're-sequenced'),
    ('sample_008', 'Homo sapiens', 'TP53', '', ''),
]

def main():
    raw = raw_samples()
    assert len(raw) == len(DECISIONS)
    rows = []
    for i, (r, decision) in enumerate(zip(raw, DECISIONS), 1):
        dob, sex, site = decision.split(',')
        rows.append(sample_row(r, dob, sex, 'Site ' + site, f'S{i:04d}'))
    write('ai_samples.csv', rows)
    records = fasta()
    assert len(records) == len(HEADERS)
    write('ai_sequences.csv', [sequence_row(h, s, *d) for (h, s), d in zip(records, HEADERS)])

if __name__ == '__main__':
    main()
