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

    def test_index_students(self):
        responce = self.__tester.get('/students')
        statuscode = responce.status_code
        self.assertEqual(statuscode, 200)

    def test_index_student_course_put(self):
        courses_id = [1, 2, 3, 4, 5, 6, 7, 8, 9]
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

    def test_index_and_data_student_solo(self):
        student = session.query(Student).filter(Student.first_name == 'test').first()
        student_id = student.id
        responce = self.__tester.get(f'/students/{student_id}')
        statuscode = responce.status_code
        json_data = responce.json
        self.assertEqual(statuscode, 200)
        self.assertTrue('test' in json_data['first_name'])
        self.assertTrue('case' in json_data['last_name'])
        self.assertNotEqual(json_data['courses'], None)
        self.assertEqual(None, json_data['group'])

    def test_index_student_courses(self):
        student = session.query(Student).filter(Student.first_name == 'test').first()
        student_id = student.id
        responce = self.__tester.get(f'/students/{student_id}/courses')
        statuscode = responce.status_code
        self.assertEqual(statuscode, 200)

    def test_index_data(self):
        responce = self.__tester.get('/students')
        self.assertTrue(b'first_name' and b'last_name' and b'courses' in responce.data)


if __name__ == '__main__':
    unittest.main()