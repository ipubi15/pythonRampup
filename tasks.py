import time
import pickle
from utils import *
from enum import Enum
from dataclasses import dataclass


taskList = []

@dataclass
class TaskItem:
    """Struct like object"""
    name : str
    description : str = "No description"

    def getFullTask(self) -> str:
        return self.name + ": " + self.description

class Commands(Enum):
    add = 0
    update = 1
    lists = 2
    delete = 3
    exits = 4

def loadFile():
    global taskList 
    try:
        fileHandler = open('file.txt', 'rb')
        taskList = pickle.load(fileHandler)
        fileHandler.close()
    except:
        print("Couldn't load file")

def persist():
    fileHandler = open('file.txt', 'wb')
    pickle.dump(taskList, fileHandler)
    fileHandler.close()

def addTask():
    """Adds task to list
    """
    newTask = input("Insert task name: ")
    newTaskDesc = input("Insert task description: ")
    try:
        if validateTaskInput(newTask):
            task = TaskItem(name=newTask, description=newTaskDesc)
            taskList.append(task)
        else:
            return
    except:
        print("Failed to add: " + newTask)
    else:
        print("Successfully added: " + newTask)
        persist()

def listTasks():
    """Lists added tasks
    """
    print("---Task List---")
    if len(taskList) == 0:
        print("Empty Task List")
    else:
        for index, task in enumerate(taskList):
            print(f"ID: {index:d} - Task: " + task.getFullTask())

    print("---------------\n")
    input("Type to continue...")

def updateTask():
    """Updates existing task
    """
    updateTaskID = int(input("Task ID to be updated: ").strip())
    nameOrDescription = int(input("Update Name(0) or Description(1) ? "))
    if nameOrDescription != 0 and nameOrDescription != 1:
        print("Invalid Option.")
        return

    try:
        if nameOrDescription == 0:
            newTask= input("Insert new task name: ")
            if validateTaskInput(newTask):
                taskList[updateTaskID].name = newTask
        else:
            taskList[updateTaskID].description = input("Insert new task description: ")
    except:
        print("Task ID not found")
    else:
        print(f"Successfully updated: {updateTaskID:d}")
        persist()

def deleteTask():
    """Removes previously added task
    """
    deleteTask = input("Task ID to be deleted: ").strip()
    deleteTask = int(deleteTask)
    try:
        taskList.pop(deleteTask)
        print(f"Successfully deleted ID: {deleteTask:d}")
    except:
        print("Task ID not found")
