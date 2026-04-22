from flask import Blueprint, request, jsonify
from database import db
from models import Students, Teachers

routes = Blueprint('routes', __name__)

@routes.route('/students', methods=['POST'])
def addStudent():
    data = request.get_json()
    newStudent = Students(
        firstName=data['firstName'],
        lastName=data['lastName'],
        identityNumber=data['identityNumber'],
        classN=data['classN']
    )
    db.session.add(newStudent)
    db.session.commit()
    return jsonify({'message': 'Student added successfully'}), 201


@routes.route('/teachers', methods=['POST'])
def addTeacher():
    data = request.get_json()
    newTeacher = Teachers(
        firstName=data['firstName'],
        lastName=data['lastName'],
        identityNumber=data['identityNumber'],
        classN=data['classN']
    )
    db.session.add(newTeacher)
    db.session.commit()
    return jsonify({'message': 'Teacher added successfully'}), 201


@routes.route('/students', methods=['GET'])
def getStudents():
    students = Students.query.all()
    output = []
    for student in students:
        student_data = {
            'firstName': student.firstName,
            'lastName': student.lastName,
            'identityNumber': student.identityNumber,
            'classN': student.classN
        }
        output.append(student_data)
    return jsonify({'students': output})


@routes.route('/teachers', methods=['GET'])
def getTeachers():
    teachers = Teachers.query.all()
    output = []
    for teacher in teachers:
        teacher_data = {
            'firstName': teacher.firstName,
            'lastName': teacher.lastName,
            'identityNumber': teacher.identityNumber,
            'classN': teacher.classN
        }
        output.append(teacher_data)
    return jsonify({'teachers': output})


@routes.route('/students/id/<identityNumber>', methods=['GET'])
def getStudent(identityNumber):
    student = Students.query.filter_by(identityNumber=identityNumber).first()
    if student:
        return jsonify({
            'firstName': student.firstName,
            'lastName': student.lastName,
            'identityNumber': student.identityNumber,
            'classN': student.classN
        })
    return jsonify({'message': 'Student not found'}), 404


@routes.route('/teachers/id/<identityNumber>', methods=['GET'])
def getTeacher(identityNumber):
    teacher = Teachers.query.filter_by(identityNumber=identityNumber).first()
    if teacher:
        return jsonify({
            'firstName': teacher.firstName,
            'lastName': teacher.lastName,
            'identityNumber': teacher.identityNumber,
            'classN': teacher.classN
        })
    return jsonify({'message': 'Teacher not found'}), 404


@routes.route('/students/class/<classN>', methods=['GET'])
def getClassStudents(classN):
    classStudents = Students.query.filter_by(classN=classN).all()
    output = []
    if classStudents:
        for student in classStudents:
            student_data = {
                'firstName': student.firstName,
                'lastName': student.lastName,
                'identityNumber': student.identityNumber,
                'classN': student.classN
            }
            output.append(student_data)
    return jsonify({'students': output})