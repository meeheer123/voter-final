import psycopg2

# Connect to PostgreSQL (replace placeholders with your actual credentials)
conn = psycopg2.connect(
    user="neondb_owner",
    password="WfUh8X4irjuS",
    host="ep-dry-silence-a1cd2fru.ap-southeast-1.aws.neon.tech",
    database="neondb"
)

# Function to fetch data from the database and organize it
def get_data_from_postgres():
    formatted_data = {}

    with conn.cursor() as cursor:
        # Fetch data from the AssemblyConstituencies table
        cursor.execute("SELECT district_name, districts.district_id, constituency_name, assemblyconstituencies.constituency_id FROM districts INNER JOIN assemblyconstituencies ON districts.district_id = assemblyconstituencies.district_id")
        data_assembly = cursor.fetchall()

        # Organize data by district and constituency
        for district_name, district_id, constituency_name, constituency_id in data_assembly:
            if district_name not in formatted_data:
                formatted_data[district_name] = {}
            formatted_data[district_name][constituency_name] = []

        # Fetch data from the Parts table
        cursor.execute("SELECT district_name, districts.district_id, constituency_name, assemblyconstituencies.constituency_id, part_name, part_id FROM districts INNER JOIN assemblyconstituencies ON districts.district_id = assemblyconstituencies.district_id INNER JOIN Parts ON districts.district_id = parts.district_id AND assemblyconstituencies.constituency_id = parts.constituency_id")
        data_parts = cursor.fetchall()

        # Organize data by district, constituency, and part
        for district_name, district_id, constituency_name, constituency_id, part_name, part_id in data_parts:
            booth_data = {'id': part_id, 'name': part_name}
            formatted_data[district_name][constituency_name].append(booth_data)

    return formatted_data

def get_candidates_for_location(location_data):

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    try:
        # Example query: Fetch candidates based on location data
        query = """
            SELECT v.full_name as candidate_info
            FROM voters v
            JOIN booths vb ON v.booth_number = vb.booth_number
            JOIN parts p ON vb.part_id = p.part_id
            JOIN assemblyconstituencies ac ON p.constituency_id = ac.constituency_id
            JOIN districts d ON ac.district_id = d.district_id
            WHERE d.district_name = %s
            AND ac.constituency_name = %s

        """

        # Extract data from the location_data dictionary
        district = location_data.get('city', '').lower().title()
        region = location_data.get('region', '').lower().title()
        ward = location_data.get('ward', '').lower().title()

        parameters = (district, region)

        if ward:
            query += " AND p.part_name = %s"
            parameters += (ward,)

        # Execute the query with the location data
        cursor.execute(query, parameters)

        # Fetch all the candidates
        candidates = cursor.fetchall()

        # Return the list of candidates
        return candidates

    except Exception as e:
        print(f"Error fetching candidates: {e}")
        return []

# Example usage
if __name__ == "__main__":
    data_from_postgres = get_data_from_postgres()
    print(data_from_postgres)

# Close the database connection
# conn.close()
