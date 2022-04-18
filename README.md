# crypto_trading_bot_repo

This is the official repository for my cryptocurrency trading bot. 

I have created two versions of this trading bot: 
1) Trading bot that uses your real money to trade cryptocurrencies in Coinbase (__tb_cb_v1.py__)
2) Trading bot that uses paper money or fake money to simulate the actual trading bot (__trading_bot_paper_money.py__)

# HOW MY TRADING BOT WORKS

My trading bot's algorithm is simple. It first sends a market buy order and sets a sell price below the price at which the cryptocurrency was bought. The sell price is determined by the __gap__ which is a predetermined input by the user. If the cryptocurrency's price rises and the difference between the price and the sell price is more than the __gap__, the sell price will be updated to a higher price. If the cryptocurrency's price drops, the sell price doesn't move. If the sell price is hit, a market sell order is sent

For the first version that uses actual money, you can enter your information in __config_v1.txt__. Be advised that this information is sensitive. The information includes your API key, API secret key, passphrase, product id, the gap, and the amount of money to use. 