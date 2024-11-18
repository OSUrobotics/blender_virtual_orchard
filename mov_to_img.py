import cv2
import os
from glob import glob

def process_video_folder(folder_path, output_root):
    # Find all .mov files in the folder
    video_files = glob(os.path.join(folder_path, '*.mov'))

    if not video_files:
        print("No .mov files found in the specified folder.")
        return

    for video_path in video_files:
        # Create a subfolder for each video to store its frames
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        output_folder = os.path.join(output_root, video_name)
        os.makedirs(output_folder, exist_ok=True)

        # Open the video file
        cap = cv2.VideoCapture(video_path)
        frame_count = 0

        # Process each frame
        while True:
            ret, frame = cap.read()
            if not ret:
                break  # Stop if there are no frames left

            # Save each frame as an image
            frame_filename = os.path.join(output_folder, f'frame_{frame_count:04d}.jpg')
            cv2.imwrite(frame_filename, frame)
            frame_count += 1

        # Release the video capture object
        cap.release()
        print(f"Extracted {frame_count} frames from '{video_name}' to '{output_folder}'.")

# Usage
input_folder = 'C://Users//abhin//Downloads//UFO_Cellphone//UFO_Cellphone'  # Folder containing .mov files
output_folder = 'C://Users//abhin//Downloads//UFO_Cellphone//UFO_Cellphone//frames'       # Root output folder for frames

process_video_folder(input_folder, output_folder)
