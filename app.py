from flask import Flask, Response
from flask_restful import Api, Resource, reqparse
from helpers import convert_to_json
from get_data import get_students_data_from_db, get_groups_data_from_db, get_solo_student_from_db,\
    delete_solo_student_from_db, add_courses_to_student, add_new_student, delete_course_from_student,\
    get_student_courses, find_student


app = Flask(__name__)
api = Api(app)
parser_group = reqparse.RequestParser()
parser_group.add_argument('less_than')

parser_course = reqparse.RequestParser()
parser_course.add_argument('courses_id', type=int, action='append')

parser_student_data = reqparse.RequestParser()
parser_student_data.add_argument('first_name', type=str)
parser_student_data.add_argument('last_name', type=str)


class StudentSolo(Resource):
    def get(self, student_id):
        student = get_solo_student_from_db(student_id)
        if student is None:
            return 404
        else:
            return Response(convert_to_json(student), mimetype='application/json')

    def delete(self, student_id):
        delete_solo_student_from_db(student_id)
        return '', 204


class StudentCourses(Resource):
    def get(self, student_id):
        student = get_student_courses(student_id)
        if student is None:
            return '', 404
        else:
            return student

    def delete(self, student_id):
        args = parser_course.parse_args()
        delete_course_from_student(student_id, args['courses_id'])
        return '', 204

    def put(self, student_id):
        student = find_student(student_id)
        if student is None:
            return '', 404
        else:
            args = parser_course.parse_args()
            add_courses_to_student(student, args['courses_id'])
            return get_student_courses(student_id)


class StudentList(Resource):
    def get(self):
        args = parser_course.parse_args()
        return Response(convert_to_json(get_students_data_from_db(args['courses_id'])), mimetype='application/json')

    def put(self):
        args = parser_student_data.parse_args()
        return Response(convert_to_json(add_new_student(args['first_name'], args['last_name'])),
                        mimetype='application/json')


class GroupList(Resource):
    def get(self):
        args = parser_group.parse_args()
        return Response(convert_to_json(get_groups_data_from_db(args['less_than'])), mimetype='application/json')


api.add_resource(StudentCourses, '/students/<student_id>/courses')
api.add_resource(StudentSolo, '/students/<student_id>')
api.add_resource(StudentList, '/students')
api.add_resource(GroupList, '/groups')


if __name__ == '__main__':
    app.run(debug=True)
