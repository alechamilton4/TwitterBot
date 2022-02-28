from db import Session
from bot import TwitterBot
import time




def main():
    session = Session()
    bot = TwitterBot()
    while True:
        bot.search()













