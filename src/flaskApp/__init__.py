from flask import Flask
app = Flask(__name__)
import os
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv("FLASK_KEY")

app.config['SECRET_KEY'] = secret_key
