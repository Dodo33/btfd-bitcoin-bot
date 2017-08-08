<h1 align="center">BTFDBot</h1>
Bitcoin is in bull run since the summer of 2015, let's automate the "buy the dip" process! <br />

As we see in the [BTCUSD](https://www.bitcoinwisdom.com/markets/bitstamp/btcusd) chart when bitcoin have a correction it lose about 30% in a handful of days. Why don't buy & hold in these occasion?


### Getting started
For the moment it works just for [kraken](https://www.kraken.com) but the support for [bitstamp](https://www.bitstamp.net) will be implemented soon.


### Prerequisites
The bot requires just a module: [krakenex](www.github.com/veox/python3-krakenex) <br />
Krakenex installation guide [here](www.github.com/veox/python3-krakenex/blob/master/README.rst) <br />
Python3 is required.


### Running 
Change the settings in the `config.ini` as you prefer and past your private and secret keys into the `kraken.key` file. Remember: don't allow withdrawal permission while you create the key. <br />
Now you can run:

`python3 btfdbot.py`


### Notifications
To have telegram notifications you need to get a bot id from the BotFather. Once you have a bot id you need to get your Chat ID or create a channel and invite the bot so it can chat there. Once you have all this in place you configure it in `config.ini`. <br />
- `botId` : Check [BotFather](https://www.telegram.me/BotFather).
- `chatId` : A simple tool to get it is [here](https://github.com/Dodo33/telegram-chatid-dumper).


### Api documentation
A full documentation of the api [here](https://www.kraken.com/help/api)
