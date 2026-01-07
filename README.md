# AI-Assisted Hough Circle Transform for Microparticle Recognition

## Overview
This repository contains the Python code and algorithms described in the paper: 
**"Artificial Intelligence–Assisted Hough Circle Transform for Real-Time Microparticle Recognition and Counting in Microfluidic Platforms"**

This software is designed to automate particle detection, sizing, and counting under dynamic microfluidic conditions. It utilizes an optimized Hough Circle Transform (HCT) to identify particles (such as 3 μm and 5 μm polystyrene microbeads) with high accuracy.

## Contents
* **hough_optimizer_final.py**: The Generation II algorithm that includes parallelized parameter optimization and statistical metrics.
* **Sample Images**: Example images (e.g., 1 min.png) to test the detection.

## Requirements
* Python 3.x
* OpenCV (`cv2`)
* NumPy

## How to Run & Configuration
1. **Install dependencies:** Open your terminal or command prompt and run:
   `pip install -r requirements.txt`

2. **Prepare your images:** Place your experimental images (e.g., `.jpg`, `.png`) in the same folder as the script.

3. **Configure the script (CRITICAL STEP):** Open the python file (`HCT_optimizer_final.py`) in a text editor.
   * Find the section marked **"USER ACTION REQUIRED"** (approx. line 15).
   * Update the `test_images_dict` with your specific filenames and your manual particle counts (You can use the GUI for an initial fast approximate count).
   * *Example:* `{"my_experiment_1.jpg": 150, "my_experiment_2.jpg": 200}`

4. **Run the analysis:** `python HCT_optimizer_final.py`

**IMPORTANT:** The images provided in this repository are for demonstration only. 
To use this code with your own experiments:
* Place your image files in the same folder.
* Open `HCT_optimizer_final.py` and update the `test_images_dict` with your own filenames and manual particle counts.

## Citation
If you use this code in your research, please cite our publication:



