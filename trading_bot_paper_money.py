"""
This version of the program updates the selling price levels when prices rise and updates the buying price
levels when prices drop. This version only uses paper money or fake money.
"""
import cbpro, cryptocompare

config = open("trading_bot_paper_money_config.txt", "r").read().splitlines()

product_id = config[1]
gap = config[3]
initial_money = config[5]

