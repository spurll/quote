from flask import Flask
from yaml import load


app = Flask(__name__)
app.config.from_object('config')

with open(app.config['CONTENTS'], 'r') as f:
    contents = load(f)


from quote import views
