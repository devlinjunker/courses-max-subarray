#! /usr/bin/python
# CS 325 Implementation Assignment 1
# Devlin Junker
# 2/1/13

import fileinput
import argparse
import string
import time
import sys
import resource

NUM_TEST_CASES = 1

def main():
    sys.setrecursionlimit(100000)
    soft, hard = resource.getrlimit(resource.RLIMIT_STACK)
    resource.setrlimit(resource.RLIMIT_STACK, (hard, hard))
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
                
                run_test_case(nums, args.method)
                
        except IOError:
            print("Error Opening File")
        finally:
            if(input):
                input.close()
    
    return 0

def run_test_case(nums, method):
    start_time = time.time()

    if(method == 1):
         inversions = brute_force(nums)
    elif(method == 2):
         inversions = divide(nums)
    elif(method == 3):
         (inversions,sorted_nums) = merge_count(nums)
    else:
        print("Invalid Method Input Must be 1, 2 or 3")
        return 0
    
    end_time = time.time()

    total_time = end_time-start_time

    details = {"max": len(nums), "nums": ",".join([str(x) for x in nums]), "inversions": inversions, "elapsed": total_time}
    
    print_case_details(details)


def brute_force(nums):
    count = 0
    
    for x in range(0, len(nums)):
        for y in range(x, len(nums)):
            #print(int(nums[x]), int(nums[y]))
            if nums[x] > nums[y]:
                count += 1
    
    return count   


def divide(nums):
    count = 0
    
    if( len(nums) > 2 ):
        mid = len(nums)/2
        count += divide(nums[0:len(nums)/2])
        count += divide(nums[len(nums)/2:len(nums)])
        
        for x in range(0, len(nums)/2):
            for y in range(len(nums)/2, len(nums)):
                if nums[x] > nums[y]:
                    count += 1

    elif( len(nums) > 1):
        if( nums[0] > nums[1] ):
            count += 1
    
    return count


def merge_count(nums):
    count = 0
    
    if( len(nums) > 1 ):
        (count, merged_nums) = merge( merge_count( nums[0:len(nums)/2] ), merge_count( nums[len(nums)/2:] ) ) 
        #print (count, merged_nums)
        return (count, merged_nums)
    else:
        return (0, nums)


def merge(count_arr1, count_arr2):
    (count1, arr1) = count_arr1
    (count2, arr2) = count_arr2
    
    count = count1 + count2

    #print arr1
    #print arr2

    if( not(arr1) ):
        return (0, arr2)
    if( not(arr2) ):
        return (0, arr1)

    if( arr1[0] <= arr2[0] ):
        (new_count, merged_arrays) = merge( (0, arr1[1:]), (0, arr2))
        return (new_count+count, [arr1[0]]+merged_arrays )
    elif( arr1[0] > arr2[0] ):
        (new_count, merged_arrays) = merge((0, arr1), (0, arr2[1:]))
        return (new_count+count+len(arr1), [arr2[0]]+merged_arrays )


def print_case_details(details):
    global NUM_TEST_CASES
    output = """
    Test Case: {0}
    Input: {1}
    n: {2}
    Inversions: {3}
    Elapsed Time: {4}
    """.format(NUM_TEST_CASES, details["nums"], details["max"], details["inversions"], details["elapsed"])
    
    NUM_TEST_CASES = NUM_TEST_CASES + 1

    print(output)

if __name__ == '__main__':
    main()
