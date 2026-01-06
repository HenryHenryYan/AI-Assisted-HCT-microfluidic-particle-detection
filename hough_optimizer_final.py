
import cv2 as cv
import itertools
import numpy as np
import statistics
import time

# Original Parameters-to-Test List
medianBlurList1 = [*range(1,14,2)]
param1List1 = [*range(1,41,1)]
param2List1 = [*range(1,31,1)]
minRadiusList1 = [*range(1,12,1)]
maxRadiusList1 = [*range(4,16,1)]
minDistList1 = [*range(1,26,1)]

combos_total =  len(medianBlurList1)*len(param1List1)*len(param2List1)*len(minRadiusList1)*len(maxRadiusList1)*len(minDistList1)

# Successful Parameters from Analysis 1
medianBlurList2 = []                   
param1List2 = []
param2List2 = []
minRadiusList2 = []
maxRadiusList2 = []
minDistList2 = []

# Images for Analysis 1
# For each entry in this list, use the following format:
# "image file name including extension":number of circles of desired size that would be detected in successful test
# separate entries by a comma.
# (be sure to maintain the {} (dictionary) brackets, not [] which denote a different data receptacle type (list) in Python)
image_circle_dict1 = {"1 min.png":43,
                     "2 min.png":46,
                     "3 min.png":56,
                      "4 min.png":63,
                      "5 min.png":66,
                      "6 min.png":68,
                      "7 min.png":70,
                      "8 min.png":66,
                      "9 min.png":67,
                      "10 min.png":74}

# list for print-out of top params
top_matching_param1 = []

def analysis_1():
    top_match_count1 = 0
    calc_counter1 = 0

    for i in medianBlurList1:

        for k in param1List1:

            for l in param2List1:

                for m in minRadiusList1:

                    for n in maxRadiusList1:
                        pct = calc_counter1*100/combos_total
                        print(str(round(pct, 4)),"% of calculations complete.")

                        for o in minDistList1:
                            calc_counter1 += 1
                            match_count1 = 0

                            for key in image_circle_dict1:
                                img = cv.imread(cv.samples.findFile(key), cv.IMREAD_COLOR)
                                
                                gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                                gray = cv.medianBlur(gray, i)

                                circles1 = cv.HoughCircles(image=gray, method=cv.HOUGH_GRADIENT, dp=1, minDist=o,
                                                                            param1=k, param2=l, minRadius=m,
                                                                              maxRadius=n)
                                if circles1 is not None and len(circles1[0,:]) == image_circle_dict1[key]:
                                    match_count1 += 1
                                    #print("current param test is a match for ", str(match_count1), " of ", str(len(image_circle_dict1)), " test images.")
                                #else:
                                if match_count1 == 0:
                                    break

                                elif match_count1 > top_match_count1:
                                    top_match_count1 = match_count1
                                    top_matching_param1.clear()
                                    medianBlurList2.clear()
                                    param1List2.clear()
                                    param2List2.clear()
                                    minRadiusList2.clear()
                                    maxRadiusList2.clear()
                                    top_matching_param1.append("Top-Matching Parameter Set is: DP: 1 Minimum Distance: " + str(o) + " Median Blur: " + str(i) +
                                                              " Param 1: " + str(k) + " Param 2: " + str(l) + "Minimum Radius: " + str(m) + " Maximum Radius: " + str(n) +
                                                              " # Images Matched: " + str(match_count1) + " out of " + str(len(image_circle_dict1)) + " test images.")
                                    medianBlurList2.append(i)
                                    param1List2.append(k)
                                    param2List2.append(l)
                                    minRadiusList2.append(m)
                                    maxRadiusList2.append(n)
                                    print(top_matching_param1)
                                        
                                elif match_count1 == top_match_count1:
                                    top_matching_param1.append("Additional Top-Matching Parameter Set is: DP: 1 Minimum Distance: " + str(o) + " Median Blur: " + str(i) +
                                                              " Param 1: " + str(k) + " Param 2: " + str(l) + "Minimum Radius: " + str(m) + " Maximum Radius: " + str(n) +
                                                              " # Images Matched: " + str(match_count1) + " out of " + str(len(image_circle_dict1)) + " test images.")
                                    medianBlurList2.append(i)
                                    param1List2.append(k)
                                    param2List2.append(l)
                                    minRadiusList2.append(m)
                                    maxRadiusList2.append(n)
                                    print(top_matching_param1)           
                                    break

    print(top_matching_param1)
    print("End of analysis.")
 
def main():
    analysis_1()

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))