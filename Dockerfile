FROM ubuntu

MAINTAINER Sij

WORKDIR /app

RUN apt update
RUN apt install -y python3.8

COPY './requirements.txt' .

# RUN apt-get install libgtk2.0-dev pkg-config -yqq
RUN apt install -y python3-pip
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 3000

COPY . .

CMD ["python3", "app.py"]


# CMD ["flask", "run"]
