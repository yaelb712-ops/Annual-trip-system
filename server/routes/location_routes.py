from flask import Blueprint, request, jsonify
from database import db
from models import Students, Locations, TeacherLocations
from math import radians, sin, cos, sqrt, atan2

location_routes = Blueprint('location_routes', __name__)

@location_routes.route('/Locations', methods=['POST'])
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
    return jsonify({'message': 'location sent to parents'}), 201


@location_routes.route('/Locations', methods=['GET'])
def getLocations():
    outpot = []
    locations = Locations.query.all()
    for location in locations:
        outpot.append({
            'studentIdentity': location.studentIdentity,
            'longitude': location.longitude,
            'latitude': location.latitude,
            'timeS': location.timeS
        })
    return jsonify({'Locations': outpot})


@location_routes.route('/student-view/<identityNumber>', methods=['GET'])
def studentView(identityNumber):
    student = Students.query.filter_by(identityNumber=identityNumber).first()
    if not student:
        return jsonify({'message': 'Student not found'}), 404

    studentLocation = Locations.query.filter_by(studentIdentity=identityNumber).order_by(Locations.id.desc()).first()
    teacherLocation = TeacherLocations.query.order_by(TeacherLocations.id.desc()).first()

    inRange = False
    if studentLocation and teacherLocation:
        R = 6371000
        lat1, lon1 = radians(teacherLocation.latitude), radians(teacherLocation.longitude)
        lat2, lon2 = radians(studentLocation.latitude), radians(studentLocation.longitude)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
        distance = R * 2 * atan2(sqrt(a), sqrt(1-a))
        inRange = distance <= 3000

    return jsonify({
        'firstName': student.firstName,
        'lastName': student.lastName,
        'identityNumber': student.identityNumber,
        'inRange': inRange
    })


@location_routes.route('/teacher-location', methods=['POST'])
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


@location_routes.route('/teacher-location', methods=['GET'])
def getTeacherLocation():
    location = TeacherLocations.query.order_by(TeacherLocations.id.desc()).first()
    if location:
        return jsonify({
            'teacherIdentity': location.teacherIdentity,
            'longitude': location.longitude,
            'latitude': location.latitude,
            'timeS': location.timeS
        })
    return jsonify({'message': 'no location found'}), 404
