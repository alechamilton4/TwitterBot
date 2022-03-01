from db import Session
from bot import TwitterBot
import time


def main() -> None:
    session = Session()
    bot = TwitterBot(session=session)
    while True:
        bot.search()
        for _ in range(10):
            bot.tweet()
        time.sleep(60*30) #Sleep for 30 minutes to avoid rate limit
if __name__ == "__main__":
    main()
    
    











