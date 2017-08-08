import krakenex
from time import time, sleep
import datetime
import logging

from OHLCData import OHLCData

class KrakenApi:
    def __init__(self, kraken = krakenex.API()):
        self.kraken = kraken

    def getLastCandle(self, pair, timeframe):
        while True:
            last = self.kraken.query_public('OHLC',{'pair': pair, 'interval': str(timeframe)})
            if "result" in str(last):
                last = last['result']['last']
                break
            logging.warning("The response do not contains the result field. Will retry in 30s.")
            sleep(30)
        
        candles = self.kraken.query_public('OHLC',{'pair': pair, 'interval': str(timeframe), 'since' : str(last - 1)})['result']["X" + pair[:3] + "Z" + pair[3:6]]

        lastCandle = False
        for candle in candles:
            if candle[0] == last:
                lastCandle = candle
                break

        if lastCandle == False:
            return OHLCData()

        return OHLCData(datetime.datetime.fromtimestamp(int(lastCandle[0])), float(lastCandle[1]), float(lastCandle[2]), float(lastCandle[3]), float(lastCandle[4]))

    def getCandlesSinceTime(self, pair, unixtime, timeframe):
        while True:
            exchangeCandles = self.kraken.query_public('OHLC',{'pair': pair, 'interval': str(timeframe), 'since' : str(unixtime)})
            if "result" in str(exchangeCandles):
                exchangeCandles = exchangeCandles['result']["X" + pair[:3] + "Z" + pair[3:6]]
                break
            logging.warning("The response do not contains the result field. Will retry in 30s.")
            sleep(30)
        candles = []

        for candle in exchangeCandles:
            candles.append(OHLCData(datetime.datetime.fromtimestamp(int(candle[0])), float(candle[1]), float(candle[2]), float(candle[3]), float(candle[4])))

        return candles

    #Return orderId
    def openLimitBuyOrder(self, pair, price, eurVolume):
        if self.getBalance(pair[-3:]) < eurVolume:
            logging.warning("Not enought " + pair[-3:] + " on balance to buy. Order not placed.")
            return 0
        
        btcAmount = eurVolume / price
        result = self.kraken.query_private('AddOrder', {'pair': str("X" + pair[:3] + "Z" + pair[3:6]),
                                               'type': 'buy',
                                               'ordertype': 'limit',
                                               'price': str(price),
                                               'volume': str(btcAmount)})
        return result['result']['txid'][0]

    #Return orderId
    def openMarketBuyOrder(self, pair, eurVolume):
        if self.getBalance(pair[-3:]) < eurVolume:
            logging.warning("Not enought " + pair[-3:] + " on balance to buy. Order not placed.")
            return 0
        
        bestAskPrice = self.getSecondBestBidPrice(pair)
        btcAmount = eurVolume / float(bestAskPrice)
        result = self.kraken.query_private('AddOrder', {'pair': str("X" + pair[:3] + "Z" + pair[3:6]),
                                               'type': 'buy',
                                               'ordertype': 'market',
                                               'volume': str(btcAmount)})
        return result['result']['txid'][0]

    def getOrderBook(self, pair, count = 10):
        while True:
            response = self.kraken.query_public('Depth', {'pair': str("X" + pair[:3] + "Z" + pair[3:6]), 'count': str(count)})
            if "result" in str(response):
                break
            logging.warning("The response do not contains the result field. Will retry in 30s.")
            sleep(30)
        return response['result']["X" + pair[:3] + "Z" + pair[3:6]]             

	#The second due to slippage
    def getSecondBestAskPrice(self, pair):
        return float(self.getOrderBook(pair)['asks'][1][0])

    def getSecondBestBidPrice(self, pair):
        return float(self.getOrderBook(pair)['bids'][1][0])

    def getBalance(self, currency):
        if currency == "EUR" or currency == "USD":
            currency = "Z" + currency
        else:
            currency = "X" + currency

        while True:
            response = self.kraken.query_private("Balance")
            if "result" in str(response):
                break
            logging.warning("The response do not contains the result field. Will retry in 30s.")
            sleep(30)
        
        return float(response['result'][currency])
