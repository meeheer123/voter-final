from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

cities = ['Nagpur', 'City2']
regions = {'Nagpur': ['East', 'West', 'Northeast'], 'City2': ['Region1', 'Region2']}
wards = {'East': ['Wardhaman Nagar', 'Another Ward'], 'West': ['Ward1', 'Ward2'],
         'Northeast': ['Ward3', 'Ward4'], 'Region1': ['WardA', 'WardB'], 'Region2': ['WardX', 'WardY']}

@app.route('/')
def index():
    return render_template('index.html', cities=cities)

@app.route('/get_regions/<city>', methods=['GET'])
def get_regions(city):
    return jsonify(regions.get(city, []))

@app.route('/get_wards/<region>', methods=['GET'])
def get_wards(region):
    return jsonify(wards.get(region, []))

@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.json
    print('Received data:', data)
    # Add your logic to process the data here

    # For demonstration purposes, let's return a simple response
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
