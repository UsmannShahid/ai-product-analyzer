#Let the user view all contacts
#Search for a contact by name
#Add a new contact
#Exit the program

#How do you view all contacts --- by reading the file
#How do you search for a contact by name --- by asking user for name using input and matching input to the name in the file. We can use dictinary to store the name and phone number.
#How to add a new contact --- using write function to add new contact to the file
#How to exit the program --- using break statement to exit the loop

#Set up the CSV file
import csv

try:
    with open('contacts.csv', 'r') as file:
        
        print('File opened successfully')

except FileNotFoundError:
    with open('contacts.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Phone Number', 'Email'])
        print('File created successfully')
      
#While loop for the menu
while True:
  print('1. View all contacts')
  print('2. Search for a contact by name')
  print('3. Add a new contact')
  print('4. Exit the program \n')

  user_input = input('\n Enter your choice: ')

# View all contacts
  if user_input == '1':
    with open('contacts.csv', 'r') as file:
      reader = csv.reader(file)
      next(reader)
      for row in reader:
        print("Name: ", row[0], "Phone Number: ", row[1], "Email: ", row[2])
        
  elif user_input == '2':
    user_input_name = input('Enter the name of the contact you want to search for: ').lower()
    with open('contacts.csv', 'r') as file:
      reader = csv.reader(file)
      
      next(reader)
      found = False

      for row in reader:
        if row[0].lower() == user_input_name:
          print("Name: ", row[0], "Phone Number: ", row[1], "Email: ", row[2])
          found = True

      if not found:
        print('Contact not found \n')

  elif user_input == '3':
    new_contact = input("Enter the new contact's name, phone number, and email separated by commas: ")
    parts = [item.strip() for item in new_contact.split(',')]
    if len(parts) == 3 and all(parts):
      with open('contacts.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(new_contact.split(','))
        print('Contact added successfully \n')
    else:
      print('Invalid input. Please enter the contact details in the correct format.')

  elif user_input == '4':
    print('Goodbye!')
    break
        