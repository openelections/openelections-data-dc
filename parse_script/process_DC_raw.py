'''
This works for the 2004 results in python 2 or 3.
Pass in precinct, ward or general to parse respective raw files.
'''

import csv
import re
import sys

results = []
precinct_ward_mapping = {None: ''}

if sys.argv[1] == 'precinct':
    ward_file = 'precinct_ward_mapping_2002_2011.csv'
    input_file = '2004/DC_raw_precinct.csv'
    output_file = '../2004/20041102__dc__general__precinct.csv'
    fieldnames = ['ward', 'precinct', 'office', 'district', 'party', 'candidate', 'votes']

    with open(ward_file, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            precinct_ward_mapping[row[0]] = row[1]

if sys.argv[1] == 'ward':
    input_file = '2004/DC_raw_ward.csv'
    output_file = '../2004/20041102__dc__general__ward.csv'
    fieldnames = ['ward', 'office', 'district', 'party', 'candidate', 'votes']

if sys.argv[1] == 'general':
    input_file = '2004/DC_raw_general.csv'
    output_file = '../2004/20041102__dc__general.csv'
    fieldnames = ['office', 'district', 'party', 'candidate', 'votes']


def include_record(text):
    '''
    Don't record lines that are not votes
    '''
    for item in ['Registration', 'Turnout', 'Completed Precincts', 'Under Votes', 'Over Votes']:
        if item in text:
            return(False)
    return(True)


def append_record(precinct, office, ward, candidate, party, district, votes):
    office = office.upper()
    if sys.argv[1] == 'precinct':
        results.append({
            'precinct': precinct, 'office': office, 'candidate': candidate,
            'party': party, 'votes': votes, 'ward': ward, 'district': district,
        })
    if sys.argv[1] == 'ward':
        results.append({
            'office': office, 'candidate': candidate, 'party': party, 'votes': votes,
            'ward': ward, 'district': district,
        })
    if sys.argv[1] == 'general':
        results.append({
            'office': office, 'candidate': candidate, 'party': party, 'votes': votes,
            'district': district,
        })


def parse_record(row, precinct, office, ward):
    """
    Keeps track of the information that is stored as headings
    by updating the variable. Adds vote tally to results.
    """
    if include_record(row[0]) is False:
        return(precinct, office, ward)
    elif 'Precinct' in row[0]:
        precinct = re.findall('\d+', row[0])[0]
        ward = precinct_ward_mapping[precinct]
        office = 'turnout'
    elif 'City of Washington Ward' in row[0]:
        precinct = None
        ward = 'Ward ' + str(re.findall('\d+', row[0])[0])
        office = 'turnout'
    elif 'City of Washington Ward' in row[0]:
        precinct = None
        ward = 'Ward ' + str(re.findall('\d+', row[0])[0])
        office = 'turnout'
    elif 'PRESIDENT' in row[0]:
        office = 'president'
    elif 'DELEGATE' in row[0]:
        office = 'delegate'
    elif 'MEMBER OF THE COUNCIL' in row[0] or 'BOARD OF EDU' in row[0]:
        office = row[0]
    elif 'UNITED STATES REPRESENTATIVE' in row[0]:
        office = 'shadow senator'
    else:
        if office == 'turnout':
            return(precinct, office, ward)

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
        votes = row[1]
        append_record(precinct, office, ward, candidate, party, district, votes)
        return(precinct, office, ward)
    return(precinct, office, ward)


with open(input_file, "r") as csvfile:
    reader = csv.reader(csvfile)
    precinct = None
    office = None
    ward = None

    for row in reader:
        (precinct, office, ward) = parse_record(row, precinct, office, ward)


with open(output_file, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for r in results:
        writer.writerow(r)
