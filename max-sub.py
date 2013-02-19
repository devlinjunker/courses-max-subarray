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
         (maxval, subarray) = brute_force(nums)
    elif(method == 2):
         (maxval, subarray)= divide(nums)
    elif(method == 3):
         (maxval, subarray) = dynamic(nums)
    else:
        print("Invalid Method Input Must be 1, 2 or 3")
        return 0
    
    end_time = time.time()

    total_time = end_time-start_time

    details = {"size": len(nums), "max": maxval, "subarray": ",".join([str(x) for x in subarray]), "inversions": inversions, "elapsed": total_time}
    
    print_case_details(details)


def brute_force(nums):
    count = 0
    
    return count   


def divide(nums):
    count = 0
    
    return count


def dynamic(nums):
    count = 0

    return (0, nums)

def print_case_details(details):
    global NUM_TEST_CASES
    output = """
    Test Case: {0}
    Input: {1}
    n: {2}
    output:{3}
    Max: {4}
    Elapsed Time: {5}
    """.format(NUM_TEST_CASES, details["nums"], details["size"], details["subarray"], details["max"], details["elapsed"])
    
    NUM_TEST_CASES = NUM_TEST_CASES + 1

    print(output)

if __name__ == '__main__':
    main()
