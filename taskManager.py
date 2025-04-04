import time
import pdb 
from enum import Enum

taskList = []

class Commands(Enum):
    add = 0
    update = 1
    lists = 2
    delete = 3
    exits = 4

def addTask():
    """Adds task to list
    """
    newTask = input("Insert task name: ").strip()
    try:
        taskList.append(newTask)
        print("Successfully added: " + newTask)
    except:
        print("Failed to add: " + newTask)
    time.sleep(1)

def listTasks():
    """Lists added tasks
    """
    print("---Task List---")
    pdb.set_trace()
    if len(taskList) == 0:
        print("Empty Task List")
    else:
        for task in taskList:
            print(task)
    print("---------------\n")
    input("Type to continue...")

def updateTask():
    """Updates existing task
    """
    mainMenu()

def deleteTask():
    """Removes previously added task
    """
    deleteTask = input("Task to be deleted: ").strip()
    try:
        taskList.remove(deleteTask)
        print("Successfully deleted: " + deleteTask)
    except:
        print("Value not found")
    time.sleep(1)

def mainMenu():
    print("\n\n==Task Manager==")
    print("Commands: ", end='')
    for i in Commands:
        print(i.name + ", ", end='')
    print("\n")

def main():
    while True:
        mainMenu()
        command = input("Insert command: ").strip()
        if command == Commands.add.name:
            addTask()
        elif command == Commands.lists.name:
            listTasks()
        elif command == Commands.exits.name:
            print("Closing program...")
            break;
        elif command == Commands.delete.name:
            deleteTask()
        else:
            print("Unknown parameter. Try again")


if __name__ == "__main__":
    main()
