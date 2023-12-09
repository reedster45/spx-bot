
import datetime
import time
import yfinance as yf



# returns converted timestamp in yyy-mm-dd format
def timestampconverter(timestp):
    return timestp.strftime('%Y-%m-%d %H:%M:%S')

# renames index from timestamps to strings
def rename_index(data):
    for i in data.index:
        data.rename(index={i:timestampconverter(i)}, inplace=True)

# returns 4 dataframes of price history for 30d, 60d, 90d w set interval (d, h)
def get_data(TICK, interval):
    spx = yf.Ticker(TICK)
    # print(spx.info)  # should i refactor all this code to make it better?????/

    data07 = spx.history(period='7d', interval=interval)
    data30 = spx.history(period='30d', interval=interval)
    data60 = spx.history(period='60d', interval=interval)
    data90 = spx.history(period='90d', interval=interval)

    rename_index(data07)
    rename_index(data30)
    rename_index(data60)
    rename_index(data90)

    return data07, data30, data60, data90
    




# return average of all values in list
def calculate_avg(data):
    return round(sum(data) / len(data), 2)

# returns percentage of True and False values in a list
def calculate_percentage(data):
    bull = data.count(True)
    bear = data.count(False)
    total = len(data)
    p_bull = round((bull / total) * 100, 2)
    p_bear = round((bear / total) * 100, 2)

    return [p_bull, p_bear]

# return average range in data (high-low) for each day in timeframe
def avg_range_days(data):
    diff = []
    for i in data.index:
        diff.append(data['High'][i] - data['Low'][i])
    
    return calculate_avg(diff)

# return average range in first & last hours for each day in timeframe
def avg_range_hours(data, hour):
    diff = []
    for i in data.index:
        if (hour == 'last'):
            if ('15:30:00' in i):
                diff.append(data['High'][i] - data['Low'][i])
        elif (hour == 'first'):
            if ('09:30:00' in i):
                    diff.append(data['High'][i] - data['Low'][i])
    
    return calculate_avg(diff)

# return percentage of bull days and bear days
def bull_bear(data):
    green = []
    for i in data.index:
        if (data['Open'][i] < data['Close'][i]):
            green.append(True)
        else:
            green.append(False)

    return calculate_percentage(green)




# gets daily price data and returns a list of the average range for each day
# also returns percentage of bear/bull days
def get_avg_range_days(TICK):
    # daily price data in last 07 - 90 days
    days07, days30, days60, days90 = get_data(TICK, '1d')

    d07 = avg_range_days(days07)
    d30 = avg_range_days(days30)
    d60 = avg_range_days(days60)
    d90 = avg_range_days(days90)

    bb07 = bull_bear(days07)
    bb30 = bull_bear(days30)
    bb60 = bull_bear(days60)
    bb90 = bull_bear(days90)

    return d07, d30, d60, d90, bb07, bb30, bb60, bb90

# get daily price data of first and last hours and returns the average range of each day in the first and last hour
def get_avg_range_hours(TICK):
    # last hour (30 MINS) in last 30 - 90 days
    # first hour in last 30 - 90 days
    hours07, hours30, hours60, hours90 = get_data(TICK, '1h')

    lh07 = avg_range_hours(hours07, "last")
    lh30 = avg_range_hours(hours30, "last")
    lh60 = avg_range_hours(hours60, "last")
    lh90 = avg_range_hours(hours90, "last")

    fh07 = avg_range_hours(hours07, "first")
    fh30 = avg_range_hours(hours30, "first")
    fh60 = avg_range_hours(hours60, "first")
    fh90 = avg_range_hours(hours90, "first")

    return lh07, lh30, lh60, lh90, fh07, fh30, fh60, fh90



# requests data for TICK from yahoo finance api
def main():
    # S&P 500 Index (SPX)
    TICK = '^GSPC'

    # DAILY AVERAGE RANGES
    d07, d30, d60, d90, bb07, bb30, bb60, bb90 = get_avg_range_days(TICK)

    # LAST & FIRST HOUR AVERAGE RANGES
    lh07, lh30, lh60, lh90, fh07, fh30, fh60, fh90 = get_avg_range_hours(TICK)


    # print all results
    print("AVERAGE RANGES:\n")

    print("_07 days_")
    print("daily: ", d07)
    print("first hour: ", fh07)
    print("last hour: ", lh07)
    print(f"bull/bear: {bb07[0]}% / {bb07[1]}%")
    print("\n")

    print("_30 days_")
    print("daily: ", d30)
    print("first hour: ", fh30)
    print("last hour: ", lh30)
    print(f"bull/bear: {bb30[0]}% / {bb30[1]}%")
    print("\n")

    print("_60 days_")
    print("daily: ", d60)
    print("first hour: ", fh60)
    print("last hour: ", lh60)
    print(f"bull/bear: {bb60[0]}% / {bb60[1]}%")
    print("\n")

    print("_90 days_")
    print("daily: ", d90)
    print("first hour: ", fh90)
    print("last hour: ", lh90)
    print(f"bull/bear: {bb90[0]}% / {bb90[1]}%")
    print("\n")


main()