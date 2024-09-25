import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

class Config:
    # Use environment variable for SECRET_KEY or provide a default (not recommended for production)
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Use environment variable for DATABASE_URL or provide a default connection string
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # Disable SQLAlchemy event notifications to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
    # Debugging
    print(f"SECRET_KEY: {os.environ.get('SECRET_KEY')}")
    print(f"DATABASE_URL: {os.environ.get('DATABASE_URL')}")
