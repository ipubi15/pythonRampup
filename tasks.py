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

class updateOption(Enum):
    Name = 0
    Description = 1
    Status = 2

class Task:
    __index : int
    __name : str
    __description : str
    __status : TaskStatus

    def __init__(self, name, description, status=TaskStatus.ToDo, index=-1):
        self.__name = name
        self.__description = description
        self.__status = status
        self.__index = index

    def addToDB(self) -> bool:
        task = (self.__name, self.__description, self.__status.value)
        newTaskIndex = addTaskDB(task)
        if newTaskIndex != -1:
            self.__index = newTaskIndex
            return True
        else:
            print("Error adding to DB")
            return False


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

def addTask(newTask : str, newTaskDesc : str) -> bool:
    global taskList
    try:
        if validateTaskInput(newTask):
            task = Task(name=newTask, description=newTaskDesc)
            if task.addToDB():
                taskList[task.getIndex()] = task
    except:
        print("Failed to add: " + newTask)
        return False
    else:
        print("Successfully added: " + newTask)
        return True

def addTaskInput():
    """Adds task to list
    """
    newTask = input("Insert task name: ")
    newTaskDesc = input("Insert task description: ")
    addTask(newTask, newTaskDesc)

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

def updateTask(option : int, taskId : int, value) -> bool:
    """Updates existing task
    """
    if option < updateOption.Name.value or option > updateOption.Status.value:
        print("Invalid Option.")
        return False

    try:
        if option == updateOption.Name.value:
            if validateTaskInput(value):
                taskList[taskId].setName(value)
        elif option == updateOption.Description.value:
            taskList[taskId].setDescription(value)
        else:
            if value < TaskStatus.ToDo.value or value > TaskStatus.Done.value:
                print("Invalid Status")
            else:
                taskList[taskId].setStatus(TaskStatus(value))
    except:
        print("Task ID not found")
        return False
    else:
        print(f"Successfully updated: {taskId:d}")
        return True

def updateTaskInput():
    taskId = int(input("Task ID to be updated: ").strip())
    option = int(input("Update Name(0), Description(1) or Status(2)? "))
    if option == updateOption.Name.value:
        inputStr = "Insert new task name: "
    elif option == updateOption.Description.value:
        inputStr = "Insert new task description: "
    elif option == updateOption.Status.value:
        inputStr = "Insert Task Status(ToDo=0, InProgress=1, Done=2): "
    else:
        print("Invalid option")
        return
    value = input(inputStr)
    updateTask(option, taskId, value)

def deleteTask(indexId : int) -> bool:
    """Removes previously added task
    """
    try:
        task = taskList.pop(indexId)
        deleteTaskDB(task.getIndex())
        del task
        print(f"Successfully deleted ID: {indexId:d}")
    except:
        print("Task ID not found")
        return False
    else:
        return True

def deleteTaskInput():
    indexId = int(input("Task ID to be deleted: ").strip())
    deleteTask(indexId)
