from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from TrackerApp import db
from TrackerApp.models import Task, Job, JobTasks
from TrackerApp.tasks.forms import TaskForm
from TrackerApp.utils.utils import convert_lon_lat

tasks = Blueprint('tasks',__name__)

@tasks.route('/<int:job_id>/create_task',methods=['GET','POST'])
@login_required
def create_task(job_id):
    
    job = Job.query.get_or_404(job_id)

    form = TaskForm()

    def_map_center = "{ lat: -26.1366920469943, lng: 28.241102981516946}"  ### Johannesburg International Airport
    
    if form.validate_on_submit():

        #first add a task, return task_id
        task = Task( name = form.name.data,
                   note = form.note.data,
                   status = form.status.data,
                   lon_lat = form.lon_lat.data,
                   order = form.order.data,
                   address = form.address.data )
        
        db.session.add(task)
        db.session.flush()
        
        #Now add a JobTasks
        link_task_to_job = JobTasks( job.id, task.id)
        db.session.add(link_task_to_job)

        #commit
        db.session.commit()

        return redirect(url_for('jobs.list_jobs'))

    return render_template('create_task.html',form=form, update=False, job_name = job.name, map_center = def_map_center)

@tasks.route('/<int:job_id>/list_tasks')
@login_required
def list_tasks(job_id):

    job = Job.query.get_or_404(job_id)
    # tasks = db.session.query( JobTasks.job_id.label('job_id'), Task.name, Task.note, Task.status, Task.order, Task.loc_lon, Task.loc_lat ).filter( JobTasks.job_id == job_id).join( Task, JobTasks.task_id == Task.id).order_by(Task.order.asc() ).all()
    tasks = db.session.query( JobTasks.job_id, Task ).filter( JobTasks.job_id == job.id).join( Task, JobTasks.task_id == Task.id).order_by(Task.order.asc() ).all()

    return render_template('list_tasks.html',task_list=tasks, job_name=job.name)

@tasks.route("/<int:job_id>/<int:task_id>/update_task", methods=['GET', 'POST'])
@login_required
def update_task(job_id, task_id):

    map_center = "{ lat: -26.1366920469943, lng: 28.241102981516946}" # Johannesburg International Airport

    task = Task.query.get_or_404(task_id)
    job = Job.query.get_or_404(job_id)

    form = TaskForm()
    if form.validate_on_submit():

        task.name = form.name.data
        task.note = form.note.data
        task.status = form.status.data
        task.lon_lat = form.lon_lat.data
        task.order = form.order.data 
        task.address = form.address.data

        db.session.commit()
        return redirect(url_for('tasks.list_tasks', job_id=job.id))
    # Pass back the old task information so they can start again with
    elif request.method == 'GET':
        form.name.data = task.name
        form.note.data = task.note 
        form.status.data = task.status 
        form.lon_lat.data = task.lon_lat 
        form.address.data = task.address
        form.order.data = task.order 
        
        if task.lon_lat:
            map_center = convert_lon_lat(task.lon_lat)
            #ll = task.lon_lat.replace('(','').replace(')','').split(',')
            #map_center = "{ lat: " + ll[0] + ", lng: " + ll[1] + " }"
        
    return render_template('create_task.html',form=form, task_id=task.id, job_id=job.id, update=True, job_name = job.name, map_center = map_center, task_address=task.address)

@tasks.route("/<int:job_id>/<int:task_id>/delete", methods=['POST'])
@login_required
def delete_task(job_id, task_id):
    task = Task.query.get_or_404(task_id)
    job_task = JobTasks.query.filter( JobTasks.job_id ==job_id, JobTasks.task_id == task_id).first_or_404()
    
    #we might need to delete all children tables first, not sure if there is a cascade with delete
    db.session.delete(task)
    db.session.delete(job_task)
    db.session.commit()
    return redirect(url_for('tasks.list_tasks', job_id=job_id ))