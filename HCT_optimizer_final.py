import csv
import cv2 as cv
import datetime
import glob
import multiprocessing as mp
import numpy as np
import os
import pandas as pd
import pickle
import time

# Set ranges of possible parameters to test
# To determine reasonable ranges, consider using the Hough GUI program
# Hough GUI is especially helpful in finding good radius and minimum distance ranges

# ==========================================
# USER ACTION REQUIRED: INPUT YOUR DATA HERE
# ==========================================
# The dictionary below contains demonstration data used in the manuscript.
# To use this program with your own experimental data:
# 1. Add your image files to the same folder as this script.
# 2. Replace the demonstration filenames below with your exact filenames.
# 3. Replace the numbers with your manual particle count for that image (this is used to calculate accuracy statistics).
#
# Format: "your_image_name.jpg": your_manual_count,

test_images_dict = {"1_min.jpg": 137,
                    "2_min.jpg": 215,
                    "3_min.jpg": 261,
                    "4_min.jpg": 304,
                    "5_min.jpg": 343,
                    "6_min.jpg": 370,
                    "7_min.jpg": 393,
                    "8_min.jpg": 408,
                    "9_min.jpg": 421,
                    "10_min.jpg": 433}

# ranges for each HoughCircles parameter to be tested
median_blur_list = [*range(1, 8, 2)]
param_1_list = [*range(1, 65, 1)]
param_2_list = [*range(1, 25, 1)]
min_radius_list = [*range(3, 4, 1)]
max_radius_list = [*range(6, 7, 1)]
min_dist_list = [*range(1, 6, 1)]

# dp is a Hough Circle Transform parameter that can often be kept constant
# 1 should be a suitable default value
dp_default = 1


def build_param_list():
    # List of all possible parameters to test. The following loop builds it
    parameter_sets_all = []
    build_count = 0

    for alpha in median_blur_list:
        for beta in param_1_list:
            build_count += 1
            if build_count % 25 == 0:
                print("List build in progress...")
            for gamma in param_2_list:
                for delta in min_radius_list:
                    for epsilon in max_radius_list:
                        for zeta in min_dist_list:
                            parameter_sets_all.append([str(alpha), str(zeta), str(dp_default), str(beta),
                                                       str(gamma), str(delta), str(epsilon)])

    # note: this program is currently designed to work on 8 cores
    # subset amount should match amount of cores on computer
    # adjust as needed
    set_eighth = int(len(parameter_sets_all)/8)     
    
    # write each subset's parameter lists to a .txt file
    subset_1 = parameter_sets_all[0:set_eighth]
    with open('subset_1.txt', 'wb') as filehandle:
        pickle.dump(subset_1, filehandle)
    print("Parameter sub-list 1 built. Number of parameter sets in this sublist: " + str(len(subset_1)))

    subset_2 = parameter_sets_all[set_eighth:(2*set_eighth)]
    with open('subset_2.txt', 'wb') as filehandle:
        pickle.dump(subset_2, filehandle)
    print("Parameter sub-list 2 built. Number of parameter sets in this sublist: " + str(len(subset_2)))

    subset_3 = parameter_sets_all[(2*set_eighth):(3*set_eighth)]
    with open('subset_3.txt', 'wb') as filehandle:
        pickle.dump(subset_3, filehandle)
    print("Parameter sub-list 3 built. Number of parameter sets in this sublist: " + str(len(subset_3)))

    subset_4 = parameter_sets_all[(3*set_eighth):(4*set_eighth)]
    with open('subset_4.txt', 'wb') as filehandle:
        pickle.dump(subset_4, filehandle)
    print("Parameter sub-list 4 built. Number of parameter sets in this sublist: " + str(len(subset_4)))

    subset_5 = parameter_sets_all[(4*set_eighth):(5*set_eighth)]
    with open('subset_5.txt', 'wb') as filehandle:
        pickle.dump(subset_5, filehandle)
    print("Parameter sub-list 5 built. Number of parameter sets in this sublist: " + str(len(subset_5)))

    subset_6 = parameter_sets_all[(5*set_eighth):(6*set_eighth)]
    with open('subset_6.txt', 'wb') as filehandle:
        pickle.dump(subset_6, filehandle)
    print("Parameter sub-list 6 built. Number of parameter sets in this sublist: " + str(len(subset_6)))

    subset_7 = parameter_sets_all[(6*set_eighth):(7*set_eighth)]
    with open('subset_7.txt', 'wb') as filehandle:
        pickle.dump(subset_7, filehandle)
    print("Parameter sub-list 7 built. Number of parameter sets in this sublist: " + str(len(subset_7)))

    subset_8 = parameter_sets_all[(7*set_eighth):(8*set_eighth)]
    with open('subset_8.txt', 'wb') as filehandle:
        pickle.dump(subset_8, filehandle)
    print("Parameter sub-list 8 built. Number of parameter sets in this sublist: " + str(len(subset_8)))

    print("(The purpose of building sub-lists is to allow for multitasking, for faster calculation times!)")
    print("List build complete. Moving on to analysis.")
    print("Total parameter sets to be tested: " + str(len(parameter_sets_all)))
    print("Time: " + str(datetime.datetime.now()))


def analysis_1():
    with open('subset_1.txt', 'rb') as filehandle:
        subset_1 = pickle.load(filehandle)
    print("Confirming number of parameter sets in sub-list 1: " + str(len(subset_1)))
    print("        Analysis beginning")
    calc_counter = 0
    subset_count = len(subset_1)
    for paramSet in subset_1:
        found_div_correct_sum = 0
        d_p = int(paramSet[0])
        min_dist = int(paramSet[1])
        median_blur = int(paramSet[2])
        parameter_one = int(paramSet[3])
        parameter_two = int(paramSet[4])
        min_radius = int(paramSet[5])
        max_radius = int(paramSet[6])
        calc_counter += 1
        sd_set = []
        if calc_counter % 1000 == 0:
            percent_done = round(100 * calc_counter / subset_count, 2)
            print("Set 1 calculations: " + str(calc_counter) + "/" + str(subset_count)
                  + "     (" + str(percent_done) + "%)")
            print("Time: " + str(datetime.datetime.now()))

        for key in test_images_dict:
            # FIX: Use direct file path
            img = cv.imread(key, cv.IMREAD_COLOR)
            if img is None: continue 
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            gray = cv.medianBlur(gray, median_blur)
            circles = cv.HoughCircles(image=gray, method=cv.HOUGH_GRADIENT,
                                      dp=d_p, minDist=min_dist,
                                      param1=parameter_one, param2=parameter_two,
                                      minRadius=min_radius, maxRadius=max_radius)
            if circles is not None:
                circles_found = len(circles[0, :])
                circles_total = test_images_dict[key]
                paramSet.append(str(circles_found))
                paramSet.append(str(circles_found / circles_total))
                sd_set.append(circles_found / circles_total)
                found_div_correct_sum += (circles_found / circles_total)
            else:
                paramSet.append(0)
                paramSet.append(0)
                sd_set.append(0)

        found_div_correct_average = found_div_correct_sum / 10
        paramSet.append(str(found_div_correct_average))
        found_div_correct_dist_from_1 = abs(1 - found_div_correct_average)
        paramSet.append(str(found_div_correct_dist_from_1))
        standard_dev = np.std(sd_set)
        paramSet.append(standard_dev)
        metric_sum = found_div_correct_dist_from_1 + standard_dev
        paramSet.append(metric_sum)

    print("Subset One Complete: Printout (for backup in case of .csv file issues): " + str(subset_1))

    fields = ['DP', 'Minimum Distance', 'Median Blur', 'Param 1', 'Param 2', 'Minimum Radius', 'Maximum Radius',
              'Image 1 Beads Found', 'Image 1 Found/Total', 'Image 2 Beads Found', 'Image 2 Found/Total',
              'Image 3 Beads Found', 'Image 3 Found/Total', 'Image 4 Beads Found', 'Image 4 Found/Total',
              'Image 5 Beads Found', 'Image 5 Found/Total', 'Image 6 Beads Found', 'Image 6 Found/Total',
              'Image 7 Beads Found', 'Image 7 Found/Total', 'Image 8 Beads Found', 'Image 8 Found/Total',
              'Image 9 Beads Found', 'Image 9 Found/Total', 'Image 10 Beads Found', 'Image 10 Found/Total',
              'Average % of Correct Count', 'Metric 1', 'Metric 2 (S.D.)', 'MetricSum']

    with open('hough_secondary_analysis_1.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(subset_1)

def analysis_2():
    with open('subset_2.txt', 'rb') as filehandle:
        subset_2 = pickle.load(filehandle)
    print("Confirming number of parameter sets in sub-list 2: " + str(len(subset_2)))
    print("        Analysis beginning")
    calc_counter = 0
    subset_count = len(subset_2)
    for paramSet in subset_2:
        found_div_correct_sum = 0
        d_p = int(paramSet[0])
        min_dist = int(paramSet[1])
        median_blur = int(paramSet[2])
        parameter_one = int(paramSet[3])
        parameter_two = int(paramSet[4])
        min_radius = int(paramSet[5])
        max_radius = int(paramSet[6])
        calc_counter += 1
        sd_set = []
        if calc_counter % 1000 == 0:
            percent_done = round(100 * calc_counter / subset_count, 2)
            print("Set 2 calculations: " + str(calc_counter) + "/" + str(subset_count)
                  + "     (" + str(percent_done) + "%)")
            print("Time: " + str(datetime.datetime.now()))

        for key in test_images_dict:
            # FIX: Use direct file path
            img = cv.imread(key, cv.IMREAD_COLOR)
            if img is None: continue
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            gray = cv.medianBlur(gray, median_blur)
            circles = cv.HoughCircles(image=gray, method=cv.HOUGH_GRADIENT,
                                      dp=d_p, minDist=min_dist,
                                      param1=parameter_one, param2=parameter_two,
                                      minRadius=min_radius, maxRadius=max_radius)
            if circles is not None:
                circles_found = len(circles[0, :])
                circles_total = test_images_dict[key]
                paramSet.append(str(circles_found))
                paramSet.append(str(circles_found / circles_total))
                sd_set.append(circles_found / circles_total)
                found_div_correct_sum += (circles_found / circles_total)
            else:
                paramSet.append(0)
                paramSet.append(0)
                sd_set.append(0)

        found_div_correct_average = found_div_correct_sum / 10
        paramSet.append(str(found_div_correct_average))
        found_div_correct_dist_from_1 = abs(1 - found_div_correct_average)
        paramSet.append(str(found_div_correct_dist_from_1))
        standard_dev = np.std(sd_set)
        paramSet.append(standard_dev)
        metric_sum = found_div_correct_dist_from_1 + standard_dev
        paramSet.append(metric_sum)

    print("Subset Two Complete: Printout (for backup in case of .csv file issues): " + str(subset_2))

    fields = ['DP', 'Minimum Distance', 'Median Blur', 'Param 1', 'Param 2', 'Minimum Radius', 'Maximum Radius',
              'Image 1 Beads Found', 'Image 1 Found/Total', 'Image 2 Beads Found', 'Image 2 Found/Total',
              'Image 3 Beads Found', 'Image 3 Found/Total', 'Image 4 Beads Found', 'Image 4 Found/Total',
              'Image 5 Beads Found', 'Image 5 Found/Total', 'Image 6 Beads Found', 'Image 6 Found/Total',
              'Image 7 Beads Found', 'Image 7 Found/Total', 'Image 8 Beads Found', 'Image 8 Found/Total',
              'Image 9 Beads Found', 'Image 9 Found/Total', 'Image 10 Beads Found', 'Image 10 Found/Total',
              'Average % of Correct Count', 'Metric 1', 'Metric 2 (S.D.)', 'MetricSum']

    with open('hough_secondary_analysis_2.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(subset_2)

def analysis_3():
    with open('subset_3.txt', 'rb') as filehandle:
        subset_3 = pickle.load(filehandle)
    print("Confirming number of parameter sets in sub-list 3: " + str(len(subset_3)))
    print("        Analysis beginning")
    calc_counter = 0
    subset_count = len(subset_3)
    for paramSet in subset_3:
        found_div_correct_sum = 0
        d_p = int(paramSet[0])
        min_dist = int(paramSet[1])
        median_blur = int(paramSet[2])
        parameter_one = int(paramSet[3])
        parameter_two = int(paramSet[4])
        min_radius = int(paramSet[5])
        max_radius = int(paramSet[6])
        calc_counter += 1
        sd_set = []
        if calc_counter % 1000 == 0:
            percent_done = round(100 * calc_counter / subset_count, 2)
            print("Set 3 calculations: " + str(calc_counter) + "/" + str(subset_count)
                  + "     (" + str(percent_done) + "%)")
            print("Time: " + str(datetime.datetime.now()))

        for key in test_images_dict:
            # FIX: Use direct file path
            img = cv.imread(key, cv.IMREAD_COLOR)
            if img is None: continue
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            gray = cv.medianBlur(gray, median_blur)
            circles = cv.HoughCircles(image=gray, method=cv.HOUGH_GRADIENT,
                                      dp=d_p, minDist=min_dist,
                                      param1=parameter_one, param2=parameter_two,
                                      minRadius=min_radius, maxRadius=max_radius)
            if circles is not None:
                circles_found = len(circles[0, :])
                circles_total = test_images_dict[key]
                paramSet.append(str(circles_found))
                paramSet.append(str(circles_found / circles_total))
                sd_set.append(circles_found / circles_total)
                found_div_correct_sum += (circles_found / circles_total)
            else:
                paramSet.append(0)
                paramSet.append(0)
                sd_set.append(0)

        found_div_correct_average = found_div_correct_sum / 10
        paramSet.append(str(found_div_correct_average))
        found_div_correct_dist_from_1 = abs(1 - found_div_correct_average)
        paramSet.append(str(found_div_correct_dist_from_1))
        standard_dev = np.std(sd_set)
        paramSet.append(standard_dev)
        metric_sum = found_div_correct_dist_from_1 + standard_dev
        paramSet.append(metric_sum)

    print("Subset Three Complete: Printout (for backup in case of .csv file issues): " + str(subset_3))

    fields = ['DP', 'Minimum Distance', 'Median Blur', 'Param 1', 'Param 2', 'Minimum Radius', 'Maximum Radius',
              'Image 1 Beads Found', 'Image 1 Found/Total', 'Image 2 Beads Found', 'Image 2 Found/Total',
              'Image 3 Beads Found', 'Image 3 Found/Total', 'Image 4 Beads Found', 'Image 4 Found/Total',
              'Image 5 Beads Found', 'Image 5 Found/Total', 'Image 6 Beads Found', 'Image 6 Found/Total',
              'Image 7 Beads Found', 'Image 7 Found/Total', 'Image 8 Beads Found', 'Image 8 Found/Total',
              'Image 9 Beads Found', 'Image 9 Found/Total', 'Image 10 Beads Found', 'Image 10 Found/Total',
              'Average % of Correct Count', 'Metric 1', 'Metric 2 (S.D.)', 'MetricSum']

    with open('hough_secondary_analysis_3.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(subset_3)

def analysis_4():
    with open('subset_4.txt', 'rb') as filehandle:
        subset_4 = pickle.load(filehandle)
    print("Confirming number of parameter sets in sub-list 4: " + str(len(subset_4)))
    print("        Analysis beginning")
    calc_counter = 0
    subset_count = len(subset_4)
    for paramSet in subset_4:
        found_div_correct_sum = 0
        d_p = int(paramSet[0])
        min_dist = int(paramSet[1])
        median_blur = int(paramSet[2])
        parameter_one = int(paramSet[3])
        parameter_two = int(paramSet[4])
        min_radius = int(paramSet[5])
        max_radius = int(paramSet[6])
        calc_counter += 1
        sd_set = []
        if calc_counter % 1000 == 0:
            percent_done = round(100 * calc_counter / subset_count, 2)
            print("Set 4 calculations: " + str(calc_counter) + "/" + str(subset_count)
                  + "     (" + str(percent_done) + "%)")
            print("Time: " + str(datetime.datetime.now()))

        for key in test_images_dict:
            # FIX: Use direct file path
            img = cv.imread(key, cv.IMREAD_COLOR)
            if img is None: continue
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            gray = cv.medianBlur(gray, median_blur)
            circles = cv.HoughCircles(image=gray, method=cv.HOUGH_GRADIENT,
                                      dp=d_p, minDist=min_dist,
                                      param1=parameter_one, param2=parameter_two,
                                      minRadius=min_radius, maxRadius=max_radius)
            if circles is not None:
                circles_found = len(circles[0, :])
                circles_total = test_images_dict[key]
                paramSet.append(str(circles_found))
                paramSet.append(str(circles_found / circles_total))
                sd_set.append(circles_found / circles_total)
                found_div_correct_sum += (circles_found / circles_total)
            else:
                paramSet.append(0)
                paramSet.append(0)
                sd_set.append(0)

        found_div_correct_average = found_div_correct_sum / 10
        paramSet.append(str(found_div_correct_average))
        found_div_correct_dist_from_1 = abs(1 - found_div_correct_average)
        paramSet.append(str(found_div_correct_dist_from_1))
        standard_dev = np.std(sd_set)
        paramSet.append(standard_dev)
        metric_sum = found_div_correct_dist_from_1 + standard_dev
        paramSet.append(metric_sum)

    print("Subset Four Complete: Printout (for backup in case of .csv file issues): " + str(subset_4))

    fields = ['DP', 'Minimum Distance', 'Median Blur', 'Param 1', 'Param 2', 'Minimum Radius', 'Maximum Radius',
              'Image 1 Beads Found', 'Image 1 Found/Total', 'Image 2 Beads Found', 'Image 2 Found/Total',
              'Image 3 Beads Found', 'Image 3 Found/Total', 'Image 4 Beads Found', 'Image 4 Found/Total',
              'Image 5 Beads Found', 'Image 5 Found/Total', 'Image 6 Beads Found', 'Image 6 Found/Total',
              'Image 7 Beads Found', 'Image 7 Found/Total', 'Image 8 Beads Found', 'Image 8 Found/Total',
              'Image 9 Beads Found', 'Image 9 Found/Total', 'Image 10 Beads Found', 'Image 10 Found/Total',
              'Average % of Correct Count', 'Metric 1', 'Metric 2 (S.D.)', 'MetricSum']

    with open('hough_secondary_analysis_4.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(subset_4)

def analysis_5():
    with open('subset_5.txt', 'rb') as filehandle:
        subset_5 = pickle.load(filehandle)
    print("Confirming number of parameter sets in sub-list 5: " + str(len(subset_5)))
    print("        Analysis beginning")
    calc_counter = 0
    subset_count = len(subset_5)
    for paramSet in subset_5:
        found_div_correct_sum = 0
        d_p = int(paramSet[0])
        min_dist = int(paramSet[1])
        median_blur = int(paramSet[2])
        parameter_one = int(paramSet[3])
        parameter_two = int(paramSet[4])
        min_radius = int(paramSet[5])
        max_radius = int(paramSet[6])
        calc_counter += 1
        sd_set = []
        if calc_counter % 1000 == 0:
            percent_done = round(100 * calc_counter / subset_count, 2)
            print("Set 5 calculations: " + str(calc_counter) + "/" + str(subset_count)
                  + "     (" + str(percent_done) + "%)")
            print("Time: " + str(datetime.datetime.now()))

        for key in test_images_dict:
            # FIX: Use direct file path
            img = cv.imread(key, cv.IMREAD_COLOR)
            if img is None: continue
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            gray = cv.medianBlur(gray, median_blur)
            circles = cv.HoughCircles(image=gray, method=cv.HOUGH_GRADIENT,
                                      dp=d_p, minDist=min_dist,
                                      param1=parameter_one, param2=parameter_two,
                                      minRadius=min_radius, maxRadius=max_radius)
            if circles is not None:
                circles_found = len(circles[0, :])
                circles_total = test_images_dict[key]
                paramSet.append(str(circles_found))
                paramSet.append(str(circles_found / circles_total))
                sd_set.append(circles_found / circles_total)
                found_div_correct_sum += (circles_found / circles_total)
            else:
                paramSet.append(0)
                paramSet.append(0)
                sd_set.append(0)

        found_div_correct_average = found_div_correct_sum / 10
        paramSet.append(str(found_div_correct_average))
        found_div_correct_dist_from_1 = abs(1 - found_div_correct_average)
        paramSet.append(str(found_div_correct_dist_from_1))
        standard_dev = np.std(sd_set)
        paramSet.append(standard_dev)
        metric_sum = found_div_correct_dist_from_1 + standard_dev
        paramSet.append(metric_sum)

    print("Subset Five Complete: Printout (for backup in case of .csv file issues): " + str(subset_5))

    fields = ['DP', 'Minimum Distance', 'Median Blur', 'Param 1', 'Param 2', 'Minimum Radius', 'Maximum Radius',
              'Image 1 Beads Found', 'Image 1 Found/Total', 'Image 2 Beads Found', 'Image 2 Found/Total',
              'Image 3 Beads Found', 'Image 3 Found/Total', 'Image 4 Beads Found', 'Image 4 Found/Total',
              'Image 5 Beads Found', 'Image 5 Found/Total', 'Image 6 Beads Found', 'Image 6 Found/Total',
              'Image 7 Beads Found', 'Image 7 Found/Total', 'Image 8 Beads Found', 'Image 8 Found/Total',
              'Image 9 Beads Found', 'Image 9 Found/Total', 'Image 10 Beads Found', 'Image 10 Found/Total',
              'Average % of Correct Count', 'Metric 1', 'Metric 2 (S.D.)', 'MetricSum']

    with open('hough_secondary_analysis_5.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(subset_5)

def analysis_6():
    with open('subset_6.txt', 'rb') as filehandle:
        subset_6 = pickle.load(filehandle)
    print("Confirming number of parameter sets in sub-list 6: " + str(len(subset_6)))
    print("        Analysis beginning")
    calc_counter = 0
    subset_count = len(subset_6)
    for paramSet in subset_6:
        found_div_correct_sum = 0
        d_p = int(paramSet[0])
        min_dist = int(paramSet[1])
        median_blur = int(paramSet[2])
        parameter_one = int(paramSet[3])
        parameter_two = int(paramSet[4])
        min_radius = int(paramSet[5])
        max_radius = int(paramSet[6])
        calc_counter += 1
        sd_set = []
        if calc_counter % 1000 == 0:
            percent_done = round(100 * calc_counter / subset_count, 2)
            print("Set 6 calculations: " + str(calc_counter) + "/" + str(subset_count)
                  + "     (" + str(percent_done) + "%)")
            print("Time: " + str(datetime.datetime.now()))

        for key in test_images_dict:
            # FIX: Use direct file path
            img = cv.imread(key, cv.IMREAD_COLOR)
            if img is None: continue
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            gray = cv.medianBlur(gray, median_blur)
            circles = cv.HoughCircles(image=gray, method=cv.HOUGH_GRADIENT,
                                      dp=d_p, minDist=min_dist,
                                      param1=parameter_one, param2=parameter_two,
                                      minRadius=min_radius, maxRadius=max_radius)
            if circles is not None:
                circles_found = len(circles[0, :])
                circles_total = test_images_dict[key]
                paramSet.append(str(circles_found))
                paramSet.append(str(circles_found / circles_total))
                sd_set.append(circles_found / circles_total)
                found_div_correct_sum += (circles_found / circles_total)
            else:
                paramSet.append(0)
                paramSet.append(0)
                sd_set.append(0)

        found_div_correct_average = found_div_correct_sum / 10
        paramSet.append(str(found_div_correct_average))
        found_div_correct_dist_from_1 = abs(1 - found_div_correct_average)
        paramSet.append(str(found_div_correct_dist_from_1))
        standard_dev = np.std(sd_set)
        paramSet.append(standard_dev)
        metric_sum = found_div_correct_dist_from_1 + standard_dev
        paramSet.append(metric_sum)

    print("Subset Six Complete: Printout (for backup in case of .csv file issues): " + str(subset_6))

    fields = ['DP', 'Minimum Distance', 'Median Blur', 'Param 1', 'Param 2', 'Minimum Radius', 'Maximum Radius',
              'Image 1 Beads Found', 'Image 1 Found/Total', 'Image 2 Beads Found', 'Image 2 Found/Total',
              'Image 3 Beads Found', 'Image 3 Found/Total', 'Image 4 Beads Found', 'Image 4 Found/Total',
              'Image 5 Beads Found', 'Image 5 Found/Total', 'Image 6 Beads Found', 'Image 6 Found/Total',
              'Image 7 Beads Found', 'Image 7 Found/Total', 'Image 8 Beads Found', 'Image 8 Found/Total',
              'Image 9 Beads Found', 'Image 9 Found/Total', 'Image 10 Beads Found', 'Image 10 Found/Total',
              'Average % of Correct Count', 'Metric 1', 'Metric 2 (S.D.)', 'MetricSum']

    with open('hough_secondary_analysis_6.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(subset_6)

def analysis_7():
    with open('subset_7.txt', 'rb') as filehandle:
        subset_7 = pickle.load(filehandle)
    print("Confirming number of parameter sets in sub-list 7: " + str(len(subset_7)))
    print("        Analysis beginning")
    calc_counter = 0
    subset_count = len(subset_7)
    for paramSet in subset_7:
        found_div_correct_sum = 0
        d_p = int(paramSet[0])
        min_dist = int(paramSet[1])
        median_blur = int(paramSet[2])
        parameter_one = int(paramSet[3])
        parameter_two = int(paramSet[4])
        min_radius = int(paramSet[5])
        max_radius = int(paramSet[6])
        calc_counter += 1
        sd_set = []
        if calc_counter % 1000 == 0:
            percent_done = round(100 * calc_counter / subset_count, 2)
            print("Set 7 calculations: " + str(calc_counter) + "/" + str(subset_count)
                  + "     (" + str(percent_done) + "%)")
            print("Time: " + str(datetime.datetime.now()))

        for key in test_images_dict:
            # FIX: Use direct file path
            img = cv.imread(key, cv.IMREAD_COLOR)
            if img is None: continue
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            gray = cv.medianBlur(gray, median_blur)
            circles = cv.HoughCircles(image=gray, method=cv.HOUGH_GRADIENT,
                                      dp=d_p, minDist=min_dist,
                                      param1=parameter_one, param2=parameter_two,
                                      minRadius=min_radius, maxRadius=max_radius)
            if circles is not None:
                circles_found = len(circles[0, :])
                circles_total = test_images_dict[key]
                paramSet.append(str(circles_found))
                paramSet.append(str(circles_found / circles_total))
                sd_set.append(circles_found / circles_total)
                found_div_correct_sum += (circles_found / circles_total)
            else:
                paramSet.append(0)
                paramSet.append(0)
                sd_set.append(0)

        found_div_correct_average = found_div_correct_sum / 10
        paramSet.append(str(found_div_correct_average))
        found_div_correct_dist_from_1 = abs(1 - found_div_correct_average)
        paramSet.append(str(found_div_correct_dist_from_1))
        standard_dev = np.std(sd_set)
        paramSet.append(standard_dev)
        metric_sum = found_div_correct_dist_from_1 + standard_dev
        paramSet.append(metric_sum)

    print("Subset Seven Complete: Printout (for backup in case of .csv file issues): " + str(subset_7))

    fields = ['DP', 'Minimum Distance', 'Median Blur', 'Param 1', 'Param 2', 'Minimum Radius', 'Maximum Radius',
              'Image 1 Beads Found', 'Image 1 Found/Total', 'Image 2 Beads Found', 'Image 2 Found/Total',
              'Image 3 Beads Found', 'Image 3 Found/Total', 'Image 4 Beads Found', 'Image 4 Found/Total',
              'Image 5 Beads Found', 'Image 5 Found/Total', 'Image 6 Beads Found', 'Image 6 Found/Total',
              'Image 7 Beads Found', 'Image 7 Found/Total', 'Image 8 Beads Found', 'Image 8 Found/Total',
              'Image 9 Beads Found', 'Image 9 Found/Total', 'Image 10 Beads Found', 'Image 10 Found/Total',
              'Average % of Correct Count', 'Metric 1', 'Metric 2 (S.D.)', 'MetricSum']

    with open('hough_secondary_analysis_7.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(subset_7)

def analysis_8():
    with open('subset_8.txt', 'rb') as filehandle:
        subset_8 = pickle.load(filehandle)
    print("Confirming number of parameter sets in sub-list 8: " + str(len(subset_8)))
    print("        Analysis beginning")
    calc_counter = 0
    subset_count = len(subset_8)
    for paramSet in subset_8:
        found_div_correct_sum = 0
        d_p = int(paramSet[0])
        min_dist = int(paramSet[1])
        median_blur = int(paramSet[2])
        parameter_one = int(paramSet[3])
        parameter_two = int(paramSet[4])
        min_radius = int(paramSet[5])
        max_radius = int(paramSet[6])
        calc_counter += 1
        sd_set = []
        if calc_counter % 1000 == 0:
            percent_done = round(100 * calc_counter / subset_count, 2)
            print("Set 8 calculations: " + str(calc_counter) + "/" + str(subset_count)
                  + "     (" + str(percent_done) + "%)")
            print("Time: " + str(datetime.datetime.now()))

        for key in test_images_dict:
            # FIX: Use direct file path
            img = cv.imread(key, cv.IMREAD_COLOR)
            if img is None: continue
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            gray = cv.medianBlur(gray, median_blur)
            circles = cv.HoughCircles(image=gray, method=cv.HOUGH_GRADIENT,
                                      dp=d_p, minDist=min_dist,
                                      param1=parameter_one, param2=parameter_two,
                                      minRadius=min_radius, maxRadius=max_radius)
            if circles is not None:
                circles_found = len(circles[0, :])
                circles_total = test_images_dict[key]
                paramSet.append(str(circles_found))
                paramSet.append(str(circles_found / circles_total))
                sd_set.append(circles_found / circles_total)
                found_div_correct_sum += (circles_found / circles_total)
            else:
                paramSet.append(0)
                paramSet.append(0)
                sd_set.append(0)

        found_div_correct_average = found_div_correct_sum / 10
        paramSet.append(str(found_div_correct_average))
        found_div_correct_dist_from_1 = abs(1 - found_div_correct_average)
        paramSet.append(str(found_div_correct_dist_from_1))
        standard_dev = np.std(sd_set)
        paramSet.append(standard_dev)
        metric_sum = found_div_correct_dist_from_1 + standard_dev
        paramSet.append(metric_sum)

    print("Subset Eight Complete: Printout (for backup in case of .csv file issues): " + str(subset_8))

    fields = ['DP', 'Minimum Distance', 'Median Blur', 'Param 1', 'Param 2', 'Minimum Radius', 'Maximum Radius',
              'Image 1 Beads Found', 'Image 1 Found/Total', 'Image 2 Beads Found', 'Image 2 Found/Total',
              'Image 3 Beads Found', 'Image 3 Found/Total', 'Image 4 Beads Found', 'Image 4 Found/Total',
              'Image 5 Beads Found', 'Image 5 Found/Total', 'Image 6 Beads Found', 'Image 6 Found/Total',
              'Image 7 Beads Found', 'Image 7 Found/Total', 'Image 8 Beads Found', 'Image 8 Found/Total',
              'Image 9 Beads Found', 'Image 9 Found/Total', 'Image 10 Beads Found', 'Image 10 Found/Total',
              'Average % of Correct Count', 'Metric 1', 'Metric 2 (S.D.)', 'MetricSum']

    with open('hough_secondary_analysis_8.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(subset_8)


def show_top_param_sets():
    print("Combining subset data into one .csv file, titled 'all_params.csv' (this will be a big file) ")
    all_files = glob.glob(os.path.join("*.csv"))
    df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
    df.to_csv('all_params.csv', index=False)

    print("Determining top parameter set(s)")
    top_scoring_params_df = df[df.MetricSum == df.MetricSum.min()]
    print("Saving top parameter set(s) to .csv file, titled 'top_scoring_params.csv'")
    top_scoring_params_df.to_csv('top_scoring_params.csv', index=False)

    print("Obtaining HoughCircles output images for every image for each top parameter set")
    print("These are saved in the format 'top_param_set_(number)_image_(number).png'")
    top_scoring_params_df.to_csv('top_scoring_params_list-able.csv', index=False, header=False)
    
    with open('top_scoring_params_list-able.csv', 'r') as f:
        csv_readout = csv.reader(f)
        top_params_list_raw = list(csv_readout)
        top_params_list_final = []
        for row in top_params_list_raw:
            params_only = row[0:7]
            top_params_list_final.append(params_only)
        param_count = 0
        for row in top_params_list_final:
            param_count += 1
            param_name = "top_param_set_" + str(param_count)
            d_p = int(row[0])
            min_dist = int(row[1])
            median_blur = int(row[2])
            parameter_one = int(row[3])
            parameter_two = int(row[4])
            min_radius = int(row[5])
            max_radius = int(row[6])
            image_count = 0
            for key in test_images_dict:
                image_count += 1
                image_name = param_name + "_image" + str(image_count) + ".png"
                # FIX: Use direct file path
                img = cv.imread(key, cv.IMREAD_COLOR)
                if img is None: continue
                gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                gray = cv.medianBlur(gray, median_blur)
                circles = cv.HoughCircles(image=gray, method=cv.HOUGH_GRADIENT,
                                          dp=d_p, minDist=min_dist,
                                          param1=parameter_one, param2=parameter_two,
                                          minRadius=min_radius, maxRadius=max_radius)
                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    for i in circles[0, :]:
                        center = (i[0], i[1])
                        cv.circle(img, center, 1, (0, 100, 100), 1)
                        radius = i[2]
                        cv.circle(img, center, radius, (0, 255, 0), 1)

                cv.imwrite(image_name, img)
    print("Images all saved.")


if __name__ == "__main__":
    start_time_total = time.time()
    build_param_list()
    p1 = mp.Process(target=analysis_1)
    p2 = mp.Process(target=analysis_2)
    p3 = mp.Process(target=analysis_3)
    p4 = mp.Process(target=analysis_4)
    p5 = mp.Process(target=analysis_5)
    p6 = mp.Process(target=analysis_6)
    p7 = mp.Process(target=analysis_7)
    p8 = mp.Process(target=analysis_8)
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    p8.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    p7.join()
    p8.join()
    show_top_param_sets()
    print("Program complete. Bye for now!")
    print("--- %s seconds ---" % (time.time() - start_time_total))
