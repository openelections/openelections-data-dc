import csv
import re

results = []
precinct_ward_mapping = {}

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
    if 'Registration' in row[0] or 'Turnout' in row[0]:
        pass
    elif 'Precinct' in row[0]:
        precinct = re.findall('\d+', row[0])[0]
        # turnout is listed first, this filters that out
        office = 'turnout'
    elif 'PRESIDENT' in row[0]:
        office = 'president'
    elif 'DELEGATE' in row[0]:
        office = 'delegate'
    elif 'MEMBER OF THE COUNCIL' in row[0]:
        office = 'council'
    elif 'BOARD OF EDU' in row[0]:
        office = 'board of education'
    elif 'UNITED STATES REPRESENTATIVE' in row[0]:
        office = 'shadow senator'
    else:
        if office == 'turnout':
            return (precinct, office)
        if '-' in row[0]:
            candidate = row[0][5:]
            party = row[0][:3]
        elif 'Total' in row[0]:
            candidate = 'Total'
            party = ''
        elif 'Write In' in row[0]:
            candidate = 'Write in'
            party = ''
        else:
            candidate = row[0]
            party = ''
        if office == 'delegate':
            district = 'At Large'
        else:
            district = ''
        results.append({
            'precinct': precinct,
            'office': office,
            'candidate': candidate,
            'party': party,
            'votes': row[1],
            'ward': precinct_ward_mapping[precinct],
            'district': district,
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
    fieldnames = [
        'ward', 'precinct', 'office', 'district',
        'party', 'candidate', 'votes',
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for r in results:
        writer.writerow(r)
