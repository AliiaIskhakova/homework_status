import os
import requests
import telegram
import time
from dotenv import load_dotenv

load_dotenv()


PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

proxy = telegram.utils.request.Request(proxy_url='https://81.174.11.227:34167') 
url = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
params = {'from_date':current_timestamp}


def parse_homework_status(homework):
    response = requests.get(url=url, headers=headers, params=params).json().response.get('homeworks')[0]
    homework_name = response['homework_name']

    if response['status'] == 'approved':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    response = requests.get(url=url, headers=headers, params=params).json()
    homework_statuses = response.get('homeworks')[0]['status']
    return homework_statuses


def send_message(message):
    bot = telegram.Bot(token=TELEGRAM_TOKEN, request=proxy)
    return bot.send_message(chat_id=CHAT_ID, text='Я бот!')
    
def main():
    current_timestamp = int(time.time())  # начальное значение timestamp

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(new_homework.get('homeworks')[0]))
            current_timestamp = new_homework.get('current_date')  # обновить timestamp
            time.sleep(300)  # опрашивать раз в пять минут

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()
