import csv
from collections import Counter

with open('contacts.csv', 'r') as file:
  reader = csv.reader(file)
  next(reader)
  domains = []
  for row in reader:
    email = row[2]
    domain = email.split('@')[1]
    domains.append(domain)
  domain_counts = Counter(domains)
  print(domain_counts)
  