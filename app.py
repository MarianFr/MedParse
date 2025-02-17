from flask import Flask, render_template, jsonify
import json
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

app = Flask(__name__)

def load_patient_data():
    with open('processed_patients.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def create_ecog_plot(data):
    ecog_counts = Counter(str(patient.get('ecog', 'Unknown')) for patient in data)
    fig = px.bar(
        x=list(ecog_counts.keys()),
        y=list(ecog_counts.values()),
        title='ECOG Status Distribution',
        labels={'x': 'ECOG Status', 'y': 'Number of Patients'}
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_tumor_stage_plot(data):
    tumor_stages = Counter(patient.get('tumor_status', 'Unknown') for patient in data)
    fig = px.pie(
        values=list(tumor_stages.values()),
        names=list(tumor_stages.keys()),
        title='Tumor Stage Distribution'
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_bmi_plot(data):
    bmi_data = [
        {
            'name': patient.get('name', 'Unknown'),
            'bmi': float(patient.get('bmi', 0)) if patient.get('bmi', '').replace('.', '').isdigit() else 0
        }
        for patient in data
        if patient.get('bmi')
    ]
    
    if not bmi_data:
        return None
        
    fig = px.bar(
        bmi_data,
        x='name',
        y='bmi',
        title='Patient BMI Distribution',
        labels={'bmi': 'BMI', 'name': 'Patient Name'}
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_age_distribution(data):
    age_data = [
        int(patient.get('age', 0))
        for patient in data
        if patient.get('age', '').replace('.', '').isdigit()
    ]
    
    if not age_data:
        return None
        
    fig = px.histogram(
        x=age_data,
        nbins=10,
        title='Age Distribution',
        labels={'x': 'Age', 'y': 'Count'}
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def process_allergies(data):
    all_allergies = []
    for patient in data:
        if patient.get('allergies'):
            all_allergies.extend(patient['allergies'])
    return Counter(all_allergies)

@app.route('/')
def index():
    data = load_patient_data()
    ecog_plot = create_ecog_plot(data)
    tumor_plot = create_tumor_stage_plot(data)
    bmi_plot = create_bmi_plot(data)
    age_plot = create_age_distribution(data)
    allergy_stats = process_allergies(data)
    
    return render_template(
        'index.html',
        patients=data,
        ecog_plot=ecog_plot,
        tumor_plot=tumor_plot,
        bmi_plot=bmi_plot,
        age_plot=age_plot,
        allergy_stats=dict(allergy_stats)
    )

@app.route('/api/patients')
def get_patients():
    return jsonify(load_patient_data())

if __name__ == '__main__':
    app.run(debug=True) 