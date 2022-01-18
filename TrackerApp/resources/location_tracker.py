from TrackerApp.models import LocationTracker 
from TrackerApp import db, api
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

class WorkerLocationsApi(Resource):
    @jwt_required()
    def get(self, worker_id, n):

        # Get last n Locations for given Worker Id
        location_tracker = db.session.query( LocationTracker ).filter( LocationTracker.worker_id == worker_id).order_by(LocationTracker.create_dtm.desc()).limit(n).all()

        if location_tracker:
            return [ lt.json() for lt in location_tracker ]
        else:
            msg = 'No location for this worker id: ' + str(worker_id)
            return {'msg':msg}, 404

class LocationTrackerApi(Resource):
    @jwt_required()
    def post(self,job_id, lon_lat):

        #Insert Location Tracker for given Job and Location
        location_tracker = LocationTracker( get_jwt_identity(), job_id, lon_lat)
        db.session.add(location_tracker)

        #commit
        db.session.commit()
        return {'msg':'Location updated'}, 200

