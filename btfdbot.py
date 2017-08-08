#!/usr/bin/env python3

import sys

if sys.version_info < (3, 0):
    print("Python3 required.")
    exit()

import krakenex
from time import time, sleep
import logging

from KrakenApi import KrakenApi
from Utils import notify, loadConfig


logging.basicConfig(filename = "log.log", format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S', level = logging.DEBUG)

config = loadConfig("config.ini")

if config["debugOnConsole"]:
    stderrLogger=logging.StreamHandler()
    stderrLogger.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logging.getLogger().addHandler(stderrLogger)

exchange = krakenex.API()
exchange.load_key(config["apiFileName"])

api = KrakenApi(exchange)
dailyTimeframe = 1440
fourHourTimeframe = 240

logging.info(config["botName"] + " started up!")
if config["notifications"]:
    notify(config["botName"], config["botId"], config["chatId"], "Started up!")

lastCandles = api.getCandlesSinceTime(config["pair"], time() - 86400 * (config["days"] + 1), dailyTimeframe)[:-1]
lastDailyCandle = api.getLastCandle(config["pair"], dailyTimeframe)
lastFourHourCandle = api.getLastCandle(config["pair"], fourHourTimeframe)
boughtToday = False
highs = []

for i in range(0, config["days"]):
    highs.append(lastCandles[i].high)#High

logging.info("Let's start polling!")       

while(True):
    try:
        fourHourCandle = api.getLastCandle(config["pair"], fourHourTimeframe)
        dailyCandle = api.getLastCandle(config["pair"], dailyTimeframe)
        
        if lastFourHourCandle.date != fourHourCandle.date:
            logging.debug("New 4h candle detected!")
            percHigherLower = (fourHourCandle.close - max(highs)) / max(highs) * 100
            logging.info("Dip of " + str(percHigherLower) + "% detected!")
            
            if percHigherLower < config["dipAmount"] and boughtToday == False:
                if config["notifications"]:
                    notify(config["botName"], config["botId"], config["chatId"], "Dip of " + str(percHigherLower) + "% detected!")
                balanceAmount = api.getBalance(config["pair"][-3:])
                amountToBuy = float(config["amountToBuy"]) / 100 * balanceAmount
                orderId = api.openMarketBuyOrder(config["pair"], amountToBuy)
                if orderId != 0:
                    logging.info("MarketOrder correctly placed.")
                    if config["notifications"]:
                        notify(config["botName"], config["botId"], config["chatId"], "MarketOrder correctly placed.")
                boughtToday = True
            lastFourHourCandle = fourHourCandle

        if lastDailyCandle.date != dailyCandle.date:
            logging.debug("New daily candle detected!")
            for i in range(0, config["days"] - 1):
                highs[i] = highs[i + 1]
            highs[config["days"] - 1] = dailyCandle.high
            
            lastDailyCandle = dailyCandle
            boughtToday = False

        logging.debug("Going to sleep for a while.")
        sleep(config["pollingDelay"] * 60)#pollingDelay is in minutes but sleep(arg) want seconds then multiply for 60
        logging.debug("Waked up!")
    except Exception as exc:
        logging.critical("Exception " + str(exc.__class__.__name__) + " : " + str(exc))
        if config["notifications"]:
            notify(config["botName"], config["botId"], config["chatId"], "Exception " + str(exc.__class__.__name__) + " : " + str(exc))


