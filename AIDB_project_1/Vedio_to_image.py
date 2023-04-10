import os
import cv2

def extract_frames(video_path, output_folder, frame_frequency):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Get the total number of frames in the video
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Process each frame
    for frame_idx in range(0, total_frames, frame_frequency):
        # Set the video's position to the current frame index
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)

        # Read the frame from the video
        ret, frame = video.read()

        # If the frame was read successfully, save it as an image
        if ret:
            image_path = os.path.join(output_folder, f"frame{frame_idx:04d}.png")
            cv2.imwrite(image_path, frame)
            print(f"Saved frame {frame_idx} to {image_path}")
        else:
            print(f"Failed to read frame {frame_idx}")

    # Release the video file
    video.release()

def vedio_to_image():
    video_path = "input1.mp4"         
    output_folder = "images"  
    frame_frequency = 15                         # Frequency at which to extract frames

    extract_frames(video_path, output_folder, frame_frequency)
