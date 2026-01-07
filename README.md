# AI-Assisted Hough Circle Transform for Microparticle Recognition

## Overview
This repository contains the Python code and algorithms described in the paper: 
**"Artificial Intelligence–Assisted Hough Circle Transform for Real-Time Microparticle Recognition and Counting in Microfluidic Platforms"**

This software is designed to automate particle detection, sizing, and counting under dynamic microfluidic conditions. It utilizes an optimized Hough Circle Transform (HCT) to identify particles (such as 3 μm and 5 μm polystyrene microbeads) with high accuracy.

Accurate identification and enumeration of microscopic particles are essential for research in microfluidics, electrokinetics, and biosensing. This study introduces an artificial intelligence–assisted Hough Circle Transform (HCT) algorithm designed to automate particle detection, sizing, and counting under dynamic microfluidic conditions. Gold interdigitated electrode arrays (IDEAs) were fabricated on wafer substrates to generate electroosmotic flow, and 3 μm and 5 μm polystyrene microbeads were used as model particles. The first-generation algorithm validated the feasibility of automated detection but exhibited computational inefficiency and sensitivity to algorithmic parameter selection. To overcome these limitations, a second-generation algorithm was developed incorporating parallelized, multi-core parameter optimization and new statistical metrics based on detection accuracy and standard deviation across multiple frames. The optimized system achieved consistent and precise identification of both uniform and mixed particle populations, maintaining high success rates while minimizing false detections. The AI-assisted HCT framework demonstrates strong adaptability to variations in particle size, concentration, and imaging conditions, establishing a robust platform for real-time particle quantification. To facilitate broader adoption and utility, the developed program and its associated graphical user interface (GUI) are made freely available to the research community. Beyond microfluidic automation, the method provides structured, high-quality datasets suitable for neural network training and feedback learning, linking experimental imaging with intelligent algorithm development. This work represents a step toward fully automated, data-driven electrokinetic sorting and microassembly and contributes to the broader vision of physical artificial intelligence in microscale systems. 

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

## Output Data & Results
The HCT optimization script generates detailed data files (CSV format, compatible with Excel) to help you analyze performance:

* **`all_params.csv`**: A massive dataset containing results for *every* parameter combination tested.
* **`top_scoring_params.csv`**: A filtered list of the best parameter sets that yielded the highest accuracy.

### Key Columns in the Excel Files:
* **Hough Parameters:** The specific settings used for that test (DP, MinDist, Canny Edge Threshold, Accumulator Threshold, Min/Max Radius).
* **Detection Counts:** Raw bead counts for each image (e.g., `Image 1 Beads Found`).
* **Accuracy Metrics:**
    * **Average % Correct:** The average detection rate across all test images (Target = 100%).
    * **Metric 1 (Accuracy):** How close the average detection was to the manual count (Lower is better).
    * **Metric 2 (Consistency):** The standard deviation between images (Lower is better).
    * **MetricSum:** The final combined score used to rank the parameters (Metric 1 + Metric 2).

## Citation
If you use this code in your research, please cite our publication:

## Graphical User Interface (GUI)
The repository includes a GUI (`hough_GUI_latest.py`) for real-time visualization and manual parameter tuning.

### How to Use the GUI:
1. **Launch the Program:**
   Run the following command in your terminal:
   `python hough_GUI_latest.py`

2. **Select Mode:**
   Click the **"Run Mode 1"** button on the main menu.

3. **Load an Image:**
   Click **"STEP 1: Select Tester Image"** and choose one of your experimental images (e.g., `1_min.jpg`).

4. **Tune Parameters:**
   * Adjust the sliders to change detection sensitivity, radius, and edge detection.
   * **Red Outline:** Controls parameters for smaller beads.
   * **Green Outline:** Controls parameters for larger beads.
   * *Tip:* Click **"STEP 2: Hough Detection Preview"** frequently to visually check if the circles match your particles.

5. **Run Full Analysis:**
   Once satisfied with the parameters, click **"STEP 3: Confirm Parameters"**. The program will process all images in the folder and generate a graph of the results.






