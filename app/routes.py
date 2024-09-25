from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import User, History
from app.forms import RegistrationForm, PatientIDForm, DiagnosisForm
from app.inference_engine import InferenceEngine
from wtforms import StringField
import json

from flask import jsonify

routes = Blueprint('routes', __name__)

inference_engine = InferenceEngine()

@routes.route('/', methods=['GET', 'POST'])
def home():
    form = PatientIDForm()
    
    # Check if the form is submitted via POST
    if form.validate_on_submit():
        user_id = form.patient_id.data
        user = User.query.get(user_id)
        
        if user:
            flash('Patient ID found!', 'success')
            return redirect(url_for('routes.dashboard', user_id=user_id))
        else:
            flash('Patient ID not found!', 'danger')
            return redirect(url_for('routes.home'))
    
    # Render the home page with the form if GET request or form validation fails
    return render_template('home.html', form=form)
    
    
@routes.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    user = User.query.get_or_404(user_id)
    history_entries = History.query.filter_by(user_id=user_id).order_by(History.timestamp.desc()).all()
    
    # Convert History objects to dictionaries
    history_data = [
        {
            'timestamp': entry.timestamp.isoformat(),  # Convert datetime to ISO format string
            'symptoms': entry.symptoms,
            'diagnosis': entry.diagnosis,
            'treatment': entry.treatment
        }
        for entry in history_entries
    ]
    
    # Get the user's age
    age = user.get_age()
    
    return render_template('dashboard.html', user=user, history=history_data, age=age)



@routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data, 
            date_of_birth=form.date_of_birth.data, 
            gender=form.gender.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Patient registered successfully!', 'success')
        return redirect(url_for('routes.dashboard', user_id=user.id))
    return render_template('register.html', form=form)

@routes.route('/diagnose/<int:user_id>', methods=['GET', 'POST'])
def diagnose(user_id):
    form = DiagnosisForm()
    
    # If the request method is GET, populate the symptoms dynamically
    symptoms_list = inference_engine.df['symptom'].tolist()
    form.symptoms.choices = [(symptom, symptom) for symptom in symptoms_list]

    # If the form is submitted and validated
    if form.validate_on_submit():
        # Get the selected symptoms from the form
        selected_symptoms = form.symptoms.data        
        
        # Fetch user to get age
        user = User.query.get(user_id)
        if not user:
            flash('User not found!', 'danger')
            return redirect(url_for('routes.home'))

        age = user.get_age()
        user = User.query.get_or_404(user_id)
        
        # Diagnose and get recommendations
        diagnosis_probabilities = inference_engine.diagnose(selected_symptoms)
        highest_diagnosis = max(diagnosis_probabilities, key=diagnosis_probabilities.get)
        recommendations = inference_engine.get_recommendation(diagnosis_probabilities, age)
        
        # Get recommendation for the highest probability illness
        top_recommendation = {highest_diagnosis: recommendations[highest_diagnosis]}
        
        # Create a new history entry
        new_history = History(
            user_id=user_id,
            symptoms=', '.join(selected_symptoms),
            diagnosis=highest_diagnosis,  # Only the highest probability diagnosis
            treatment=top_recommendation[highest_diagnosis]  # Only the recommendation for the highest diagnosis
        )
        db.session.add(new_history)
        db.session.commit()
        
        # Pass only the top recommendation to the result.html template
        return render_template('result.html', 
                               probabilities=diagnosis_probabilities, 
                               recommendations=top_recommendation,
                               history=new_history,
                               user=user
                               )

    # Render the diagnose page with the form
    return render_template('diagnose.html', user_id=user_id, form=form)