import pymongo
from flask import Flask, render_template
from flask_pymongo import PyMongo
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Match_History/')
def Match_History():
    return render_template('Match_History.html')

@app.route('/Champions/')
def Champions():
    return render_template('Champions.html')

if __name__=='__main__':
    app.run()