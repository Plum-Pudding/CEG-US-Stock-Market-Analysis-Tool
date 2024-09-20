#system
import os;
import sys;
import math

import vendor.plotly;

#vendor libraries
parent_dir = os.path.abspath(os.path.dirname(__file__));
vendor_dir = os.path.join(parent_dir, "vendor");

sys.path.append(vendor_dir);

import vendor.requests; #Fucking stupid way of doing this but Python can't find the source and the above code isn't working
import vendor.plotly;
import vendor.PyQt6;

#internal 
import utilAPI;
import utilStockAnalysis;
import stockPrediction;

def main():
    #TODO: Learn how to use PyQt6 GUI library (GPL v3 license)
    #TODO: Check out Plotly as a lib for drawing graphs (MIT license)



    #Start GUI


    print("sus");
    pass;

if __name__ == "__main__":
    main();