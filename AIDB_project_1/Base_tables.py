import os
import sqlite3
import pytesseract
from PIL import Image
from PIL import ImageOps

# Database functions
def connect_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS basetable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_name TEXT,
        text TEXT
    )
    ''')
    conn.commit()

def insert_image_text_to_db(conn, image_name, text):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO basetable (image_name, text) VALUES (?, ?)", (image_name, text))
    conn.commit()

def recognize_text(image_path):
    try:
        img = Image.open(image_path)

        # Enlarge the canvas and fill the enlarged blank area with black
        new_size = (img.width * 2, img.height * 2)
        enlarged_img = Image.new(img.mode, new_size, (0, 0, 0))
        enlarged_img.paste(img, ((new_size[0] - img.width) // 2, (new_size[1] - img.height) // 2))

        text = pytesseract.image_to_string(enlarged_img)
        return text
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return ""


def process_images_in_folder(folder_path, db_name):
    conn = connect_db(db_name)
    create_table(conn)

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                image_path = os.path.join(root, file)
                recognized_text = recognize_text(image_path)
                print(f"Recognized text for {file}:", recognized_text)

                insert_image_text_to_db(conn, file, recognized_text)
                print(f"Text for {file} has been inserted into the SQLite database.")

    conn.close()

def base_table():
    folder_path = "images"  # Replace with the path to your folder containing the images
    db_name = "Datamodel.db"
    process_images_in_folder(folder_path, db_name)
