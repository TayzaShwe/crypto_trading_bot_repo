# CRYPTOCURRENCY TRADING BOT #

This is the official repository for my cryptocurrency trading bot. 

I have created three versions of this trading bot: 
1) Trading bot that uses your real money to trade cryptocurrencies in Coinbase Pro(__tb_cb_v1.py__)
2) Trading bot that uses paper money or fake money to simulate the actual trading bot (__trading_bot_paper_money.py__)
3) Web version of paper money trading bot (https://tayzashwe.github.io/crypto_trading_bot_repo/)

### Table of Contents ###
1) Why I developed this trading bot
2) How my trading bot works
3) Results
4) How to use the first version of bot (uses actual money)
5) How to use the second version of bot (uses fake money)
6) Technologies involved 

## WHY I DEVELOPED THIS TRADING BOT ##

When I started off trading cryptocurrencies as a beginner, I noticed that I missed out on important price movements when I was away from the trading screen, especially while I was asleep. To combat this, I developed this trading bot to imitate my behvavior as if I were looking at the trading screen at all times. 

## HOW MY TRADING BOT WORKS ##

My trading bot's algorithm is simple. It first sends a __market buy order__ and sets a __sell price__ below the price at which the cryptocurrency was bought. The __sell price__ is determined by the __gap__ which is a predetermined input by the user. If the cryptocurrency's price rises and the difference between the price and the __sell price__ is more than the __gap__, the __sell price__ will be updated to a higher price. If the cryptocurrency's price drops, the __sell price__ doesn't move. If the __sell price__ is hit, a __market sell order__ is sent and a __buy price__ is set to the former __sell price__. If cryptocurrency's price drops, the __buy price__ will maintain a difference of the __gap__ similar to how the __sell price__ changes. If the price moves up again, the __buy price__ doesn't move. If the __buy price__ is hit, a __market buy order__ is sent and the sell price is set to the __buy price__. The bot, in essence, is supposed to try to __"buy low, sell high."__

Link to demonstration video: https://youtu.be/QSSdd1R9y-4

## RESULTS ##

To assess whether this bot is effective, I compared it to the profit gained from just buying a certain amount of cryptocurrency at one point in time, without using the bot. You can think of this strategy as just simply buying and holding. 

The trading bot __outperforms__ the mentioned strategy __sometimes__ and __underperforms__ sometimes. The trading bot __excels__ at specific price movement patterns. The trading bot does well in markets with __large swings__ but does poorly in __sideways markets__ (markets where the price moves very little between a certain range). This is because the __sell price__ and __buy price__ gets constantly hit and because __market orders__ buy or sell below the optimal price (it prioritizes the filling of an order over the best price), you lose a bit of the total value everytime a __market order__ is sent. In a __sideways market__, the __buy price__ and __sell price__ get constantly hit which slowly causes you to lose money. The performance of the bot also depends on the input of the __gap__. 

Having said the above, after numerous trials, the trading bot seems to __outperform__ the general buying and holding strategy __more often__ than it __underperforms__. The biggest __indicator of success__ is how much value is lost with the __market orders__. 

## HOW TO USE THE FIRST VERSION OF BOT (USES ACTUAL MONEY) ##

For the first version that uses actual money, you can enter your information in __config_v1.txt__. This only works with Coinbase Pro. Be advised that this information is sensitive. The information includes your API key, API secret key, passphrase, product id, the gap, and the amount of money to use. 

Run __tb_cb_v1.py__. Updates on orders and your total value will appear whenever a __market order__ is sent. To end the program, press __CTRL+C__. A prompt will appear asking if you want to send a __market sell order__ before exiting or not. Enter what you want to do and the program will end. After the program ends, the information of the session is stored in __data_v1.txt__. The program will use this data when you run the program again to continue with the same conditions as when the program last ended. Make sure to copy __data_backup.txt__'s content into __data_v1.txt__ before running the program if you want to start new. 

## HOW TO USE THE SECOND VERSION OF BOT (USES PAPER MONEY) ##

For the second version that uses paper money (fake money), you have more control over how you want to simulate actual trading. In __trading_bot_paper_money_config.txt__, you can enter the cryptocurrency to trade, the __gap__, the amount of money to use, the start and end dates, the time range (days, hours, minutes), and the percentage of loss incurred from sending __market orders__. After inputting this information, run __trading_bot_paper_money.py__. 

The net profit gained from using the bot and the net profit gained from the normal strategy will be displayed along with a matlibplot plot of the results. 
* Yellow line - cryptocurrency price
* Orange line - total value of money and the cryptocurrency from using the trading bot
* Pink line -  total value of money and the cryptocurrency without using the trading bot
* Blue line - the buy/sell price levels
* Red dot - the sell price
* Green dot - the buy price

A simple rule to remember is that the trading bot has outperformed the normal strategy if the orange line ends at a higher price than the pink line. 

## TECHNOLOGIES INVOLVED ##

* Python (for the both versions)
* Matplotlib (for the second version)
* Coinbase Pro API (for the first version) (link: https://github.com/danpaquin/coinbasepro-python) 
* Cryptocompare API (for the second version) (link: https://github.com/lagerfeuer/cryptocompare)

