from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS  


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*") 

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc:///?odbc_connect='
    'DRIVER={SQL Server};'
    'SERVER=YAEL\\SQLEXPRESS;'
    'DATABASE=AnnualTripSystem;'
    'Trusted_Connection=yes;'
)

db = SQLAlchemy(app) 

if __name__ == '__main__':
    socketio.run(app, debug=True)  