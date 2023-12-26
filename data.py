import psycopg2

# Connect to PostgreSQL (replace placeholders with your actual credentials)
conn = psycopg2.connect(
    user="postgres",
    password="35789512357",
    host="localhost",
    database="election_database"
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

# Example usage
if __name__ == "__main__":
    data_from_postgres = get_data_from_postgres()
    print(data_from_postgres)

# Close the database connection
# conn.close()
