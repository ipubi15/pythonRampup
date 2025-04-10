from utils import *
from enum import Enum
from db import *
import sys

taskList = {}

class Commands(Enum):
    add = 0
    update = 1
    lists = 2
    delete = 3
    exits = 4

class TaskStatus(Enum):
    ToDo = 0
    InProgress = 1
    Done = 2

class Task:
    __index : int
    __name : str
    __description : str
    __status : TaskStatus

    def __init__(self, name, description, status=TaskStatus.ToDo, index=None):
        self.__name = name
        self.__description = description
        self.__status = status
        task = (name, description, status.value)
        if index == None:
            newTaskIndex = addTaskDB(task)
            if newTaskIndex != -1:
                self.__index = newTaskIndex
            else:
                raise Exception("Error adding to DB")
        else:
            self.__index = index

    def getIndex(self) -> int:
        return self.__index

    def getName(self) -> str:
        return self.__name

    def getDescription(self) -> str:
        return self.__description

    def getStatus(self) -> TaskStatus:
        return self.__status

    def setName(self, name : str):
        if updateTaskDB("name", name, self.__index):
            self.__name = name

    def setDescription(self, description : str):
        if updateTaskDB("description", description, self.__index):
            self.__description = description

    def setStatus(self, status : TaskStatus):
        if updateTaskDB("status", status.value, self.__index):
            self.__status = status

    def printTask(self) -> str:
        print(f"ID: {self.__index} - Status: " + self.__status.name + " - Task: " + self.__name + " - Description: " + self.__description )

def loadFile():
    global taskList 
    rows = []

    if not initDB(rows):
        print("Exiting program DB failed!")
        sys.exit()

    for row in rows:
        task = Task(name=row[1], description=row[2], status=TaskStatus(row[3]), index=row[0])
        taskList[row[0]] = task

def addTask():
    """Adds task to list
    """
    global taskList
    newTask = input("Insert task name: ")
    newTaskDesc = input("Insert task description: ")
    try:
        if validateTaskInput(newTask):
            task = Task(name=newTask, description=newTaskDesc)
            taskList[task.getIndex()] = task
        else:
            return
    except:
        print("Failed to add: " + newTask)
    else:
        print("Successfully added: " + newTask)

def listTasks():
    """Lists added tasks
    """
    print("---Task List---")
    if len(taskList) == 0:
        print("Empty Task List")
    else:
        for task in taskList.values():
            task.printTask()

    print("---------------\n")
    input("Type to continue...")

def updateTask():
    """Updates existing task
    """
    updateTaskID = int(input("Task ID to be updated: ").strip())
    option = int(input("Update Name(0), Description(1) or Status(2)? "))
    if option < 0 or option > 2:
        print("Invalid Option.")
        return

    try:
        if option == 0:
            newTask = input("Insert new task name: ")
            if validateTaskInput(newTask):
                taskList[updateTaskID].setName(newTask)
        elif option == 1:
            description = input("Insert new task description: ")
            taskList[updateTaskID].setDescription(description)
        else:
            status = int(input("Insert Task Status(ToDo=0, InProgress=1, Done=2): "))
            if status < 0 or status > 2:
                print("Invalid Status")
            else:
                taskList[updateTaskID].setStatus(TaskStatus(status))
    except:
        print("Task ID not found")
    else:
        print(f"Successfully updated: {updateTaskID:d}")

def deleteTask():
    """Removes previously added task
    """
    deleteTask = input("Task ID to be deleted: ").strip()
    deleteTask = int(deleteTask)
    try:
        task = taskList.pop(deleteTask)
        deleteTaskDB(task.getIndex())
        del task
        print(f"Successfully deleted ID: {deleteTask:d}")
    except:
        print("Task ID not found")
