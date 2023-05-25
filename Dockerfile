FROM python:3.9-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN apt-get -y update
RUN apt-get -y upgrade

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]