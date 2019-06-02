from flask import Flask
from yaml import load, FullLoader
from codecs import open


app = Flask(__name__)
app.config.from_object('config')

with open(app.config['CONTENTS'], 'r', encoding='utf8') as f:
    contents = load(f, Loader=FullLoader)


from quote import views
