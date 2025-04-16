import unittest
from unittest.mock import Mock
from unittest.mock import patch
from utils import validateTaskInput
import tasks
import db
import os

dbPath = 'db_test.db'

class TestValidateInput(unittest.TestCase):

    def test_validateASCii(self):
        string = 'Read Book'
        result = validateTaskInput(string)
        self.assertEqual(result, True)

    def test_validateEmpty(self):
        string = ''
        result = validateTaskInput(string)
        self.assertEqual(result, False)

    def test_validateNonAscii(self):
        string = '34€3^^7'
        result = validateTaskInput(string)
        self.assertEqual(result, False)

    @patch("db.addTaskDB")
    def test_addTaskToDB(self, mock):
        mock.return_value = 1
        task = tasks.Task("read manga", "shintaro kago")
        result = task.addToDB()
        self.assertEqual(result, True)

    @patch("db.addTaskDB")
    def test_addTaskToDBFail(self, mock):
        mock.return_value = -1
        task = tasks.Task("read manga", "shintaro kago")
        result = task.addToDB()
        self.assertEqual(result, False)

    @patch("db.updateTaskDB")
    def test_setDesc(self, mock):
        mock.return_value = True
        task = tasks.Task("read manga", "shintaro kago")
        task.setDescription("newDesc")
        self.assertEqual("newDesc", task.getDescription())

    @patch("db.updateTaskDB")
    def test_setDescFail(self, mock):
        mock.return_value = False
        task = tasks.Task("read manga", "shintaro kago")
        task.setDescription("newDesc")
        self.assertNotEqual("newDesc", task.getDescription())

    @patch("db.updateTaskDB")
    def test_setDescUnchanged(self, mock):
        mock.return_value = False
        task = tasks.Task("read manga", "shintaro kago")
        task.setDescription("newDesc")
        self.assertEqual("shintaro kago", task.getDescription())

    @patch("db.updateTaskDB")
    def test_setName(self, mock):
        mock.return_value = True
        task = tasks.Task("read manga", "shintaro kago")
        task.setName("newName")
        self.assertEqual("newName", task.getName())

    @patch("db.updateTaskDB")
    def test_setNameFail(self, mock):
        mock.return_value = False
        task = tasks.Task("read manga", "shintaro kago")
        task.setName("newName")
        self.assertNotEqual("newName", task.getName())

    @patch("db.updateTaskDB")
    def test_setNameUnchanged(self, mock):
        mock.return_value = False
        task = tasks.Task("read manga", "shintaro kago")
        task.setName("newName")
        self.assertEqual("read manga", task.getName())

    @patch("db.updateTaskDB")
    def test_setStatus(self, mock):
        mock.return_value = True
        task = tasks.Task("read manga", "shintaro kago")
        st = tasks.TaskStatus(2)
        task.setStatus(st)
        self.assertEqual(st, task.getStatus())

    @patch("db.updateTaskDB")
    def test_setStatusFail(self, mock):
        mock.return_value = False
        task = tasks.Task("read manga", "shintaro kago")
        st = tasks.TaskStatus(2)
        task.setStatus(st)
        self.assertNotEqual(st, task.getStatus())

    @patch("db.updateTaskDB")
    def test_setStatusUnchanged(self, mock):
        mock.return_value = False
        task = tasks.Task("read manga", "shintaro kago")
        st = tasks.TaskStatus(2)
        task.setStatus(st)
        self.assertEqual(tasks.TaskStatus(0), task.getStatus())

    @patch("tasks.Task.addToDB")
    def test_addTask(self, mock):
        mock.return_value = True
        returnv = tasks.addTask('read manga', 'shintaro kago')
        self.assertEqual(returnv, True)

    @patch("tasks.Task.addToDB")
    def test_addTaskFail(self, mock):
        mock.return_value = False
        returnv = tasks.addTask('read manga', 'shintaro kago')
        self.assertEqual(returnv, False)

    def test_UpdateOptionFail(self):
        returnValue = tasks.updateTask(4, 1, 'anything')
        self.assertEqual(returnValue, False)


    @patch("tasks.Task.setName", return_value = True)
    @patch("db.addTaskDB", return_value = 1)
    def test_updateName(self, mock, mock2):
        tasks.addTask("read manga", "anything")
        returnValue = tasks.updateTask(tasks.updateOption.Name.value, 1, 'anything')
        self.assertEqual(returnValue, True)

    @patch("tasks.Task.setName", return_value = True)
    @patch("db.addTaskDB", return_value = 1)
    def test_updateName(self, mock, mock2):
        tasks.addTask("read manga", "anything")
        returnValue = tasks.updateTask(tasks.updateOption.Description.value, 1, 'shintaro kago')
        self.assertEqual(returnValue, True)

    @patch("tasks.Task.setName", return_value = True)
    @patch("db.addTaskDB", return_value = 1)
    def test_updateName(self, mock, mock2):
        tasks.addTask("read manga", "anything")
        returnValue = tasks.updateTask(tasks.updateOption.Status.value, 1, 2)
        self.assertEqual(returnValue, True)

    @patch("tasks.Task.setName", return_value = True)
    @patch("db.addTaskDB", return_value = 1)
    def test_updateName(self, mock, mock2):
        # tasks.addTask("read manga", "anything")
        returnValue = tasks.updateTask(tasks.updateOption.Status.value, 1, 2)
        self.assertEqual(returnValue, False)

    def test_deleteTaskFail(self):
        returnValue = tasks.deleteTask(2)
        self.assertEqual(returnValue, False)

    @patch("db.addTaskDB", return_value = 1)
    def test_deleteTask(self, mock):
        tasks.addTask("read manga", "anything")
        returnValue = tasks.deleteTask(1)
        self.assertEqual(returnValue, True)

if __name__ == '__main__':
    unittest.main()



