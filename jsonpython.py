import json

user = {"username": "john_doe", "email": "john@example.com", "age": 30, "is_active": True}

with open('user.json', 'w') as file:
  json.dump(user, file)

with open('user.json', 'r') as file:
  user = json.load(file)
  print(user["username"])