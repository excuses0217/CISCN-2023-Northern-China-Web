FROM ubuntu:22.04

RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
RUN apt-get update \
    && apt-get install -y python3 python3-pip
RUN python3 -m pip install --upgrade pip
WORKDIR /srv
COPY . /srv
RUN mkdir /srv/uploads
RUN chmod a+rw -R /srv/uploads
COPY flag /flag
RUN chmod 777 /flag
RUN useradd --no-create-home -u 1000 ctf

RUN python3 -m pip install -r requirements.txt

USER ctf

CMD python3 app.py
EXPOSE 1337