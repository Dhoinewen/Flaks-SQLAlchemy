from flask import Flask, Response
from flask_restful import Api, Resource, abort, reqparse
from models import session, Student, Group, Course
from helpers import convert_to_xml
from get_data import get_students_data_from_db, get_groups_data_from_db


app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('student_id')
parser.add_argument('less_than')


class StudentSolo(Resource):
    def get(self):
        args = parser.parse_args()
        student = session.query(Student).filter(Student.id == args['student_id']).first()
        return Response(student.first_name)


class StudentList(Resource):
    def get(self):
        args = parser.parse_args()
        return Response(convert_to_xml(get_students_data_from_db()), mimetype='text/xml')


class GroupList(Resource):
    def get(self):
        args = parser.parse_args()
        print(args['less_than'])
        return Response(convert_to_xml(get_groups_data_from_db(args['less_than'])), mimetype='text/xml')


api.add_resource(StudentSolo, '/student')
api.add_resource(StudentList, '/student_list')
api.add_resource(GroupList, '/group_list')


if __name__ == '__main__':
    app.run(debug=True)
