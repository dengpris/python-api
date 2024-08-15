FROM python:3.12.4-slim

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000

ENV FLASK_APP=application

CMD ["flask", "run", "--host=0.0.0.0"]