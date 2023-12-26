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
        cursor.execute("SELECT district_name, constituency_name FROM Districts INNER JOIN AssemblyConstituencies ON Districts.district_id = AssemblyConstituencies.district_id")
        data_assembly = cursor.fetchall()

        # Organize data by district and constituency
        for district_name, constituency_name in data_assembly:
            if district_name not in formatted_data:
                formatted_data[district_name] = {}
            formatted_data[district_name][constituency_name] = []

        # Fetch data from the Parts table
        cursor.execute("SELECT district_name, constituency_name, part_name FROM Districts INNER JOIN AssemblyConstituencies ON Districts.district_id = AssemblyConstituencies.district_id INNER JOIN Parts ON Districts.district_id = Parts.district_id AND AssemblyConstituencies.constituency_id = Parts.constituency_id")
        data_parts = cursor.fetchall()

        # Organize data by district, constituency, and part
        for district_name, constituency_name, part_name in data_parts:
            formatted_data[district_name][constituency_name].append(part_name)

    return formatted_data

# Example usage
if __name__ == "__main__":
    data_from_postgres = get_data_from_postgres()
    print(data_from_postgres)

# Close the database connection
# conn.close()
