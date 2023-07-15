FROM python:3.8.16-slim-bullseye
ENV LANG C.UTF-8

# 将环境变量设置为非交互的
ENV DEBIAN_FRONTEND noninteractive

# 设置工作目录
WORKDIR /app

COPY src/ ./
COPY files /

# 换源以及各种安装以及移动文件
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
	&& apt-get -y update \
	&& apt-get -y install procps \
	&& pip3 install /ExifRead-3.0.0 \
	&& pip3 install /webpy-0.62 \
	&& mv /flag.txt /root \
	&& chmod -R 777 /app/sessions \
	&& chmod -R 777 /app/static \
	&& chmod -R 777 /app/uploads \
	&& groupadd -r ctfer \
	&& useradd -r -g ctfer ctfer \
	&& chmod 400 /flag \
	&& chmod u+s /readflag \
	&& chmod 4111 /readflag \
	&& chmod +x /start.sh

ENTRYPOINT /start.sh

EXPOSE 8080