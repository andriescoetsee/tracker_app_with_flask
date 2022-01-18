from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime

class TaskForm(FlaskForm):

    name = StringField('Task Name', validators=[DataRequired()])
    note = TextAreaField('Note', description="Test Text area")
    status = SelectField('Task Status', validators=[DataRequired()], 
                        choices=[("Ready", 'Ready'), ("Busy",'Busy'), ("Done",'Done'), ("Pending",'Pending') ])
    order = IntegerField("Task Order", default = 1)

    lon_lat = StringField()
    address = TextAreaField()
    
    submit = SubmitField('Save')