import sys
import os
from database import Item, Session

def main():
    while True:
        print(f"{os.linesep}What do you want to do today?")
        print("1: View todo items")
        print("2: Create new todo item")
        print("3: Remove item")
        print("4: Exit" + os.linesep)
        
        selection = input()
        if selection == "1": showItems()
        if selection == "2": createItems()
        if selection == "3": removeItems()
        if selection == "4": sys.exit("Goodbye!")

def showItems():
    print("Your todo lists:")
    print("---")
    with Session() as session:
        items = session.query(Item)
        for item in items:
            itemId = item.itemId
            itemName = item.name
            print(f"{itemId}: {itemName}")
    print("---" + os.linesep)
    
def createItems():
    print("Name for the item:")
    itemName = input()
    
    with Session() as session:
        newItem = Item( name = itemName )
        session.add(newItem)
        session.commit()
    
def removeItems():
    with Session() as session:
        itemAmount = session.query(Item).count()
        if itemAmount < 1:
            print("You should add some items first.")
            return
        
        print("Give ID to remove:")
        itemId = int(input())
        
        removableItem = session.query(Item).filter( Item.itemId == itemId )
        if (removableItem.count() > 0):
            session.delete(removableItem.one())
            session.commit()
        else:
            print("Invalid ID!")
         
print("Welcome to TOD-O LIST O-MAKER Version 5123.524")
main()
