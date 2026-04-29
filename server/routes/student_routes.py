from flask import Blueprint, request, jsonify
from database import db
from models import Students, Teachers
from utils import verifyTeacher

student_routes = Blueprint('student_routes', __name__)

@student_routes.route('/students', methods=['POST'])
def addStudent():
    teacher = verifyTeacher()
    if not teacher:
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.get_json()

    if data['classN'] != teacher.classN:
        return jsonify({'message': 'You can only add students to your class'}), 403

    newStudent = Students(
        firstName=data['firstName'],
        lastName=data['lastName'],
        identityNumber=data['identityNumber'],
        classN=data['classN']
    )
    db.session.add(newStudent)
    db.session.commit()
    return jsonify({'message': 'Student added successfully'}), 201


@student_routes.route('/students', methods=['GET'])
def getStudents():
    teacher = verifyTeacher()
    if not teacher:
        return jsonify({'message': 'Unauthorized'}), 403

    students = Students.query.all()
    output = []
    for student in students:
        output.append({
            'firstName': student.firstName,
            'lastName': student.lastName,
            'identityNumber': student.identityNumber,
            'classN': student.classN
        })
    return jsonify({'students': output})


@student_routes.route('/students/id/<identityNumber>', methods=['GET'])
def getStudent(identityNumber):
    teacher = verifyTeacher()
    if not teacher:
        return jsonify({'message': 'Unauthorized'}), 403

    student = Students.query.filter_by(identityNumber=identityNumber).first()
    if student:
        return jsonify({
            'firstName': student.firstName,
            'lastName': student.lastName,
            'identityNumber': student.identityNumber,
            'classN': student.classN
        })
    return jsonify({'message': 'Student not found'}), 404


@student_routes.route('/students/class/<classN>', methods=['GET'])
def getClassStudents(classN):
    teacher = verifyTeacher()
    if not teacher:
        return jsonify({'message': 'Unauthorized'}), 403
    if classN != teacher.classN:
        return jsonify({'message': 'You can only view your own class'}), 403

    classStudents = Students.query.filter_by(classN=classN).all()
    output = []
    for student in classStudents:
        output.append({
            'firstName': student.firstName,
            'lastName': student.lastName,
            'identityNumber': student.identityNumber,
            'classN': student.classN
        })
    return jsonify({'students': output})
