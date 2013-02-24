#! usr/bin/python
#  CS 325 Assignment 1
#  List Generator for List Inversion Algorithm
#  2/1/13

import argparse
import random

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("size", default=100, type=int, help="The size of the randomly generated list to create")
    parser.add_argument("-output", default="output.txt", dest="output", help="File to save randomly generated list in")
    parser.add_argument("-count", default=1, type=int, dest="count", help="Number of lists to create")

    args = parser.parse_args()
    
    num_list = []

    try:
        output = open(args.output, 'w')
        
        output.truncate(0)
        
        random.seed()
       
        for i in range(0, args.count):
            for x in range(1, int(args.size)+1 ):
                x = random.randrange(2000)
                output.write("{},".format(x-1000))

            output.write("\n")
        
    except IOError:
        print("Error Opening File")
        
    finally:
        output.close()

if __name__ == "__main__":
    main()
    
