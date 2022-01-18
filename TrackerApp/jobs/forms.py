from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime

class JobForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    note = TextAreaField('Note')
    status = SelectField('Job Status', validators=[DataRequired()], 
                        choices=[("Ready", 'Ready'), ("Start",'Start'), ("Complete",'Complete'), ("Pending",'Pending')])
    job_date = DateField("Job Date", validators=[DataRequired()], format="%Y-%m-%d", default=datetime.utcnow)
    priority = IntegerField("Job Priority", default = 1)
    submit = SubmitField('Save')

