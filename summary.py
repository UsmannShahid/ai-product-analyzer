#Build a tool that:

#Asks the user for a CSV filename (default to contacts.csv)

#Shows total number of data rows (excluding header)

#Lets user search any column by a keyword

#Bonus: Show how many matches were found

import csv
#Here we are asking the user for CSV filename and if the user does not enter anything, we will default to contacts.csv

  
#Here we are opening the file and reading it and then we are skipping the header row and then we are counting the number of row in the file and then we are printing the total number of data rows.

def load_csv(filename):
  try:
    file = open(filename, 'r')
    reader = csv.reader(file)
    header = next(reader)
    return reader,header,file
  except FileNotFoundError:
    print('File not found.')
    return None,None,None

# Testing file loading and header reading
# reader, header, file = load_csv("contacts.csv")
# print("Header: ", header)
# file.close()

def count_rows(reader):
  row_count = 0
  for row in reader:
    row_count += 1
  return row_count

#Testing row counting
# reader, header, file = load_csv("contacts.csv")
# if reader:
#   total = count_rows(reader)
#   print('Total number of data rows: ', total)
# file.close()
      
# row_count = 0
# for row in reader:
#   row_count += 1

# print('Total number of data rows: ', row_count)

# #Here we are asking the user if they want to search for a keyword in any column and if they say yes, we will ask them for the column name and the keyword and then we will search for the keyword in the column and then we will print the row that contains the keyword.
#Function searches for a keyword in a specific column
def search_csv(reader, column_index, keyword):
  matches = []
  for row in reader:
    if column_index < len(row) and keyword.lower() in row[column_index].lower():
      matches.append(row)

  return matches

#Feature to write matched to a new file
def export_matches(matches, header, filename="matches.csv"):
  with open(filename, 'w', newline='') as file:
    write = csv.writer(file)
    write.writerow(header)
    write.writerows(matches)

  print(f"Matches exported to {filename}")


user_filename = input('Enter the CSV filename (default to contacts.csv): ').strip()
if not user_filename:
  user_filename = 'contacts.csv'
  print('Defaulting to contacts.csv')

reader, header, file = load_csv(user_filename)

if reader:
  print("Available columns: ")
  for col in header:
    print("-", col)

  search_col = input("Which column to search?").strip().lower()
  header_lower = [col.lower() for col in header]
  if search_col in header_lower:
    col_index = header_lower.index(search_col)
    keyword = input("Enter the keyword to search for: ").strip().lower()

    file.seek(0)
    reader = csv.reader(file)
    next(reader)

    matches = search_csv(reader, col_index, keyword)
    print(f"Found {len(matches)} matches.")
    for match in matches:
      print(match)

    export = input("Export matches to a new file? (yes/no): ").strip().lower()
    if export == "yes":
      export_matches(matches, header)
      
  else:
      print("Column not found.")
      
if file:
  file.close()

#   user_search_confirmation = input('Do you want to search for a keyword in any column? (yes/no): ').lower()

#   if user_search_confirmation == 'yes':
#     user_search_column = input('Enter the column you want to search for (e.g. Name,Email): ').lower()
#     user_search_keyword = input('Enter the keyword you want to search for: ').lower()

#     with open(user_filename, 'r') as file:
#       reader = csv.reader(file)
#       header_row = next(reader) # Reads the first line (column names)
#       print("Available columns: ")
#       for column in header_row:
#         print("-", column)

#       header_row_lower = [column.lower() for column in header_row] # Converts all column names to lowercase for case-insensitive search
#       if user_search_column in header_row_lower:
#         column_index = header_row_lower.index(user_search_column)
  
#         match_count = 0
#         for row in reader:
#           if user_search_keyword.lower() in row[column_index].lower():
#             print(row)
#             match_count += 1
#         print("Found", match_count, "matches.")
#       else:
#         print("Column not found.")


# except FileNotFoundError:
#   print('File not found. Please try again.')


