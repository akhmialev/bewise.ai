import time

import uvicorn
from fastapi import FastAPI
import requests

from db import add_data_to_db, db_have_data, check_question

app = FastAPI()


def add_data(num: int):
    """
    Функция, которая делает запросы к апи до тех пор, пока в бд не будут все запросы уникальны.
    :param num: количество вопросов
    """
    questions_added = 0
    while questions_added < num:
        url = f"https://jservice.io/api/random?count=1"
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            answer = response[0]['answer']
            question = response[0]['question']

            if check_question(question):
                add_data_to_db(answer, question)
                questions_added += 1
                print('added')
            else:
                print(f"Вопрос '{question}' уже существует. Генерация нового вопроса...")
        else:
            time.sleep(3)
            continue


@app.post('/api/v1/number')
def get_number(num: int):
    """Апи для получения вопроса, если база данных пустая вернет пустой объект.<p>
     Введите число от 1 до 100
    """
    if db_have_data():
        add_data(num)
        return {'question': db_have_data()}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')
