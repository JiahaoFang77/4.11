import sqlite3

def process_database(database_file):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Remove newline characters and extra spaces from the text
    cursor.execute("UPDATE Mlmappings SET text = REPLACE(REPLACE(text, '\n', ''), ' ', '')")

    # Create the output table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS User_defined_metadata (
        id INTEGER PRIMARY KEY,
        text_grouped TEXT,
        difference INTEGER
    )
    ''')

    # Group by the text column and calculate the difference between the largest and smallest image numbers
    cursor.execute('''
    INSERT INTO User_defined_metadata (text_grouped, difference)
    SELECT text, (MAX(CAST(SUBSTR(image_name, 6, LENGTH(image_name) - 9) AS INTEGER)) - MIN(CAST(SUBSTR(image_name, 6, LENGTH(image_name) - 9) AS INTEGER)))/20 + 1
    FROM Mlmappings
    WHERE text != ''
    GROUP BY text
    ''')

    conn.commit()
    conn.close()

def User_defined_metadata():
    database_file = "DATAMODEL.db"  # Update this path to your SQLite database file
    process_database(database_file)
