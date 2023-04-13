import os
import cv2
import torch
import torchvision
from torchvision import transforms
from PIL import Image

# Load the pre-trained model
def load_model():
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    model.eval()
    return model

# Detect objects in the image
def detect_objects(image, model):
    transform = transforms.Compose([transforms.ToTensor()])
    image_tensor = transform(image)
    image_tensor = image_tensor.unsqueeze(0)
    with torch.no_grad():
        detections = model(image_tensor)
    return detections[0]

# Process the image with object detection
def process_image_with_object_detection(input_path, output_path, model):
    img = Image.open(input_path).convert("RGB")
    detections = detect_objects(img, model)

    scores = detections["scores"]
    boxes = detections["boxes"]
    labels = detections["labels"]

    img_cv2 = cv2.imread(input_path)

    for i in range(len(scores)):
        if scores[i] > 0.5:
            box = boxes[i].numpy()
            x_min, y_min, x_max, y_max = box.astype(int)
            cv2.rectangle(img_cv2, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
    cv2.imwrite(output_path, img_cv2)

def process_images_in_folder(input_folder, output_folder, model):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_folder, file)
                process_image_with_object_detection(input_path, output_path, model)
                print(f"Processed {input_path} and saved filtered image to {output_path}")

if __name__ == "__main__":
    input_folder = "images"    # Replace with the path to your folder containing the input images
    output_folder = "images_preprocessed"  # Replace with the path to the folder where you want to save the filtered images

    model = load_model()
    process_images_in_folder(input_folder, output_folder, model)
