import os
import random

# --- CONFIGURATION ---
BASE_PATH = "dataset"
FOLDERS = ["train", "val"]
DELETE_PERCENTAGE = 0.70  # Delete 70% of empty files

def is_file_empty(file_path):
    # Returns True if file is empty or only contains newlines/spaces
    try:
        if os.path.getsize(file_path) == 0:
            return True
        with open(file_path, 'r') as f:
            content = f.read().strip()
            return len(content) == 0
    except:
        return False

def clean_subset(subset):
    lbl_dir = os.path.join(BASE_PATH, "labels", subset)
    img_dir = os.path.join(BASE_PATH, "images", subset)
    
    print(f"\n--- Scanning '{subset}' ---")
    
    if not os.path.exists(lbl_dir):
        print(f"Skipping {subset} (folder not found)")
        return

    # 1. Find all text files that are effectively empty
    empty_label_files = []
    all_txts = [f for f in os.listdir(lbl_dir) if f.endswith('.txt') and f != "classes.txt"]

    for txt_file in all_txts:
        txt_path = os.path.join(lbl_dir, txt_file)
        if is_file_empty(txt_path):
            empty_label_files.append(txt_file)

    total_empty = len(empty_label_files)
    print(f"Found {total_empty} empty label files.")

    if total_empty == 0:
        return

    # 2. Calculate removal count
    count_to_delete = int(total_empty * DELETE_PERCENTAGE)
    print(f"-> Goal: Delete {count_to_delete} pairs (Keeping {total_empty - count_to_delete})")

    # 3. Randomly select
    files_to_delete = random.sample(empty_label_files, count_to_delete)

    # 4. Delete the Text AND the Image
    deleted_count = 0
    for txt_name in files_to_delete:
        # Construct paths
        txt_full_path = os.path.join(lbl_dir, txt_name)
        
        # Guess image extension (usually .jpg, but checking just in case)
        base_name = os.path.splitext(txt_name)[0]
        img_name = base_name + ".jpg" # Assuming .jpg
        img_full_path = os.path.join(img_dir, img_name)

        try:
            # Delete Label
            os.remove(txt_full_path)
            
            # Delete Image (if it exists)
            if os.path.exists(img_full_path):
                os.remove(img_full_path)
            
            deleted_count += 1
        except Exception as e:
            print(f"Error deleting {base_name}: {e}")

    print(f"✅ Cleaned {subset}: Deleted {deleted_count} empty pairs.")

if __name__ == "__main__":
    print(f"Scanning for EMPTY text files to delete {DELETE_PERCENTAGE*100}% of them...")
    confirm = input("Type 'yes' to proceed: ")
    if confirm.lower() == "yes":
        for folder in FOLDERS:
            clean_subset(folder)
        print("\n--- Done ---")