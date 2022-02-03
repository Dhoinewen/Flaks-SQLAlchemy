from models import session, Student, Group, Course
from sqlalchemy import func


def delete_course_from_student(student_id, course_name):
    print(student_id, course_name)
    student = session.query(Student).filter(Student.id == student_id).first()
    course = session.query(Course).filter(Course.name == course_name).first()
    student.courses.remove(course)
    session.commit()
    return student.courses


def add_new_student(first_name, last_name):
    sample_student = {'first_name': first_name, 'last_name': last_name}
    student = Student(**sample_student)
    session.add(student)
    session.commit()
    student = session.query(Student).filter(Student.first_name == first_name).first()
    return student


def add_course_to_student(student_id, course_name):
    student = session.query(Student).filter(Student.id == student_id).first()
    course = session.query(Course).filter(Course.name == course_name).first()
    student.courses.append(course)
    session.commit()
    return student


def delete_solo_student_from_db(student_id):
    student = session.query(Student).filter(Student.id == student_id).first()
    session.delete(student)
    session.commit()
    return student


def get_solo_student_from_db(student_id):
    student = session.query(Student).filter(Student.id == student_id).first()
    if student is None:
        return None
    sample = {'first_name': student.first_name,
              'last_name': student.last_name,
              'id': student.id,
              'courses': student.courses,
              'group': student.group}
    return sample


def get_students_data_from_db(course_name):
    students_list = list()
    if course_name is None:
        students = session.query(Student).all()
    else:
        students = session.query(Student).filter(Student.courses.any(Course.name == course_name)).all()
    for student in students:
        sample = {
            'first_name': student.first_name,
            'last_name': student.last_name,
            'id': student.id,
            'courses': student.courses,
            'group': student.group
        }
        students_list.append(sample)
    return students_list


def get_groups_data_from_db(less_than):
    groups_list = list()
    if less_than is None:
        groups = session.query(Group).all()
    else:
        groups = session.query(Group).join(Student).group_by(Group).having(func.count(Group.students) < less_than).all()
    for group in groups:
        sample = {
            'id': group.id,
            'name': group.name,
            'students': group.students
        }
        groups_list.append(sample)
    return groups_list
