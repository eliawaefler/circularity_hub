import psycopg2
import os


def write_to_db(connection_string, table, data):
    try:
        conn = psycopg2.connect(connection_string)
        cur = conn.cursor()
        columns = ', '.join(data.keys())
        values = [data[col] for col in data.keys()]
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cur.execute(query, values)
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        return True


def read_db(connection_string, table, condition='1=1', printout=False):
    try:
        conn = psycopg2.connect(connection_string)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table} WHERE {condition}")
        rows = cur.fetchall()
        if printout:
            for row in rows:
                print(row)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def main():
    connection_string = os.environ["NEON_URL"]
    table_name = "geb"
    data_to_insert = {
        'id': 7,
        'baujahr': 1990,
        'user_name': 'laptop',
        'nutzung': 'Residential',
        'datenstufe': 'Initial',
        'autor': 'webscraper',
        'typ': 'neu',
        'name': 'Neubau EFX',
        'adresse': '1234 Main St.'
    }

    write_to_db(connection_string, table_name, data_to_insert)
    print("\nEntries in the database:")
    read_db(connection_string, table_name, printout=True)


if __name__ == "__main__":
    main()
