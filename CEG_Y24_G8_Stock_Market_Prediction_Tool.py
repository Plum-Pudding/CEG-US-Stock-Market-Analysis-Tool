#system
import os;
import sys;
import math;

#vendor libraries
parent_dir = os.path.abspath(os.path.dirname(__file__));
vendor_dir = os.path.join(parent_dir, 'vendor');
sys.path.append(vendor_dir);

import plotly;
import requests;
import PyQt5;

#internal 
import utilAPI;
import utilStockAnalysis;
import stockPrediction;

def main():
    #TODO: Learn how to use PyQt6 GUI library (GPL v3 license-- no NDAs I guess)
    #TODO: Check out Plotly as a lib for drawing graphs (MIT license-- do as you please)



    #Start GUI


    print("sus");
    pass;

if __name__ == "__main__":
    main();