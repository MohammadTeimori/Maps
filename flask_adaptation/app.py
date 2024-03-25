from flask import Flask, request, render_template, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        origin = request.form['origin']
        destinations = request.form['destinations'].split(',')
        data = get_distance_matrix(origin, destinations)
        return render_template('results.html', data=data, origin=origin, destinations=destinations)
    return render_template('index.html')

def get_distance_matrix(origin, destinations):
    api_key = os.getenv('API_KEY')
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": "|".join(destinations),
        "key": api_key
    }
    response = requests.get(url, params=params)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
