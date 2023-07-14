FROM ruby:2.7

RUN gem install sinatra

WORKDIR /app

COPY . .

CMD ["ruby", "app.rb", "-o", "0.0.0.0"]
