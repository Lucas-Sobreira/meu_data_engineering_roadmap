import csv

path:str = './exemplo.csv'

archive_csv:list = []

with open(file = path, mode = 'r', encoding = 'utf-8') as archive:
    read_csv:csv.DictReader = csv.DictReader(archive)
 
    for line in read_csv: 
        archive_csv.append(line)

print(archive_csv)