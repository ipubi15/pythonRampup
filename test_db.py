import unittest
from unittest.mock import Mock
from unittest.mock import patch
import db
import os

dbPath = 'db_test.db'

class TestValidateInput(unittest.TestCase):
    def setUp(self):
        rows = []
        if os.path.isfile(dbPath):
            os.system('rm ' + dbPath)
        db.initDB(dbPath, rows)
        return super().setUp()

    def tearDown(self):
        db.closeDB()
        os.system('rm ' + dbPath)
        return super().tearDown()

    def test_dbInsert(self):
        rows = []
        task = ("read manga", "shintaro kago", 0)
        index = db.addTaskDB(task)
        db.readTaskDB(index, rows)
        self.assertEqual(rows[0][0], "read manga")

    def test_dbInsertFail(self):
        rows = []
        task = ("read manga", "shintaro kago", 0)
        db.closeDB()
        index = db.addTaskDB(task)
        db.initDB(dbPath, rows)
        rows = []
        db.readTaskDB(index, rows)
        self.assertEqual(len(rows), 0)

    def test_dbInsertMultiple(self):
        rows = []
        task = ("read manga", "shintaro kago", 0)
        index = db.addTaskDB(task)
        task = ("play CS2", "video game", 1)
        index2 = db.addTaskDB(task)
        db.readTaskDB(index, rows)
        self.assertEqual(rows[0][0], "read manga")
        db.readTaskDB(index2, rows)
        self.assertEqual(rows[1][1], "video game")

    def test_dbDelete(self):
        rows = []
        task = ("read manga", "shintaro kago", 0)
        index = db.addTaskDB(task)
        db.readTaskDB(index, rows)
        db.deleteTaskDB(index)
        rows = []
        db.readTaskDB(index, rows)
        self.assertEqual(len(rows), 0)

    def test_dbDeleteFail(self):
        rows = []
        task = ("read manga", "shintaro kago", 0)
        index = db.addTaskDB(task)
        db.readTaskDB(index, rows)
        db.closeDB()
        db.deleteTaskDB(index)
        db.initDB(dbPath, rows)
        rows = []
        db.readTaskDB(index, rows)
        self.assertEqual(len(rows), 1)


    def test_dbDeleteMultiple(self):
        rows1 = []
        rows2 = []
        task = ("read manga", "shintaro kago", 0)
        index = db.addTaskDB(task)
        task = ("play CS2", "video game", 1)
        index2 = db.addTaskDB(task)
        db.deleteTaskDB(index)
        db.deleteTaskDB(index2)
        db.readTaskDB(index, rows1)
        db.readTaskDB(index2, rows2)
        self.assertEqual(len(rows1), 0)
        self.assertEqual(len(rows2), 0)

    def test_dbUpdateName(self):
        rows = []
        task = ("read manga", "shintaro kago", 0)
        index = db.addTaskDB(task)
        db.updateTaskDB("name", "read HQ", index)
        db.readTaskDB(index, rows)
        self.assertEqual(rows[0][0], "read HQ")

    def test_dbUpdateDesc(self):
        rows = []
        task = ("read manga", "shintaro kago", 0)
        index = db.addTaskDB(task)
        db.updateTaskDB("description", "Preacher", index)
        db.readTaskDB(index, rows)
        self.assertEqual(rows[0][1], "Preacher")

    def test_dbUpdateStatus(self):
        rows = []
        task = ("read manga", "shintaro kago", 0)
        index = db.addTaskDB(task)
        db.updateTaskDB("status", 1, index)
        db.readTaskDB(index, rows)
        self.assertEqual(rows[0][2], 1)

    def test_dbUpdateFail(self):
        rows = []
        task = ("read manga", "shintaro kago", 0)
        index = db.addTaskDB(task)
        db.closeDB()
        db.updateTaskDB("status", 1, index)
        db.initDB(dbPath, rows)
        rows = []
        db.readTaskDB(index, rows)
        self.assertNotEqual(rows[0][2], 1)

    def test_dbReadFail(self):
        rows = []
        task = ("read manga", "shintaro kago", 0)
        index = db.addTaskDB(task)
        db.closeDB()
        db.readTaskDB(index, rows)
        self.assertEqual(len(rows), 0)

if __name__ == '__main__':
    unittest.main()

