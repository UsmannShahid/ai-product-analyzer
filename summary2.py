import csv

try:
  with open('contacts.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    row_count = 0
    for row in reader:
      row_count += 1
    print('Total number of data rows: ', row_count)

  user_search_column = input('Enter the column you want to search for (e.g. Name, Email): ')
  user_search_keyword = input('Enter the keyword you want to search for: ')

  with open('contacts.csv', 'r') as file:
    reader = csv.reader(file)
    header_row = next(reader)
    header_row_lower = [column.lower() for column in header_row]

    if user_search_column.lower() in header_row_lower:
      column_index = header_row_lower.index(user_search_column.lower())

      match_count = 0
      for row in reader:
        if user_search_keyword.lower() in row[column_index].lower():
          match_count += 1

      print('Found', match_count, 'matches.')

except FileNotFoundError:
  print('File not found. Please try again.')