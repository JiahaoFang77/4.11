import os
import sqlite3
import numpy as np
from PIL import Image, ImageOps, ImageFilter

def mse(image_a, image_b):
    err = np.sum((image_a.astype("float") - image_b.astype("float")) ** 2)
    err /= float(image_a.shape[0] * image_a.shape[1])
    return err

def process_images(image_folder, threshold=350, resize_size=(200, 200)):
    image_files = sorted(os.listdir(image_folder))
    prev_image = None
    prev_image_name = None

    # Create and set up the database
    conn = sqlite3.connect("DATAMODEL.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS basetable (id INTEGER PRIMARY KEY, image_name TEXT)")

    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        current_image = Image.open(image_path).convert("L")  # Convert to grayscale
        current_image = ImageOps.fit(current_image, resize_size, Image.Resampling.LANCZOS)  # Resize the image
        current_image = np.array(current_image)

        if prev_image is not None:
            difference = mse(prev_image, current_image)

            if difference > threshold:
                cursor.execute("INSERT INTO basetable (image_name) VALUES (?)", (prev_image_name,))
                cursor.execute("INSERT INTO basetable (image_name) VALUES (?)", (image_file,))
                conn.commit()
                print(f"Significant change detected between images: {prev_image_name} and {image_file}")

        prev_image = current_image
        prev_image_name = image_file

    conn.close()

def approximate_similarity():
    image_folder = "images"  # Update this path to your folder containing the images
    process_images(image_folder)
