import os

# --- CONFIGURATION ---
# PASTE YOUR PATH HERE AGAIN
TARGET_FOLDER = "/Users/dong/Documents/aim_assist_train_backup/labels_batch_4/obj_train_data"

def flip_labels():
    print(f"--- Flipping Labels in: {TARGET_FOLDER} ---")
    
    # Get all text files (excluding classes.txt)
    txt_files = [f for f in os.listdir(TARGET_FOLDER) if f.endswith('.txt') and f != 'classes.txt']
    
    if not txt_files:
        print("No text files found. Check your path.")
        return

    flipped_count = 0

    for filename in txt_files:
        path = os.path.join(TARGET_FOLDER, filename)
        
        new_lines = []
        file_changed = False
        
        with open(path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split()
                if not parts: continue
                
                # --- SAFETY CHECK ---
                try:
                    class_id = int(parts[0])
                except ValueError:
                    # If the first word is not a number (e.g. "data/img..."), skip this line/file
                    continue

                # SWAP LOGIC: 0 becomes 1, 1 becomes 0
                if class_id == 0:
                    parts[0] = "1"
                    file_changed = True
                elif class_id == 1:
                    parts[0] = "0"
                    file_changed = True
                
                new_lines.append(" ".join(parts) + "\n")
        
        # Only overwrite if we actually changed something
        if file_changed:
            with open(path, 'w') as f:
                f.writelines(new_lines)
            flipped_count += 1
            
    print(f"Success! Fixed labels in {flipped_count} files.")

if __name__ == "__main__":
    confirm = input(f"This will swap 0 and 1 in folder: {TARGET_FOLDER}\nType 'yes' to proceed: ")
    if confirm.lower() == "yes":
        flip_labels()