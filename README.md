# YOLOv8 Human Detection Project 🎯

This repository contains a complete pipeline for training a custom YOLOv8 model to detect human **Heads** and **Bodies**, optimized for Apple Silicon (M-Series chips).

## 📦 1. Installation & Setup

Before running the scripts, set up your Python environment.

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Mac Users Only) Setup Mac-specific optimizations
chmod +x setup_mac.sh
./setup_mac.sh
```

---

## 🛠 2. The Workflow (Order of Operations)

Follow these steps to prepare your data and train the model.

### Step 1: Initialize Project Structure
Creates the necessary folder hierarchy (`dataset/images`, `dataset/labels`, etc.).
```bash
python3 init_project.py
```

### Step 2: Data Collection
Use these tools to gather raw images from video sources.
* **From YouTube:** Download videos to extract frames.
    ```bash
    python3 collect_youtube.py
    ```
* **From Local Video:** Turn a saved video file into thousands of images.
    ```bash
    python3 video_to_frames.py
    ```

### Step 3: Data Cleaning (Pre-Training)
Once you have labeled your data (using CVAT/LabelImg), run these scripts to clean the dataset before training.

1.  **Fix Class IDs:** (Optional) If your labels use `0=Body` but you want `0=Head`, use this to swap them.
    ```bash
    python3 flip_labels.py
    ```
2.  **Remove Orphans:** Deletes images that don't have a matching `.txt` label file.
    ```bash
    python3 cleanup.py
    ```
3.  **Balance Backgrounds:** Randomly deletes 60% of empty (background) images to prevent class imbalance.
    ```bash
    python3 reduce_background.py
    ```
4.  **Create Validation Set:** Randomly moves 20% of your training data to the validation folder.
    ```bash
    python3 split_data.py
    ```

### Step 4: Training
The core training script. Includes "Turbo Mode" (`cache=True`, `workers=4`) and Apple Metal (MPS) acceleration.

* **Config:** Ensure `data.yaml` points to your `dataset/` folder.
* **Run Training:**
    ```bash
    python3 train_mac.py
    ```

---

## 📂 File Dictionary

| File | Description |
| :--- | :--- |
| **`train_mac.py`** | **The Main Engine.** Trains the YOLOv8 model using Apple Metal (GPU) acceleration. |
| **`data.yaml`** | Configuration file defining paths to Train/Val data and Class names (Head/Body). |
| **`cleanup.py`** | Scans dataset folders and removes images that are missing label files. |
| **`split_data.py`** | Automates the train/val split (e.g., moves 20% of files to validation). |
| **`reduce_background.py`** | Deletes a percentage of non-labeled images to balance the dataset. |
| **`flip_labels.py`** | Utility to swap Class ID `0` and `1` in text files if labeled incorrectly. |
| **`collect_youtube.py`** | Helper to download datasets or videos from YouTube. |
| **`video_to_frames.py`** | Converts `.mp4` video files into individual `.jpg` frames for labeling. |
| **`get_cords.py`** | Utility tool to find screen coordinates (x, y) for capturing specific regions. |
| **`setup_mac.sh`** | Shell script to verify and install Mac-specific dependencies. |

---

## 📝 Notes
* **Data Structure:** The scripts assume the standard YOLO format:
    ```text
    dataset/
    ├── images/
    │   ├── train/
    │   └── val/
    └── labels/
        ├── train/
        └── val/
    ```
* **Performance:** `train_mac.py` is configured with `batch=8` by default to prevent `malloc` errors on Macs with 16GB RAM. If crashing, lower to `batch=4`.
