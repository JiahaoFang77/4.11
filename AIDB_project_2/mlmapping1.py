import os
import shutil
import sqlite3

def connect_db(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def get_image_names(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT image_name FROM {table_name}")
    image_names = [row[0] for row in cursor.fetchall()]
    return image_names

def copy_images_to_folder(image_names, source_folder, destination_folder):
    for image_name in image_names:
        source_path = os.path.join(source_folder, image_name)
        destination_path = os.path.join(destination_folder, image_name)

        if os.path.exists(source_path):
            shutil.copy(source_path, destination_path)
            print(f"Copied {image_name} to {destination_folder}")
        else:
            print(f"Image {image_name} not found in {source_folder}")

def mlmapping1():
    db_file = "datamodel.db"  # Replace with the name of your database file
    table_name = "basetable"  # Replace with the name of your table containing the image names

    source_folder = "images"  # Replace with the path to the folder containing the source images
    destination_folder = "images_preprocessed"  # Replace with the path to the folder where the selected images will be copied

    conn = connect_db(db_file)
    image_names = get_image_names(conn, table_name)
    conn.close()

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    copy_images_to_folder(image_names, source_folder, destination_folder)
