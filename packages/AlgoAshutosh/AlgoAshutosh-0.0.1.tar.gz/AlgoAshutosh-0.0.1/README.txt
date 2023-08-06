This is a basic trading strategy backtesting library.
It can be used to backtest option strategies.

Three files are needed to backtest the option strategies.
One file with the futures data.
Another file with the call option data.
Third file with the put option data.

Ensure the below format for the files and the files should be of the csv format.

Futures file : Order of Columns : yyyy-mm-dd,	date,	month,	year,	expiry_date(of the format dd-(first three characters of month)-yy example : 26-May-22),	open,	high,	low,	close
Call Option File : Order of Columns : datetime	year	month	Date	expiry_date	Time	strike_price	open	high	low	close (example : 2022-01-03 9:15:00	2022	1	3	27-Jan-22	9:15:00	15500	1961.55	2010	1961.55	2004.45)
Put Option File : Order of Columns : datetime	year	month	date	expiry_date	time	strike_price	open	high	low	close (example : 2022-04-01 9:15:00	2022	4	1	28-Apr-22	9:15:00	15500	25.1	25.55	19.95	20.1)

Argument list for ironCondorStrategy :
self, putFile, callFile, spotFile, sellPut, sellCall, buyCall, buyPut, entry, exit, lotSize

example of code

from AlgoAshutosh import *

object = ironCondor()
object.ironCondorStrategy("/Users/username/Desktop/putOptionsFile.csv","/Users/username/Desktop/callOptionsFile.csv","/Users/username/Desktop/futuresFile.csv",100,100,200,200,1,10,50)
This means if spot price is 15000 then call sold at strike price 15000+100, call bought at 15000+200, put sold at strike price 15000-100, put bought at 15000-200, would be backtested.
The entry would be at the first day of the month and exit at expiry date - 10 days before.
So for example to exit position at expiry date pass that argument as 0.
50 represents the lot size.

Argument list for shortStraddleStrategy :
self, putFile, callFile, spotFile, entry, exit, lotSize

Argument list for shortStrangleStrategy :
self, putFile, callFile, spotFile, sellPut, sellCall, entry,exit, lotSize
