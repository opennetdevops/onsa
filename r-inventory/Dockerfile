FROM ruby:2.5.1
RUN apt-get update -qq && apt-get install -y build-essential libpq-dev sqlite3 nodejs
RUN mkdir /r-inventory
ENV RAILS_ENV production
WORKDIR /r-inventory
COPY Gemfile /r-inventory/Gemfile
COPY Gemfile.lock /r-inventory/Gemfile.lock
RUN bundle install
COPY . /r-inventory
EXPOSE 3000
CMD ["bundle", "exec", "rails", "server", "-b", "0.0.0.0"]
