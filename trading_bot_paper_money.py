"""
This version of the program updates the selling price levels when prices rise and updates the buying price
levels when prices drop. This version only uses paper money or fake money.
"""
import cryptocompare, datetime
import matplotlib.pyplot as plt

config = open("trading_bot_paper_money_config.txt", "r").read().splitlines()

asset = config[1].split("-")[0]
currency = config[1].split("-")[1]
gap = float(config[3])
initial_currency_amt = float(config[5])
current_currency_amt = float(config[5])
initial_asset_amt = 0.0
current_asset_amt = 0.0
current_asset_value = 0.0
total_asset_value = float(config[5])
mo_loss_perc = float(config[13])
first_order = True
buy_price = 0.0
sell_price = 0.0
bought = False
sold = False

date_from = config[7].split("/")
date_from = datetime.date(int(date_from[2]), int(date_from[1]), int(date_from[0]))
date_to = config[9].split("/")
date_to = datetime.date(int(date_to[2]), int(date_to[1]), int(date_to[0]))
time_range = config[11]

# helper function for market orders
def get_hist_price(asset, currency, date_from, date_to, time_range):
    dif = date_to - date_from
    if dif.days < 1:
        print("Invalid date input")
        exit()
    if dif.days > 2000:
        print("Exceeds 2000 days/hours/minutes")
        exit()
    if time_range.lower() == "day":
        price_data = cryptocompare.get_historical_price_day(asset, currency, limit=dif.days, exchange='CCCAGG', \
            toTs=date_to)
        price_list = [x["close"] for x in price_data]
        return price_list
    elif time_range.lower() == "hour":
        price_data = cryptocompare.get_historical_price_hour(asset, currency, limit=dif.days, exchange='CCCAGG', \
            toTs=date_to)
        price_list = [x["close"] for x in price_data]
        return price_list
    elif time_range.lower() == "minute":
        price_data = cryptocompare.get_historical_price_minute(asset, currency, limit=dif.days, exchange='CCCAGG', \
            toTs=date_to)
        price_list = [x["close"] for x in price_data]
        return price_list
    else:
        print("Invalid time range input")
        exit()

# helper function for market orders
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

# takes in a list of prices and returns the profit using the trading bot
def main_program(price_list):
    global first_order, sell_price, buy_price, current_currency_amt,\
        current_asset_amt, current_asset_value, total_asset_value,\
        bought, sold, initial_asset_amt

    a_t_l = [] 
    t_l = []
    sell_prices = []
    buy_prices = []
    b_s_price = []
    
    for price in price_list:
        if first_order:
            market_order("buy", price)
            initial_asset_amt = current_asset_amt
            first_order = False
            sell_price = price - gap
            bought = True
        else:
            if bought:
                current_asset_value = price*current_asset_amt
                total_asset_value = current_currency_amt+current_asset_value
                if price <= sell_price:
                    market_order("sell", price)
                    buy_price = sell_price
                    sell_price = 0
                    bought = False
                    sold = True
                elif (price - sell_price) > gap:
                    sell_price = price - gap
            elif sold:
                if price >= buy_price:
                    market_order("buy", price)
                    sell_price = buy_price
                    buy_price = 0
                    bought = True
                    sold = False
                elif (buy_price - price) > gap:
                    buy_price = price + gap
        a_t_l.append(initial_asset_amt*price)
        t_l.append(total_asset_value)
        sell_prices.append(sell_price)
        buy_prices.append(buy_price)
        if sell_price == 0:
            b_s_price.append(buy_price)
        else:
            b_s_price.append(sell_price)
        
        #print("debug", price, buy_price, sell_price, total_asset_value)
    plt.plot(t_l, color='orange')
    plt.plot(a_t_l, color='pink')
    plt.scatter(x=list(range(len(price_list))), y=sell_prices, color='red')
    plt.scatter(x=list(range(len(price_list))), y=buy_prices, color='green')
    plt.plot(b_s_price, color='blue')
    return total_asset_value-initial_currency_amt



# ------------- MAIN PROGRAM ------------- #

price_list = get_hist_price(asset, currency, date_from, date_to, time_range) # list of asset prices
#price_list = [10000, 9000, 8000, 7000, 6000, 7000, 8000, 9000, 10000, \
# 11000, 12000, 15000, 16000, 17000, 22000, 20000, 18000, 16000, 14000, 17000] # simple test 
alt_total_asset_value = ((initial_currency_amt/price_list[0])*price_list[-1]) - initial_currency_amt # this is the net profit without the program
print(f"Net profit using trading bot: {main_program(price_list)}\nNet profit without using trading bot: {alt_total_asset_value}")
plt.plot(price_list, color='yellow')
plt.xlabel(f"{time_range.lower()}s")
plt.ylabel("Value in the chosen currency")
plt.show()





