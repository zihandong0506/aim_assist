import os
import shutil
import random

# --- CONFIGURATION ---
# Define your paths relative to the project root
TRAIN_IMG_DIR = "dataset/images/train"
TRAIN_LBL_DIR = "dataset/labels/train"
VAL_IMG_DIR = "dataset/images/val"
VAL_LBL_DIR = "dataset/labels/val"

SPLIT_RATIO = 0.2  # 20% to validation

def move_files():
    # 1. Get list of all images in the training folder
    images = [f for f in os.listdir(TRAIN_IMG_DIR) if f.endswith('.jpg')]
    total_images = len(images)
    
    if total_images == 0:
        print("Error: No images found in training folder.")
        return

    # 2. Calculate how many to move
    num_to_move = int(total_images * SPLIT_RATIO)
    print(f"Found {total_images} images. Moving {num_to_move} (20%) to Validation...")

    # 3. Randomly select files
    files_to_move = random.sample(images, num_to_move)

    moved_count = 0

    # 4. Move them
    for img_file in files_to_move:
        # Construct the filenames
        base_name = os.path.splitext(img_file)[0]
        lbl_file = base_name + ".txt"

        src_img = os.path.join(TRAIN_IMG_DIR, img_file)
        dst_img = os.path.join(VAL_IMG_DIR, img_file)
        
        src_lbl = os.path.join(TRAIN_LBL_DIR, lbl_file)
        dst_lbl = os.path.join(VAL_LBL_DIR, lbl_file)

        # Move Image
        shutil.move(src_img, dst_img)

        # Move Label (Check if it exists first)
        if os.path.exists(src_lbl):
            shutil.move(src_lbl, dst_lbl)
            moved_count += 1
        else:
            print(f"Warning: Label missing for {img_file}, moving image anyway.")

    print(f"--- Success! Moved {moved_count} pairs to Validation. ---")

if __name__ == "__main__":
    move_files()