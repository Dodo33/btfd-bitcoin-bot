from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from configparser import SafeConfigParser
import logging


def notify(botName, botId, chatId, msg):
    postData = {"chat_id": chatId, "text": str(botName) + ": " + msg}
    url = "https://api.telegram.org/bot" + botId + "/sendMessage"
    try:
        response = urlopen(url, urlencode(postData).encode("utf-8"))
    except HTTPError as e:
        logging.error("Your telegram bot id is probably configured incorrectly.")


def loadConfig(fileName = "config.ini"):
    config = SafeConfigParser()
    config.read(fileName)
    info = {}
    
    try:
        info["botName"] = config.get('main', "botName")
        info["apiFileName"] = config.get('main', "apiFileName")
        info["pair"] = config.get('main', 'pair')
        info["days"] = config.getint('main', 'days')
        info["dipAmount"] = config.getfloat('main', 'dipAmount')
        info["amountToBuy"] = config.getfloat('main', 'amountToBuy')
        info["pollingDelay"] = config.getint('main', 'pollingDelay')
        info["debugOnConsole"] = config.getboolean('main', 'debugOnConsole')
        info["notifications"] = config.getboolean('notifications', 'notifications')
        if info["notifications"]:
            info["botId"] = config.get('notifications', 'botId')
            info["chatId"] = config.get('notifications', 'chatId')
    except Exception as exc:
        logging.critical("Exception " + str(exc.__class__.__name__) + " : " + str(exc))

    return info
