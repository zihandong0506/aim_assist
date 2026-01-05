from ultralytics import YOLO
import torch
import os

def main():
    # --- 1. SETUP DEVICE (Mac Optimization) ---
    # We prioritize Apple Metal (MPS) for speed. 
    # If that fails or is unavailable, we fall back to CPU.
    if torch.backends.mps.is_available():
        device = "mps"
        print(f"✅ Success: Using Apple Metal (MPS) Acceleration.")
    else:
        device = "cpu"
        print(f"⚠️ Warning: Apple Silicon not detected. Using CPU (Slower but stable).")

    # --- 2. INITIALIZE MODEL ---
    # Load the lightweight YOLOv8 Nano model (pretrained on COCO dataset)
    print("--- Loading YOLOv8 Nano Model ---")
    model = YOLO('yolov8n.pt') 

    # --- 3. START TRAINING (TURBO CONFIG) ---
    print(f"--- Starting Training on {device.upper()} ---")
    
    try:
        results = model.train(
            data="data.yaml",   # Path to your config file
            epochs=100,         # How many times to cycle through the data
            imgsz=640,          # Standard image size
            device=device,      # Use the Mac's GPU
            
            # --- PERFORMANCE SETTINGS ---
            batch=8,            # Compromise: High enough for speed, low enough to prevent crashes
            workers=4,          # Uses 4 CPU cores to prepare images in background
            cache=True,         # CRITICAL: Loads all images into RAM for instant access
            amp=True,           # Automatic Mixed Precision (Faster math)
            
            # --- OUTPUT SETTINGS ---
            project="human_detection_project",
            name="mac_run_optimized",
            exist_ok=True,      # Overwrite folder if it exists (saves disk space)
            patience=20         # Stop early if it stops learning for 20 epochs
        )
        
        print("\n✅ Training Complete!")
        print(f"Best model saved at: {results.save_dir}/weights/best.pt")

    except Exception as e:
        print(f"\n❌ CRASH DETECTED: {e}")
        print("Tip: If this is a 'Memory' or 'Malloc' error, change 'batch=8' to 'batch=4' in the code.")

if __name__ == '__main__':
    # This protection is required for Multiprocessing (workers=4) on Mac/Windows
    main()