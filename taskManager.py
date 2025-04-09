from tasks import *

def mainMenu():
    print("\n\n==Task Manager==")
    print("Commands: ", end='')
    for i in Commands:
        print(i.name + ", ", end='')
    print("\n")

def main():
    while True:
        mainMenu()
        command = input("Insert command: ").strip().lower()
        if command.__len__() == 0:
            print("Empty command is not valid")
        elif Commands.add.name.find(command, 0) == 0:
            addTask()
        elif Commands.lists.name.find(command, 0) == 0:
            listTasks()
        elif Commands.exits.name.find(command, 0) == 0:
            print("Closing program...")
            break;
        elif Commands.delete.name.find(command, 0) == 0:
            deleteTask()
        elif Commands.update.name.find(command, 0) == 0:
            updateTask()
        else:
            print("Unknown parameter. Try again")


if __name__ == "__main__":
    loadFile()
    main()
