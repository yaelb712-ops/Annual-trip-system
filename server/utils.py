from flask import request
from models import Teachers

def verifyTeacher():
    teacherId = request.headers.get('teacherId')
    if not teacherId:
        return None
    return Teachers.query.filter_by(identityNumber=teacherId).first()
