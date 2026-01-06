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

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run the optimizer: `python hough_optimizer_final.py`

## Citation
If you use this code in your research, please cite our publication:
[Insert your Paper DOI or Citation here once published]