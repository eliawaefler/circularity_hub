import os
import psycopg2

def add_to_db(table, name, pet):
    connection_string = os.environ.get('NEON_URL')
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()

    try:
        query = f"INSERT INTO {table} (name, pet) VALUES (%s, %s)"
        cur.execute(query, (name, pet))
        conn.commit()
        print("Added to database successfully!")
    except Exception as e:
        print(f"Failed to add to database: {str(e)}")
    finally:
        cur.close()
        conn.close()

def write_to_db(table, data):
    connection_string = os.environ.get('NEON_URL')
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()

    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
    columns = [row[0] for row in cur.fetchall() if row[0] != 'id']

    columns_sql = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(columns))

    for entry in data:
        query = f"INSERT INTO {table} ({columns_sql}) VALUES ({placeholders})"
        cur.execute(query, entry)

    conn.commit()
    cur.close()
    conn.close()
    print("Records inserted successfully")

def read_db(table, criteria='1=1'):
    connection_string = os.environ.get('NEON_URL')
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()

    query = f"SELECT * FROM {table} WHERE {criteria}"
    cur.execute(query)
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

    return rows

def main():
    table_name = "home"
    data_to_insert = [("John Doe", "Dog"), ("Jane Smith", "Cat")]

    print("Reading all entries from the database:")
    read_db(table_name)

    write_to_db(table_name, data_to_insert)

    print("\nReading specific entries from the database:")
    read_db(table_name, "name='John Doe' AND pet='Dog'")

    print("\nReading all entries from the database after insertion:")
    read_db(table_name)

if __name__ == "__main__":
    main()
