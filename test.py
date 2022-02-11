import json
import unittest
import app
import random

from models import session, Student, Group, Course


class FlaskTest(unittest.TestCase):

    def setUp(self) -> None:
        self.__tester = app.app.test_client(self)
        sample_student = {'first_name': 'test', 'last_name': 'case'}
        student = Student(**sample_student)
        session.add(student)
        session.commit()
        course = session.query(Course).filter(Course.id == random.randint(1, 9)).first()
        student.courses.append(course)
        session.commit()

    def tearDown(self) -> None:
        del self.__tester
        session.query(Student).filter(Student.first_name == 'test').delete()
        session.commit()

    def test_db_students(self):
        students = session.query(Student).all()
        self.assertEqual(len(students), 198)

    def test_index_students(self):
        responce = self.__tester.get('/students')
        statuscode = responce.status_code
        self.assertEqual(statuscode, 200)

    def test_db_before_put(self):
        student = session.query(Student).filter(Student.id == 111).first()
        student_courses = student.courses
        self.assertEqual(len(student_courses), 3)

    def test_index_student_course_put(self):
        courses_id = [1, 2, 3, 4, 5, 6, 7, 8, 9,]
        student = session.query(Student).filter(Student.first_name == 'test').first()
        student_id = student.id
        student_courses_before = len(student.courses)
        courses_id = {'courses_id': random.sample(courses_id, 3)}
        headers = {'content-type': 'application/json'}
        responce = self.__tester.put(f'/students/{student_id}/courses', data=json.dumps(courses_id), headers=headers)
        statuscode = responce.status_code
        student = session.query(Student).filter(Student.first_name == 'test').first()
        student_courses_after = len(student.courses)
        self.assertEqual(statuscode, 200)
        self.assertLess(student_courses_before, student_courses_after)

    def test_index_student_course_delete(self):
        student = session.query(Student).filter(Student.first_name == 'test').first()
        student_id = student.id
        course_for_delete = random.choice(student.courses)
        student_courses_before = len(student.courses)
        responce = self.__tester.delete(f'/students/{student_id}/courses/{course_for_delete.id}')
        statuscode = responce.status_code
        student = session.query(Student).filter(Student.first_name == 'test').first()
        student_courses_after = len(student.courses)
        self.assertEqual(statuscode, 204)
        self.assertLess(student_courses_after, student_courses_before)

    def test_index_student_solo(self):
        responce = self.__tester.get('/students/112')
        statuscode = responce.status_code
        self.assertEqual(statuscode, 200)

    def test_index_student_courses(self):
        responce = self.__tester.get('/students/111/courses')
        statuscode = responce.status_code
        self.assertEqual(statuscode, 200)

    def test_index_data(self):
        responce = self.__tester.get('/students')
        self.assertTrue(b'first_name' and b'last_name' and b'courses' in responce.data)


if __name__ == '__main__':
    unittest.main()
