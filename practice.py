import sqlite3 # Imports sqlite3 into the program

# Create a database file
conn = sqlite3.connect("practice.db")  # makes a file instead of in-memory
cursor = conn.cursor() # Creates a variable called cursor and assigns it conn.cursor()
user_input = "" # Defines the user_input variable so that it can be used

# Creates a table called customers if one doesn't exist to begin with
cursor.execute("""CREATE TABLE IF NOT EXISTS customers (
            first_name text,
            last_name text,
            email text
        )""")

# Creates a table called orders if one doesn't exist to begin with
cursor.execute("""CREATE TABLE IF NOT EXISTS orders (
               customer_id INTEGER,
               product TEXT,
               price REAL)""")

conn.commit() # Commits the code to be executed

# Prints a welcome statement when using the program
print("\nWelcome to the customer record system. Please select an option below:")

# Defines a function to insert a product into the orders table
def insertProduct():
    displayAllCustomers() # First we see all of the customers that are in the database so we can see the ID's of each customer
    # Defines a variable called customer_id that will store the id of the customer that purchased the item
    try: # Starts with a try block to see if the customer_id is an int
        customer_id = int(input("\nEnter the ID of the customer that this order belongs to: "))
    except ValueError: # A ValueError occurs if the the customer_id is not an int
        print("Please enter a valid ID") # Prints the following message if customer_id is not an int
        return
    # Adds validation to check the database to see if the customer ID that was entered is valid
    cursor.execute("SELECT rowid FROM customers WHERE rowid = ?", (customer_id,))
    if cursor.fetchone() is None: # If the customer ID that was entered is not valid
        print(f"The customer ID {customer_id} that you entered is not a valid ID") # The following message is printed
        return
    # Defines a variable called product that will store the name of the item that the customer purchased
    product = input("Enter the name of the product that was purchased: ").title()
    # Defines a variable called price that will store the price of the item that the customer purchased
    try: # Starts with a try block to see if the price is equal to a float
        price = float(input("Enter the price of the product that was purchased: "))
    except ValueError: # A ValueError occurs if price is not equal to a float
        print("Please enter a valid price") # Prints the following message if price is not a float
        return

    # Builds out the SQL command that will insert the product into the orders table
    cursor.execute("INSERT INTO orders VALUES (?, ?, ?)", (customer_id, product, price))

    # Prints a message saying that the product was successfully entered into the table
    print(f"\n✅Your product {product} has been entered successfully!✅")

    conn.commit() # Commits the code to be executed

# Defines a function called displayAllOrders that will display all orders from the database
def displayAllOrders():
    cursor.execute("SELECT rowid, * from orders") # Pulls all of the items including the rowid from the database
    items = cursor.fetchall() # Stores all of the orders in a variable called items

    id_header = "ID" # Defines a variable called id_header and sets it equal to "ID"
    customer_header = "Customer ID" # Defines a variable called customer_header and sets it equal to "Customer ID"
    product_header = "Product" # Defines a variable called product_header and sets it equal to "Product"
    price_header = "Price" # Defines a variable called price_header and sets it equal to "Price"

    id_width = 5 # Defines a variable called id_width and sets it equal to 5
    customer_width = 15 # Defines a variable called customer_width and sets it equal to 15
    product_width = 15 # Defines a variable called product_width and sets it equal to 15
    price_width = 15 # Defines a variable called price_width and sets it equal to 15

    print("\nHere's all of the info for all of your orders:\n") # Prints a header saying that all of the order info is below

    # Prints out the header info for all of the various columns that are in the table
    print(f"{id_header:<{id_width + 1}}{customer_header:<{customer_width + 1}}{product_header:<{product_width + 1}}{price_header:<{price_width}}")

    # Prints a breaker line under all of the column headers stated above
    print("-" * id_width + " " + "-" * customer_width + " " + "-" * product_width + " " + "-" * price_width)

    # Defines a for loop to go through each of the items that was pulled from the database
    for item in items:
        # Defines a variable called formatted_price and formats it to be displayed
        formatted_price = f"${item[3]:.2f}"
        # Prints out all of the values associated with each value that was pulled from the database
        print(f"{item[0]:<{id_width + 1}}{item[1]:<{customer_width + 1}}{item[2]:<{product_width + 1}}{formatted_price:<{price_width}}")


# Defines a function called displayAllOrdersByID to display all order that a certain customer has bade
def displayAllOrdersByID():
    displayAllCustomers() # All of the customers are displayed first
    try: # Starts with a try block to see if the customer ID is an int
        customer_id = int(input("Enter a customer ID to show all of their orders: "))
    except ValueError: # If it's not an int then the a ValueError occurs
        print("Please enter a valid ID") # And the following message is printed
        return
    
    # Pulls all info from the customers table based on the customer_id
    cursor.execute("SELECT rowid, * FROM customers WHERE rowid = ?", (customer_id,))
    customer = cursor.fetchone() # Gets the info from the database and stores it in the customer variable
    if customer is None: # If the customer id equal to None
        print(f"The customer id {customer_id} doesn't exist") # The following message is displayed
        return

    # Prints out a header message
    print(f"Here's the info for {customer[1]} {customer[2]}")

    # Executes the SQL statement to pull info from both tables
    cursor.execute("SELECT customer_id, product, price FROM orders JOIN customers ON customers.rowid = orders.customer_id WHERE customers.rowid = ?", (customer_id,))

    # Gets all of the info and stores it in the orders variable
    orders = cursor.fetchall()

    # Checks to see if the customer has an orders
    if not orders:
        print(f"Customer {customer[1]} {customer[2]} does not have any orders")
        return
    
    id_header = "ID:" # Defines a variable id_header and gives it the value of "ID"
    product_header = "Product:" # Defines a variable product_header and gives it the value of "Product"
    price_header = "Price:" # Defines a variable price_header and gives it the value of "Price"

    id_width = 5 # Defines a variable id_width and gives it the value of 5
    product_width = 15 # Defiens a variable product_width and gives it the value of 15
    price_width = 15 # Defines a variable price_width and gives it the value of 15
    
    print("\nOrders:") # Prints an Orders header
    # Prints out the headers for all of the columns
    print(f"{id_header:<{id_width + 1}}{product_header:<{product_width + 1}}{price_header:<{price_width}}")
    # Prints out breaker lines for each of the columns
    print("-" * id_width + " " + "-" * product_width + " " + "-" * price_width)
    for order in orders: # Starts a for loop to go through the orders
        formatted_price = f"${order[2]:.2f}" # Defines a variable called formatted_price to store the price of the order
        # Prints all of the values associated with the order
        print(f"{order[0]:<{id_width + 1}}{order[1]:<{product_width + 1}}{formatted_price:<{price_width}}")


# Defines a function called insertCustomer that will create a SQL command to add a user to the customer table
def insertCustomer():
    first_name = input("Enter a first name: ").title() # Gets the first name of the user and stores it in the first_name variable
    last_name = input("Enter a last name: ").title() # Gets the last name of the user and stores it in the last_name variable
    email = input("Enter an email: ").lower() # Gets the email of the user and stores it in the email variable
    cursor.execute("INSERT INTO customers VALUES (?, ?, ?)", (first_name, last_name, email)) # Populates the values from the user and sends it to the database

    print(f"\nYour customer {first_name} {last_name} has been entered successfully!") # Prints statement saying that the user you entered was successfully added

    conn.commit() # Commits the code to be executed


# Function to display all of the contents of the database
def displayAllCustomers():
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
    print("\nHere's all of the info for all of your customers:\n")

    # Prints out the header info for the items in the foor loop
    print(f"{id_header:<{id_width + 1}}{first_header:<{first_width + 1}}{last_header:<{last_width + 1}}{email_header:<{email_width + 1}}")
    # Prints out breaker lines for each of the headers
    print("-" * id_width + " " + "-" * first_width + " " + "-" * last_width + " " + "-" * email_width)

    for item in items: # Loops through the items using a for loop and prints out the info
        # Prints out head item by the index of where it falls in the list
        print(f"{item[0]:<{id_width + 1}}{item[1]:<{first_width + 1}}{item[2]:<{last_width + 1}}{item[3]:<{email_width + 1}}")


# Defines a function called updateUser
def updateUser():
    displayAllCustomers() # First displays all of the records currently in the database
    try:
        # First the program tries to get the user_id
        user_id = int(input("\nEnter the ID of the customer that you want to change: "))
    # If the user_id is not a valid number then a ValueError is raised
    except ValueError:
        # A message is printed saying to enter a valid number
        print("Please enter a valid ID number")
        return

    cursor.execute("SELECT rowid, * FROM customers WHERE rowid = ?", (user_id,)) # Pulls everything from the database
    user = cursor.fetchone() # Stores all of the items from the query into a variable

    if user is None: # Checks to see if the user submitted exists
        print(f"The ID of {user_id} that you entered doesn't exist") # If it doesn't exist a message is printed
        return
    
    # Prints a header message for the the info of the customer that was selected
    print(f"\nHere's the info for the customer you selected with ID {user_id}:")
    print(f"- First Name: {user[1]}") # Prints the first name of the customer
    print(f"- Last Name: {user[2]}") # Prints the last name of the customer
    print(f"- Email: {user[3]}") # Prints the email address of the customer

    # Prints a header asking what value the user wants to change about the customer
    print("\nWhich value are you wanting to change?")
    print("1) First Name") # Option 1
    print("2) Last Name") # Option 2
    print("3) Email") # Option 3

    # First the original_value is checked to be a valid number option
    try:
        original_value = int(input("Enter a number of which value to change: "))
    # If the value of original_value is not a valid number selection    
    except ValueError:
        print("Please enter a valid option") # The following message is printed
        return
    
    # Maps out the values in a dictionary that can be selected from for editing
    mapped_values = {
        1: ("first_name", "First Name"),
        2: ("last_name", "Last Name"),
        3: ("email", "Email")
    }

    # Checks to see if the option that the user selected is not a valid option
    if original_value not in mapped_values:
        # If so then the following message is printed
        print("Please choose a valid option from 1, 2, or 3")
        return
    
    # Unpacks the tuple
    requested_value, field_display =  mapped_values[original_value]
    changed_value = input(f"What would you like to change the {field_display} to: ") # Asks what to change the field_display to

    # Checks to see if the requested_value is either first_name or last_name
    if requested_value in ["first_name", "last_name"]:
        changed_value = changed_value.title() # Sets the value of changed_value to itself but sets it to title case
    # Checks to see if the requested_value is equal to email
    elif requested_value == "email":
        changed_value = changed_value.lower() # Sets the value of changed_value to itself but sets it to title case

    # Builds out the SQL statement to update the customer based on the values provided by the user
    cursor.execute(f"UPDATE customers SET {requested_value} = ? WHERE rowid = ?",
                   (changed_value, user_id))

    # Prints out a success message telling the user that their request was fulfilled
    print(f"\n✅ {field_display} has been successfully updated to {changed_value} for user with ID {user_id}!✅ ")

    conn.commit() # Commits the code to be executed


# Defines a function called deleteUser
def deleteUser():
    displayAllCustomers() # First displays all of the customer records in the database
    try: # First we try to get a valid ID of a customer to delete
        user_id = int(input("\nEnter the ID of the customer that you want to delete: "))
    # If the user_id is not a number then a ValueError occurs
    except ValueError:
        # The following message is printed if the value of the input is not a number
        print("Please enter a valid ID number")
        return
    
    cursor.execute("SELECT rowid, * FROM customers WHERE rowid = ?", (user_id,)) # Pulls everything from the database based on rowid
    user = cursor.fetchone() # Stores all of the items from the query into a variable

    if user is None: # If the user that was pulled does not exist
        # The following message is displayed saying the customer doesn't exist
        print(f"The ID of {user_id} that you entered doesn't exist")
        return
    
    # Prints the first and last name of the customer that was pulled
    print(f"\nThis is the customer that was found: {user[1]} {user[2]}")

    cursor.execute("SELECT COUNT(*) FROM orders WHERE customer_id = ?", (user_id,))
    orderCount = cursor.fetchone()[0]
    if orderCount > 0:
        print(f"⚠️ Your user {user[1]} {user[2]} has {orderCount} orders that will also be deleted ⚠️")

    # Asks for confirmation on if we want to delete the customer and assigns the value to confirm_deletion
    confirm_deletion = input(f"Are you sure you want to delete {user[1]} {user[2]} and all coresponding orders? (yes/no): ")

    # If the value of confirm_deletion is anything other then "yes"
    if confirm_deletion != "yes":
        # The following message is printed saying that the deletion is being cancelled
        print("Canceling deletion...")
        return

    cursor.execute("DELETE FROM orders WHERE customer_id = ?", (user_id,))

    # The SQL statement is created to delete the customer based on the id that's passed in
    cursor.execute("DELETE FROM customers WHERE rowid = ?", (user_id,))

    # A message is printed saying that the customer that was requested was successfully deleted
    print(f"\n✅ Your user '{user[1]} {user[2]}' with the ID of {user_id} has been successfully deleted ✅")

    conn.commit() # Commits the code to be executed


# Defines a function to delete an order
def deleteOrder():
    displayAllOrders() # First all of the orders from the database are displayed
    try: # Starts a try loop to get the ID of the order to be deleted
        order_id = int(input("\nEnter the order ID that you want to delete: ")) # Stores the ID in a variable called order_id
    except ValueError: # If the input is not a number then a ValueError occurs
        print("Please enter a valid order ID") # The following message is printed if the input is not a number
        return
    
    # Builds and executes the SQL statement to get the info of the order based on the order_id
    cursor.execute("SELECT rowid, * from orders WHERE rowid = ?", (order_id,))
    order = cursor.fetchone() # Get's one order from the database and stores it in a variable called order

    # Checks to see if an order exists
    if order is None:
        # If the order doesn't exist then the following message is printed
        print(f"The ID of {order_id} that you entered doesn't exist")
        return
    
    print(f"\nThis is the order info that was found:\n") # Prints a header for the info that's pulled from the database
    print(f"Customer ID: {order[1]}") # Prints out the customer ID of the order
    print(f"Product: {order[2]}") # Prints out the product that's in the order
    print(f"Price: ${order[3]:.2f}") # Prints out the price of the order

    # Defines a variable called confirm_deletion to check that the user wants to delete the order
    confirm_deletion = input(f"\nAre you sure that you want to delete the order for {order[2]}? (yes/no): ")
    if confirm_deletion != "yes": # If the value of confirm_deletion doesn't equal "yes"
        print("Canceling deletion...") # Prints the following message saying that the deletion is being canceled
        return
    
    # Builds and executes the SQL statement to delete the order from the database
    cursor.execute("DELETE FROM orders WHERE rowid = ?", (order_id,))

    # Prints a message saying that the order has been deleted
    print(f"\n✅ Your order for '{order[2]}' with the order ID of {order_id} has been successfully deleted ✅")

    conn.commit() # Commits the code to be executed

# While loop to determine when to stop running
while user_input != 9: # States to keep running if the input that's entered is not 8
    print("") # Prints an empty line
    # Prints out the different options that the user can choose from
    print("""Options:
        1. Enter a new customer
        2. Update a customer record
        3. Delete a customer record
        4. Display all Customers
        5. Input an order
        6. Display all orders
        7. Display all orders by customer ID
        8. Delete an order 
        9. Quit program""")
    try: # Tries to see if the value of user_input is equal to an integar
        user_input = int(input("\nEnter your selection: "))
    except ValueError: # If user_input is not a number then a ValueError occurs
        # The following message is printed if the option entered is not a valid numeric option
        print("Please enter a valid numeric option")
        continue

    if user_input == 1: # Checks to see if user_input is equal to 1
        insertCustomer() # If so then the insertItem() function is called
    elif user_input == 2: # Checks to see if user_input is equal to 2
        updateUser() # If so then the updateUser() function is called
    elif user_input == 3: # Checks to see if user_input is equal to 3
        deleteUser() # If so then the deleteUser() function is called
    elif user_input == 4: # Checks to see if user_input is equal to 4
        displayAllCustomers() # If so then the displayAllCustomers() function is called
    elif user_input == 5: # Checks to see if user_input is equal to 5
        insertProduct() # If so then the insertProduct() function is called
    elif user_input == 6: # Checks to see if the user_input is equal to 6
        displayAllOrders() # If so then the displayAllOrders() function is called
    elif user_input == 7: # Checks to see if the user_input isi equal to 7
        displayAllOrdersByID() # If so then the displayAllOrdersByID() function is called
    elif user_input == 8: # Checks to see if the user_input is equal to 8
        deleteOrder() # If so then the deleteOrder() function is called
    elif user_input == 9:
        print("Thanks for using the program!") # If so then the program closes and the following is printed
    else: # If any other option outside of (1, 2, 3, 4, 5, 6, 7, 8,9) is entered then the folowing message is printed
        print("Please select from options 1-9")

conn.close() # Closes the connection at the end of the program