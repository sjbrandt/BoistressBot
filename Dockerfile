FROM python:3.12-alpine

WORKDIR /

COPY . ./

RUN pip install -r requirements.txt

CMD [ "python", "bot.py" ]

