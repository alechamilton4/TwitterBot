import os

import dotenv
from sqlalchemy import true
from constants import TWEETS, ACCOUNTS, KEYWORDS
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
        data = self.client.search_recent_tweets(query=query)
        
        for tweet in data.data:
            if self.__determine_keyword_hit(tweet.text):
                self.__store_tweet(tweet.id)
                ids.append(tweet.id)
        
        return ids

    def __keyword_search(self, keyword: str, ids: list[int]) -> list:
        query = f"{keyword}"
        data = self.client.search_recent_tweets(query=query, tweet_fields=['public_metrics'],max_results=100)
        
        for tweet in data.data:
            if self.__analyze_metrics(tweet.public_metrics):
                self.__store_tweet(tweet.id)
                ids.append(tweet.id)
        
        return ids

    def __analyze_metrics(self, metrics: dict[str:any]) -> bool:
        total = metrics['retweet_count'] + metrics['reply_count'] + metrics['like_count'] + metrics['quote_count']

        if total > METRIC_COUNT:
            return True
        else:
            return False

    def __determine_keyword_hit(self, text: str) -> bool:
        for keyword in KEYWORDS:
            if keyword in text:
                return true
        return False

    def __store_tweet(self, id: int) -> None:

        if id not in Tweet.get_all_tweeted(self.session):
            tweet = Tweet(id=id, replied_to=False)
            self.session.add(tweet)
            self.session.commit()

    def search(self) -> list:

        ids = []

        for keyword in KEYWORDS:
            self.__keyword_search(keyword, ids)

        for account in ACCOUNTS:
            self.__big_account_search(account, ids)

        return ids
        
    
    def tweet(self) -> None:
        tweet: Tweet = Tweet.get_last(self.session)
        if tweet is not None:
            tweet.tweet()
        

    # def search_tweets(self, query):
    #     data = self.client.search_recent_tweets(query=query, tweet_fields=['public_metrics','author_id','lang'])
    #     return data.data

    # def get_tweet(self, id):
    #     data = self.client.get_tweet(id=id)
    #     return data.data

    # def get_user_tweets(self,username):
    #     user = self.client.get_user(username=username)
    #     data = self.client.get_users_tweets(user.data.id)
    #     return data.data

    






