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
            username = input("Please enter your username: ")
            with Session() as session:
                user = session.query(User).filter(
                    User.username == username).first()
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

    password = input("Please enter your password: ")
    passwordConfirm = input("Please re-enter your password: ")
    print("---")

    if password != passwordConfirm:
        while password != passwordConfirm:
            print("Passwords entered do not match!")
            password = input("Please enter your password: ")
            passwordConfirm = input("Please re-enter your password: ")
    else:
        with Session() as session:
            try:
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
    login()

#
# Login
#

def login():
    print("Login Page")
    with Session() as session:
        try:
            print("---")
            username = input("Please Enter your Username: ")
            user = session.query(User).filter(
                User.username == username).first()
            if user:
                password = input("Please Enter your Password: ")
                if user.password == password:
                    print("Login Successful!")
                else:
                    while password != user.password:
                        print("Incorrect Password!")
                        password = input("Please Enter your Password: ")
            else:
                print("User does not exist!")
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
        print(f"{os.linesep}What do you want to do today?")
        print("1: View todo items")
        print("2: Create new todo item")
        print("3: Remove item")
        print("4: Share Note")
        print("5: Exit" + os.linesep)

        selection = input("Your Choice: ")
        try:
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
                    sys.exit("Goodbye!")
                case other:
                    print("---")
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
    print("Your todo lists:")
    print("---")
    with Session() as session:
        try:
            itemAmount = session.query(Item).filter(Item.users.any(User.userId == loggedUser[0])).count()
            if itemAmount > 0:
                items = session.query(Item).filter(Item.users.any(User.userId == loggedUser[0]))
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
            else:
                print("---")
                print("You should add some items first.")
                print("---")
        except Exception as e:
            print("---")
            print(
                f"Error occurred while performing operation!{os.linesep}Details: {e}")
            print("---")
            return

#
# Create Item
#

def createItems():
    try:
        itemName = input("Name for the item: ")

        print("Would you like to add a description?")
        print('''
            1: Yes
            2: NO  
        ''')

        userInput = input("Your Choice: ")
        match userInput:
            case "1":
                description = input("Please enter the description: ")
            case "2":
                description = None

        with Session() as session:
            newItem = Item(owner=loggedUser[0],
                           name=itemName, description=description)
            session.add(newItem)

            user = session.query(User).filter(
                User.userId == loggedUser[0]).first()
            newItem.users.append(user)
            session.commit()
            
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
        with Session() as session:
            itemAmount = session.query(Item).filter(Item.users.any(User.userId == loggedUser[0])).count()
            if itemAmount < 1:
                print("You should add some items first.")
                return

            itemId = int(input("Give ID to remove: "))

            removableItem = session.query(Item).filter(Item.itemId == itemId)
            if (removableItem.count() > 0):
                session.delete(removableItem.one())
                session.commit()
            else:
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
            itemAmount = session.query(Item).filter(Item.users.any(User.userId == loggedUser[0])).count()
            if itemAmount < 1:
                print("You should add some items first.")
                return

            showItems()
            print("---")
            print("Which Note would you like to share?")    
            itemId = int(input("Your Choice: "))
            print("---")
#
#   Note To Self:
#   Pay extra attention
#   To this section
#
            note = session.query(Item).filter(Item.itemId == itemId).first()
            if note:
                print("---")
                shareUser = input("Enter the user's ID you wish to share the note with: ")
                print("---")

                user = session.query(User).filter(
                    User.userId == shareUser).first()
                if user:
                    user.sharedNotes = itemId
                    note.sharedUser = user.userId
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
#
#
#
#
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
