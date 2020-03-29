# импорты стандартных библиотек
import os
import time

# импорты сторонних библиотек
import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

PRAKTIKUM_TOKEN = os.getenv("PRAKTIKUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
params = {'from_date': 0}


def parse_homework_status(homework):
    url = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'

    try:
        response = requests.get(url=url, headers=headers, params=params).json().get('homeworks', [])

    except requests.exceptions.RequestException as e:
        print(f'Ошибка запроса: {e}')
 
    try:
        homework_name = response[0]['homework_name']

    except NameError:
        print('Произошла ошибка запроса')

    except LookupError:
	    print('Список домашек пуст')

    except Exception as e:
        print(f'Ошибка: {e}')

    try:
        if response[0]['status'] == 'rejected':
            verdict = 'К сожалению в работе нашлись ошибки.'
        else:
            verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
        return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'

    except NameError:
        print('Произошла ошибка запроса')

    except LookupError:
	    print('Список домашек пуст')

    except Exception as e:
        print(f'Ошибка: {e}')


def get_homework_statuses(current_timestamp):
    url = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
    homework_statuses = requests.get(url=url, headers=headers, params=params).json()
    return homework_statuses


def send_message(message, bot):
    return bot.send_message(chat_id=CHAT_ID, text=message)
    

def main():
    current_timestamp = int(time.time())  # начальное значение timestamp

    proxy = telegram.utils.request.Request(proxy_url='https://62.201.238.250:8080') 
    bot = telegram.Bot(token=TELEGRAM_TOKEN, request=proxy)

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework:
                send_message(parse_homework_status(new_homework.get('homeworks', [])), bot)
                current_timestamp = new_homework.get('current_date', 0)  # обновить timestamp
            time.sleep(300)  # опрашивать раз в пять минут

        except KeyboardInterrupt:
            print('Бот остановлен.')
            break

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(10)

if __name__ == '__main__':
    main()
