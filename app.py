from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from data import get_data_from_postgres, get_candidates_for_location
import psycopg2

app = Flask(__name__)
app.secret_key = 'ENS'

db_params = {
    'dbname': 'election_database',
    'user': 'mihir',
    'password': '2f1dXRnCquM3IxCVmsEjZEir0HmKp2fA',
    'host': 'dpg-cm5tuba1hbls73alqd4g-a.singapore-postgres.render.com',
    'port': 5432
}

@app.route('/')
def index():
    data = get_data_from_postgres()
    session['data'] = data
    return render_template('index.html', cities=list(data.keys()))

@app.route('/get_regions/<district>', methods=['GET'])
def get_regions(district):
    district_data = session['data'].get(district, {})
    regions = list(district_data.keys())
    return jsonify(regions)

@app.route('/get_wards/<district>/<region>', methods=['GET'])
def get_wards(district, region):
    region_data = session['data'].get(district, {}).get(region, [])
    session['region_data'] = {'city':district, 'region':region}
    session['candidates'] = get_candidates_for_location(session['region_data'])
    return jsonify(region_data)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    location_data = request.json
    candidates = get_candidates_for_location(location_data)
    session['location_data'] = location_data
    session['candidates'] = candidates
    return redirect(url_for('user'))


# Function to execute SQL queries
def execute_query(query, parameters=None):
    """
    Executes a SQL query using the psycopg2 library to connect to a PostgreSQL database.

    Args:
        query (str): The SQL query to be executed.
        parameters (list, optional): The parameters to be used in the query. Defaults to None.

    Returns:
        list: The result of the executed query, which is a list of tuples representing the rows returned by the query.
    """
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    try:
        cursor.execute(query, parameters)
        result = cursor.fetchall()
        return result

    finally:
        cursor.close()
        connection.close()

@app.route("/user", methods=["GET", "POST"])
def user():
    """
    Handle GET and POST requests to retrieve voter information.

    Args:
        request (Flask request object): The request object containing the form data.
        session (Flask session object): The session object for storing user data.
        db_params (dict): The parameters for connecting to the PostgreSQL database.

    Returns:
        Rendered template with the user data, if found in the session.
        Rendered template with the option to select the desired data, if there is a name conflict.
        Voter information retrieved from the database, if there is a single match.
    """
    if request.method == "POST":
        # formats the name in the way its stored in DB
        name = request.form.get("name").lower().title()
        voter_id = request.form.get("voting-id")
        location_data = session.get('location_data', {})
        # candidates = session.get('candidates', [])
        district_name = location_data.get('city', "").title()
        region_name = location_data.get('region', "").title()
        part_name = location_data.get('ward', "").title()

        if not name and not voter_id:
            return render_template("users.html", error_message="Please Enter Name")
        
        if name:

            # Split the full name into parts
            name_parts = name.split()

            # Extract first name, middle name (if available), and last name
            first_name = name_parts[0]
            last_name = name_parts[-1]
            middle_name = name_parts[1] if len(name_parts) > 2 else None

            # Check if user data is in the session
            # user_data = session.get(name)

            # SQL query for cases with or without middle name
            query = """
                SELECT v.first_name, v.middle_name, v.last_name, v.age, v.gender, vb.coordinates, v.voter_id, vb.polling_station_address, v.full_name
                FROM voters v
                JOIN booths vb ON v.booth_number = vb.booth_number
                JOIN parts p ON vb.part_id = p.part_id
                JOIN assemblyconstituencies ac ON p.constituency_id = ac.constituency_id
                JOIN districts d ON ac.district_id = d.district_id
                WHERE v.first_name = %s
                AND v.last_name = %s
                AND d.district_name = %s
                AND ac.constituency_name = %s
            """

            parameters = [first_name, last_name, district_name, region_name]

            if part_name:
                query += " AND p.part_name = %s"
                parameters.append(part_name)

            if middle_name:
                query += " AND v.middle_name = %s"
                parameters.append(middle_name)

            try:
                result = execute_query(query, parameters)
                # if name conflict arrises
                if len(result) > 1:
                    # redirect to same page with option to pick your own data
                    """
                    Here will be the logic for using pagination
                    """
                    return render_template('users.html', result=result, show_table = True)
                
                # if single data
                # add here a middle step
                elif len(result) == 1:
                    # session[name] = result
                    location = result[0][5]
                    location = location.replace('&', '%26').replace(',', '%2C').replace('.', '%2E').replace(' ', '')
                    cpy = result[0][5].replace(' ', '')
                    print(result)
                    return render_template('restpage.html', result=result[0], location=location, cpy=cpy)

                # If no results, show an error message
                return render_template("users.html", error_message="No Data Found")

            except Exception as e:
                return render_template("users.html", error_message=str(e))
                
        elif voter_id:
            # Search by voter ID
            query = """
                SELECT v.first_name, v.middle_name, v.last_name, v.gender, v.age, vb.coordinates, v.full_name
                FROM voters v
                JOIN booths vb ON v.booth_number = vb.booth_number
                JOIN parts p ON vb.part_id = p.part_id
                JOIN assemblyconstituencies ac ON p.constituency_id = ac.constituency_id
                JOIN districts d ON ac.district_id = d.district_id
                WHERE v.voter_id = %s
            """

            try:
                result = execute_query(query, [voter_id])

                if len(result) == 1:
                    # session[name] = result
                    return render_template('restpage.html', result=result[0])
                else:
                    return render_template("users.html", error_message="No Data Found")

            except Exception as e:
                return render_template("users.html", error_message=str(e))
    else:
        candidates = session.get('candidates', [])
        candidates = [candidates[x][0] for x in range(0, len(candidates))]
        return render_template("users.html", candidates=candidates)
    
    
@app.route("/redirect/<address>")
def redirect(address):

    query = """
    SELECT vb.coordinates, vb.polling_station_address, v.full_name
    FROM voters v
    JOIN booths vb ON v.booth_number = vb.booth_number
    JOIN parts p ON vb.part_id = p.part_id
    JOIN assemblyconstituencies ac ON p.constituency_id = ac.constituency_id
    JOIN districts d ON ac.district_id = d.district_id
    WHERE vb.coordinates = %s
    """

    try:
        result = execute_query(query, [address])
        location=address
        cpy = location.replace(' ', '')
        location = location.replace('&', '%26').replace(',', '%2C').replace('.', '%2E').replace(' ', '')
        return render_template("multirestpage.html", result=result, location=location, cpy=cpy)
    except Exception as e:
        return render_template('users.html')



# Error handlers
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500

if __name__ == '__main__':
    app.run(debug=True)
