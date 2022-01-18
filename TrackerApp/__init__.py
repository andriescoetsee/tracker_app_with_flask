import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Api
from flask_jwt_extended import JWTManager
from TrackerApp.utils.utils import config

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

basedir = os.path.abspath(os.path.dirname(__file__))
config_ini_file = os.path.join(basedir, 'config.ini')
#############################################################################
############ CONFIGURATIONS (CAN BE SEPARATE CONFIG.PY FILE) ###############
###########################################################################

# Remember you need to set your environment variables at the command line
# when you deploy this to a real website.
# export SECRET_KEY=mysecret
# set SECRET_KEY=mysecret

params = config(config_ini_file, section='keys')
app.config['GOOGLEMAPS_KEY'] = params['GOOGLEMAPS_KEY']
app.config['SECRET_KEY'] = params['SECRET_KEY']

#################################
### DATABASE SETUPS ############
###############################

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

params = config(config_ini_file, section='json_web_tokens')

app.config['JWT_SECRET_KEY'] = params['JWT_SECRET_KEY']

db = SQLAlchemy(app)
Migrate(app,db)

###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "users.login"

###########################
#### BLUEPRINT CONFIGS ####
###########################

# Import these at the top if you want
# We've imported them here for easy reference
from TrackerApp.core.views import core
from TrackerApp.users.views import users
from TrackerApp.job_status.views import job_status
from TrackerApp.jobs.views import jobs
from TrackerApp.tasks.views import tasks

# from TrackerApp.location_tracker.views import location_tracker
# from TrackerApp.task_status.views import task_status
#from TrackerApp.error_pages.handlers import error_pages

# Register the apps
app.register_blueprint(users)
app.register_blueprint(job_status)
app.register_blueprint(jobs)
app.register_blueprint(tasks)
# app.register_blueprint(location_tracker)
# app.register_blueprint(task_status)
app.register_blueprint(core)
#app.register_blueprint(error_pages)

###########################
#### API CONFIGS #########
###########################

from TrackerApp.resources.job import JobsApi, JobApi
from TrackerApp.resources.task import TasksApi, TaskApi
from TrackerApp.resources.auth import SignupApi, LoginApi
from TrackerApp.resources.location_tracker import WorkerLocationsApi, LocationTrackerApi

### Jobs
api.add_resource(JobsApi, '/api/jobs/<string:status>')
api.add_resource(JobApi, '/api/job_update/<int:job_id>/<string:status>')

### Tasks
api.add_resource(TasksApi, '/api/tasks/<int:job_id>')
api.add_resource(TaskApi, '/api/task_update/<int:job_id>/<int:task_id>/<string:status>')

## User
api.add_resource(SignupApi, '/api/auth/register')
api.add_resource(LoginApi, '/api/auth/login')

## LocationTracker
api.add_resource(WorkerLocationsApi, '/api/worker_loc/<int:worker_id>/<int:n>')
api.add_resource(LocationTrackerApi, '/api/track_loc/<int:job_id>/<string:lon_lat>')

