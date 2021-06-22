FROM python:3.8

WORKDIR /maximum_telegram_bot

COPY . .

RUN pip3 install -r requirements.txt

CMD [ "python3", "bot.py" ]