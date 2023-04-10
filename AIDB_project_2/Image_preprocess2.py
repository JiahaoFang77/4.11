import cv2
import os

def preprocess_license_plate(input_folder, output_folder):
    input_files = os.listdir(input_folder)

    for input_file in input_files:
        input_path = os.path.join(input_folder, input_file)
        output_path = os.path.join(output_folder, input_file)

        img = cv2.imread(input_path)

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (9, 9), 0)

        # Perform edge detection using Canny method
        edges = cv2.Canny(blurred, 100, 200)

        # Apply morphological transformations (dilation and erosion)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilated = cv2.dilate(edges, kernel, iterations=2)
        eroded = cv2.erode(dilated, kernel, iterations=1)

        # Save the preprocessed image
        cv2.imwrite(output_path, eroded)

if __name__ == "__main__":
    input_folder = "images"
    output_folder = "images_preprocessed"

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    preprocess_license_plate(input_folder, output_folder)
