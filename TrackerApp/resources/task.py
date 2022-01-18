from TrackerApp.models import Task, JobTasks, TaskStatus
from TrackerApp import db, api
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

class TasksApi(Resource):
    @jwt_required()
    def get(self, job_id):

        # List Tasks for a given Job Id

        jobTasks = db.session.query( JobTasks.job_id, Task ).filter( JobTasks.job_id == job_id).join( Task, JobTasks.task_id == Task.id).order_by(Task.order.asc()).all()

        if jobTasks:
            return [ j.Task.json() for j in jobTasks]
        else:
            msg = 'No tasks for this job: ' + job_id
            return {'msg':msg}, 404

class TaskApi(Resource):
    @jwt_required()
    def put(self,job_id, task_id, status):

        #Update Status for a given Job and Task
        #Insert Task Status to track who changed the Status
        jobTask = db.session.query( JobTasks.job_id, Task ).filter( JobTasks.job_id == job_id).join( Task, JobTasks.task_id == Task.id).filter( Task.id == task_id).first_or_404()

        #Update Task Status for given Job
        task = jobTask.Task
        if task:
            task.status=status
            db.session.add(task)
        else:
            msg = 'Task not found: ' + job_id
            return {'msg':msg}, 404

        #Insert into Task Status
        task_status = TaskStatus( get_jwt_identity(), task_id, status)
        db.session.add(task_status)

        #commit
        db.session.commit()
        return {'msg':'Task status updated'}, 200

