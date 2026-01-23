# Copyright 2026 Trevor Gerdes. All rights reserved.
# This software is licensed under the MIT License.

import operator
import os
import tkinter as tk
import tkinter.font as font
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk

import cv2 as cv
import numpy as np


def main():

    HoughTestGUI_window()

def HoughTestGUI_window():

    global root1
    root1 = tk.Tk()
    root1.geometry("700x500")
    root1.resizable(True, True)
    root1.title('Hough Circle Transform Parameter Tester GUI')

    buttonsFont = font.Font(size=14, weight='bold')

    button_HoughTestGUI_0 = tk.Button(root1, text='STEP 1: Select Tester Image', command=HoughTestGUI_selectTesterImage, font=buttonsFont)
    button_HoughTestGUI_0.grid(column=0, row=0)

    button_HoughTestGUI_1 = tk.Button(root1, text='STEP 2: Hough Detection Preview', command=HoughTestGUI_detectionPreview, font=buttonsFont)
    button_HoughTestGUI_1.grid(column=0, row=1)

    text1 = Label(root1, text='Set parameters for smaller beads (RED OUTLINE)', font=buttonsFont)
    text1.grid(column=0, row=2)
    
    global canny_1
    canny_1 = tk.IntVar()
    canny_1 = tk.Scale(root1, from_=1, to=200, orient='horizontal')
    canny_1.set(16)
    canny_1_label = ttk.Label(root1, text='Canny Edge Detector (smaller)')
    canny_1.grid(column=0, row=3)
    canny_1_label.grid(column=0,row=4)

    global center_1
    center_1 = tk.IntVar()
    center_1 = tk.Scale(root1, from_=1, to=100, orient='horizontal')
    center_1.set(14)
    center_1_label = ttk.Label(root1, text='Center Detection Threshold (smaller)')
    center_1.grid(column=1, row=3)
    center_1_label.grid(column=1, row=4)

    global minimum_radius_1
    minimum_radius_1 = tk.IntVar()
    minimum_radius_1 = tk.Scale(root1, from_=0, to=50, orient='horizontal')
    minimum_radius_1.set(12)
    minimum_radius_1_label = ttk.Label(root1, text='Minimum Circle Radius (smaller)')
    minimum_radius_1.grid(column=0, row=5)
    minimum_radius_1_label.grid(column=0, row=6)

    global maximum_radius_1
    maximum_radius_1 = tk.IntVar()
    maximum_radius_1 = tk.Scale(root1, from_=0, to=100, orient='horizontal')
    maximum_radius_1.set(15)
    maximum_radius_1_label = ttk.Label(root1, text='Maximum Circle Radius (smaller)')
    maximum_radius_1.grid(column=1, row=5)
    maximum_radius_1_label.grid(column=1, row=6)

    global minimum_distance_1
    minimum_distance_1 = tk.IntVar()
    minimum_distance_1 = tk.Scale(root1, from_=1, to=100, orient='horizontal')
    minimum_distance_1.set(39)
    minimum_distance_1_label = ttk.Label(root1, text='Minimum Distance btw. Centers')
    minimum_distance_1.grid(column=0, row=7)
    minimum_distance_1_label.grid(column=0, row=8)

    global blur_level_1
    blur_level_1 = tk.IntVar()
    blur_level_1 = tk.Scale(root1, from_=1, to=65, orient='horizontal')
    blur_level_1_label = ttk.Label(root1, text='Blur')
    blur_level_1.grid(column=1, row=7)
    blur_level_1_label.grid(column=1, row=8)

    text2 = Label(root1, text='Set parameters for larger beads (GREEN OUTLINE)', font=buttonsFont)
    text2.grid(column=0, row=9)

    global canny_2
    canny_2 = tk.IntVar()
    canny_2 = tk.Scale(root1, from_=1, to=200, orient='horizontal')
    canny_2.set(33)
    canny_2_label = ttk.Label(root1, text='Canny Edge Detector')
    canny_2.grid(column=0, row=10)
    canny_2_label.grid(column=0,row=11)

    global center_2
    center_2 = tk.IntVar()
    center_2 = tk.Scale(root1, from_=1, to=100, orient='horizontal')
    center_2.set(18)
    center_2_label = ttk.Label(root1, text='Center Detection Threshold')
    center_2.grid(column=1, row=10)
    center_2_label.grid(column=1, row=11)

    global minimum_radius_2
    minimum_radius_2 = tk.IntVar()
    minimum_radius_2 = tk.Scale(root1, from_=0, to=50, orient='horizontal')
    minimum_radius_2.set(18)
    minimum_radius_2_label = ttk.Label(root1, text='Minimum Circle Radius')
    minimum_radius_2.grid(column=0, row=12)
    minimum_radius_2_label.grid(column=0, row=13)

    global maximum_radius_2
    maximum_radius_2 = tk.IntVar()
    maximum_radius_2 = tk.Scale(root1, from_=0, to=100, orient='horizontal')
    maximum_radius_2.set(29)
    maximum_radius_2_label = ttk.Label(root1, text='Maximum Circle Radius')
    maximum_radius_2.grid(column=1, row=12)
    maximum_radius_2_label.grid(column=1, row=13)

    global minimum_distance_2
    minimum_distance_2 = tk.IntVar()
    minimum_distance_2 = tk.Scale(root1, from_=1, to=100, orient='horizontal')
    minimum_distance_2.set(13)
    minimum_distance_2_label = ttk.Label(root1, text='Minimum Distance btw. Centers')
    minimum_distance_2.grid(column=0, row=14)
    minimum_distance_2_label.grid(column=0, row=15)

    global blur_level_2
    blur_level_2 = tk.IntVar()
    blur_level_2 = tk.Scale(root1, from_=1, to=65, orient='horizontal')
    blur_level_2_label = ttk.Label(root1, text='Blur')
    blur_level_2.grid(column=1, row=14)
    blur_level_2_label.grid(column=1, row=15)

    text3 = Label(root1, text='Number of circles detected per parameter set will print to console.', font=buttonsFont)
    text3.grid(column=0, row=16)

    root1.mainloop()


def HoughTestGUI_selectTesterImage():

    global tester_image_name
    tester_image_name = fd.askopenfilename(title='Open a .PNG or .JPEG file')

def HoughTestGUI_detectionPreview():
    
    img = cv.imread(cv.samples.findFile(tester_image_name), cv.IMREAD_COLOR)

    gray_1 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray_1 = cv.medianBlur(gray_1, blur_level_1.get())
    rows = gray_1.shape[0]

    global hough_dictionary_1
    hough_dictionary_1 = {
        'image': gray_1,
        'method': cv.HOUGH_GRADIENT,
        'dp': 1,
        'param1': int(canny_1.get()),
        'param2': int(center_1.get()),
        'minRadius': int(minimum_radius_1.get()),
        'maxRadius': int(maximum_radius_1.get()),
        'minDist': int(minimum_distance_1.get()),
        }

    # Circle detection for "smaller" set
    circles1 = cv.HoughCircles(**hough_dictionary_1)
    if circles1 is not None:
        circles_found1 = len(circles1[0, :])
        print("***********************************************************")
        print("'Smaller'/RED Parameter Set: " + str(circles_found1) + " circles detected")
        print("(Note: This number may include closely overlapping, 'duplicate' detected circles)\n")
    else:
        print("***********************************************************")
        print("'Smaller'/RED Parameter Set: No circles detected\n")

    gray_2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray_2 = cv.medianBlur(gray_2, blur_level_2.get())
    rows = gray_2.shape[0]

    global hough_dictionary_2
    hough_dictionary_2 = {
        'image': gray_2,
        'method': cv.HOUGH_GRADIENT,
        'dp': 1,
        'param1': int(canny_2.get()),
        'param2': int(center_2.get()),
        'minRadius': int(minimum_radius_2.get()),
        'maxRadius': int(maximum_radius_2.get()),
        'minDist': int(minimum_distance_2.get()),
        }
    # Circle detection for "larger" set
    circles2 = cv.HoughCircles(**hough_dictionary_2)
    if circles2 is not None:
        circles_found2 = len(circles2[0, :])
        print("'Larger'/GREEN Parameter Set: " + str(circles_found2) + " circles detected")
        print("(Note: This number may include closely overlapping, 'duplicate' detected circles)\n\n\n")
    else:
        print("'Larger'/GREEN Parameter Set: No circles detected\n\n\n")

    if circles1 is not None:
        circles1 = np.uint16(np.around(circles1))
        for i in circles1[0, :]:
            center = (i[0], i[1])
            # Circle center
            cv.circle(img, center, 1, (0, 100, 100), 1)
            #Circle outline
            radius = i[2]
            cv.circle(img, center, radius, (0, 0, 255), 2)
    
    if circles2 is not None:
        circles2 = np.uint16(np.around(circles2))
        for i in circles2[0, :]:
            center = (i[0], i[1])
            # Circle center
            cv.circle(img, center, 1, (0, 100, 100), 1)
            #Circle outline
            radius = i[2]
            cv.circle(img, center, radius, (0, 255, 0), 1)

    cv.imshow("detected circles", img)


if __name__ == "__main__":
    main()
