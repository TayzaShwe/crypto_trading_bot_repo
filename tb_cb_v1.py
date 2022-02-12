"""
This version of the program updates the selling price levels when prices rise and updates the buying price
levels when prices drop. 
"""
import cbpro, time, pprint, signal, decimal, urllib.request, socket, datetime

#change the following two lines to wherever config_v1.txt and data_v1.txt is located
config = open("/home/tayzashwe/Documents/Stocks_and_Crypto/Trading_bot/Coinbase/tb_cb_v1/config_v1.txt", "r").read().splitlines()
data = open("/home/tayzashwe/Documents/Stocks_and_Crypto/Trading_bot/Coinbase/tb_cb_v1/data_v1.txt", "r").read().splitlines()

api_key = config[1]
api_secret = config[3]
passphrase = config[5]
product_id = config[7] #eg.BTC-USD
product = config[9] #eg.BTC
gap = float(config[11])
money_init = float(config[13])

is_first_order = data[1]
if (is_first_order == "False"):
    is_first_order = False
holding = data[3]
if (holding == "False"):
    holding = False
amount_holding = float(data[5])
total_value_sold = float(data[7])
buy_price = float(data[9])
sell_price = float(data[11])
current_total_value = float(data[13])
profit_loss = float(data[15])
percent_change = float(data[17])
money_leftover = float(data[19])
starting_money = 0
end_money = 0

TIME_START = time.clock_gettime(time.CLOCK_REALTIME)
TIME_TO_EXIT = time.clock_gettime(time.CLOCK_REALTIME) + 90000

class order_info:
    def __init__(self, filled_size, executed_value, fill_fees, id):
        self.filled_size = float(filled_size)
        self.executed_value = float(executed_value)
        self.fill_fees = float(fill_fees)
        self.id = id
    
    def update(self, filled_size, executed_value, fill_fees, id):
        self.filled_size = float(filled_size)
        self.executed_value = float(executed_value)
        self.fill_fees = float(fill_fees)
        self.id = id

buy_info = order_info(float(data[21]), float(data[23]), float(data[25]), data[27])
sell_info = order_info(float(data[29]), float(data[31]), float(data[33]), data[35])

pp = pprint.PrettyPrinter(indent=1)

auth_client = cbpro.AuthenticatedClient(api_key, api_secret, passphrase)

#checks the available amount of currency
def check_currency_available(currency):
    accounts = auth_client.get_accounts()
    for i in range(len(accounts)):
        if (accounts[i]['currency'] == currency):
            return float(accounts[i]['available'])
starting_money = check_currency_available("USDT")

#displays order or action information
def display_order_info(case, price):
    time = datetime.datetime.now()
    if (case == 'first_order'): 
        print("=================================")
        print(" FIRST MARKET BUY ORDER EXECUTED")
        print("---------------------------------")
        print(f"Current time: {time}")
        print(f"Current price: {price}")
        print(f"Amount bought: {buy_info.filled_size}")
        print(f"Total value bought: {buy_info.executed_value}")
        print(f"Sell price set at: {sell_price}")
        print(f"Curent total value: {current_total_value}")
        print(f"Money at the start: {starting_money}")
        print("=================================")
    elif (case == 'buy_price_updated'): #buy price updated 
        print("\n=================================")
        print("        BUY PRICE UPDATED")
        print("---------------------------------")
        print(f"Current time: {time}")
        print(f"Current price: {price}")
        print(f"New buy price: {buy_price}")
        print(f"Profit/Loss: {profit_loss}")
        print(f"Percent Change: {percent_change}%")
        print(f"Curent total value: {current_total_value}")
        print(f"Money at the start: {starting_money}")
        print("=================================")
    elif (case == 'sell_price_updated'): #sell price updated 
        print("\n=================================")
        print("       SELL PRICE UPDATED")
        print("---------------------------------")
        print(f"Current time: {time}")
        print(f"Current price: {price}")
        print(f"New sell price: {sell_price}")
        print(f"Profit/Loss: {profit_loss}")
        print(f"Percent Change: {percent_change}%")
        print(f"Curent total value: {current_total_value}")
        print(f"Money at the start: {starting_money}")
        print("=================================")
    elif (case == 'buy_price_reached_market_buy'): #buy price reached, market buy executed
        print("\n================================================")
        print(" BUY PRICE REACHED -> MARKET BUY ORDER EXECUTED")
        print("------------------------------------------------")
        print(f"Current time: {time}")
        print(f"Current price: {price}")
        print(f"Amount bought: {buy_info.filled_size}")
        print(f"Total value bought: {buy_info.executed_value}")
        print(f"Sell price set at: {sell_price}")
        print(f"Profit/Loss: {profit_loss}")
        print(f"Percent Change: {percent_change}%")
        print(f"Curent total value: {current_total_value}")
        print(f"Money at the start: {starting_money}")
        print("================================================")
    elif (case == 'sell_price_reached_market_sell'): #sell price reached, market sell executed
        print("\n==================================================")
        print(" SELL PRICE REACHED -> MARKET SELL ORDER EXECUTED")
        print("------------------------------------------------")
        print(f"Current time: {time}")
        print(f"Current price: {price}")
        print(f"Amount sold: {sell_info.filled_size}")
        print(f"Total value sold: {sell_info.executed_value}")
        print(f"Buy price set at: {buy_price}")
        print(f"Profit/Loss: {profit_loss}")
        print(f"Percent Change: {percent_change}%")
        print(f"Curent total value: {current_total_value}")
        print(f"Money at the start: {starting_money}")
        print("==================================================")
    elif (case == 'program_exit_market_sell'): #sell price reached, market sell executed
        print("\n==================================================")
        print("    PROGRAM ENDED -> MARKET SELL ORDER EXECUTED")
        print("------------------------------------------------")
        print(f"Current time: {time}")
        print(f"Current price: {price}")
        print(f"Amount sold: {sell_info.filled_size}")
        print(f"Total value sold: {sell_info.executed_value}")
        print(f"Profit/Loss: {profit_loss}")
        print(f"Percent Change: {percent_change}%")
        print(f"Curent total value: {current_total_value}")
        print(f"Money at the start: {starting_money}")
        print(f"Money at the end: {end_money}")
        print("==================================================")
    
#for the size, you can only enter up to a certain amount of decimal places.
# You need to wait until order_intial's status becomes done to check with get_order.                  
def market_order(side, size):
    global buy_info, sell_info
    order_initial = auth_client.place_market_order(product_id=product_id, side=side, size=size)
    order_final = auth_client.get_order(order_initial['id'])
    while True:
        try: 
            order_final = auth_client.get_order(order_initial['id'])
            if (order_final['status'] == 'done'):
                break
        except:
            time.sleep(0.5)
    #pp.pprint(order_final)
    if (side == 'buy'):
        buy_info.update(order_final['filled_size'], order_final['executed_value'], \
            order_final['fill_fees'], order_final['id'])
    else:
        sell_info.update(order_final['filled_size'], order_final['executed_value'], \
            order_final['fill_fees'], order_final['id'])

#function that stores final data into a file 
def store_final_data():
    data = ['[IS FIRST ORDER:]', str(is_first_order),
            '[HOLDING:]', str(holding),
            '[AMOUNT HOLDING:]', str(amount_holding),
            '[TOTAL VALUE SOLD:]', str(total_value_sold),
            '[BUY PRICE:]', str(buy_price),
            '[SELL PRICE:]', str(sell_price),
            '[CURRENT TOTAL VALUE:]', str(current_total_value),
            '[PROFIT/LOSS:]', str(profit_loss),
            '[PERCENT CHANGE:]', str(percent_change),
            '[LEFTOVER MONEY:]', str(money_leftover),
            '[BUY INFO FILLED SIZE:]', str(buy_info.filled_size),
            '[BUY INFO EXECUTED VALUE:]', str(buy_info.executed_value),
            '[BUY INFO FILLED FEES:]', str(buy_info.fill_fees),
            '[BUY INFO ID:]', str(buy_info.id),
            '[SELL INFO FILLED SIZE:]', str(sell_info.filled_size),
            '[SELL INFO EXECUTED VALUE:]', str(sell_info.executed_value),
            '[SELL INFO FILLED FEES:]', str(sell_info.fill_fees),
            '[SELL INFO ID:]', str(sell_info.id)]
    with open("/home/tayzashwe/Documents/Stocks_and_Crypto/Trading_bot/Coinbase/tb_cb_v1/data_v1.txt", "w") as f:
        for line in data:
            f.write(line)
            f.write('\n')

#function that handles Control+C input. Cancels all orders and prints conditions with the help of end().
def handler(signum, frame):
    ans = input('\b\bDo you want to place a market sell? This will reset data as well (y/n):\n' )
    while (ans not in 'yn'):
        ans = input('Please enter a valid input. (y/n)\n')
    if (ans=='y'):
        market_order('sell', check_currency_available(product))
        price = float(auth_client.get_product_ticker(product_id=product_id)['price'])
        update_info('program_exit_market_sell', price)
        display_order_info('program_exit_market_sell', price)
        with open("/home/tayzashwe/Documents/Stocks_and_Crypto/Trading_bot/Coinbase/tb_cb_v1/data_backup.txt") as f:
            with open("/home/tayzashwe/Documents/Stocks_and_Crypto/Trading_bot/Coinbase/tb_cb_v1/data_v1.txt", "w") as f1:
                for line in f:
                    f1.write(line)
    else:     
        store_final_data()
    print("You have ended the program")
    exit()
signal.signal(signal.SIGINT, handler)

#helper function to round up or down numbers to a specified number of decimal places
def round_ud(dir, i, place):
    dec = "0"*place
    if (dir == "down"):
        decimal.getcontext().rounding = decimal.ROUND_DOWN
        i = float(decimal.Decimal(i).quantize(decimal.Decimal(f"1.{dec}")))
        return i
    else:
        decimal.getcontext().rounding = decimal.ROUND_UP
        i = float(decimal.Decimal(i).quantize(decimal.Decimal(f"1.{dec}")))
        return i

#decides the size based on the amount of money entered
def decide_size(money, price):
    size = round_ud('down', money/price, 3)
    #print(f'size decided: {size}')
    return size

#updates terminal info 
def update_info(case, price):
    global is_first_order, buy_price, sell_price, holding, amount_holding, money_leftover,\
        total_value_sold, buy_info, sell_info, current_total_value, profit_loss, percent_change, starting_money, end_money
    if (case == 'first_order'):
        sell_price = price - gap 
        holding = True
        amount_holding = buy_info.filled_size
        money_leftover = money_init - buy_info.executed_value - buy_info.fill_fees
        current_total_value = money_leftover + buy_info.executed_value
        is_first_order = False
    elif (case == 'sell_price_reached_market_sell') or (case == 'program_exit_market_sell'):
        end_money = check_currency_available("USDT")
        buy_price = sell_price
        holding = False
        total_value_sold = sell_info.executed_value
        amount_holding = 0.0
        current_total_value = money_leftover + total_value_sold - sell_info.fill_fees
        money_leftover = 0.0
        profit_loss = current_total_value - money_init
        percent_change = round_ud('down', (profit_loss/money_init)*100, 2)
    elif (case == 'sell_price_updated'):
        sell_price = price - gap
        current_total_value = (sell_price*buy_info.filled_size) + money_leftover
        profit_loss = current_total_value - money_init
        percent_change = round_ud('down', (profit_loss/money_init)*100, 2)
    elif (case == 'buy_price_reached_market_buy'):
        sell_price = buy_price
        holding = True
        amount_holding = buy_info.filled_size
        money_leftover = current_total_value - buy_info.executed_value - buy_info.fill_fees
        current_total_value = money_leftover + buy_info.executed_value
        profit_loss = current_total_value - money_init
        percent_change = round_ud('down', (profit_loss/money_init)*100, 2)
    elif (case == 'buy_price_updated'):
        buy_price = price + gap

#decides what to do next based on price info
def decide_order(price):
    global is_first_order, buy_price, sell_price, holding, amount_holding, money_leftover,\
        total_value_sold, buy_info, sell_info, current_total_value, profit_loss, percent_change, starting_money
    if is_first_order:
        size = decide_size(money_init, price)
        market_order('buy', size)
        update_info('first_order', price)
        display_order_info('first_order', price)
    else:
        if (percent_change < -15.0):
            if (holding): 
                size = check_currency_available(product)
                while (size == 0.0):
                    time.sleep(1)
                    size = check_currency_available(product)
                market_order('sell', size)
                update_info('program_exit_market_sell', price)
                display_order_info('program_exit_market_sell', price)
            else:
                print("Loss percentage has exceeded limit")
            exit()
        if (holding):
            if (price < sell_price):
                size = check_currency_available(product)
                while (size == 0.0):
                    time.sleep(1)
                    size = check_currency_available(product)
                market_order('sell', size)
                update_info('sell_price_reached_market_sell', price)
                display_order_info('sell_price_reached_market_sell', price)
            elif (price - sell_price > gap):
                update_info('sell_price_updated', price)
                display_order_info('sell_price_updated', price)
            else:
                print(f"\rCurrent price: {price}", end='')
        elif (not holding):
            if (price > buy_price):
                size = decide_size(current_total_value, price)
                market_order('buy', size)
                update_info('buy_price_reached_market_buy', price)
                display_order_info('buy_price_reached_market_buy', price)
            elif (buy_price - price > gap):
                update_info('buy_price_updated', price)
                display_order_info('buy_price_updated', price)
            else:
                print(f"\rCurrent price: {price}", end='')
    
#checks internet connection. Returns -1 if bad connection
def check_connection(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
    except:
        return -1

while True:
    #checks for a good internet connection by attemting to conenct to google.com
    while (check_connection() == -1):
        print("Bad internet connection. Waiting for a good conneciton.")
        time.sleep(5)
    current_time = time.clock_gettime(time.CLOCK_REALTIME)
    #exits program if it has been running for 25 hours
    """
    if (current_time >= TIME_TO_EXIT):
        store_final_data()
        print("25 hours have passed since the start of running this program. Program has been exited.")
        exit()
    """
    #tries to connect to the api. If it throws an exception, waits for a few seconds 
    try:
        price = float(auth_client.get_product_ticker(product_id=product_id)['price'])
        #print (f"current price is: {price}", flush=True)
        decide_order(price)
        store_final_data() #stores data every minute in case pc shuts down or program ends abruptly 
        time.sleep(60)
    except socket.error as socket_error:
        #prints the error in detail
        print(f"Error: {socket_error}.")
        print("Couldn't connect to the socket api. Retrying.")
        time.sleep(5)
