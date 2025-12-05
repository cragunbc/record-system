import sqlite3

# Create a database file
conn = sqlite3.connect("practice.db")  # makes a file instead of in-memory
cursor = conn.cursor()
user_input = "" # Defines the user_input variable so that it can be used

# Creates a table called customers if one doesn't exist to begin with
# cursor.execute("""CREATE TABLE customers (
#             first_name text,
#             last_name text,
#             email text
#         )""")

# Prints a welcome statement when using the program
print("\nWelcome to the student record system. Please select an option below:")

# Defines a function called insertItem that will create a SQL command to add a user to the customer table
def insertItem():
    first_name = input("Enter a first name: ").title() # Gets the first name of the user and stores it in the first_name variable
    last_name = input("Enter a last name: ").title() # Gets the last name of the user and stores it in the last_name variable
    email = input("Enter an email: ").lower() # Gets the email of the user and stores it in the email variable
    cursor.execute("INSERT INTO customers VALUES (?, ?, ?)", (first_name, last_name, email)) # Populates the values from the user and sends it to the database

    print(f"\nYour user of {first_name} {last_name} has been entered successfully!") # Prints statement saying that the user you entered was successfully added

    conn.commit() # Commits the code to be executed


# Function to display all of the contents of the database
def displayAllContents():
    cursor.execute("SELECT rowid, * FROM customers") # Pulls everything from the database
    items = cursor.fetchall() # Stores all of the items from the query into a variable

    id_header = "ID:" # Sets the value of "ID:" to the id_header variable
    first_header = "First Name:" # Sets a value of "First Name:" to the first_header variable
    last_header = "Last Name:" # Sets a value of "Last Name:" to the last_header variable
    email_header = "Email:" # Sets a value of "Email:" to the email_header variable

    id_width = 5 # Defines a width of the id column
    first_width = 15 # Defines a width of the first_name column
    last_width = 15 # Defines a width of the last_name column
    email_width = 30 # Defines a widht of the email column

    # Prints out a header for all of the user info
    print("\nHere's all of the info for all of your users:\n")

    # Prints out the header info for the items in the foor loop
    print(f"""{id_header}{' ' * (id_width - len(id_header) + 1)}{first_header}{' ' * (first_width - len(first_header) + 1)}{last_header}{' ' * (last_width - len(last_header) + 1)}{email_header}{' ' * (email_width - len(email_header))}""")
    # Prints out breaker lines for each of the headers
    print("-" * id_width + " " + "-" * first_width + " " + "-" * last_width + " " + "-" * email_width)

    for item in items: # Loops through the items using a for loop and prints out the info
        # Prints out head item by the index of where it falls in the list
        print(f"{item[0]}{' ' * (id_width)}{item[1]}{' ' * (first_width - len(item[1]) + 1)}{item[2]}{' ' * (last_width - len(item[2]) + 1)}{item[3]}{' ' * (email_width - len(item[3]))}")


def updateUser():
    displayAllContents()
    try:
        user_id = int(input("\nEnter the ID of the user that you want to change: "))
    except ValueError:
        print("Please enter a valid ID number")
        return

    cursor.execute("SELECT rowid, * FROM customers WHERE rowid = ?", (user_id,)) # Pulls everything from the database
    user = cursor.fetchone() # Stores all of the items from the query into a variable

    if user is None:
        print(f"The ID of {user_id} that you entered doesn't exist")
        return
    
    print(f"\nHere's the info for the user you selected with ID {user_id}:")
    print(f"- First Name: {user[1]}")
    print(f"- Last Name: {user[2]}")
    print(f"- Email: {user[3]}")

    # first_name = input("Enter the first name of the user that you want to change: ").title()
    # last_name = input("Enter the last name of the user that you're wanting to change: ").title()

    print("\nWhich value are you wanting to change?")
    print("1) First Name")
    print("2) Last Name")
    print("3) Email")

    try:
        original_value = int(input("Enter a number of which value to change: "))
    except ValueError:
        print("Please enter a valid option")
        return
    
    mapped_values = {
        1: ("first_name", "First Name"),
        2: ("last_name", "Last Name"),
        3: ("email", "Email")
    }

    if original_value not in mapped_values:
        print("Please choose a valid option from 1, 2, or 3")
        return
    
    requested_value, field_display =  mapped_values[original_value]
    changed_value = input(f"What would you like to change the {field_display} to: ")

    if requested_value in ["first_name", "last_name"]:
        changed_value = changed_value.title()
    elif requested_value == "email":
        changed_value = changed_value.lower()

    cursor.execute(f"UPDATE customers SET {requested_value} = ? WHERE rowid = ?",
                   (changed_value, user_id))
    
    print(f"{field_display} has been successfully updated to {changed_value} for user with ID {user_id}!")

    conn.commit() # Commits the code to be executed


def deleteUser():
    displayAllContents()

    try:
        user_id = int(input("\nEnter the ID of the user that you want to change: "))
    except ValueError:
        print("Please enter a valid ID number")
        return
    
    cursor.execute("SELECT rowid, * FROM customers WHERE rowid = ?", (user_id,)) # Pulls everything from the database
    user = cursor.fetchone() # Stores all of the items from the query into a variable

    if user is None:
        print(f"The ID of {user_id} that you entered doesn't exist")
        return
    
    print(f"\nThis is the user that was found: {user[1]} {user[2]}")
    confirm_deletion = input(f"Are you sure you want to delete {user[1]} {user[2]}? (yes/no): ")

    if confirm_deletion != "yes":
        print("Canceling deletion...")
        return

    cursor.execute("DELETE FROM customers WHERE rowid = ?", (user_id,))

    print(f"\nYour user {user[1]} {user[2]} with the ID of {user_id} has been successfully deleted")

    conn.commit() # Commits the code to be executed


# While loop to determine when to stop running
while user_input != 5: # Flips
    print("")
    print("""Options:
        1. Enter a new student
        2. Update a student record
        3. Delete a student record
        4. Display all contents  
        5. Quit program""")
    user_input = int(input("\nEnter your selection: "))

    if user_input == 1:
        insertItem()
    elif user_input == 2:
        updateUser()
    elif user_input == 3:
        deleteUser()
    elif user_input == 4:
        displayAllContents()
    elif user_input == 5:
        print("Thanks for using the program!")
    else:
        print("Please select from options 1-4")

conn.commit() # Commits the code to be executed
conn.close() # Closes the connection

# print("Database created successfully → practice.db")
