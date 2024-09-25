# tests/test_routes.py

import unittest
from app import create_app, db
from app.models import User, Symptom, Diagnosis, Treatment

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test variables and create a test client."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            self.create_test_data()

    def tearDown(self):
        """Tear down test variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_test_data(self):
        """Create initial data for testing."""
        user = User(name='John Doe', age=30, gender='Male')
        db.session.add(user)
        db.session.commit()

    def test_home_page(self):
        """Test if the home page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Expert System for Healthcare', response.data)

    def test_register_page(self):
        """Test if the register page loads correctly and registers a user."""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register New Patient', response.data)

        response = self.client.post('/register', data=dict(
            name='Jane Doe',
            age=25,
            gender='Female'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Patient Dashboard', response.data)

    def test_dashboard_page(self):
        """Test if the dashboard page displays user information."""
        response = self.client.get('/dashboard/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Patient Dashboard', response.data)

if __name__ == '__main__':
    unittest.main()
