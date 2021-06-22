FROM python:3.8

WORKDIR /usr/src/app

RUN pip3 install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "bot.py" ]