from flask import Blueprint, request, jsonify
from database import db
from models import Students, Teachers, Locations, TeacherLocations

routes = Blueprint('routes', __name__)

def verifyTeacher():
    teacherId = request.headers.get('teacherId')
    if not teacherId:
        return None
    return Teachers.query.filter_by(identityNumber=teacherId).first()

@routes.route('/students', methods=['POST'])
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


@routes.route('/teachers', methods=['POST'])
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


@routes.route('/students', methods=['GET'])
def getStudents():
    teacher = verifyTeacher()
    if not teacher:
        return jsonify({'message': 'Unauthorized'}), 403

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
    teacher = verifyTeacher()
    if not teacher:
        return jsonify({'message': 'Unauthorized'}), 403

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


@routes.route('/teachers/id/<identityNumber>', methods=['GET'])
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


@routes.route('/students/class/<classN>', methods=['GET'])
def getClassStudents(classN):
    teacher = verifyTeacher()
    if not teacher:
        return jsonify({'message': 'Unauthorized'}), 403
    if classN != teacher.classN:
        return jsonify({'message': 'You can only view your own class'}), 403

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

@routes.route('/Locations', methods=['POST'])
def newLocation():
    data = request.get_json()
    refLo = data['Coordinates']['Longitude']
    refLa = data['Coordinates']['Latitude']

    decimelLO = float(refLo['Degrees']) + float(refLo['Minutes'])/60 + float(refLo['Seconds'])/3600
    decimelLA = float(refLa['Degrees']) + float(refLa['Minutes'])/60 + float(refLa['Seconds'])/3600

    locationS = Locations(
        studentIdentity=str(data['ID']),
        longitude=decimelLO,
        latitude=decimelLA,
        timeS=data['Time']
    )
    db.session.add(locationS)
    db.session.commit()
    return jsonify({'message': 'location send to parents'}), 201

@routes.route('/Locations', methods=['GET'])
def getLocations():
    outpot = []
    locations = Locations.query.all()
    for location in locations:
        location_data= {
            'studentIdentity': location.studentIdentity,
            'longitude': location.longitude,
            'latitude': location.latitude,
            'timeS': location.timeS
        }
        outpot.append(location_data)
    return jsonify({'Locations': outpot})

@routes.route('/teacher-location', methods=['POST'])
def newTeacherLocation():
    data = request.get_json()
    refLo = data['Coordinates']['Longitude']
    refLa = data['Coordinates']['Latitude']

    decimelLO = float(refLo['Degrees']) + float(refLo['Minutes'])/60 + float(refLo['Seconds'])/3600
    decimelLA = float(refLa['Degrees']) + float(refLa['Minutes'])/60 + float(refLa['Seconds'])/3600

    locationS = TeacherLocations(
        teacherIdentity=str(data['ID']),
        longitude=decimelLO,
        latitude=decimelLA,
        timeS=data['Time']
    )
    db.session.add(locationS)
    db.session.commit()
    return jsonify({'message': 'location send'}), 201


@routes.route('/teacher-location', methods=['GET'])
def getTeacherLocation():
    location = TeacherLocations.query.order_by(TeacherLocations.id.desc()).first()
    if location:
        return jsonify ({
            'teacherIdentity': location.teacherIdentity,
            'longitude': location.longitude,
            'latitude': location.latitude,
            'timeS': location.timeS
        })
    return jsonify({'message': 'no location found'}), 404