from models import session, Course, Student, Group
from names import get_last_name, get_first_name

"""course = Course(name='history')
session.add(course)
session.commit()

student = Student(first_name=get_first_name('male'), last_name=get_last_name())"""
"""session.add(student)
session.commit()"""
"""print(student.courses)"""
"""student.courses.append(course)
session.commit()"""

rows = session.query(Student).all()
print(rows)