FROM php:7.4-apache

# 设置文件上传和系统命令的配置
RUN echo "file_uploads = On\n" \
         "upload_max_filesize = 2M\n" \
         "post_max_size = 8M\n" \
         > /usr/local/etc/php/conf.d/uploads.ini

# 设置文件权限
RUN chown -R www-data:www-data /var/www/html/

# 将当前目录下的所有文件复制到Docker image的相应位置
COPY . /var/www/html/

# 开放端口80供外部访问
EXPOSE 80
