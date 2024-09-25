import pandas as pd

class InferenceEngine:
    def __init__(self, data_file='app/data/healthcare_data.csv'):
        self.data_file = data_file
        self.df = pd.read_csv(data_file)

    def diagnose(self, symptoms):
        diagnosis_prob = {'malaria': 0, 'typhoid': 0, 'fever': 0}

        for symptom in symptoms:
            if symptom in self.df['symptom'].values:
                row = self.df[self.df['symptom'] == symptom]
                diagnosis_prob['malaria'] += row['malaria'].values[0]
                diagnosis_prob['typhoid'] += row['typhoid'].values[0]
                diagnosis_prob['fever'] += row['fever'].values[0]

        num_symptoms = len(symptoms)
        if num_symptoms > 0:
            for key in diagnosis_prob:
                diagnosis_prob[key] = diagnosis_prob[key] / num_symptoms

        return diagnosis_prob

    def get_recommendation(self, diagnosis, age):
        age_group = self.get_age_group(age)

        recommendations = {
            'malaria': {
                'high': {
                    'baby': 'Immediate medical attention is recommended. Artemisinin-based combination therapies (ACTs).',
                    'child': 'Artemisinin-based combination therapies (ACTs), Quinine, Doxycycline.',
                    'youth': 'Artemisinin-based combination therapies (ACTs), Quinine, Doxycycline.',
                    'elderly': 'Artemisinin-based combination therapies (ACTs), Quinine, Doxycycline. Monitor closely.'
                },
                'medium': {
                    'baby': 'Hydration and immediate medical consultation.',
                    'child': 'Artemisinin-based combination therapies (ACTs), Hydration, and rest.',
                    'youth': 'Artemisinin-based combination therapies (ACTs), Hydration, and rest.',
                    'elderly': 'Artemisinin-based combination therapies (ACTs), Hydration, and rest. Monitor closely.'
                },
                'low': {
                    'baby': 'Hydration and seek medical advice.',
                    'child': 'Hydration and over-the-counter antipyretics.',
                    'youth': 'Hydration and over-the-counter antipyretics.',
                    'elderly': 'Hydration and seek medical advice.'
                }
            },
            'typhoid': {
                'high': {
                    'baby': 'Hospitalization may be necessary. Ciprofloxacin, Azithromycin, Ceftriaxone.',
                    'child': 'Ciprofloxacin, Azithromycin, Ceftriaxone. Hospitalization may be needed for severe cases.',
                    'youth': 'Ciprofloxacin, Azithromycin, Ceftriaxone.',
                    'elderly': 'Ciprofloxacin, Azithromycin, Ceftriaxone. Hospitalization might be necessary for severe cases.'
                },
                'medium': {
                    'baby': 'Rest and antibiotics. Seek medical consultation.',
                    'child': 'Ciprofloxacin or Azithromycin. Rest and hydration.',
                    'youth': 'Ciprofloxacin or Azithromycin. Rest and hydration.',
                    'elderly': 'Ciprofloxacin or Azithromycin. Rest and hydration. Monitor closely.'
                },
                'low': {
                    'baby': 'Rest and hydration. Mild antibiotics.',
                    'child': 'Rest and hydration. Mild antibiotics if necessary.',
                    'youth': 'Rest and hydration. Mild antibiotics if necessary.',
                    'elderly': 'Rest and hydration. Consult a doctor if symptoms persist.'
                }
            },
            'fever': {
                'high': {
                    'baby': 'Paracetamol with medical supervision. Ensure hydration.',
                    'child': 'Paracetamol, Ibuprofen, and hydration. Consult a doctor if fever persists.',
                    'youth': 'Paracetamol, Ibuprofen, and hydration. Consult a doctor if fever persists.',
                    'elderly': 'Paracetamol, Ibuprofen, and hydration. Consult a doctor for persistent fever.'
                },
                'medium': {
                    'baby': 'Paracetamol and hydration. Consult a doctor if needed.',
                    'child': 'Paracetamol and rest. Maintain hydration.',
                    'youth': 'Paracetamol and rest. Maintain hydration.',
                    'elderly': 'Paracetamol and rest. Monitor closely for any complications.'
                },
                'low': {
                    'baby': 'Rest and hydration.',
                    'child': 'Rest and hydration. Over-the-counter antipyretics if necessary.',
                    'youth': 'Rest and hydration. Over-the-counter antipyretics if necessary.',
                    'elderly': 'Rest and hydration. Consult a doctor if needed.'
                }
            }
        }

        result_recommendations = {}
        for illness, probability in diagnosis.items():
            if probability >= 0.75:
                result_recommendations[illness] = recommendations[illness]['high'][age_group]
            elif probability >= 0.5:
                result_recommendations[illness] = recommendations[illness]['medium'][age_group]
            else:
                result_recommendations[illness] = recommendations[illness]['low'][age_group]

        return result_recommendations

    def get_age_group(self, age):
        if age < 2:
            return 'baby'
        elif 2 <= age < 12:
            return 'child'
        elif 12 <= age < 60:
            return 'youth'
        else:
            return 'elderly'
