import sqlite3

__sqlInit = """CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY, 
                        name text NOT NULL, 
                        description text,
                        status INT NOT NULL
                    );"""

__sqlInsert = '''INSERT INTO tasks(name, description, status)
             VALUES(?,?,?) '''

__sqlLoad = 'select * from tasks'

__sqlSelectID = 'SELECT name, description, status FROM tasks WHERE id = ?'

__sqlUpdateP1 = 'UPDATE tasks SET '
__sqlUpdateP2 = ' = ? WHERE id = ?'

__sqlDelete = 'DELETE FROM tasks WHERE id = ?'

def initDB(db_file : str, rows) -> bool:
    try:
        global conn
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(__sqlInit)
            conn.commit()
            print("Table created!")
            cursor.execute(__sqlLoad)
            for row in cursor.fetchall():
                rows.append(row)
            return True
    except:
        print("Failed to open database")
        return False


def closeDB():
    conn.close()

def updateTaskDB(field, value, Id) -> bool:
    try:
        sql = __sqlUpdateP1 + field + __sqlUpdateP2
        cursor = conn.cursor()
        cursor.execute(sql, (value, Id))
        conn.commit()
        return True
    except:
        print("Error updating DB")
        return False

def addTaskDB(task) -> int:
    try:
        cursor = conn.cursor()
        cursor.execute(__sqlInsert, task)
        conn.commit()
        return cursor.lastrowid
    except:
        print("Error adding task to DB")
        return -1

def deleteTaskDB(Id) -> bool:
    try:
        cursor = conn.cursor()
        cursor.execute(__sqlDelete, (Id,))
        conn.commit()
        return True
    except:
        print("Error deleting task from DB")
        return False

def readTaskDB(Id, row) -> bool:
    try:
        cursor = conn.cursor()
        cursor.execute(__sqlSelectID, (Id,))
        item = cursor.fetchone()
        if item != None:
            row.append(item)
        return True
    except:
        print("Error reading task from DB")
        return False

