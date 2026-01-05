import pyautogui
import time
import os

def main():
    print("--- Screen Coordinate Finder ---")
    print("1. Move mouse to TOP-LEFT of the YouTube video.")
    print("2. Wait 3 seconds...")
    time.sleep(3)
    x1, y1 = pyautogui.position()
    print(f"Top-Left captured: ({x1}, {y1})")
    
    print("\n1. Move mouse to BOTTOM-RIGHT of the YouTube video.")
    print("2. Wait 3 seconds...")
    time.sleep(3)
    x2, y2 = pyautogui.position()
    print(f"Bottom-Right captured: ({x2}, {y2})")
    
    width = x2 - x1
    height = y2 - y1
    
    print("\n--- COPY THIS INTO YOUR SCRIPT ---")
    print(f"SCREEN_REGION = {{'top': {y1}, 'left': {x1}, 'width': {width}, 'height': {height}}}")

if __name__ == "__main__":
    main()