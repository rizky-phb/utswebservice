# nama kelompok :
# Rizky Dwi Saputra 19090107
# Wahyu Zuhudistia Khoiri 19090129
# Arief Rachman 19090012 
# M Rizqi Fauzi Maksum 19090142
from flask import Flask,request,jsonify
import random, os, string,datetime
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Resource, Api
from werkzeug.security import check_password_hash
from sqlalchemy import DATETIME, TIMESTAMP

app=Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "DBGPS.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
api = Api(app)
CORS(app)
db = SQLAlchemy(app)
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
    event_start_lng = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_finish_lat = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_finish_lng = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    created_at = db.Column(TIMESTAMP,default=datetime.datetime.now)
class logs(db.Model):
    username = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    event_name = db.Column(db.String(20), unique=True,nullable=False, primary_key=False)
    log_lat = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    log_lng = db.Column(db.String(20), unique=False,nullable=False, primary_key=False)
    created_at = db.Column(TIMESTAMP,default=datetime.datetime.now, unique=False,nullable=False, primary_key=True)

class no1(Resource):
    def post(self):
        username = request.json['username']
        password = request.json['password']
        user = users(username=username,password=password,token= '')
        db.session.add(user)
        db.session.commit()
        return jsonify({"msg" : "registrasi sukses","status":200})
class no2(Resource):
    def post(self):
        username = request.json['username']
        password = request.json['password']
        j=15
        user= users.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            token = ''.join(random.choices(string.ascii_uppercase + string.digits, k = j))
            user.token= token
            db.session.commit()
        return jsonify({"msg":"login sukses","token":token, "status":200})
class no3(Resource):
    def post(self):
        token =  request.json['token']
        username=users.query.filter_by(token=token).first()
        user = str(username.username)
        event_name = request.json['event_name']
        event_start_time = request.json['event_start_time']
        event_start_time_obj = datetime.datetime.strptime(event_start_time, '%Y-%m-%d %H:%M:%S.%f')
        event_end_time = request.json['event_end_time']
        event_end_time_obj = datetime.datetime.strptime(event_end_time, '%Y-%m-%d %H:%M:%S.%f')
        eventt = events(event_creator = user,
                        event_name = event_name,
                        event_start_time = event_start_time_obj,
                        event_end_time = event_end_time_obj,
                        event_start_lat = request.json['event_start_lat'],
                        event_start_lng = request.json['event_start_lng'],
                        event_finish_lat = request.json['event_finish_lat'],
                        event_finish_lng = request.json['event_finish_lng'])
        db.session.add(eventt)
        db.session.commit()
        return jsonify({"msg": "membuat event sukses","status":200})
class no4(Resource):
    def post(self):
        token = request.json['token']
        username=users.query.filter_by(token=token).first()
        user=str(username.username)
        print(user)
        log = logs(username = format(user), event_name = request.json['event_name'],log_lat = request.json['log_lat'], log_lng = request.json['log_lng'])
        db.session.add(log)
        db.session.commit()
        return jsonify({"msg": "Log berhasil dibuat","status":200})
class no5(Resource):
    def get(self,token,event_name):
        view= logs.query.filter_by(event_name=event_name).all()
        log = []
        for i in view:
            dictlogs = {}
            dictlogs.update({"username": i.username,"log_lat": i.log_lat, "log_lng": i.log_lng, "create_at": i.created_at})
            log.append(dictlogs)
        return jsonify(log)

api.add_resource(no1, '/api/v1/users/create', methods=['POST'])
api.add_resource(no2, '/api/v1/users/login', methods=['POST'])
api.add_resource(no3, "/api/v1/events/create", methods=["POST"])
api.add_resource(no4, '/api/v1/logs', methods=['POST'])
api.add_resource(no5, '/api/v1/users/logs/<token>/<event_name>', methods=['GET'])

if __name__ == '__main__':
  app.run(debug = True, port=5000)