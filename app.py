from flask import Flask, Response
from flask_restful import Api, Resource, reqparse
from helpers import convert_to_xml
from get_data import get_students_data_from_db, get_groups_data_from_db, get_solo_student_from_db,\
    delete_solo_student_from_db, add_course_to_student, add_new_student, delete_course_from_student


app = Flask(__name__)
api = Api(app)
parser_group = reqparse.RequestParser()
parser_student = reqparse.RequestParser()
parser_student_data = reqparse.RequestParser()
parser_delete_course_for_student = reqparse.RequestParser()
parser_group.add_argument('less_than')
parser_student.add_argument('course_name')
parser_student_data.add_argument('student_data', action='append')
parser_delete_course_for_student.add_argument('delete_course_name')


class StudentSolo(Resource):
    def get(self, student_id):
        return Response(convert_to_xml(get_solo_student_from_db(student_id)), mimetype='text/xml')

    def delete(self, student_id):
        return Response(convert_to_xml(delete_solo_student_from_db(student_id)), mimetype='text/xml')

    def put(self, student_id):
        if parser_student.parse_args() is not None:
            args = parser_student.parse_args()
            return Response(convert_to_xml(add_course_to_student(student_id, args['course_name'])), mimetype='text/xml')
        if parser_delete_course_for_student.parse_args() is not None:
            args = parser_delete_course_for_student.parse_args()
            return Response(convert_to_xml(delete_course_from_student(student_id, args['delete_course_name'])),
                            mimetype='text/xml')


class StudentList(Resource):
    def get(self):
        args = parser_student.parse_args()
        return Response(convert_to_xml(get_students_data_from_db(args['course_name'])), mimetype='text/xml')

    def put(self):
        args = parser_student_data.parse_args()
        return Response(convert_to_xml(add_new_student(args['student_data'][0], args['student_data'][1])),
                        mimetype='text/xml')


class GroupList(Resource):
    def get(self):
        args = parser_group.parse_args()
        return Response(convert_to_xml(get_groups_data_from_db(args['less_than'])), mimetype='text/xml')


api.add_resource(StudentSolo, '/students/<student_id>')
api.add_resource(StudentList, '/students')
api.add_resource(GroupList, '/groups')


if __name__ == '__main__':
    app.run(debug=True)
