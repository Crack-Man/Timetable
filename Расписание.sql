SELECT [Academic disciplines].Название,
       Groups.Название,
       ФИО,
       Rooms.Название,
       [Номер пары],
       [День недели],
       [Код практической подгруппы],
       [Код лабораторной подгруппы],
       [Тип занятия]
  FROM Timetable
       INNER JOIN
       [Academic disciplines] ON [Код занятия] = [Код дисциплины],
       Groups ON Timetable.[Код группы] = Groups.[Код группы],
       Teachers ON Timetable.[Код преподавателя] = Teachers.[Код преподавателя],
       Rooms ON Timetable.[Код помещения] = Rooms.[Код помещения];
