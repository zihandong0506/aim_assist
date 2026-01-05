import cv2
import os

# --- CONFIGURATION ---
VIDEO_PATH = "/Users/dong/Documents/aim_assist_train_backup/video_raw/video3.mp4"       # Put your video filename here
OUTPUT_FOLDER = "/Users/dong/Documents/aim_assist_train_backup/video_to_img" # Where the images will go
FRAME_STEP = 10                    # 1 = Save every frame. 10 = Save every 10th frame.

def extract_frames():
    # 1. Create output folder if it doesn't exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"Created folder: {OUTPUT_FOLDER}")

    # 2. Open the video file
    cap = cv2.VideoCapture(VIDEO_PATH)
    
    if not cap.isOpened():
        print(f"❌ Error: Could not open video {VIDEO_PATH}.")
        print("Tip: If this is AV1, ensure your OpenCV supports it or convert to H.264 first.")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"--- Processing {VIDEO_PATH} ---")
    print(f"Total frames in video: {total_frames}")

    count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        
        # If no frame is returned, we reached the end
        if not ret:
            break

        # Only save if we hit the step count
        if count % FRAME_STEP == 0:
            # Create a filename like 'frame_0001.jpg'
            filename = os.path.join(OUTPUT_FOLDER, f"frame_{saved_count:05d}.jpg")
            cv2.imwrite(filename, frame)
            saved_count += 1
            
            # Print progress every 100 saved frames
            if saved_count % 100 == 0:
                print(f"Saved {saved_count} images...")

        count += 1

    cap.release()
    print(f"✅ Done! Extracted {saved_count} images to '{OUTPUT_FOLDER}'.")

if __name__ == "__main__":
    extract_frames()