import os

class Config:
    SECRET_KEY= os.environ.get('SECRET KEY', 'vervang_met_een_veilige_sleutel')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

