from flask import Flask, render_template
from dotenv import load_dotenv
load_dotenv()
import DBHandler

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Match_History/')
def Match_History():
    match = DBHandler.Match_collection.find({})
    return render_template('Match_History.html', match = match)

@app.route('/Champions/')
def Champions():
    champions = DBHandler.Champ_collection.find({})
    return render_template('Champions.html', champions = champions)

if __name__=='__main__':
    app.run()