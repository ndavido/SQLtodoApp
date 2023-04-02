import sys
import os
from database import User, Item, Session
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
            print("Please enter your username: ")
            username = input()
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

    print("Please enter your password: ")
    password = input()
    print("Please re-enter your password: ")
    passwordConfirm = input()
    print("---")

    if password != passwordConfirm:
        while password != passwordConfirm:
            print("Passwords entered do not match!")
            print("Please enter your password: ")
            password = input()
            print("Please re-enter your password: ")
            passwordConfirm = input()
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
            print("Please Enter your Username: ")
            username = input()
            user = session.query(User).filter(
                User.username == username).first()
            if user:
                print("Please Enter your Password: ")
                password = input()
                if user.password == password:
                    print("Login Successful!")
                else:
                    while password != user.password:
                        print("Incorrect Password!")
                        print("Please Enter your Password: ")
                        password = input()
            else:
                print("User does not exist!")
            loggedUser.append(user.username)
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
        print("4: Exit" + os.linesep)

        selection = input()
        try:
            match selection:
                case "1":
                    showItems()
                case "2":
                    createItems()
                case "3":
                    removeItems()
                case "4":
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
            items = session.query(Item).filter(Item.owner == loggedUser[0])
            table = []
            for item in items:
                itemId = item.itemId
                owner = item.owner
                itemName = item.name
                description = item.description
                timeStamp = item.timeStamp
                table.append([itemId, owner, itemName, description, timeStamp])
            headers = ["ID", "Owner", "ItemName", "Description", "TimeStamp"]
            print(tabulate(table, headers=headers, tablefmt='orgtbl'))
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
        print("Name for the item:")
        itemName = input()

        print("Would you like to add a description?")
        print('''
            1: Yes
            2: NO  
        ''')

        userInput = input()
        match userInput:
            case "1":
                print("Please enter the description:")
                description = input()
            case "2":
                description = None

        with Session() as session:
            newItem = Item(owner=loggedUser[0],
                           name=itemName, description=description)
            session.add(newItem)

            user = session.query(User).filter(
                User.username == loggedUser[0]).first()
            newItem.users.append(user)
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
            itemAmount = session.query(Item).count()
            if itemAmount < 1:
                print("You should add some items first.")
                return

            print("Give ID to remove:")
            itemId = int(input())

            removableItem = session.query(Item).filter(Item.itemId == itemId)
            if (removableItem.count() > 0):
                session.delete(removableItem.one())
                session.commit()
            else:
                print("Invalid ID!")
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
    userInput = input()

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
