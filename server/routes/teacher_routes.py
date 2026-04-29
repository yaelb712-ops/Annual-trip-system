from flask import Blueprint, request, jsonify
from database import db
from models import Teachers
from utils import verifyTeacher

teacher_routes = Blueprint('teacher_routes', __name__)

@teacher_routes.route('/teachers', methods=['POST'])
def addTeacher():
    teacher = verifyTeacher()
    if not teacher:
        return jsonify({'message': 'Unauthorized'}), 403

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


@teacher_routes.route('/teachers', methods=['GET'])
def getTeachers():
    teacher = verifyTeacher()
    if not teacher:
        return jsonify({'message': 'Unauthorized'}), 403

    teachers = Teachers.query.all()
    output = []
    for teacher in teachers:
        output.append({
            'firstName': teacher.firstName,
            'lastName': teacher.lastName,
            'identityNumber': teacher.identityNumber,
            'classN': teacher.classN
        })
    return jsonify({'teachers': output})


@teacher_routes.route('/teachers/id/<identityNumber>', methods=['GET'])
def getTeacher(identityNumber):
    teacher = verifyTeacher()
    if not teacher:
        return jsonify({'message': 'Unauthorized'}), 403

    teacher = Teachers.query.filter_by(identityNumber=identityNumber).first()
    if teacher:
        return jsonify({
            'firstName': teacher.firstName,
            'lastName': teacher.lastName,
            'identityNumber': teacher.identityNumber,
            'classN': teacher.classN
        })
    return jsonify({'message': 'Teacher not found'}), 404
