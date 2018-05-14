AlphaVantage (alphavantage.co) custom command-line csv scraper for stocks. Daily, Weekly, and Monthly queries return up to 20 years of historical data. The intraday time series typically spans the last 10-15 trading days

### Installation

AVScraper.py requires [Python](https://www.python.org/downloads/release/python-364/) v3+ to run.

After downloading the py file, enter the directory where AVScraper resides (e.g., in Documents)
```sh
$ cd .../Documents/
```
Also make sure you have Pandas and AlphaVantage packages installed. If you don't have either install, type (Windows example)
```sh
$ pip install alpha_vantage
$ pip install pandas
```
### Run AVScraper.py
In the same terminal prompt, run
```sh
$ python AVScraper.py
```

Query will return a csv of the time-series data specified as follows:
```sh
$ api key
```

Enter your personal API key from alphavantage.co. For example,
```sh
$ api key A123B456C789D123
```
Next
```sh
$ single stock (‘s’) or multiple (‘m’)
```
If you want to query a single stock, enter
```sh
$ single stock (‘s’) or multiple (‘m’) s
```
If you want to query multiple stocks into a combined csv file, enter
```sh
$ single stock (‘s’) or multiple (‘m’) m
```

For a single stock:
```sh
$ symbol, time period, data to keep
```
Enter the symbol of the stock, e.g. Apple = ‘AAPL’

Enter the time period of interest:
-	Intraday = ‘intraday’
This API returns intraday time series (timestamp, open, high, low, close, volume of the equity specified, updated realtime. The timestamp values are the periods specified in the ‘interval’ prompt. Period options are ‘1min’, ‘5min’, ‘15min’, ‘30min’, ‘60min’.
-	Daily = ‘daily’
This API returns daily time series (date, daily open, daily high, daily low, daily close, daily volume) of the equity specified, covering up to 20 years of historical data
-	Daily Adjusted = ‘daily_adjusted’
This API returns daily time series (date, daily open, daily high, daily low, daily close, daily volume, daily adjusted close, and split/dividend events) of the equity specified, covering up to 20 years of historical data
-	Weekly = ‘weekly’
This API returns weekly time series (last trading day of each week, weekly open, weekly high, weekly low, weekly close, weekly volume) of the equity specified, covering up to 20 years of historical data
-	Weekly Adjusted = ‘weekly_adjusted’
This API returns weekly adjusted time series (last trading day of each week, weekly open, weekly high, weekly low, weekly close, weekly adjusted close, weekly volume, weekly dividend) of the equity specified, covering up to 20 years of historical data
-	Monthly = ‘monthly’
This API returns monthly time series (last trading day of each month, monthly open, monthly high, monthly low, monthly close, monthly volume) of the equity specified, covering up to 20 years of historical data
-	Monthly Adjusted = ‘monthly_adjusted’
This API returns monthly adjusted time series (last trading day of each month, monthly open, monthly high, monthly low, monthly close, monthly adjusted close, monthly volume, monthly dividend) of the equity specified, covering up to 20 years of historical data
Intraday query returns OHLCV data where the close values are the periods specified in the ‘interval’ prompt. Period options are ‘1min’, ‘5min’, ‘15min’, ‘30min’, ‘60min’.

Enter the data to keep for your csv export:
From the optional ‘O’ = open, ‘H’ = high, ‘L’ = low, ‘C’ = close, ‘A’ = adjusted close, ‘D’ = dividend amount, ‘S’ = split coefficient, enter data you’d like to keep (e.g., ‘OHL’ or ‘ohl’ will only return the open, high, and low data for the particular stock)

A typical query may look as follows: 
```sh
$ symbol, time period, data to keep
  ZIOP weekly_adjusted OHC
```

For multiple-stock queries:
```sh
$ symbols
```
Simple enter as many stocks of interest, say m stocks, and the program will return a csv file containing a n x m dataframe where each column represents one of m stocks and the n data points are the daily closing prices. 

###### NOTE: the size of the dataframe (n) will be as long as the most recently IPO’s stock in your query where closing price data has existed

A typical query may look as follows: 
```sh
$ symbols FB AAPL AMZN GOOGL GS MS
``` 

```sh
$ ’p’ for preview, Enter to continue
```  
If you’d like to preview the dataframe formatted as a Pandas DataFrame, enter ‘p’ before continuing, otherwise press Enter on your keyboard

```sh
$ path and csv file name
``` 
Enter the path of directory where you’d like the program to save your csv file and the name of the file. Say Bob wanted to save his Amazon data to his Documents directory. He would enter, for example,
```sh
$ path and csv file name C:\Users\Bob\Desktop\Documents\
``` 
(note the last backslash) for the directory and then the name of the file, say ‘AMZN_closing’.

So in all, Bob would enter
```sh
$ path and csv file name C:\Users\Bob\Desktop\Documents\ AMZN_closing
``` 
If an incorrect path is specified, the file will save to the location of the py script, AVScraper.py.  

