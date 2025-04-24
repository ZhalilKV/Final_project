import unittest
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class TestFitnessModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        cls.db = QSqlDatabase.addDatabase("QSQLITE")
        cls.db.setDatabaseName(":memory:")
        cls.db.open()


        query = QSqlQuery()
        query.exec_("""
            CREATE TABLE fitness (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                calories INTEGER,
                distance REAL,
                description TEXT
            )
        """)

    def test_insert_workout(self):
        query = QSqlQuery()
        query.prepare("INSERT INTO fitness (date, calories, distance, description) VALUES (?, ?, ?, ?)")
        query.addBindValue("2025-04-24")
        query.addBindValue(300)
        query.addBindValue(5.0)
        query.addBindValue("Morning jog")
        result = query.exec_()

        self.assertTrue(result)

    def test_fetch_workouts(self):
        query = QSqlQuery("SELECT * FROM fitness")
        count = 0
        while query.next():
            count += 1
            self.assertEqual(query.value(1), "2025-04-24")
            self.assertEqual(query.value(2), 300)
            self.assertEqual(query.value(3), 5.0)
            self.assertEqual(query.value(4), "Morning jog")
            self.assertGreater(count, 0)

    def test_delete_workout(self):

        query = QSqlQuery()
        query.prepare("INSERT INTO fitness (date, calories, distance, description) VALUES (?, ?, ?, ?)")
        query.addBindValue("2025-04-25")
        query.addBindValue(400)
        query.addBindValue(6.0)
        query.addBindValue("Evening run")
        query.exec_()


        last_id = query.lastInsertId()


        delete_query = QSqlQuery()
        delete_query.prepare("DELETE FROM fitness WHERE id = ?")
        delete_query.addBindValue(last_id)
        result = delete_query.exec_()

        self.assertTrue(result)


        check_query = QSqlQuery()
        check_query.prepare("SELECT * FROM fitness WHERE id = ?")
        check_query.addBindValue(last_id)
        check_query.exec_()

        self.assertFalse(check_query.next())

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

if __name__ == '__main__':
    unittest.main()

