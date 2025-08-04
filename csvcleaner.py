import csv

with open('contacts.csv', 'r') as file:
  reader = csv.reader(file)
  header = next(reader)
  cleaned_contacts = []
  for row in reader:
    if len(row) == 3 and all(cell.strip() for cell in row):
      cleaned_contacts.append(row)
      print(row)

with open('cleaned_contacts.csv', 'w', newline='') as out_file:
  writer = csv.writer(out_file)
  writer.writerow(header)
  counter = 0
  for row in cleaned_contacts:
      writer.writerow(row)
      counter += 1

print('Cleaned', counter)

