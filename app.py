from flask import Flask, render_template, request, jsonify, redirect, url_for, session
# from data import get_data_from_postgres

app = Flask(__name__)
app.secret_key = 'ENS'

data = {'Nagpur': {'Katol': [], 'Savner': [], 'Hingna': [], 'Umred (SC)': [], 'Nagpur South West': [{'id': 1, 'name': 'Ambazari'}, {'id': 154, 'name': 'Ajni'}], 'Nagpur South': [], 'Nagpur East': [], 'Nagpur Central': [], 'Nagpur West': [], 'Nagpur North (SC)': [], 'Kamthi': [], 'Ramtek': []}}

@app.route('/')
def index():
    # global data  # Use the global variable
    # data = get_data_from_postgres()
   
    return render_template('final.html', cities=list(data.keys()))

@app.route('/get_regions/<district>', methods=['GET'])
def get_regions(district):
    district_data = data.get(district, {})
    regions = list(district_data.keys())
    return jsonify(regions)

@app.route('/get_wards/<district>/<region>', methods=['GET'])
def get_wards(district, region):
    region_data = data.get(district, {}).get(region, [])
    return jsonify(region_data)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    location_data = request.json
    session['location_data'] = location_data
    return redirect(url_for('user'))

@app.route('/user')
def user():
    location_data = session.get('location_data', {})
    print(location_data)
    return render_template('users.html')

if __name__ == '__main__':
    app.run(debug=True)
