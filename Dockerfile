FROM python:3.7
RUN pip install pipenv
WORKDIR /usr/local/newsfeed_server
COPY . .
RUN pipenv install
