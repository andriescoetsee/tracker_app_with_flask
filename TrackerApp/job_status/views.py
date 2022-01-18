
from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from TrackerApp import db
from TrackerApp.models import LocationTracker, Task, Job, JobTasks, User
from TrackerApp.utils.utils import convert_lon_lat, Marker


job_status = Blueprint('job_status',__name__)

@job_status.route('/<int:job_id>/job_status')
@login_required
def view_job_status(job_id):

    home = "{ lat: -33.89841798142526, lng: 18.63517371060965}"
    vredelust = "{ lat: -33.89776654999885, lng: 18.613481705404496}"
    stellies = "{ lat: -33.861950206381096, lng: 18.661396633823276}"
    driver_loc_mkem = "{ lat: -33.887176872603455, lng: 18.634873422118662}"
    driver_loc_brakenfell = "{ lat: -33.86733012097939, lng: 18.687235941304422}"
    driver_loc_gg = "{ lat: -33.8536018402705, lng: 18.670414380755922}"

    job = Job.query.get_or_404(job_id)
    
    # get first 'Busy' task for this job otherwhise get task with lowest order, 
    # so that we can set current destination
    r = db.session.query( JobTasks.job_id, Task ).filter( JobTasks.job_id == job_id).join( Task, JobTasks.task_id == Task.id).filter( Task.status == 'Busy').first()

    if not r:
        r = db.session.query( JobTasks.job_id, Task ).filter( JobTasks.job_id == job_id).join( Task, JobTasks.task_id == Task.id).order_by(Task.order.asc() ).first()
        if not r:
            #it means not tasks yet configured so return to Job List
            return redirect(url_for('jobs.list_jobs'))

    marker = Marker();
    #print(task)
    #set current destination
    marker.current_dest = convert_lon_lat(r.Task.lon_lat)

    # get from driver location table otherwise use where order == 1 first
    driver = db.session.query( LocationTracker ).filter( LocationTracker.job_id == job_id).order_by(LocationTracker.create_dtm.desc() ).first()

    if not driver:
        marker.current_loc = convert_lon_lat(r.Task.lon_lat) 
    else:
        marker.current_loc = convert_lon_lat(driver.lon_lat) 
    
    # set map center
    def_map_center = marker.current_loc
    
    # get all the destinations for this job
    destinations = db.session.query( JobTasks.job_id, Task ).filter( JobTasks.job_id == job_id).join( Task, JobTasks.task_id == Task.id).order_by(Task.order.asc()).all()

    for i, dest in enumerate(destinations):
        marker.loc_list.append(convert_lon_lat(dest.Task.lon_lat)) 
        marker.text_list.append(str(dest.Task.order) + " - " + dest.Task.name + " : " + dest.Task.address)
    
        if i < len(marker.label_nrs):
            marker.label_list.append(marker.label_nrs[i])
        else:
            marker.label_list.append(marker.label_transit) 

    marker.label_list[-1] = marker.label_destination

    #now add the car to our marker arrays if we have a driver
    if driver:
        marker.loc_list.append( marker.current_loc)
        marker.label_list.append(marker.label_car) 
        user = User.query.get_or_404(driver.worker_id)
        marker.text_list.append( "Driver:  " + user.username )
        
    marker.length = len(marker.label_list)    

    return render_template('view_job_status.html',job_name=job.name, map_center=def_map_center, task = r.Task, marker = marker, len=range(marker.length))

