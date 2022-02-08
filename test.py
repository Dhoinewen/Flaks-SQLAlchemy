import unittest
import app


class FlaskTest(unittest.TestCase):

    def setUp(self) -> None:
        self.__tester = app.app.test_client(self)

    def tearDown(self) -> None:
        del self.__tester

    def test_index(self):
        responce = self.__tester.get('/students')
        statuscode = responce.status_code
        self.assertEqual(statuscode, 200)

    def test_index_groups(self):
        responce = self.__tester.get('/groups')
        statuscode = responce.status_code
        self.assertEqual(statuscode, 200)

    def test_index_student(self):
        responce = self.__tester.get('/students')
        statuscode = responce.status_code
        self.assertEqual(statuscode, 200)

    def test_index_student_solo(self):
        responce = self.__tester.get('/students/111')
        statuscode = responce.status_code
        self.assertEqual(statuscode, 200)

    def test_index_student_courses(self):
        responce = self.__tester.get('/students/111/courses')
        statuscode = responce.status_code
        self.assertEqual(statuscode, 200)

    def test_index_content_json(self):
        responce = self.__tester.get('/students')
        self.assertEqual(responce.content_type, 'application/json')

    def test_index_content_xml(self):
        responce = self.__tester.get('/groups')
        self.assertEqual(responce.content_type, 'application/json')

    def test_index_data(self):
        responce = self.__tester.get('/students')
        self.assertTrue(b'first_name' in responce.data)


if __name__ == '__main__':
    unittest.main()
