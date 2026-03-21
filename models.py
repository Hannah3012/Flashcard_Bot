from sqlalchemy import Column , Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Flashcards(Base):
    __tablename__ = "Flashcards"
    id = Column(Integer , primary_key=True)
    user_id = Column(Integer)
    question = Column(String)
    answer = Column(String)

engine = create_engine('sqlite://flashcards.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

