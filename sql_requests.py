import sqlite3

class Requests:
    def __init__(self, database_file):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_teachers(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `teachers`").fetchall()