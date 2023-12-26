from flask import Flask, render_template, request, jsonify, redirect, url_for
from data import get_data_from_postgres

app = Flask(__name__)

data = {
    'Nagpur': {
        'Katol': [],
        'Savner': [],
        'Hingna': [],
        'Umred (SC)': [],
        'Nagpur South West': ['Ambazari', 'Ajni'],
        'Nagpur South': [],
        'Nagpur East': [],
        'Nagpur Central': [],
        'Nagpur West': [],
        'Nagpur North (SC)': [],
        'Kamthi': [],
        'Ramtek': []
    }
}

@app.route('/')
def index():
    data = get_data_from_postgres()
    return render_template('index.html', cities=list(data.keys()))

@app.route('/get_regions/<city>', methods=['GET'])
def get_regions(city):
    city_data = data.get(city, {})
    regions = list(city_data.keys())
    return jsonify(regions)

@app.route('/get_wards/<city>/<region>', methods=['GET'])
def get_wards(city, region):
    region_data = data.get(city, {}).get(region, [])
    return jsonify(region_data)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.json
    print('Received data:', data)
    # Add your logic to process the data here
    # For demonstration purposes, let's return a simple response
    return redirect(url_for('user'))

@app.route('/user')
def user():
    return render_template('users.html')

if __name__ == '__main__':
    app.run(debug=True)
