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

    def get_rooms_busy(self):
        with self.connection:
            rooms_tuple = self.cursor.execute("SELECT [Код помещения], [День недели], [Номер пары], [Тип], [Вместимость], 0 AS [Занятость] FROM [Rooms], [Days of the week], [Call schedule]").fetchall()
        rooms_list = []
        for room in rooms_tuple:
            rooms_list.append(list(room))
        return rooms_list

    def get_teachers_busy(self):
        with self.connection:
            teachers_tuple = self.cursor.execute("SELECT [Код преподавателя], [День недели], [Номер пары], 0 AS [Занятость] FROM [Teachers], [Days of the week], [Call schedule]").fetchall()
        teachers_list = []
        for teacher in teachers_tuple:
            teachers_list.append(list(teacher))
        return teachers_list

    def get_timetable(self):
        with self.connection:
            timetable_tuple = self.cursor.execute("SELECT [Код группы], [День недели], [Номер пары], 0 AS [Код дисциплины], "
                                                  "0 AS [Код преподавателя], 0 AS [Код помещения], 0 AS Тип, 0 AS [Код практической подгруппы], 0 AS [Код лаборатнорной подгруппы]  "
                                                   "FROM [Groups], [Days of the week], [Call schedule]"
                                                    ).fetchall()
        timetable_list = []
        for double_class in timetable_tuple:
            timetable_list.append(list(double_class))
        return timetable_list

    def get_subgroups(self, id_group):
        with self.connection:
            practice = self.cursor.execute("SELECT * FROM [Practice subgroups] WHERE [Код группы] = ?", (id_group,)).fetchall()
            lab = self.cursor.execute("SELECT * FROM [Laboratory subgroups] WHERE [Код группы] = ?", (id_group,)).fetchall()
        subgroups = []
        subgroups.append(practice)
        subgroups.append(lab)
        return subgroups