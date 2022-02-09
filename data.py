import random

from models import session, Student, Group, Course
from names import get_last_name, get_first_name



def students_data():
    for student in range(200):
        random_student = {'first_name': get_first_name(), 'last_name': get_last_name()}
        students = Student(**random_student)
        session.add(students)
        session.commit()


def groups_data():
    group_names = ['Tigers-12', 'Beers-23', 'Raccoons-32', 'Squirrels-48', 'Cats-54', 'Lions-64', 'Wolves-76',
                   'Owls-85', 'Elephants-92', 'Mice-41']
    for group in group_names:
        groups = Group(name=group)
        session.add(groups)
        session.commit()


def course_data():
    course_names = ['mathematics', 'physics', 'chemistry', 'history', 'literature', 'biology', 'algebra', 'geometry',
                    'informatics', 'metrology']
    for course in course_names:
        courses = Course(name=course)
        session.add(courses)
        session.commit()


def relationship_from_group_to_student():
    groups_list = session.query(Group).all()
    students_list = session.query(Student).all()
    for student in students_list:
        student.group = random.choice(groups_list).id
        session.commit()


def relationship_from_student_to_courses():
    students_list = session.query(Student).all()
    courses_list = session.query(Course).all()
    for student in students_list:
        for course in range(random.randint(1, 3)):
            student.courses.append(random.choice(courses_list))
            session.commit()


def create_data():
    students_data()
    groups_data()
    course_data()
    relationship_from_group_to_student()
    relationship_from_student_to_courses()


create_data()
