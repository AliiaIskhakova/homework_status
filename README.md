<b>Telegram-бот.</b>
<br>Обращаясь к API Яндекс.Практикума бот присылает сообщения при изменении статуса домашнего задания.

<b>Как развернуть проект локально</b>

1. Склонируйте репозиторий
<br><code>git clone <ссылка на репозиторий> <название локальной папки></code>

2. Создайте и активируйте виртуальное окружение
<br><code>python -m venv venv && . venv\scripts\activate</code>

3. Установите необходимые пакеты
<br><code>pip install -r requirements.txt</code>

4. Создайте бота в Телеграм (он будет присылать вам сообщения):
Найдите @BotFather,нажмите Start  и выполните команду /newbot.
Задайте имя и техническое имя вашего бота.
После создания бота вы получите токен TELEGRAM_TOKEN.

5. В директории проекта нужно создать файл .env с личными данными:
<br>PRAKTIKUM_TOKEN='' - можно получить по ссылке https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a.
<br>TELEGRAM_TOKEN='' - получен на предыдущем шаге.
<br>TELEGRAM_CHAT_ID='' - можно узнать, обратившись к @getmyid_bot

4. Запустить бота
<br><code>python homework.py</code>

