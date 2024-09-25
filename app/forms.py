from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SubmitField, DateField, FieldList, SelectField, FormField, SelectMultipleField
from wtforms.validators import DataRequired, NumberRange

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    submit = SubmitField('Register Patient')

class PatientIDForm(FlaskForm):
    patient_id = IntegerField('Enter Patient ID', validators=[DataRequired()])
    submit = SubmitField('Search')

class DiagnosisForm(FlaskForm):
    symptoms = SelectMultipleField('Select Symptoms', choices=[], validators=[DataRequired()])
    submit = SubmitField('Diagnose')