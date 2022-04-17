"""
This version of the program updates the selling price levels when prices rise and updates the buying price
levels when prices drop. This version only uses paper money or fake money.
"""
import cryptocompare, datetime
import matplotlib as plt

config = open("trading_bot_paper_money_config.txt", "r").read().splitlines()

asset = config[1].split("-")[0]
currency = config[1].split("-")[1]
gap = float(config[3])
initial_currency_amt = float(config[5])
current_currency_amt = float(config[5])
current_asset_amt = 0.0
current_asset_value = 0.0
total_asset_value = float(config[5])
mo_loss_perc = float(config[13][:-1])
first_order = True
buy_price = 0.0
sell_price = 0.0
bought = False
sold = False

date_from = config[7].split(",")
date_from = datetime.date(int(date_from[2]), int(date_from[1]), int(date_from[0]))
date_to = config[9].split(",")
date_to = datetime.date(int(date_to[2]), int(date_to[1]), int(date_to[0]))
time_range = config[11]


def get_hist_price(asset, currency, date_from, date_to, time_range):
    dif = date_to - date_from
    print(dif.days)
    if dif.days < 1:
        print("Invalid date input")
        exit()
    if dif.days > 2000:
        print("Exceeds 2000 days/hours/minutes")
        exit()
    if time_range.lower() == "day":
        price_data = cryptocompare.get_historical_price_day(asset, currency, limit=dif.days, exchange='CCCAGG', \
            toTs=date_from)
        price_list = [x["close"] for x in price_data]
        return price_list
    elif time_range.lower() == "hour":
        price_data = cryptocompare.get_historical_price_hour(asset, currency, limit=dif.days, exchange='CCCAGG', \
            toTs=date_from)
        price_list = [x["close"] for x in price_data]
        return price_list
    elif time_range.lower() == "minute":
        price_data = cryptocompare.get_historical_price_minute(asset, currency, limit=dif.days, exchange='CCCAGG', \
            toTs=date_from)
        price_list = [x["close"] for x in price_data]
        return price_list
    else:
        print("Invalid time range input")
        exit()

def market_order(side, current_price):
    global current_currency_amt, current_asset_amt, current_asset_value, total_asset_value

    if side == "buy":
        current_currency_amt = current_currency_amt*(1-mo_loss_perc)
        current_asset_amt = current_currency_amt/current_price
        current_currency_amt = 0
        current_asset_value = current_asset_amt*current_price
        total_asset_value = current_currency_amt+current_asset_value
    elif side == "sell":
        current_asset_amt = current_asset_amt*(1-mo_loss_perc)
        current_currency_amt = current_asset_amt*current_price
        current_asset_amt = 0
        current_asset_value = 0
        total_asset_value = current_currency_amt+current_asset_value

def main_program(price_list):
    global first_order, sell_price, buy_price, current_currency_amt,\
        current_asset_amt, current_asset_value, total_asset_value,\
        bought, sold

    
    for price in price_list:
        if first_order:
            market_order("buy", price)
            first_order = False
            sell_price = price - gap
            bought = True
        else:
            if bought:
                if price <= sell_price:
                    market_order("sell", price)
                    sell_price = 0
                    buy_price = price
                    bought = False
                    sold = True
                elif (price - sell_price) > gap:
                    sell_price = price - gap
                    current_asset_value = price*current_asset_amt
                    total_asset_value = current_currency_amt+current_asset_value
            elif sold:
                if price >= buy_price:
                    market_order("buy", price)
                    buy_price = 0
                    sell_price = price
                    bought = True
                    sold = False
                elif (buy_price - price) > gap:
                    buy_price = price + gap
        print("debug", buy_price, sell_price, total_asset_value)
    
    return total_asset_value - initial_currency_amt


price_list = get_hist_price(asset, currency, date_from, date_to, time_range)
plt.plot(price_list)
plt.show()
#price_list = [10000, 9000, 8000, 7000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 15000]
alt_total_asset_value = ((initial_currency_amt/price_list[0])*price_list[-1]) - initial_currency_amt
print(price_list[0], price_list[-1])
print("main", main_program(price_list), alt_total_asset_value)





