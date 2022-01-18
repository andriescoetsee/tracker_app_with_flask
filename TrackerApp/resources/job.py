from TrackerApp.models import Job, JobStatus
from TrackerApp import db, api
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

class JobsApi(Resource):

    @jwt_required()
    def get(self, status):
    
    # Lists all the Jobs for a given Status

        jobs = Job.query.filter_by(status=status).all()

        if jobs:
            return [ job.json() for job in jobs]
        else:
            msg = 'No jobs in status: ' + status
            return {'msg':msg}, 404

class JobApi(Resource):

    @jwt_required()
    def put(self,job_id, status):

    # Updates Job Status 
    # Inserts into Job_Status

        #Update Job Status
        job = Job.query.get_or_404(job_id)

        if job:
            job.status=status
            db.session.add(job)
        else:
            msg = 'Job not found: ' + job_id
            return {'msg':msg}, 404
        
        #Insert into Job_Status to track who changed the Job Status
        job_status = JobStatus(get_jwt_identity(), job_id, status)
        db.session.add(job_status)
        
        #commit
        db.session.commit()
        return {'msg':'Job status updated'}, 200


