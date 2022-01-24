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
    for student_id in range(1, 201):
        student = session.query(Student).filter(Student.id == student_id).first()
        student.group_id = random.randint(1, 10)
        session.commit()


def relationship_from_student_to_courses():
    for student_id in range(1, 201):
        student = session.query(Student).filter(Student.id == student_id).first()
        for courses in range(random.randint(1, 3)):
            course = session.query(Course).filter(Course.id == random.randint(1, 10)).first()
            student.courses.append(course)
            session.commit()


