from sqlalchemy import Column, DateTime, Integer, Boolean, asc
from db import Base, Session, engine
from constants import TWEETS
import random


session = Session()

class Tweet(Base):

    __tablename__ = "tweets"


    id = Column(Integer, primary_key=True, autoincrement=True)
    tweet_id = Column(Integer)
    replied_to = Column(Boolean)
    timestamp = Column(DateTime)

    def __init__(self,tweet_id,timestamp,replied_to):
        self.tweet_id = tweet_id
        self.replied_to = replied_to
        self.timestamp = timestamp

    @classmethod
    def get_all(cls, session) -> list[int]:
        query = session.query(cls).all()
        return [item.tweet_id for item in query]
    
    @classmethod
    def get_first(cls,session):
        query = session.query(cls).filter(cls.replied_to==False).order_by(asc(cls.timestamp)).first()
        return query
    
    @classmethod
    def check_if_tweeted(cls,session,tweet_id) -> bool:
        query = session.query(cls).filter(cls.tweet_id==tweet_id).first()
        if query.replied_to:
            return True
        else:
            return False

    def tweet(self, session, client):
        tweet = random.choice(TWEETS)
        response = client.create_tweet(text=tweet,in_reply_to_tweet_id=self.tweet_id)

        if response.status == 200:
            self.replied_to = True
            session.commit()
            print("Tweeted")

Base.metadata.create_all(engine)






