from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from database import db
from routes import student_routes, teacher_routes, location_routes

app = Flask(__name__)
CORS(app, origins = "*")
socketio = SocketIO(app, cors_allowed_origins="*")
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc:///?odbc_connect='
    'DRIVER={SQL Server};'
    'SERVER=YAEL\\SQLEXPRESS;'
    'DATABASE=AnnualTripSystem;'
    'Trusted_Connection=yes;'

)

db.init_app(app)
app.register_blueprint(student_routes)
app.register_blueprint(teacher_routes)
app.register_blueprint(location_routes)

if __name__ == '__main__':
    socketio.run(app, debug=True)