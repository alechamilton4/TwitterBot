from sqlalchemy import Column, DateTime, Integer, Boolean, desc
from db import Base, Session, engine


#session = Session()

class Tweet(Base):

    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True)
    replied_to = Column(Boolean)
    timestamp = Column(DateTime)

    def __init__(self,id,timestamp,replied_to):
        self.id = id
        self.replied_to = replied_to
        self.timestamp = timestamp

    @classmethod
    def get_all_tweeted(cls, session) -> list[int]:
        query = session.query(cls).filter(cls.replied_to==True).all()
        return [item.id for item in query]
    
    @classmethod
    def get_last(cls,session):
        query = session.queury(cls).filter(cls.replied_to==False).order_by(desc(cls.timestamp)).last()
        return query
    
    def tweet(self, session):
        self.replied_to = True
        #TODO actually tweet
        print(f"Tweeted {self.id}")
        session.commit()

#Base.metadata.create_all(engine)






