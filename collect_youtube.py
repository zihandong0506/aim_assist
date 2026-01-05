import cv2
import os
import time
import mss
import numpy as np

# --- CONFIGURATION ---
SAVE_PATH = "dataset/images/train"
START_INDEX = 0

# PASTE YOUR COORDINATES FROM STEP 1 HERE:
SCREEN_REGION = {'top': 200, 'left': 200, 'width': 1200, 'height': 800}

def get_next_filename(folder):
    existing = os.listdir(folder)
    count = START_INDEX
    while True:
        name = f"img_{count:04d}.jpg"
        if name not in existing:
            return os.path.join(folder, name)
        count += 1

def main():
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    sct = mss.mss()
    print(f"--- YouTube Data Collector ---")
    print(f"Region: {SCREEN_REGION}")
    print("Controls:")
    print("  [SPACE] - Save SINGLE frame")
    print("  [A]     - Toggle AUTO-CAPTURE (2 frames/sec)")
    print("  [Q]     - Quit")

    auto_mode = False
    last_capture_time = time.time()
    capture_interval = 0.5 # Seconds between auto-captures

    try:
        while True:
            # 1. Capture Screen
            sct_img = sct.grab(SCREEN_REGION)
            frame = np.array(sct_img)
            
            # Convert BGRA (Mac Screen) to BGR (OpenCV)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            # 2. Add Status Text to Preview
            preview = frame.copy()
            status_color = (0, 255, 0) if auto_mode else (0, 0, 255)
            status_text = "AUTO ON" if auto_mode else "MANUAL"
            cv2.putText(preview, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)

            # 3. Show Preview (Resize if huge Retina display makes it too big)
            cv2.imshow("YouTube Collector", preview)

            # 4. Handle Auto-Capture
            current_time = time.time()
            if auto_mode and (current_time - last_capture_time > capture_interval):
                filename = get_next_filename(SAVE_PATH)
                cv2.imwrite(filename, frame)
                print(f"[AUTO] Saved: {filename}")
                last_capture_time = current_time

            # 5. Handle Keys
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord(' '): # Spacebar
                filename = get_next_filename(SAVE_PATH)
                cv2.imwrite(filename, frame)
                print(f"[MANUAL] Saved: {filename}")
            elif key == ord('a'):
                auto_mode = not auto_mode
                print(f"Auto Mode: {auto_mode}")

    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

# python3 collect_youtube.py