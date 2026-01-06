import operator
import os
import tkinter as tk
import tkinter.font as font
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import time

average_distance_list_larger = 0
average_distance_list_smaller = 0
circles_per_image_smaller = 0
circles_per_image_larger = 0

ext = ('.png')                      # ext = shorthand for file extension

def main():
    mode0_window_setup()
    
def mode0_window_setup():

    # Opening Window Setup
    global root0
    root0 = tk.Tk()
    root0.geometry("400x525")
    root0.resizable(True,True)
    root0.title('Welcome to BeadBossPro')

    text_mode0_0 = Label(root0, wraplength=380, justify=LEFT, text='Welcome to BeadBossPro'
                             '\n\nMode 1: DEP-Tracking Image Analysis + Graph'
                              '\n(Includes Hands-On Hough Circle Parameter Customizer!)'
                              '\n\nAnalyze your series of images for automated analysis of DEP-related movement of two bead sizes.'
                             ' Outputs graph.')

    text_mode0_0.pack()

    buttonsFont = font.Font(size=14, weight='bold')

    button_mode0_0 = tk.Button(root0, text='Run Mode 1', command=mode1_window, font=buttonsFont)
    button_mode0_0.pack()

    text_mode0_1 = Label(root0, wraplength=380, justify=LEFT, text='\nMode 2: DEP Tracker Image Prep'
                                                          '\n(Includes Frequency Sequence Generator!)'
                                                          '\n\nIf you do not have the images yet, use this mode to assist in collecting new images so you can use mode 1.')

    text_mode0_1.pack()

    #button_mode0_1 = tk.Button(root0, text='Run Mode 2', command=mode2_window, font=buttonsFont)
    #button_mode0_1.pack()


    #text_mode0_2 = Label(root0, wraplength=380, justify=LEFT, text='\nMode 3: AUTO-SORT \nAutomatically separate two bead size populations in real time.'
                                                              #'(Requires microscope video feed showing on your screen)')

    #text_mode0_2.pack()

    #button_mode0_2 = tk.Button(root0, text='Run Mode 3', command=mode3_window, font=buttonsFont)
    #button_mode0_2.pack()

    #text_mode0_3 = Label(root0, wraplength=380, justify=LEFT, text='\nMode 4: AUTO-OPTIMIZE'
                                                                     #'\n\nFind effective Hough Circle Transform parameters for your image set, algorithmically.')
    #text_mode0_3.pack()

    #button_mode0_3 = tk.Button(root0, text='Run Mode 4', command=mode4_window, font=buttonsFont)
    #button_mode0_3.pack()

    root0.mainloop()

def mode1_window():

    radius_list = []

    global root1
    root1 = tk.Toplevel()
    root1.geometry("700x500")
    root1.resizable(True, True)
    root1.title('DEP-Tracking Image Analysis + Graph, with Hough Hands-On Customizer')

    buttonsFont = font.Font(size=14, weight='bold')

    button_mode1_0 = tk.Button(root1, text='STEP 1: Select Tester Image', command=mode1_selectTesterImage, font=buttonsFont)
    button_mode1_0.grid(column=0, row=0)

    button_mode1_1 = tk.Button(root1, text='STEP 2: Hough Detection Preview', command=mode1_houghTester, font=buttonsFont)
    button_mode1_1.grid(column=0, row=1)

    text_mode1_0 = Label(root1, text='Set parameters for smaller beads (RED OUTLINE)', font=buttonsFont)
    text_mode1_0.grid(column=0, row=2)
    
    global canny_1
    canny_1 = tk.IntVar()
    canny_1 = tk.Scale(root1, from_=1, to=100, orient='horizontal')
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
    blur_level_1 = tk.Scale(root1, from_=0, to=65, orient='horizontal')
    blur_level_1_label = ttk.Label(root1, text='Blur')
    blur_level_1.grid(column=1, row=7)
    blur_level_1_label.grid(column=1, row=8)

    text4 = Label(root1, text='Set parameters for larger beads (GREEN OUTLINE)', font=buttonsFont)
    text4.grid(column=0, row=9)

    global canny_2
    canny_2 = tk.IntVar()
    canny_2 = tk.Scale(root1, from_=1, to=100, orient='horizontal')
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

    button_mode1_2 = tk.Button(root1, text='STEP 3: Confirm Parameters and Begin Full Analysis', command=mode1_fullAnalysis, font=buttonsFont)
    button_mode1_2.grid(column=0, row=16)

    root1.mainloop()

def mode1_fullAnalysis():

    plt.close()

    average_distance_list_larger = []
    average_distance_list_smaller = []
    circles_per_image_smaller = []
    circles_per_image_larger = []

    line_graph_domain_tally = []

    lst = os.listdir()
    lst.sort()

    for i in lst:          
        if i.endswith(ext):

            circles1_delete_list = []

            line_graph_domain_tally.append(1)
            
            img = cv.imread(cv.samples.findFile(i), cv.IMREAD_COLOR)

            #small beads
            gray_1 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            gray_1 = cv.medianBlur(gray_1, blur_level_1.get())
            rows = gray_1.shape[0]

            height = img.shape[0]
            width = img.shape[1]
            center_x = round(width/2 - 1)

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

            circles1 = cv.HoughCircles(**hough_dictionary_1) 

            #large beads
            gray_2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            gray_2 = cv.medianBlur(gray_2, blur_level_2.get())
            rows = gray_2.shape[0]

            height = img.shape[0]
            width = img.shape[1]
            center_x = round(width/2 - 1)

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

            circles2 = cv.HoughCircles(**hough_dictionary_2) 
            if circles2 is not None:

                dist_tally_larger = 0

                large_circles = []
            
                circles2 = np.uint16(np.around(circles2))

                for i in circles2[0, :]:
                    center = (i[0], i[1])
                    large_circles.append(1)
                    dist_tally_larger += round(np.absolute(i[0] - center_x))

                average_distance_larger = np.absolute(dist_tally_larger/len(large_circles))

                average_distance_list_larger.append(average_distance_larger)

                circles_per_image_larger.append(len(large_circles))

            for i in circles2[0, :]:
                bigx = int(i[0])
                bigy = int(i[1])
                bigradius = int(i[2])
                jcount = 0
                        # for every small bead

                for j in circles1[0, :]:
                    ###fix problem when there are no circles###
                    littlex = int(j[0])
                    littley = int(j[1])
                    littleradius = int(j[2])
                    inequalityleft = (((littlex-bigx)**2)+((littley-bigy)**2))
                    inequalityright = ((bigradius)**2)
                    if inequalityleft < inequalityright:
                        circles1_delete_list.append(jcount)
                        #print('Delete: (' + str(littlex) + ',' + str(littley) + ')') 
                    jcount +=1

            #print('Circles to delete (rows):' + str(circles1_delete_list))

            circles1_del = np.delete(circles1, circles1_delete_list, 1)

            circles_per_image_smaller.append(circles1_del.shape[1])

            if circles1_del is not None:

                dist_tally_smaller = 0
            
                circles1_del = np.uint16(np.around(circles1_del))

                for i in circles1_del[0, :]:
                    center = (i[0], i[1])
                    dist_tally_smaller += round(np.absolute(i[0] - center_x))

                average_distance_smaller = np.absolute(dist_tally_smaller/(circles1_del.shape[1]))

                average_distance_list_smaller.append(average_distance_smaller)


    # set x-axis values

    #frequency_list = (0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000)

    # in future can add inputs for these to GUI so all the calculations are automated regardless of setup
    pic_interval = 10
    freq_interval = 50
    freq_duration = 30
    pics_per_freq = int(freq_duration / pic_interval)
    min_frequency = 0
    max_frequency = 1000

    # building domain for frequencies

    line_graph_domain = list(range(0, pic_interval*len(line_graph_domain_tally), pic_interval))
    #print("Domain:" + str(line_graph_domain))
    #print("Domain length:" + str(len(line_graph_domain)))

    plt.plot (line_graph_domain, average_distance_list_smaller, label = "Smaller Beads", linestyle=":")

    for j, txt in enumerate(circles_per_image_smaller):
        plt.annotate(txt, (line_graph_domain[j], average_distance_list_smaller[j]), fontsize=6)

    plt.plot (line_graph_domain, average_distance_list_larger, label = "Larger Beads", linestyle="-")

    for k, txt in enumerate(circles_per_image_larger):
        plt.annotate(txt, (line_graph_domain[k], average_distance_list_larger[k]), fontsize=6)

    xticknames = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]

    plt.xticks(np.arange(min(line_graph_domain), max(line_graph_domain), freq_duration), xticknames)

    #ax1.set_xlabel("Frequency in kHz")
    #ax1.set_xticks([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480, 510, 540, 570, 600])
    #ax1.set_xticklabels([0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000])

    #this is new 11 Oct 2022 -- trying to take derivative of each frequency          

    dy_diff_dict = {}
    freq_list_for_dt = []
    dy_diff_list = []
    
    t = 0
    tpoint = 0

    while t <= (max(line_graph_domain) - freq_duration):
        tpoint_old = tpoint
        t += freq_duration
        tpoint = int((t/freq_duration)*3)
        current_freq_b = int(((t / freq_duration) - 1)*50)
        freq_list_for_dt.append(current_freq_b)
        dy_smaller = average_distance_list_smaller[tpoint] - average_distance_list_smaller[tpoint_old] / freq_duration
        #print("dy_smaller = " + str(average_distance_list_smaller[tpoint]) + " - " + str(average_distance_list_smaller[tpoint_old]) + " / " + str(freq_duration))
        dy_larger = average_distance_list_larger[tpoint] - average_distance_list_larger[tpoint_old] / freq_duration
        #print("dy_larger = " + str(average_distance_list_larger[tpoint]) + " - " + str(average_distance_list_larger[tpoint_old]) + " / " + str(freq_duration))
        dy_diff = np.absolute(dy_smaller - dy_larger)
        dy_diff_list.append(dy_diff)
        dy_diff_dict[str(current_freq_b)] = str(dy_diff)

    dy_diff_max = max(dy_diff_dict, key=dy_diff_dict.get)
    dy_diff_max_freq = max(dy_diff_dict.items(), key=operator.itemgetter(1))[0]

    plt.suptitle('Movement of beads relative to inter-electrode reference line', fontsize=12)
    plt.title('Data labels are number of beads of given size detected by algorithm in given frame',fontsize=8)
    plt.ylabel('Average distance from reference line (pixels)')
    plt.xlabel('Frequency (kHz, frequency duration 30 seconds, screenshot interval 10 seconds)\n' + 
               'Top separation frequency candidate:' + str(dy_diff_max_freq) + 'kHz' +
               '(Maximal difference between dD/dt for small and large beads)')
    
    plt.legend(loc='lower right', fontsize=8)
    plt.show()

def mode1_selectTesterImage():
    global tester_image_name
    tester_image_name = fd.askopenfilename(title='Open a .PNG file')
    
def mode1_houghTester():
    
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

    circles1 = cv.HoughCircles(**hough_dictionary_1) 

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

    circles2 = cv.HoughCircles(**hough_dictionary_2)

    if circles1 is not None:
        circles1 = np.uint16(np.around(circles1))
        for i in circles1[0, :]:
            center = (i[0], i[1])
            # Circle center
            cv.circle(img, center, 1, (0, 100, 100), 1)
            #Circle outline
            radius = i[2]
            cv.circle(img, center, radius, (0, 0, 255), 1)
    
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
##
##def mode2_window():
##    
##    global root2
##    root2 = tk.Toplevel()
##    root2.geometry("500x500")
##    root2.resizable(True, True)
##    root2.title('DEP Tracker Image Prep, with Frequency Sequence Generator')
##
##    buttonsFont = font.Font(size=14, weight='bold')
##
##    text_mode2_0 = Label(root2, width=480, justify=LEFT, anchor="w", text="STEP 1: You may enter desired frequencies in one of two ways:")
##    text_mode2_0.pack()  
##
##    button_mode2_0 = tk.Button(root2, text='Enter frequencies as list', command=mode2_subwindow_enterList, font=buttonsFont)
##    button_mode2_0.pack()
##
##    button_mode2_1 = tk.Button(root2, text="Choose frequency range", command=mode2_subwindow_chooseRange, font=buttonsFont)
##    button_mode2_1.pack()
##
##    text_mode2_1 = Label(root2, width=480, wraplength=480, justify=LEFT, anchor="w", text="STEP 2: Select duration for each frequency, in seconds."
##                                                            " (Tip: Drag bar for big changes, click in dark gray area next to bar for small changes.)")
##    text_mode2_1.pack()
##
##    global frequency_duration
##    frequency_duration = tk.IntVar()
##    frequency_duration = tk.Scale(root2, from_=1, to=300, orient='horizontal')
##    frequency_duration.set(30)
##    frequency_duration_label = ttk.Label(root2, text='Frequency Duration')
##    frequency_duration.pack()
##    frequency_duration_label.pack()
##
##    text_mode2_2 = Label(root2, width=480, wraplength=480, justify=LEFT, anchor="w", text='STEP 3: You can either run the automated frequency sequence now'
##                                                             ' and manage screen capture on your own, or you can set up screen capture'
##                                                             ' using BeadBossPro guided setup.')
##    text_mode2_2.pack()
##
##    button_mode2_2 = tk.Button(root2, text='Run Sequence Now', command=mode2_frequencySequence, font=buttonsFont)
##    button_mode2_2.pack()
##
##    button_mode2_3 = tk.Button(root2, text='Guided Screen Capture', command=mode2_guidedCapture, font=buttonsFont)
##    button_mode2_3.pack()
##
##    root2.mainloop()
##
##def mode2_subwindow_enterList():
##    pass
##
##def mode2_subwindow_chooseRange():
##    pass
##
##def mode2_frequencySequence():
##    pass
##
##def mode2_guidedCapture():
##    pass
##
##def mode3_window():
##    pass
##    #global root3
##    #root3 = tk.Toplevel()
##    #root2.geometry("500x500")
##    #root2.resizable(True, True)
##    #root2.title('Auto-Sort')

def mode4_window():
    pass
    global root4
    root4 = tk.Toplevel()
    root4.geometry("500x500")
    root4.resizable(True, True)
    root4.title('Hough Parameters Auto-Optimizer')

    button_mode4_0 = tk.Button(root4, text='Click here for instructions/help')
    button_mode4_0.pack()



    
    root4.mainloop()

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
