import csv
import re

results = []
precinct_ward_mapping = {}
office_district_map = {'president': '', 'delegate': 'At Large'}

precint_ward_file = 'precinct_ward_mapping_2002_2011.csv'
output_file = '../2004/20041102__dc__general__precinct.csv'


with open(precint_ward_file, "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        precinct_ward_mapping[row[0]] = row[1]


def parse_record(row, precinct, office):
    """
    Keeps track of the information that is stored as headings
    by updating the variable. Adds vote tally to results.
    """
    if 'Total' in row[0] or 'Registration' in row[0] or 'Turnout' in row[0]:
        pass
    elif 'Precinct' in row[0]:
        precinct = re.findall('\d+', row[0])[0]
    elif 'PRESIDENT' in row[0]:
        office = 'president'
    elif 'DELEGATE' in row[0]:
        office = 'delegate'
    else:
        if 'Write In' in row[0]:
            party = ''
            candidate = 'Write in'
        else:
            candidate = row[0][5:]
            party = row[0][:3]
        results.append({
            'precinct': precinct,
            'office': office,
            'candidate': candidate,
            'party': party,
            'votes': row[1],
            'ward': precinct_ward_mapping[precinct],
            'district': office_district_map[office],
        })
        return (precinct, office)
    return (precinct, office)


with open("DC_RAW.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    precinct = None
    office = None

    for row in reader:
        (precinct, office) = parse_record(row, precinct, office)


with open(output_file, 'w') as csvfile:
    fieldnames = ['ward', 'precinct', 'office', 'district', 'party', 'candidate', 'votes']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for r in results:
        writer.writerow(r)
