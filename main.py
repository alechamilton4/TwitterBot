from db import Session
from bot import TwitterBot
import time


def main(sleep_seconds: int):
    session = Session()
    bot = TwitterBot(session=session)
    while True:
        bot.search()
        time.sleep(sleep_seconds*5)
        for i in range(10):
            bot.tweet()
            time.sleep(sleep_seconds)

if __name__ == "__main__":
    main(2)













