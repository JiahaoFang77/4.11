import sqlite3

def connect_db(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def create_output_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS User_defined_metadata (
        id INTEGER PRIMARY KEY,
        text TEXT,
        count INTEGER
    )
    ''')
    conn.commit()

def insert_grouped_data(conn, text, count):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO User_defined_metadata (text, count) VALUES (?, ?)", (text, count))
    conn.commit()

def group_and_process(conn):
    cursor = conn.cursor()

    # Remove all blank spaces, newline characters, and leading/trailing spaces in the text before grouping
    cursor.execute('''
    SELECT TRIM(REPLACE(REPLACE(text, ' ', ''), char(10), '')) as cleaned_text, COUNT(*) as count
    FROM basetable
    WHERE TRIM(text) != ""
    GROUP BY cleaned_text
    ''')

    # Fetch the grouped data and insert it into the output_table
    grouped_data = cursor.fetchall()
    for text, count in grouped_data:
        insert_grouped_data(conn, text, count)


def User_defined_metadata():
    db_file = "datamodel.db"  # Replace with the name of your database file

    conn = connect_db(db_file)
    create_output_table(conn)
    group_and_process(conn)
    conn.close()

