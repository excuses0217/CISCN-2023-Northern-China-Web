FROM php:8.0-cli
WORKDIR /var/www/html
COPY index.php /var/www/html/
# 设置flag
RUN echo "flag{$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 20 | head -n 1)}" > /flag
RUN chmod 777 /flag
CMD [ "php", "-S", "0.0.0.0:80" ]
EXPOSE 80
