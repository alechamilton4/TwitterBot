import os
import dotenv
from sqlalchemy import false, true
from constants import TWEETS, ACCOUNTS, KEYWORDS
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
import tweepy 
from models import Tweet

METRIC_COUNT = 1000

class TwitterBot:

    def __init__(self, session):
        self.client= self.__tweepy_init()
        self.session = session

    def __tweepy_init(self):
        dotenv_path = Path('.env')
        load_dotenv(dotenv_path=dotenv_path)
        return tweepy.Client(os.getenv("BEARER"))
    

    def __big_account_search(self, account: str, ids: list[int]) -> list[int]:
        query = f"from: {account} -is:retweet -is:reply"
        data = self.client.search_recent_tweets(query=query, tweet_fields=['created_at'])
        
        for tweet in data.data:
            if self.__determine_keyword_hit(tweet.text):
                stored = self.__store_tweet(tweet.id, tweet.created_at)
                if stored:
                    ids.append(tweet.id)
    
        return ids

    def __keyword_search(self, keyword: str, ids: list[int]) -> list:
        query = f"{keyword} is:verified"

        utc = datetime.utcnow()
        end = utc - timedelta(minutes=15)

        data = self.client.search_recent_tweets(query=query, end_time=end, tweet_fields=['public_metrics','created_at'],max_results=100)
        
        for tweet in data.data:
            if self.__analyze_metrics(tweet.public_metrics):
                stored = self.__store_tweet(tweet.id, tweet.created_at)
                if stored:
                    ids.append(tweet.id)
        
        return ids

    def __analyze_metrics(self, metrics: dict[str:any]) -> bool:
        retc = metrics['retweet_count']
        repc = metrics['reply_count']
        lc = metrics['like_count']
        qc = metrics['quote_count']

        if retc+repc+lc+qc > METRIC_COUNT and retc != 0 and repc != 0 and lc != 0 and qc != 0:
            return True
        else:
            return False

    def __determine_keyword_hit(self, text: str) -> bool:
        for keyword in KEYWORDS:
            if keyword in text:
                return true
        return False

    def __store_tweet(self, tweet_id: int, timestamp) -> None:

        if tweet_id not in Tweet.get_all(self.session):
            tweet = Tweet(tweet_id=tweet_id,timestamp=timestamp,replied_to=False)
            self.session.add(tweet)
            self.session.commit()
            return True
        return False

    def search(self) -> list:

        ids = []

        for keyword in KEYWORDS:
            self.__keyword_search(keyword, ids)

        for account in ACCOUNTS:
            self.__big_account_search(account, ids)

        print(f"Created {len(ids)} tweets")
        print(ids)

        return ids
        
    
    def tweet(self) -> None:
        tweet: Tweet = Tweet.get_first(self.session)
        if tweet is not None:
            tweet.tweet(self.session, self.client)

    
    def get_tweet(self, id):
        data = self.client.get_tweet(id)
        print(data.data)

