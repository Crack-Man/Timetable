import sqlite3

class Requests:
    def __init__(self, database_file):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_groups(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM [Groups]").fetchall()

    def get_disciplines_for_group(self, id_group):
        with self.connection:
            return self.cursor.execute("SELECT [Disciplines of groups].[Код дисциплины], [Название], [Кол-во часов на лекцию], [Кол-во часов на практику], [Кол-во часов на лабораторные], [Код преподавателя]"
                                        "FROM [Academic disciplines]"
                                        "INNER JOIN [Disciplines of groups] ON [Academic disciplines].[Код дисциплины] = [Disciplines of groups].[Код дисциплины]"
                                        "WHERE [Код группы] = ?", (id_group,)).fetchall()

    def busy_group(self, id_group, lesson, day):
        with self.connection:
            return self.cursor.execute("SELECT * FROM [Timetable] WHERE [Код группы] = ? AND [Номер пары] = ? AND [День недели] = ?", (id_group, lesson, day,)).fetchone()

    def busy_teacher(self, id_teacher, lesson, day):
        with self.connection:
            return self.cursor.execute("SELECT * FROM [Timetable] WHERE [Код преподавателя] = ? AND [Номер пары] = ? AND [День недели] = ?", (id_teacher, lesson, day,)).fetchone()

    def get_rooms(self, type_of_room, quantity_of_students):
        with self.connection:
            return self.cursor.execute("SELECT * FROM [Rooms] WHERE [Тип] = ? AND [Вместимость] >= ?", (type_of_room, quantity_of_students,)).fetchall()

    def get_busy_rooms(self, lesson, day):
        with self.connection:
            return self.cursor.execute("SELECT [Код помещения] FROM [Timetable] WHERE [Номер пары] = ? AND [День недели] = ?", (lesson, day,)).fetchall()