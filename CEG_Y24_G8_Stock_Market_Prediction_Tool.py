#system
import os;
import sys;
import math;

#vendor libraries
#parent_dir = os.path.abspath(os.path.dirname(__file__));
#vendor_dir = os.path.join(parent_dir, "vendor");

#sys.path.append(vendor_dir);

import vendor.requests.src.requests as requests; #Fucking stupid way of doing this but Python can't find the source and the above code isn't working
#Removed plotly-- see changelog
import vendor.PyQt6.sip as Qt6;
import vendor.pyqtgraph as QtGraph;

#internal 
import utilAPI;
import utilStockAnalysis;
import stockPrediction;


#online sources for data
import yfinance as yfin;


def main():
    #TODO: Learn how to use PyQt6 GUI library (GPL v3 license)
    #TODO: Check out pyqtgraph as a lib for drawing graphs (MIT license)

    rndInt = requests.get("https://www.random.org/integers/?num=1&min=0&max=9&format=plain&rnd=new");
    #rndInt = requests.get("https://www.random.org/integers/?num=10&min=1&max=6&col=1&base=10&format=plain&rnd=new");
    print(rndInt.text);

    #Start GUI


    class MyApp(Qt6.sip.QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('Hello There')
            self.setWindowIcon(Qt6.sip.QIcon('maps.ico'))
            self.resize(300,200) #width height
        pass


    print("sus");
    pass;

if __name__ == "__main__":
    main();