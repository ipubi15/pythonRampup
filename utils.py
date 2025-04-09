
def validateTaskInput(newTask : str) -> bool:
    if not newTask.isascii() or (newTask.__len__() == 0):
        print("Tasks need to be an ASCII string and not be empty...")
        return False
    else:
        return True