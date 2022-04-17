"""
This version of the program updates the selling price levels when prices rise and updates the buying price
levels when prices drop. This version only uses paper money or fake money.
"""
import cbpro, cryptocompare, datetime

config = open("trading_bot_paper_money_config.txt", "r").read().splitlines()

asset = config[1].split("-")[0]
currency = config[1].split("-")[1]
gap = config[3]
initial_currency = config[5]
current_currency = config[5]
current_asset_amt = 0
current_asset_value = 0
total_asset_value = config[5]

date_from = config[7].split("/")
date_to = config[9].split("/")
time_range = config[11]


def get_hist_price(asset, currency, date_from, date_to, time_range):
    date_from_days = (int(date_from[2])*365) + (int(date_from[1])*12) + int(date_from[0])
    date_to_days = (int(date_to[2])*365) + (int(date_to[1])*12) + int(date_to[0])
    if date_to_days <= date_from_days:
        print("Invalid date inputs")
        exit()
    days = date_to_days - date_from_days
    print(days)
    if days > 2000:
        print("Exceeds 2000 days/hours/minutes")
        exit()
    if time_range.lower() == "day":
        price_data = cryptocompare.get_historical_price_day(asset, currency, limit=days, exchange='CCCAGG', \
            toTs=datetime.datetime(int(date_from[2]), int(date_from[1]), int(date_from[0])))
        price_list = [x["close"] for x in price_data]
        return price_list
    elif time_range.lower() == "hour":
        price_data = cryptocompare.get_historical_price_hour(asset, currency, limit=days, exchange='CCCAGG', \
            toTs=datetime.datetime(int(date_from[2]), int(date_from[1]), int(date_from[0])))
        price_list = [x["close"] for x in price_data]
        return price_list
    elif time_range.lower() == "minute":
        price_data = cryptocompare.get_historical_price_minute(asset, currency, limit=days, exchange='CCCAGG', \
            toTs=datetime.datetime(int(date_from[2]), int(date_from[1]), int(date_from[0])))
        price_list = [x["close"] for x in price_data]
        return price_list
    else:
        print("Invalid time range input")
        exit()

print(get_hist_price(asset, currency, date_from, date_to, time_range))