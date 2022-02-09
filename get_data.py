from models import session, Student, Group, Course
from sqlalchemy import func


def get_student_courses(student_id):
    course_list = []
    student = session.query(Student).filter(Student.id == student_id).first()
    if student is None:
        return None
    else:
        for courses in student.courses:
            sample = {
                'Name': courses.name,
                'Id': courses.id
            }
            course_list.append(sample)
        return course_list


def delete_course_from_student(student_id, course_id):
    student = session.query(Student).filter(Student.id == student_id).first()
    course = session.query(Course).filter(Course.id == course_id[0]).first()
    if student and course is None:
        return None
    else:
        student.courses.remove(course)
        session.commit()
        return student.courses


def add_new_student(first_name, last_name):
    sample_student = {'first_name': first_name, 'last_name': last_name}
    student = Student(**sample_student)
    session.add(student)
    session.commit()
    return student


def find_student(student_id):
    student = session.query(Student).filter(Student.id == student_id).first()
    return student


def add_courses_to_student(student, courses_id):
    for course_id in courses_id:
        course = session.query(Course).filter(Course.id == course_id).first()
        if student.courses.count(course) <= 0:
            student.courses.append(course)
    session.commit()


def delete_solo_student_from_db(student_id):
    session.query(Student).filter(Student.id == student_id).delete()
    session.commit()


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


def get_students_data_from_db(course_id):
    students_list = []
    if course_id is None:
        students = session.query(Student).all()
    else:
        students = session.query(Student).filter(Student.courses.any(Course.id == course_id)).all()
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
    groups_list = []
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
