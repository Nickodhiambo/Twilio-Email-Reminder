import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'yFGGY1U7X9mRShCcgehD0sYMqYJ5nGjEga01zDKvLvz8hitHsNg'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')