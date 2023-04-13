import os
import sqlite3
import numpy as np
from PIL import Image, ImageOps
from scipy.spatial.distance import cosine
import torch
import torchvision.transforms as transforms
import torchvision.models as models

def get_image_features(image_path, model, transform):
    img = Image.open(image_path)
    img = transform(img)
    img = img.unsqueeze(0)
    
    with torch.no_grad():
        features = model(img)
    
    return features.squeeze().numpy()

def process_images(image_folder, threshold=0.5, resize_size=(224, 224)):
    image_files = sorted(os.listdir(image_folder))
    prev_image = None
    prev_image_name = None

    transform = transforms.Compose([
        transforms.Resize(resize_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    model = models.resnet18(pretrained=True)
    model = torch.nn.Sequential(*(list(model.children())[:-1]))
    model.eval()

    # Create and set up the database
    conn = sqlite3.connect("DATAMODEL.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS basetable (id INTEGER PRIMARY KEY, image_name TEXT)")

    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        current_image = get_image_features(image_path, model, transform)

        if prev_image is not None:
            similarity = 1 - cosine(prev_image, current_image)

            if similarity < threshold:
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

if __name__ == "__main__":
    approximate_similarity()
