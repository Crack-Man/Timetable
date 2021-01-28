from sql_requests import Requests

db = Requests('timetable.db')
study_weeks = 18
exam_weeks = 2

def toPer(hours):
    per_2weeks = hours / study_weeks
    return [int(per_2weeks // 2 + per_2weeks % 2), int(per_2weeks // 2)]

def allocation_of_week(hours, id_group, id_teacher, oddness, type_of_room, quantity_of_students):
    days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ"]
    lessons = [i for i in range(1, 9)]
    timetable = []
    while hours > 0:
        is_searched = False
        for day in days:
            if not is_searched:
                day_with_oddness = day + " нечет" if oddness else day + " чет"
                for lesson in lessons:
                    if not is_searched:
                        if not db.busy_group(id_group, lesson, day_with_oddness) and not db.busy_teacher(id_teacher, lesson, day_with_oddness):
                            rooms = db.get_rooms(type_of_room, quantity_of_students)
                            busy_rooms = db.get_busy_rooms(lesson, day)
                            code_of_rooms = []
                            code_of_busy_rooms = []
                            for room in rooms:
                                code_of_rooms.append(room[0])
                            for room in busy_rooms:
                                code_of_busy_rooms.append(room[3])
                            for code_of_room in code_of_rooms:
                                if not code_of_room in code_of_busy_rooms:
                                    timetable.append([id_group, id_teacher, lesson, day_with_oddness, code_of_room])
                                    hours -= 1
                                    is_searched = True
                                    break
    return timetable


def create_timetable():
    for group in db.get_groups():
        id_group = group[0]
        name_of_group = group[1]
        quantity_of_students = group[3]
        # print(group)
        timetable = []
        for discipline in db.get_disciplines_for_group(group[0]):
            # print(discipline)
            id_discipline = discipline[0]
            name_of_discipline = discipline[1]
            hours_lections = discipline[2]
            hours_practice = discipline[3]
            hours_lab = discipline[4]
            id_teacher = discipline[5]
            lections_per_week, practice_per_week, lab_per_week = toPer(hours_lections), toPer(hours_practice), toPer(hours_lab)
            # print(lections_per_week, practice_per_week, lab_per_week)
            timetable.append(allocation_of_week(lections_per_week[0], id_group, id_teacher, 1, "Лекционный", quantity_of_students))
            # function(lections_per_week[0])
    print(timetable)

if __name__ == '__main__':
    create_timetable()