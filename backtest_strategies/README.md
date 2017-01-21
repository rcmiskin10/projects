
#depends on requirements.txt

MET CS201 Introduction to Programming – Fall ‘16
Final Project- created a simple algorithmic trading program using python, pandas, numpy, and matplotlib. 
Created DataFrames in pandas of close, open, high, low historical prices using yahoo finance api in DataReader of given user input’s stock symbol. 
Then added columns to DataFrame of two simple technical analysis strategies, simple moving averages and exponential moving averages.
Calculated when the smaller moving average crossed above the larger moving average, and created a BUY signal. If opposite I created a SELL signal. 
I then recorded the price at which to buy and sell, and multiplied it by 10000 shares.
Took initial portfolio amount and calculated gain or loss on strategy. 
Written as a script file and ran through command line with standard output.
Also created matplotlib graphs with the historical price, the smaller moving average and larger moving average with buy and sell signals.

