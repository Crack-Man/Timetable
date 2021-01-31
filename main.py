from sql_requests import Requests

db = Requests('timetable.db')
study_weeks = 18
exam_weeks = 2
teachers = db.get_teachers_busy()
rooms = db.get_rooms_busy()
timetable = db.get_timetable()

def busy_teacher(id_teacher, day_with_oddness, lesson):
    for teacher in teachers:
        if teacher[0] == id_teacher and teacher[1] == day_with_oddness and teacher[2] == lesson:
                return teacher[3]

def busy_room(type_of_room, day_with_oddness, lesson, quantity_of_students):
    for room in rooms:
        if room[1] == day_with_oddness and room[2] == lesson and room[3] == type_of_room and room[4] >= quantity_of_students and not room[5]:
            return room[0]
    return False

def busy_group(id_group, day_with_oddness, lesson, **kwargs):
    if len(kwargs) == 0:
        for double_class in timetable:
            if double_class[0] == id_group and double_class[1] == day_with_oddness and double_class[2] == lesson and double_class[3] != 0:
                return True
        return False
    elif 'practice_subgroups' in kwargs:
        for double_class in timetable:
            if double_class[0] == id_group and (not double_class[7] and not double_class[8] or double_class[7] == kwargs['practice_subgroups'] or double_class[8]) and double_class[1] == day_with_oddness and double_class[2] == lesson and double_class[3] != 0:
                return True
        return False
    elif 'laboratory_subgroups' in kwargs:
        for double_class in timetable:
            if double_class[0] == id_group and (not double_class[7] and not double_class[8] or double_class[7] or double_class[8] == kwargs['laboratory_subgroups']) and double_class[1] == day_with_oddness and double_class[2] == lesson and double_class[3] != 0:
                return True
        return False

def add_lesson(id_group, day_with_oddness, lesson, id_discipline, id_teacher, id_room, type_of_room, **kwargs):
    for double_class in timetable:
        if  len(kwargs) == 0:
            if double_class[0] == id_group and double_class[1] == day_with_oddness and double_class[2] == lesson and not double_class[7] and not double_class[8]:
                double_class[3] = id_discipline
                double_class[4] = id_teacher
                double_class[5] = id_room
                double_class[6] = type_of_room
        elif 'practice_subgroups' in kwargs:
            if double_class[0] == id_group and double_class[1] == day_with_oddness and double_class[2] == lesson and double_class[7] == kwargs['practice_subgroups']:
                double_class[3] = id_discipline
                double_class[4] = id_teacher
                double_class[5] = id_room
                double_class[6] = type_of_room
        elif 'laboratory_subgroups' in kwargs:
            if double_class[0] == id_group and double_class[1] == day_with_oddness and double_class[2] == lesson and double_class[7] == kwargs['laboratory_subgroups']:
                double_class[3] = id_discipline
                double_class[4] = id_teacher
                double_class[5] = id_room
                double_class[6] = type_of_room

    for teacher in teachers:
        if teacher[0] == id_teacher and teacher[1] == day_with_oddness and teacher[2] == lesson:
            teacher[3] = 1
    for room in rooms:
        if room[0] == id_room and room[1] == day_with_oddness and room[2] == lesson:
            room[5] = 1

def print_timetable():
    for double_class in timetable:
        print(double_class)


def print_active_timetable():
    for double_class in timetable:
        if double_class[3]:
            print(double_class)

def print_timetable_for_group(id_group):
    for double_class in timetable:
        if double_class[0] == id_group and double_class[3]:
            print(double_class)

def print_teachers_timetable():
    for teacher in teachers:
        print(teacher)

def print_teachers_timetable_for_teacher(id_teacher):
    for teacher in teachers:
        if teacher[0] == id_teacher:
            print(teacher)

def print_rooms():
    for room in rooms:
        print(room)

def allocation_of_week(hours, id_group, id_teacher, oddness, type_of_room, quantity_of_students, id_discipline, **kwargs):
    days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ"]
    lessons = [i for i in range(1, 9)]
    while hours > 0:
        is_searched = False
        for day in days:
            if not is_searched:
                day_with_oddness = day + " нечет" if oddness else day + " чет"
                for lesson in lessons:
                    if not is_searched:
                        if len(kwargs) == 0:
                            group_is_busy = busy_group(id_group, day_with_oddness, lesson)
                        elif 'practice_subgroups' in kwargs:
                            group_is_busy = busy_group(id_group, day_with_oddness, lesson, practice_subgroups=kwargs['practice_subgroups'])
                        elif 'laboratory_subgroups' in kwargs:
                            group_is_busy = busy_group(id_group, day_with_oddness, lesson, laboratory_subgroups=kwargs['laboratory_subgroups'])
                        if not group_is_busy:
                            if not busy_teacher(id_teacher, day_with_oddness, lesson):
                                id_room = busy_room(type_of_room, day_with_oddness, lesson, quantity_of_students)
                                if id_room:
                                    if len(kwargs) == 0:
                                        add_lesson(id_group, day_with_oddness, lesson, id_discipline, id_teacher, id_room, type_of_room)
                                    elif kwargs['practice_subgroups']:
                                        add_lesson(id_group, day_with_oddness, lesson, id_discipline, id_teacher, id_room, type_of_room, practice_subgroups=kwargs['practice_subgroups'])
                                    elif kwargs['laboratory_subgroups']:
                                        add_lesson(id_group, day_with_oddness, lesson, id_discipline, id_teacher, id_room, type_of_room, laboratory_subgroups=kwargs['laboratory_subgroups'])
                                    hours -= 1
                                    is_searched = True
                                    break

def toPer(hours):
    per_2weeks = hours / study_weeks
    return [int(per_2weeks // 2 + per_2weeks % 2), int(per_2weeks // 2)]

def create_timetable():
    for group in db.get_groups():
        id_group = group[0]
        name_of_group = group[1]
        quantity_of_students = group[3]
        # print(group)

        for discipline in db.get_disciplines_for_group(group[0]):
            id_discipline = discipline[0]
            name_of_discipline = discipline[1]
            hours_lections = discipline[2]
            hours_practice = discipline[3]
            hours_lab = discipline[4]
            id_teacher = discipline[5]
            lections_per_week, practice_per_week, lab_per_week = toPer(hours_lections), toPer(hours_practice), toPer(hours_lab)
            # print(lections_per_week, practice_per_week, lab_per_week)
            allocation_of_week(lections_per_week[0], id_group, id_teacher, 1, "Лекционный", quantity_of_students, id_discipline)
            allocation_of_week(lections_per_week[1], id_group, id_teacher, 0, "Лекционный", quantity_of_students, id_discipline)
            subgroups = db.get_subgroups(id_group)
            if len(subgroups[0]) != 0:
                for subgroup in subgroups[0]:
                    allocation_of_week(practice_per_week[0], id_group, id_teacher, 1, "Для практических", subgroup[3], id_discipline, practice_subgroups=subgroup[0])
                    allocation_of_week(practice_per_week[1], id_group, id_teacher, 0, "Для практических", subgroup[3], id_discipline, practice_subgroups=subgroup[0])
            if len(subgroups[1]) != 0:
                for subgroup in subgroups[1]:
                    allocation_of_week(lab_per_week[0], id_group, id_teacher, 1, "Лабораторный", subgroup[3], id_discipline, practice_subgroups=subgroup[0])
                    allocation_of_week(lab_per_week[1], id_group, id_teacher, 0, "Лабораторный", subgroup[3], id_discipline, practice_subgroups=subgroup[0])
    # print_timetable()
    print_active_timetable()
    # print_teachers_timetable_for_teacher(1)
    # print_rooms()

if __name__ == '__main__':
    create_timetable()