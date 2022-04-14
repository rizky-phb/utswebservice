#nama kelompok :
# Rizky Dwi Saputra 19090107
# Wahyu Zuhudistia Khoiri 19090129
# Arief Rachman 19090012 
# M Rizqi Fauzi Maksum 19090142
from flask import Flask,request,jsonify
from flask_httpauth import HTTPTokenAuth
import random, os, string
from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import check_password_hash
from sqlalchemy import DATETIME, TIMESTAMP

app=Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "DBGPS.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
auth = HTTPTokenAuth(scheme='Bearer')
class users(db.Model):
    username = db.Column(db.String(20), unique=True,nullable=False, primary_key=True)
    password = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    token = db.Column(db.String(20), unique=False,nullable=True, primary_key=False)
    created_at = db.Column(TIMESTAMP,default=datetime.datetime.now)
class events(db.Model):
    event_creator = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_name = db.Column(db.String(20), unique=False,nullable=False, primary_key=True)
    event_start_time = db.Column(DATETIME, unique=False,nullable=False, primary_key=False)
    event_end_time = db.Column(DATETIME, unique=False,nullable=False, primary_key=False)
    event_start_lat= db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_start_lng =db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_finish_lat = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_finish_lng = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    created_at = db.Column(TIMESTAMP,default=datetime.datetime.now)
class logs(db.Model):
    username = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_name = db.Column(db.String(20), unique=True,nullable=False, primary_key=False)
    log_lat = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    log_lng = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    created_at = db.Column(TIMESTAMP,default=datetime.datetime.now, unique=False,nullable=False, primary_key=True)
@app.route('/api/v1/users/create', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    user = users(username=username,password=password,token= '')
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg" : "registrasi sukses"}), 200
@app.route('/api/v1/users/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    j=15
    user= users.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
           token = ''.join(random.choices(string.ascii_uppercase + string.digits, k = j))
           user.token= token
           db.session.commit()
    return jsonify({"msg": "login sukses","token": token,}), 200
@app.route('/api/v1/events/create', methods=['POST'])
def create_event():
    token =  request.json['token']
    username=users.query.filter_by(token=token).first()
    user = str(username.username)
    event_name = request.json['event_start_time']
    event_start_time = request.json['event_start_time']
    event_start_time_obj = datetime.datetime.strptime(event_start_time, '%Y-%m-%d %H:%M:%S.%f')
    event_end_time = request.json['event_end_time']
    event_end_time_obj = datetime.datetime.strptime(event_end_time, '%Y-%m-%d %H:%M:%S.%f')
    event_start_lat = request.json['event_start_lat']
    event_start_lng = request.json['event_start_lng']
    event_finish_lat = request.json['event_finish_lat']
    event_finish_lng = request.json['event_finish_lng']
    eventt = events(event_creator = user,
                    event_name = event_name,
                    event_start_time = event_start_time_obj,
                    event_end_time = event_end_time_obj,
                    event_start_lat = event_start_lat,
                    event_start_lng = event_start_lng,
                    event_finish_lat = event_finish_lat,
                    event_finish_lng = event_finish_lng)
    db.session.add(eventt)
    db.session.commit()
    return jsonify({"msg": "membuat event sukses"}), 200

@app.route('/api/v1/logs', methods=['POST'])
def create_logs():
    token = request.json['token']
    username=users.query.filter_by(token=token).first()
    user=str(username.username)
    print(user)
    log = logs(username = format(user), event_name = request.json['event_name'],log_lat = request.json['log_lat'], log_lng = request.json['log_lng'])
    db.session.add(log)
    db.session.commit()
    return jsonify({"msg": "Log berhasil dibuat"}), 200

@app.route('/api/v1/users/logs/<token>/<event_name>', methods=['GET'])
def view_logs(token,event_name):
    view= logs.query.filter_by(event_name=event_name).all()
    
    log = []

    for i in view:
        dictlogs = {}
        dictlogs.update({"username": i.username,"log_lat": i.log_lat, "log_lng": i.log_lng, "create_at": i.created_at})
        log.append(dictlogs)
    return jsonify(log), 200
if __name__ == '__main__':
  app.run(debug = True, port=5000)