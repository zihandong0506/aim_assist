import os

# Define your paths
IMG_DIR = "dataset/images/train"
LBL_DIR = "dataset/labels/train"

def cleanup():
    print(f"--- Cleaning up {IMG_DIR} ---")
    
    # Get list of all images and labels
    images = [f for f in os.listdir(IMG_DIR) if f.endswith('.jpg')]
    labels = [f for f in os.listdir(LBL_DIR) if f.endswith('.txt')]
    
    # Remove file extensions to compare names (e.g., 'img_001')
    label_names = {os.path.splitext(f)[0] for f in labels}
    
    deleted_count = 0

    for img_file in images:
        img_name = os.path.splitext(img_file)[0]
        
        # Check if this image has a matching label file
        if img_name not in label_names:
            img_path = os.path.join(IMG_DIR, img_file)
            
            # --- DELETE THE FILE ---
            os.remove(img_path)
            print(f"Deleted orphan image: {img_file}")
            deleted_count += 1

    print(f"--- Cleanup Complete. Deleted {deleted_count} images. ---")

if __name__ == "__main__":
    # Optional: Safety confirm
    confirm = input("This will DELETE images that have no labels. Type 'yes' to proceed: ")
    if confirm.lower() == "yes":
        cleanup()
    else:
        print("Operation cancelled.")