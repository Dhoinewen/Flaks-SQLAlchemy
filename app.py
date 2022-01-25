from flask import Flask, Response
from flask_restful import Api, Resource, abort, reqparse
from helpers import convert_to_xml
from get_data import get_students_data_from_db, get_groups_data_from_db, get_solo_student_from_db


app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('less_than')


class StudentSolo(Resource):
    def get(self, student_id):
        return Response(convert_to_xml(get_solo_student_from_db(student_id)), mimetype='text/xml')


class StudentList(Resource):
    def get(self):
        return Response(convert_to_xml(get_students_data_from_db()), mimetype='text/xml')


class GroupList(Resource):
    def get(self):
        args = parser.parse_args()
        return Response(convert_to_xml(get_groups_data_from_db(args['less_than'])), mimetype='text/xml')


api.add_resource(StudentSolo, '/students/<student_id>')
api.add_resource(StudentList, '/students')
api.add_resource(GroupList, '/groups')


if __name__ == '__main__':
    app.run(debug=True)
