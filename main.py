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
            if double_class[0] == id_group and double_class[1] == day_with_oddness and double_class[2] == lesson and double_class[8] == kwargs['laboratory_subgroups']:
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

def print_timetable_for_group(id_group, *args):
    for double_class in timetable:
        if double_class[0] == id_group and double_class[3]:
            if len(args) == 1:
                day = str(args[0])
                if double_class[1] == day:
                    print(double_class)
            else:
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

def more_5_for_group(id_group, day):
    count = 0
    for double_class in timetable:
        if double_class[0] == id_group and double_class[1] == day and double_class[3]:
            count += 1
    return count >= 5

def more_5_for_teacher(id_teacher, day):
    count = 0
    for double_class in timetable:
        if double_class[4] == id_teacher and double_class[1] == day and double_class[3]:
            count += 1
    return count >= 5

def more_1_window_group(id_group, day, lesson, **kwargs):
    active_lesson_group = 0
    for double_class in timetable:
        if double_class[0] == id_group and double_class[1] == day and double_class[3]:
            if len(kwargs) == 0:
                active_lesson_group = double_class[2]
            elif 'practise_subgroups' in kwargs:
                if not double_class[7] and not double_class[8] or double_class[7] == kwargs['practise_subgroups']:
                    active_lesson_group = double_class[2]
            elif 'laboratory_subgroups' in kwargs:
                if not double_class[7] and not double_class[8] or double_class[8] == kwargs['laboratory_subgroups']:
                    active_lesson_group = double_class[2]
    if active_lesson_group:
        return lesson - active_lesson_group > 1
    return False

def more_1_window_teacher(id_teacher, day, lesson):
    active_lesson_teacher = 0
    for double_class in timetable:
        if double_class[4] == id_teacher and double_class[1] == day and double_class[3]:
            active_lesson_teacher = double_class[2]
    if active_lesson_teacher:
        return lesson - active_lesson_teacher > 1
    return False

def allocation_of_week(hours, id_group, id_teacher, oddness, type_of_room, quantity_of_students, id_discipline, **kwargs):
    days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ"]
    lessons = [i for i in range(1, 9)]
    while hours > 0:
        is_searched = False
        for day in days:
            if not is_searched:
                day_with_oddness = day + " нечет" if oddness else day + " чет"
                if not more_5_for_group(id_group, day_with_oddness) and not more_5_for_teacher(id_teacher, day_with_oddness):
                    for lesson in lessons:
                        if not is_searched:
                            if len(kwargs) == 0:
                                more_1_group = more_1_window_group(id_group, day_with_oddness, lesson)
                            elif 'practice_subgroups' in kwargs:
                                more_1_group = more_1_window_group(id_group, day_with_oddness, lesson, practise_subgroups=kwargs['practice_subgroups'])
                            elif 'laboratory_subgroups' in kwargs:
                                more_1_group = more_1_window_group(id_group, day_with_oddness, lesson, laboratory_subgroups=kwargs['laboratory_subgroups'])
                            more_1_teacher = more_1_window_teacher(id_teacher, day_with_oddness, lesson)
                            if not more_1_group and not more_1_teacher:
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
                                            elif 'practice_subgroups' in kwargs:
                                                add_lesson(id_group, day_with_oddness, lesson, id_discipline, id_teacher, id_room, type_of_room, practice_subgroups=kwargs['practice_subgroups'])
                                            elif 'laboratory_subgroups' in kwargs:
                                                add_lesson(id_group, day_with_oddness, lesson, id_discipline, id_teacher, id_room, type_of_room, laboratory_subgroups=kwargs['laboratory_subgroups'])
                                            hours -= 1
                                            is_searched = True
                                            break
        if not is_searched:
            print("Не удалось найти свободное время для дисциплины {} группы {}".format(id_discipline, id_group))
            break

def toPer(hours):
    """
    Изначальная формула: (hours / 2) / (study_weeks / 2),
    так как один академический час равен 45 минутам, т.е. hours / 2 считаются за пары.
    С другой стороны, мы рассчитываем пары недель, т.е. study_weeks / 2, значение которого включает четную и нечетную недели
    """
    per_2weeks = hours / study_weeks
    return [int(per_2weeks // 2 + per_2weeks % 2), int(per_2weeks // 2)]

def fill_in_table():
    for double_class in timetable:
        if double_class[3]:
            db.fill_in_timetable(double_class[3], double_class[0], double_class[4], double_class[5], double_class[2], double_class[1], double_class[7], double_class[8], double_class[6])

def create_timetable():
    db.clean_timetable()
    for group in db.get_groups():
        id_group = group[0]
        name_of_group = group[1]
        quantity_of_students = group[3]

        for discipline in db.get_disciplines_for_group(group[0]):
            id_discipline = discipline[0]
            name_of_discipline = discipline[1]
            hours_lections = discipline[2]
            hours_practice = discipline[3]
            hours_lab = discipline[4]
            id_teacher = discipline[5]
            lections_per_week, practice_per_week, lab_per_week = toPer(hours_lections), toPer(hours_practice), toPer(hours_lab)
            allocation_of_week(lections_per_week[0], id_group, id_teacher, 1, "Лекционный", quantity_of_students, id_discipline)
            allocation_of_week(lections_per_week[1], id_group, id_teacher, 0, "Лекционный", quantity_of_students, id_discipline)
            subgroups = db.get_subgroups(id_group)
            if len(subgroups[0]) != 0:
                for subgroup in subgroups[0]:
                    allocation_of_week(practice_per_week[0], id_group, id_teacher, 1, "Для практических", subgroup[3], id_discipline, practice_subgroups=subgroup[0])
                    allocation_of_week(practice_per_week[1], id_group, id_teacher, 0, "Для практических", subgroup[3], id_discipline, practice_subgroups=subgroup[0])
            if len(subgroups[1]) != 0:
                for subgroup in subgroups[1]:
                    allocation_of_week(lab_per_week[0], id_group, id_teacher, 1, "Лабораторный", subgroup[3], id_discipline, laboratory_subgroups=subgroup[0])
                    allocation_of_week(lab_per_week[1], id_group, id_teacher, 0, "Лабораторный", subgroup[3], id_discipline, laboratory_subgroups=subgroup[0])
    # print_timetable()
    # print_active_timetable()
    # print_teachers_timetable_for_teacher(1)
    # print_rooms()
    print_timetable_for_group(2, "ПН нечет")
    fill_in_table()

if __name__ == '__main__':
    create_timetable()