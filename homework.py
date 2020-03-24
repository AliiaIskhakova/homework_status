import os
import requests
import time

import telegram

from dotenv import load_dotenv

load_dotenv()

PRAKTIKUM_TOKEN = os.getenv("PRAKTIKUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
params = {'from_date': 0}

proxy = telegram.utils.request.Request(proxy_url='https://62.201.238.250:8080') 
bot = telegram.Bot(token=TELEGRAM_TOKEN, request=proxy)


def parse_homework_status(homework):
    url = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
    response = requests.get(url=url, headers=headers, params=params).json().get('homeworks')
    homework_name = response[0]['homework_name']

    if response[0]['status'] == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    url = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
    homework_statuses = requests.get(url=url, headers=headers, params=params).json()
    return homework_statuses


def send_message(message, bot):
    return bot.send_message(chat_id=CHAT_ID, text=message)
    

def main():
    current_timestamp = int(time.time())  # начальное значение timestamp

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework:
                send_message(parse_homework_status(new_homework.get('homeworks')), bot)
            current_timestamp = new_homework.get('current_date')  # обновить timestamp
            time.sleep(300)  # опрашивать раз в пять минут

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(10)

        except KeyboardInterrupt:
            print('Бот остановлен.')
            break

if __name__ == '__main__':
    main()
