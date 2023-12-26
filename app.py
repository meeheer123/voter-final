from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

cities = ['Nagpur', 'City2']  # Add more cities as needed
regions = {'Nagpur': ['East', 'West', 'Northeast'], 'City2': ['Region1', 'Region2']}
wards = {'East': ['Wardhaman Nagar', 'Another Ward'], 'West': ['Ward1', 'Ward2'],
         'Northeast': ['Ward3', 'Ward4'], 'Region1': ['WardA', 'WardB'], 'Region2': ['WardX', 'WardY']}

@app.route('/')
def index():
    return render_template('index_flask.html', cities=cities)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.get_json()

    # Assuming the data received contains city, region, and ward information
    selected_city = data.get('dropdown1', '')
    selected_region = data.get('dropdown2', '')
    selected_ward = data.get('dropdown3', '')

    # Process the received data as needed
    print('Selected City:', selected_city)
    print('Selected Region:', selected_region)
    print('Selected Ward:', selected_ward)

    # You can perform further processing or validation here

    return jsonify({'message': 'Form data received successfully'})

if __name__ == '__main__':
    app.run(debug=True)
