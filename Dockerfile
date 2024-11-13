FROM python:slim

WORKDIR /my_scheduler_bot

RUN apt-get update && apt-get install -y git
RUN pip3 install aiogram --break-system-packages
RUN git clone https://github.com/STONE17th/my_scheduler_bot.git

CMD [ "git", "pull", "&&", "python3", "main.py" ]