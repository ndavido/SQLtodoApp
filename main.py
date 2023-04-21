#
# Name: Dawid Nalepa
# ID: 2209302
#

import sys
import os
from database import User, Item, UserItem, Session
from tabulate import tabulate

loggedUser = []

#
# Registration
#


def register():
    print("Registration Page")
    print("---")

    while True:
        try:
            # Ask for username
            username = input("Please enter your username: ")
            with Session() as session:
                user = session.query(User).filter(
                    User.username == username).first()
                # Check is user exists
                if user:
                    print("---")
                    print("Username is already taken!")
                    print("---")
                else:
                    break
        except Exception as e:
            print("---")
            print(
                f"Error occurred while performing operation!{os.linesep}Details: {e}")
            print("---")
            return
    # Ask for password and re-enter password
    password = input("Please enter your password: ")
    passwordConfirm = input("Please re-enter your password: ")
    print("---")
    # Check if passwords match
    if password != passwordConfirm:
        # Initilize a loop to ensure passwords match
        while password != passwordConfirm:
            print("Passwords entered do not match!")
            password = input("Please enter your password: ")
            passwordConfirm = input("Please re-enter your password: ")
    else:
        with Session() as session:
            try:
                # Create new user
                newUser = User(username=username, password=password)
                session.add(newUser)
                session.commit()
            except Exception as e:
                print("---")
                print(
                    f"Error occurred while performing operation!{os.linesep}Details: {e}")
                print("---")
                return

    print("---")
    # Prompt to login
    login()

#
# Login
#


def login():
    print("Login Page")
    with Session() as session:
        try:
            print("---")
            # Ask for username
            username = input("Please Enter your Username: ")
            user = session.query(User).filter(
                User.username == username).first()
            # Check if user exists
            if user:
                # Ask for password
                password = input("Please Enter your Password: ")
                if user.password == password:
                    print("Login Successful!")
                else:
                    # Initialize a loop to allow the user to enter correct password
                    while password != user.password:
                        print("Incorrect Password!")
                        password = input("Please Enter your Password: ")
            else:
                print("User does not exist!")
            # Store the user ID in a list
            loggedUser.append(user.userId)
        except Exception as e:
            print("---")
            print(
                f"Error occurred while performing operation!{os.linesep}Details: {e}")
            print("---")
            return
    print("---")

    main()

#
# Main
#


def main():
    while True:
        # Display menu options
        print(f"{os.linesep}What do you want to do today?")
        print("1: View todo items")
        print("2: Create new todo item")
        print("3: Remove item")
        print("4: Share Note")
        print("5: Exit" + os.linesep)
        # Get user's choice
        selection = input("Your Choice: ")
        try:
            # Match user's choice
            match selection:
                case "1":
                    showItems()
                case "2":
                    createItems()
                case "3":
                    removeItems()
                case "4":
                    shareNote()
                case "5":
                    sys.exit("Goodbye!")  # Exit the program
                case other:
                    print("---")
                    # if user enters an invalid choice
                    print("Invalid Option!")
                    print("---")
        except Exception as e:
            print("---")
            print(
                f"Error occurred while performing operation!{os.linesep}Details: {e}")
            print("---")
            return

#
# Show Item
#


def showItems():
    print("Your todo lists:")  # prints heading
    print("---")

    with Session() as session:
        try:
            # Number of items for the logged-in user
            itemAmount = session.query(Item).filter(
                Item.users.any(User.userId == loggedUser[0])).count()

            if itemAmount > 0:
                # Get the number of items owned by the user
                owned_items = session.query(Item).filter(
                    Item.owner == loggedUser[0]).count()

                if owned_items > 0:
                    # Get all the items owned by the user and print them in a table
                    items = session.query(Item).filter(
                        Item.owner == loggedUser[0])
                    createTable(items)
                    print("---")

                # Gte the number of items shared with the user
                shared_items = session.query(Item).filter(
                    Item.sharedUser == loggedUser[0]).count()

                if shared_items:
                    # Get all the items shared with the user and print them in a table
                    items = session.query(Item).filter(
                        Item.sharedUser == loggedUser[0])
                    print("Shared todo lists:")
                    print("---")
                    createTable(items)
                    print("---")
            else:
                print("---")
                print("You should add some items first.")
                print("---")
        except Exception as e:
            print("---")
            # print error message if any error occurs
            print(
                f"Error occurred while performing operation!{os.linesep}Details: {e}")
            print("---")
            return


# Function to format the items into a table
def createTable(items):
    table = []
    for item in items:
        itemId = item.itemId
        owner = item.owner
        itemName = item.name
        description = item.description
        timeStamp = item.timeStamp
        table.append([itemId, owner, itemName, description, timeStamp])
    headers = ["Item ID", "Owner ID", "Item Name", "Description", "Time Stamp"]
    print(tabulate(table, headers=headers, tablefmt='orgtbl'))

#
# Create Item
#


def createItems():
    try:
        # Ask for the name of the new item
        itemName = input("Name for the item: ")
        # Ask the user if they want to add a description
        print("Would you like to add a description?")
        print('''
            1: Yes
            2: NO  
        ''')

        # Get user input and add a description if the user wants to
        userInput = input("Your Choice: ")
        match userInput:
            case "1":
                description = input("Please enter the description: ")
            case "2":
                description = None
        # Open a new session and add the item to the database
        with Session() as session:
            newItem = Item(owner=loggedUser[0],
                           name=itemName, description=description)
            session.add(newItem)
            # Associate the item with the logged-in user
            user = session.query(User).filter(
                User.userId == loggedUser[0]).first()
            newItem.users.append(user)
            session.commit()
            # Set the logged-in user as the owner of the item
            owner = session.query(UserItem).filter(
                UserItem.userId == loggedUser[0]).first()
            owner.is_owner = True
            session.commit()

    except Exception as e:
        print("---")
        print(
            f"Error occurred while performing operation!{os.linesep}Details: {e}")
        print("---")
        return

#
# Remove Item
#


def removeItems():
    try:
        # Check if user has any items in their list
        with Session() as session:
            itemAmount = session.query(Item).filter(
                Item.users.any(User.userId == loggedUser[0])).count()
            if itemAmount < 1:
                print("You should add some items first.")
                return

            # Prompt user for the ID of the item to remove
            itemId = int(input("Give ID to remove: "))

            # Query the database for the item with the given ID
            removableItem = session.query(Item).filter(Item.itemId == itemId)
            if (removableItem.count() > 0):
                # Delete the item from the database
                session.delete(removableItem.one())
                session.commit()
            else:
                # If no item with the given ID is found, print an error message
                print("---")
                print("Invalid ID!")
                print("---")
    except Exception as e:
        print("---")
        print(
            f"Error occurred while performing operation!{os.linesep}Details: {e}")
        print("---")
        return


#
#   Share Note
#

def shareNote():
    try:
        with Session() as session:
            # Count the number of items that belong to the user
            itemAmount = session.query(Item).filter(
                Item.users.any(User.userId == loggedUser[0])).count()
            # If there are no items, exit
            if itemAmount < 1:
                print("You should add some items first.")
                return

            # Show the user's items
            showItems()
            print("---")
            # Ask the user which item they would like to share
            print("Which Note would you like to share?")
            itemId = int(input("Your Choice: "))
            print("---")

            # Find the selected item
            note = session.query(Item).filter(Item.itemId == itemId).first()
            if note:
                print("---")
                # Ask the user which user to share with
                shareUser = input(
                    "Enter the user's ID you wish to share the note with: ")
                print("---")

                # Find the user to share with
                user = session.query(User).filter(
                    User.userId == shareUser).first()
                if user:
                    # Update the user's shared notes list
                    user.sharedNotes = itemId
                    # Update the item's shared user
                    note.sharedUser = user.userId
                    # Add the user to the item's users list
                    note.users.append(user)
                    print("Note has been shared succesfully")
                else:
                    print("---")
                    print("User does not exist!")
                    print("---")
            else:
                print("---")
                print("Invalid ID!")
                print("---")

            session.commit()

    except Exception as e:
        print("---")
        print(
            f"Error occurred while performing operation!{os.linesep}Details: {e}")
        print("---")
        return


#
# Loading Application
#

if __name__ == "__main__":
    print("Welcome to TOD-O LIST O-MAKER Version 5123.524")

    print('''
        1: Login
        2: Register   
    ''')
    userInput = input("Your Choice: ")

    while True:
        try:
            match userInput:
                case "1":
                    login()
                case "2":
                    register()
                case other:
                    print("---")
                    print("Invalid Option!")
                    print("---")
        except Exception as e:
            print("---")
            print(
                f"Error occurred while performing operation!{os.linesep}Details: {e}")
            print("---")
