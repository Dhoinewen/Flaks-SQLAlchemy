from models import session, Student, Group, Course


def get_students_data_from_db():
    students_list = list()
    students = session.query(Student).all()
    for student in students:
        dict = {'first_name': student.first_name,
                'last_name': student.last_name,
                'id': student.id,
                'courses': student.courses,
                'group_id': student.group_id}
        students_list.append(dict)
    return students_list


def get_groups_data_from_db(less_than):
    groups_list = list()
    groups = session.query(Group).all()
    if less_than is not None:
        for group in groups:
            if len(group.students) < int(less_than):
                groups.remove(group)

    for group in groups:
        dict = {'id': group.id,
                'name': group.name,
                'students': group.students,
                'number of students': len(group.students)}
        groups_list.append(dict)
    return groups_list
