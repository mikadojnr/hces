import unittest
from app.inference_engine import InferenceEngine

class TestInferenceEngine(unittest.TestCase):

    def setUp(self):
        self.engine = InferenceEngine()

    def test_diagnose(self):
        symptoms = ['fever', 'headache']
        result = self.engine.diagnose(symptoms)
        self.assertGreater(result['fever'], result['typhoid'])

    def test_get_recommendation(self):
        diagnosis = {'malaria': 0.2, 'typhoid': 0.3, 'fever': 0.8}
        recommendation = self.engine.get_recommendation(diagnosis)
        self.assertEqual(recommendation, 'Antipyretics and rest. Hydration is crucial.')

if __name__ == '__main__':
    unittest.main()
