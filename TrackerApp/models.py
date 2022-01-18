#models.py
from TrackerApp import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
from flask_restful import fields, marshal_with

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class MyDateFormat(fields.Raw):
    def format(self, value):
        return value.strftime('%Y-%m-%d')

class MyDateTimeFormat(fields.Raw):
    def format(self, value):
        return value.strftime('%Y-%m-%d %H:%M:%S')
#########
# User
#########
class User(db.Model,UserMixin):

    #default
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    create_dtm = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    
    #FK
    # locations_rel = db.relationship('LocationTracker',backref='workerLocation',lazy=True)
    # jobs_rel = db.relationship('JobStatus',backref='workerJob',lazy=True)
    # tasks_rel = db.relationship('TaskStatus',backref='workerTask',lazy=True)
    
    #Attributes
    username = db.Column(db.String(65),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    
    
    def __init__(self,username,password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"User Id: {self.id} --- Username: {self.username}"

#########
# Job
#########
job_fields = {
            "id" : fields.Integer, 
            "name": fields.String,
            "status" : fields.String,
            "job_date" : MyDateFormat,
            "note" : fields.String,
            "priority" : fields.Integer
        } 

class Job(db.Model):

    #default
    __tablename__ = 'job'
    id = db.Column(db.Integer,primary_key=True)
    create_dtm = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    
    #FK
    # status_rel = db.relationship('JobStatus',backref='jobStatus',lazy=True)
    # tasks_rel = db.relationship('JobTasks',backref='jobTask',lazy=True)
    
    #Attributes
    name = db.Column(db.String(64),nullable=False)
    note = db.Column(db.Text,nullable=True)
    status = db.Column(db.String(64),nullable=False)
    job_date = db.Column(db.DateTime,nullable=False)
    priority = db.Column(db.Integer,nullable=False, default = 1)
    
    def __init__(self,name,note, status, job_date, priority):
        self.name = name
        self.note = note
        self.status = status
        self.job_date = job_date
        self.priority = priority
    
    def __repr__(self):
        return f"Job Id: {self.id} --- Name: {self.name} --- Status: {self.status} --- Date: {self.job_date}"

    @marshal_with(job_fields)
    def json(self):
        return self

#########
# Task
#########
class Task(db.Model):

    #default
    __tablename__ = 'task'
    id = db.Column(db.Integer,primary_key=True)
    create_dtm = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    
    #FK
    # status_rel = db.relationship('TaskStatus',backref='taskStatus',lazy=True)
    # job_task_rel = db.relationship('JobTasks',backref='tasksJob',lazy=True)
    
    #Attributes
    name = db.Column(db.String(64),nullable=False)
    note = db.Column(db.Text,nullable=True)
    status = db.Column(db.String(10),nullable=False)
    lon_lat = db.Column(db.String(50),nullable=True)
    order = db.Column(db.Integer,nullable=True, default=1)
    address = db.Column(db.Text,nullable=True)
    
    
    def __init__(self,name,note, status, lon_lat, order, address):
        self.name = name
        self.note = note
        self.status = status
        self.lon_lat = lon_lat
        self.order = order
        self.address = address
    
    def __repr__(self):
        return f"Task Id {id} --- Name: {self.name} --- Status: {self.status}"

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "note" :self.note,
            "status" : self.status,
            "lon_lat" : self.lon_lat,
            "order" : self.order,
            "address" : self.address
        }
            
###########################
# Job Tasks
###########################
class JobTasks(db.Model):

    #default
    __tablename__ = 'job_tasks'
    id = db.Column(db.Integer,primary_key=True)
    create_dtm = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    #FK
    job = db.relationship(Job, overlaps="jobTask,tasks_rel")
    job_id = db.Column(db.Integer,db.ForeignKey('job.id'),nullable=False)
    task = db.relationship(Task)
    task_id = db.Column(db.Integer,db.ForeignKey('task.id'),nullable=False)
    
    #Attributes
    
    def __init__(self,job_id, task_id):
        self.job_id = job_id
        self.task_id = task_id
        
    def __repr__(self):
        return f"Job Tasks: {self.id} -- Job: {self.job_id} --- Task: {self.task_id}"

###########################
# Worker Location Tracker
###########################
location_tracker_fields = {
            "worker_id" : fields.Integer, 
            "job_id" : fields.Integer,
            "create_dtm" : MyDateTimeFormat,
            "lon_lat" : fields.String
        } 

class LocationTracker(db.Model):

    #default
    __tablename__ = 'location_tracker'
    id = db.Column(db.Integer,primary_key=True)
    create_dtm = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    #FK
    user = db.relationship(User)
    worker_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    job = db.relationship(Job, overlaps="jobTask,tasks_rel")
    job_id = db.Column(db.Integer,db.ForeignKey('job.id'),nullable=False)
    
    #Attributes
    loc_lon = db.Column(db.Integer,nullable=False)
    loc_lat = db.Column(db.Integer,nullable=False)
    lon_lat = db.Column(db.String(50),nullable=True)
    
    def __init__(self,worker_id, job_id, lon_lat = '(0,0)', loc_lon=0, loc_lat=0):
        self.worker_id = worker_id
        self.job_id = job_id
        self.loc_lon = loc_lon
        self.loc_lat = loc_lat
        self.lon_lat = lon_lat
        
    def __repr__(self):
        return f"Location Tracker: {self.id} -- Worker: {self.worker_id} --- Loc string: {self.lon_lat} Loc: ({self.loc_lon} , {self.loc_lat})"

    @marshal_with(location_tracker_fields)
    def json(self):
        return self

###########################
# Worker Job Status
###########################
class JobStatus(db.Model):

    __tablename__ = 'job_status'

    # default
    id = db.Column(db.Integer,primary_key=True)
    create_dtm = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    #FK
    user = db.relationship(User)
    worker_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    job = db.relationship(Job)
    job_id = db.Column(db.Integer,db.ForeignKey('job.id'),nullable=False)
    
    #Attributes
    job_status = db.Column(db.String(50),nullable=False)
    
    def __init__(self,worker_id,job_id,job_status):
        self.worker_id = worker_id
        self.job_id = job_id
        self.job_status = job_status
    
    def __repr__(self):
        return f"Job Status: {self.id} -- Worker: {self.worker_id} --- Job: {self.job_id} --- Status: {self.job_status}"

###########################
# Worker Task Status
###########################
class TaskStatus(db.Model):

    __tablename__ = 'task_status'

    # default
    id = db.Column(db.Integer,primary_key=True)
    create_dtm = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    #FK
    user = db.relationship(User)
    worker_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    task = db.relationship(Task)
    task_id = db.Column(db.Integer,db.ForeignKey('task.id'),nullable=False)
    
    #Attributes
    task_status = db.Column(db.String(50),nullable=False)
    
    def __init__(self, worker_id, task_id, task_status):
        self.worker_id = worker_id
        self.task_id = task_id
        self.task_status = task_status

    def __repr__(self):
        return f"Task Status: {self.id} -- Worker: {self.worker_id} --- Task: {self.task_id} --- Status: {self.task_status}"

class Dummy(db.Model):

    __tablename__ = 'dummy'

    # default
    id = db.Column(db.Integer,primary_key=True)
    create_dtm = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    # id2 = db.Column(db.Integer,nullable=True)