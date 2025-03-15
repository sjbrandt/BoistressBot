FROM python:3.12-alpine

WORKDIR /

COPY . ./

RUN pip install -r requirements.txt

RUN ls -a

CMD [ "python", "bot.py" ]

