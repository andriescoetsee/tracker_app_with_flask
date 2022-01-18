from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from TrackerApp import db
from TrackerApp.models import Job, LocationTracker, Task, JobTasks
from TrackerApp.jobs.forms import JobForm

jobs = Blueprint('jobs',__name__)

@jobs.route('/create_job',methods=['GET','POST'])
@login_required
def create_job():
    form = JobForm()

    if form.validate_on_submit():

        job = Job( name = form.name.data,
                   note = form.note.data,
                   status = form.status.data,
                   job_date = form.job_date.data,
                   priority = form.priority.data )
        db.session.add(job)
        db.session.commit()

        return redirect(url_for('jobs.list_jobs'))

    return render_template('create_job.html',form=form, update=False)

@jobs.route('/list_jobs')
@login_required
def list_jobs():
    # get all jobs, we can limit it to last week or last 10 etc.
    #jobs = Job.query.filter(Job.create_dtm - 7 days).order_by(Job.create_dtm.desc() ).all()
    jobs = Job.query.order_by(Job.create_dtm.desc() ).all()

    #apply the same filter to job_tasks
    #job_tasks = db.session.query( Job.id, Task.name ).filter(Job.create_dtm - 7 days).join( JobTasks, Job.id == JobTasks.job_id).join( Task, JobTasks.task_id == Task.id).all()

    job_tasks = db.session.query( Job.id.label('job_id'), Task ).join( JobTasks, Job.id == JobTasks.job_id).join( Task, JobTasks.task_id == Task.id).order_by(Task.order.asc() ).all()
    #Task.name.label('name'), Task.status.label('status') ).join( JobTasks, Job.id == JobTasks.job_id).join( Task, JobTasks.task_id == Task.id).order_by(Task.order.asc() ).all()

    return render_template('list_jobs.html',job_list=jobs, job_tasks = job_tasks)

@jobs.route("/<int:job_id>/update_job", methods=['GET', 'POST'])
@login_required
def update_job(job_id):
    job = Job.query.get_or_404(job_id)

    form = JobForm()
    if form.validate_on_submit():
        job.name = form.name.data
        job.note = form.note.data
        job.status = form.status.data
        job.job_date = form.job_date.data
        job.priority = form.priority.data

        db.session.commit()
        return redirect(url_for('jobs.list_jobs'))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.name.data = job.name
        form.note.data = job.note 
        form.status.data = job.status
        form.job_date.data = job.job_date
        form.priority.data = job.priority
    return render_template('create_job.html',form=form, job_id=job_id, update=True)


@jobs.route("/<int:job_id>/delete", methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    # get all the Tasks Id's we want to delete for this job
    job_tasks = db.session.query( Task.id).join( JobTasks, Task.id == JobTasks.task_id).filter(JobTasks.job_id == job_id)
    #convert to list we can use to delete from Task
    filter_list = [ f[0] for f in job_tasks.all()]
    #now delete from Task
    db.session.query(Task).filter(Task.id.in_(filter_list)).delete()
    #delete from JobTasks
    db.session.query(JobTasks).filter(JobTasks.job_id == job_id).delete()
    #delete from LocationTracker
    db.session.query(LocationTracker).filter(LocationTracker.job_id == job_id).delete()
    # delete job
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('jobs.list_jobs'))