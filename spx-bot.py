
import datetime
import time
import yfinance as yf



# returns converted timestamp in yyy-mm-dd format
# yyy-mm-mm HH:MM:SS-HH:MM
def timestampconverter(timestp):
    return timestp.strftime('%Y-%m-%d %H:%M:%S')

# renames index from timestamps to strings
def rename_index(data):
    for i in data.index:
        data.rename(index={i:timestampconverter(i)}, inplace=True)

# returns 3 dataframes of price history for 30d, 60d, 90d w set interval
def get_data(TICK, interval):
    spx = yf.Ticker(TICK)

    data30 = spx.history(period='30d', interval=interval)
    data60 = spx.history(period='60d', interval=interval)
    data90 = spx.history(period='90d', interval=interval)

    rename_index(data30)
    rename_index(data60)
    rename_index(data90)

    return data30, data60, data90
    


# return average of all values in data
def calculate_avg(data):
    return sum(data) / len(data)

# return average range in data (high-low) for set number of days
def avg_range_days(data):
    diff = []
    for i in data.index:
        diff.append(data['High'][i] - data['Low'][i])
    
    return calculate_avg(diff)

# return average range in set amount of hours for set number of days
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




# requests data for TICK from yahoo finance api
def main(TICK):
    # AVERAGE RANGES

    # daily in last 30 - 90 days
    days30, days60, days90 = get_data(TICK, '1d')

    d30 = avg_range_days(days30)
    d60 = avg_range_days(days60)
    d90 = avg_range_days(days90)

    
    # last hour in last 30 - 90 days
    # first hour in last 30 - 90 days
    hours30, hours60, hours90 = get_data(TICK, '1h')

    lh30 = avg_range_hours(hours30, "last")
    lh60 = avg_range_hours(hours60, "last")
    lh90 = avg_range_hours(hours90, "last")

    fh30 = avg_range_hours(hours30, "first")
    fh60 = avg_range_hours(hours60, "first")
    fh90 = avg_range_hours(hours90, "first")


    # print all results
    print("AVERAGE RANGES:\n")

    print("_30 days_")
    print("daily: ", d30)
    print("last hour: ", lh30)
    print("first hour: ", fh30)
    print("\n")

    print("_60 days_")
    print("daily: ", d60)
    print("last hour: ", lh60)
    print("first hour: ", fh60)
    print("\n")

    print("_90 days_")
    print("daily: ", d90)
    print("last hour: ", lh90)
    print("first hour: ", fh90)
    print("\n")


main('^GSPC')