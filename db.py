import os

from sqlalchemy import create_engine, Column, Integer, Text, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)
session = Session()


class Question(Base):
    """Класс нашей модели"""
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    question_text = Column(Text)
    question_answer = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


Base.metadata.create_all(engine)


def add_data_to_db(answer: str, question: str):
    """
    Функция для создания новой записи в бд
    :param answer: вопрос
    :param question: ответ
    """
    new_question = Question(
        question_text=question,
        question_answer=answer
    )
    session.add(new_question)
    session.commit()
    session.close()


def check_question(question_text: str):
    """
    Функция для проверки уникальности ответа.
    :param question_text: ответ с апи
    """
    existing_question = session.query(Question).filter(Question.question_text == question_text).first()
    if not existing_question:
        return True
    else:
        return False


def db_have_data():
    """
    Функция для проверки наполненности бд, если есть данные вернет последний объект
    """
    try:
        save_questions = session.query(Question).order_by(Question.id.desc()).offset(1).first()
        return save_questions.question_text
    except Exception as e:
        return e
