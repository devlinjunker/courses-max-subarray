#! /usr/bin/python
# CS 325 Implementation Assignment 1
# Devlin Junker
# 2/1/13

import fileinput
import argparse
import string
import time
import sys

NUM_TEST_CASES = 1

DEBUG = 0

def main():
    input = False

    parser = argparse.ArgumentParser();
    
    parser.add_argument("-file", default="input.txt", dest="filename", help="The name of the file to read test case inputs from, defaults to input.txt (Each test case is a seperate line of numbers where each number is seperated by a comma)")
    parser.add_argument("-method", default=1, type=int, dest="method", help="The Algorithm to use to count inversions (1 = bruteforce [Default], 2 = Divide and Conquer, 3 = Merge Count")
    parser.add_argument("numbers", default=0, type=int, metavar="N", nargs='*', help="Integers to run a test case on, if none are specified then input file is read")
    
    args = parser.parse_args()
    
    if(args.numbers != 0):
        run_test_case(args.numbers, args.method)
    else:
        try:
            input = open(args.filename, 'rU')
            
            for line in input:
                line = string.replace(line, '\n', '')
                nums = string.split(line, ",")
                nums = map(int, nums)


                if(not(nums[0])):
                    continue

                
                run_test_case(nums, 1)
                run_test_case(nums, 2)
                run_test_case(nums, 3)
                
        except IOError:
            print("Error Opening File")
        finally:
            if(input):
                input.close()
    
    return 0

def run_test_case(nums, method):
    start_time = time.time()

    if(method == 1):
         (maxval, start, end) = brute_force(nums)
    elif(method == 2):
         (maxval, start, end)= divide(nums)
    elif(method == 3):
         (maxval, start, end) = dynamic(nums)
    else:
        print("Invalid Method Input Must be 1, 2 or 3")
        return 0
    
    end_time = time.time()

    total_time = end_time-start_time

    details = {"size": len(nums), "max": maxval, "subarray": nums[start:end], "nums": nums, "elapsed": total_time, "method":method}
    
    print_case_details(details)


def brute_force(nums):
    maxval = 0
    maxstart = 0
    maxend = 0
    
    vals = [ [ 0 for i in range( len(nums) ) ] for j in range( len (nums) ) ]

    for end in range( len(nums) ):
        if(end == 0):
            vals[0][end] = nums[end]
        else:
            vals[0][end] = nums[end-1]+nums[end]
        
        if DEBUG: print "0,{}:{}".format(end, vals[0][end]) 
        
        if vals[0][end] > maxval:
            maxval = vals[0][end];
            maxstart = 0
            maxend = end+1

    for end in reversed( range( len(nums) ) ):
        for start in range( end ):
            vals[start+1][end] = vals[start][end] - nums[start]
            
            if DEBUG: print "{},{}:{}".format(start+1,end, vals[start+1][end])
            
            if vals[start+1][end] > maxval:
                maxval = vals[start+1][end] 
                maxstart = start+1
                maxend = end
    
    return (maxval, maxstart, maxend);   


def divide(nums):
    print len(nums)
    tempmax = 0
    midmax = 0
    midstart = 0
    midend = 0

    leftmax = 0
    rightmax = 0
   
    if(len(nums) == 0):
        return (0, 0, 0)

    middle = len(nums)/2

    midstart = middle
    midend = middle

    if( len(nums) == 1):
        return (nums[0], 0, 1) 

    for i in reversed(range(middle)):
        tempmax = tempmax+nums[i]
        if( tempmax > leftmax ):
            leftmax = tempmax
            midstart = i

    tempmax = 0

    for i in range(middle, len(nums)):
        tempmax = tempmax + nums[i]
        if( tempmax > rightmax ):
            rightmax = tempmax
            midend = i+1

    midmax = leftmax+rightmax

    (leftmax, leftstart, leftend) = divide(nums[:middle])
    (rightmax, rightstart, rightend) = divide(nums[middle:])

    if DEBUG: print( "left({}, {}, {}) right({}, {}, {}) ".format(leftmax, leftstart, leftend, rightmax, rightstart, rightend))

    if(midmax >= leftmax and midmax >= rightmax):
        return (midmax, midstart, midend)
    elif(leftmax >= rightmax and leftmax > midmax):
        return (leftmax, leftstart, leftend)
    elif(rightmax > leftmax and rightmax > midmax):
        return (rightmax, rightstart+middle, rightend+middle)

def dynamic(nums):
    start = 0
    end = 0
    maxval = 0

    vals = [0 for x in range(len(nums))]

    for i in range(1, len(nums)):
        if(i == 0):
            vals[i] = nums[i]
        elif(nums[i] + vals[i-1] < 0):
            vals[i] = 0
        else:
            vals[i] = vals[i-1]+nums[i]

    for i in range(len(nums)):
        if(vals[i] > maxval):
            maxval = vals[i]
            end = i+1

    temp = maxval
    for i in reversed(range(end)):
        if(temp <= 0):
            start = i+1
            break
        else:
            temp = temp - nums[i];

    return (maxval, start, end)

def print_case_details(details):
    global NUM_TEST_CASES
    output = """{0},{1},{2}""".format(NUM_TEST_CASES, details["method"], details["elapsed"])
    
    NUM_TEST_CASES = NUM_TEST_CASES + 1

    print(output)

if __name__ == '__main__':
    main()
