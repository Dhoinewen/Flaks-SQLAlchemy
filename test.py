import unittest
import app
from models import session, Student, Group, Course


class FlaskTest(unittest.TestCase):

    def setUp(self) -> None:
        self.__tester = app.app.test_client(self)

    def tearDown(self) -> None:
        del self.__tester

    def test_db_students(self):
        students = session.query(Student).all()
        self.assertEqual(len(students), 200)

    def test_index_students(self):
        responce = self.__tester.get('/students')
        statuscode = responce.status_code
        self.assertEqual(statuscode, 200)

    def test_index_student_course_put(self):
        responce = self.__tester.put('/students/111/courses?courses_id=5')
        statuscode = responce.status_code
        self.assertEqual(statuscode, 200)

    def test_db_before_put(self):
        student = session.query(Student).filter(Student.id == 111).first()
        student_courses = student.courses
        self.assertEqual(len(student_courses), 5)

    def test_index_student_course_delete(self):
        responce = self.__tester.delete('/students/111/courses?courses_id=5')
        statuscode = responce.status_code
        self.assertEqual(statuscode, 204)

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
        self.assertTrue(b'first_name' in responce.data)


if __name__ == '__main__':
    unittest.main()
