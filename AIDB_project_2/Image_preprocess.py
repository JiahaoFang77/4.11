import os
import cv2

def preprocess_image(input_path, output_path):
    # Read the image
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    # Apply Gaussian blurring to smooth the image
    blurred_img = cv2.GaussianBlur(img, (5, 5), 0)

    # Apply adaptive thresholding to create a binary image
    binary_img = cv2.adaptiveThreshold(blurred_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Apply edge detection using the Canny algorithm
    edges_img = cv2.Canny(binary_img, 100, 200)

    # Save the binary image with edges enhanced
    cv2.imwrite(output_path, edges_img)

def process_images_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_folder, file)
                preprocess_image(input_path, output_path)
                print(f"Processed {input_path} and saved filtered image to {output_path}")

if __name__ == "__main__":
    input_folder = "images"    # Replace with the path to your folder containing the input images
    output_folder = "images_preprocessed"  # Replace with the path to the folder where you want to save the filtered images

    process_images_in_folder(input_folder, output_folder)