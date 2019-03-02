FROM python:3.7.2-slim

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD python3 app.py \
       --mongodb ${MONGODB_URL} \
       --user ${MONGODB_USER} \ 
       --password ${MONGODB_PASSWORD} \
       --port 5000