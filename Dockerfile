FROM python:slim

WORKDIR /code

RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/STONE17th/my_scheduler_bot.git

CMD [ "git", "pull", "&&", "python", "./main.py" ]