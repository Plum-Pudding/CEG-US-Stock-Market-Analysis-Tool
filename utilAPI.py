#API functions -- James
#TODO: Choose an API, research API data structure
#TODO: Retrieve API data, format into usable form-- object with array?

import requests;
import yfinance as yfin; #Backwards compat

def testGetRndInt():
    
    pass;

def yFinGetHist(stockCode, periodHist, intervalTime):
    stockCode = str(stockCode);
    testObj = yfin.Ticker(stockCode);
    testObjHist = testObj.history(interval=intervalTime, period=periodHist);
    #print(testObjHist);

    return(testObjHist);

    #print("sample text");

def testFunc():
    return 0;