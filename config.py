import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

# Carga las variables del archivo .env
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Clave secreta
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "super-secret-key")

    # Google OAuth
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

    # URI de la base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or \
        'sqlite:///' + os.path.join(basedir, 'Pandora.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

