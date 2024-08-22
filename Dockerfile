FROM python:3.12.4-slim

WORKDIR /usr/src/app

ARG URL
ARG USERNAME
ARG PASSWORD

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000

ENV URL=$URL
ENV USERNAME=$USERNAME
ENV PASSWORD=$PASSWORD

CMD ["flask", "run", "--host=0.0.0.0"]