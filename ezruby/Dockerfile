FROM ruby:2.7

RUN gem install sinatra

WORKDIR /app

COPY . .

# 设置flag
RUN echo "flag{$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 20 | head -n 1)}" > /flag
RUN chmod 777 /flag

CMD ["ruby", "app.rb", "-o", "0.0.0.0"]
