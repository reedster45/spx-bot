
import datetime
import time
import yfinance as yf



# returns converted timestamp in yyy-mm-dd format
# yyy-mm-mm HH:MM:SS-HH:MM
def timestampconverter(timestp):
    # timestp = int(time.mktime(date.timetuple()))
    # timestp = timestp.astype(datetime.datetime)
    return timestp.strftime('%Y-%m-%d %H:%M:%S-%H:%M')

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
def avg_range_hours(data):
    diff = []
    for i in data.index:
        if '15:30:00' in i:
            print(i)
        # diff.append(data['High'][i] - data['Low'][i])
    
    # return calculate_avg(diff)




# requests data for TICK from yahoo finance api
def main(TICK):
    # AVERAGE RANGES

    # daily in last 30 - 90 days
    days30, days60, days90 = get_data(TICK, '1d')

    print(days30) # TEMP

    d30 = avg_range_days(days30)
    d60 = avg_range_days(days60)
    d90 = avg_range_days(days90)

    
    # last hour in last 30 - 90 days
    # first hour in last 30 - 90 days
    hours30, hours60, hours90 = get_data(TICK, '1h')

    # avg_range_hours(hours30)
    # avg_range_hours(hours60)
    # avg_range_hours(hours90)



    # print all results
    print(d30)
    print(d60)
    print(d90)


main('^GSPC')