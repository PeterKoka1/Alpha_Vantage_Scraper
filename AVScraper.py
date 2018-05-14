import pandas as pd
import sys

from alpha_vantage.timeseries import TimeSeries

def alpha_vantage_pull():
    api_key = input('api key ')
    if api_key == '?':
        print_instructions()
    ts = TimeSeries(key=api_key, output_format='pandas')
    stock_scrape(ts, api_key)


def stock_scrape(ts, api_key):
    single_vs_multiple = input("single stock ('s') or multiple stocks ('m')")
    if single_vs_multiple == 's':
        print("symbol, time period, data to keep"
              "\nexample: AAPL weekly_adjusted OCV")
        try:
            user_input = input('')
            if user_input == '?':
                print_instructions()
            stock = user_input.split(' ')[0]
            time_period = user_input.split(' ')[1]
            data_to_keep = user_input.split(' ')[2]

            if time_period == 'intraday':
                print("interval (default = '1min')")
                interval = input('')
                if interval == '?':
                    print_instructions()
                interval = '1min' if interval == '' else interval

                ticker, meta_data = ts.get_intraday(symbol=stock, interval=interval)
                df = keep_data(ticker, data_to_keep)
                save_locally(df)

            elif time_period == 'daily':
                ticker, meta_data = ts.get_daily(symbol=stock)
                df = keep_data(ticker, data_to_keep)
                save_locally(df)

            elif time_period == 'daily_adjusted':
                ticker, meta_data = ts.get_daily_adjusted(symbol=stock)
                df = keep_data(ticker, data_to_keep)
                save_locally(df)

            elif time_period == 'weekly':
                ticker, meta_data = ts.get_weekly(symbol=stock)
                df = keep_data(ticker, data_to_keep)
                save_locally(df)

            elif time_period == 'weekly_adjusted':
                ticker, meta_data = ts.get_weekly_adjusted(symbol=stock)
                df = keep_data(ticker, data_to_keep)
                save_locally(df)

            elif time_period == 'monthly':
                ticker, meta_data = ts.get_monthly(symbol=stock)
                df = keep_data(ticker, data_to_keep)
                save_locally(df)

            elif time_period == 'monthly_adjusted':
                ticker, meta_data = ts.get_monthly_adjusted(symbol=stock)
                df = keep_data(ticker, data_to_keep)
                save_locally(df)

        except:
            print("Incorrect Input. Enter '?' for instructions. Press Enter to launch scraper again")
            error_input = input('')
            print_instructions() if error_input == '?' else stock_scrape(ts, api_key)

    elif single_vs_multiple == 'm':
        print("symbols"
              "\nexample: AAPL GOOGL AMZN")
        symbols = input("")
        list_of_symbols = symbols.split(' ')
        df = pd.DataFrame()
        for stock in list_of_symbols:
            try:
                ts = TimeSeries(key=api_key, output_format='pandas')
                ticker, meta_data = ts.get_daily(symbol=stock)
                drop_labs = [
                    'open',
                    'high',
                    'low',
                    'volume',
                ]
                ticker.drop(drop_labs, axis=1, inplace=True)
                ticker.rename(columns={'close': stock}, inplace=True)
                if ticker.empty:
                    print("Empty dataframe for {} - will not add to stocks_dfs dir".format(stock))
                else:
                    if df.empty:
                        df = ticker
                    else:
                        df = df.join(ticker)
            except:
                s = "Error: {}".format(sys.exc_info()[0])
                s += "\nwhile fetching data for {}".format(stock)

        see_preview(df)
        save_locally(df)


def keep_data(dataframe, data_to_keep):
    rename_cols = [
        j.replace(" ", "_")
        for i, j in enumerate(dataframe.columns)
        ]
    dataframe.columns = rename_cols
    if data_to_keep == 'all':
        see_preview(dataframe)
        return dataframe
    else:
        data = [i.lower() for i in list(data_to_keep)]
        df_cols = dataframe.columns
        cols = {dc[0]: ix for ix, dc in enumerate(df_cols)}
        drop_data = [ix for col, ix in cols.items() if col not in data]

        drop_cols = []
        for ix, col in enumerate(df_cols):
            if ix in drop_data:
                drop_cols.append(col)

        dataframe.drop(drop_cols, axis=1, inplace=True)

        see_preview(dataframe)
        return dataframe


def save_locally(df):
    """
    if incorrect path is given, csv will save where AVScraper.py file resides
    """
    path_input = input("path and csv file name\n")
    path = path_input.split(' ')[0]
    file_name = path_input.split(' ')[1]
    df.to_csv("{path}{file_name}.csv".format(path=path, file_name=file_name))


def see_preview(df):
    preview = input("'p' for preview, Enter to continue")
    if preview == 'p':
        print(df.head())
    if preview == "":
        pass


def print_instructions():
    print("Instructions")


def main():
    if __name__ == '__main__':
        alpha_vantage_pull()

main()
