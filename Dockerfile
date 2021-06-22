FROM python:3.8

WORKDIR /maximum_telegram_bot

COPY .env .
COPY bot.py .
COPY credentials.py .
COPY db_controller.py .
COPY messages.py .
COPY sheets.py .
COPY sheets.json .
COPY requirements.txt .

RUN pip3 install -r requirements.txt

CMD [ "python3", "bot.py" ]