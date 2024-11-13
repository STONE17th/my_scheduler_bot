FROM python:slim

RUN apt-get update && apt-get install -y git
RUN pip3 install aiogram --break-system-packages
RUN git clone https://github.com/STONE17th/my_scheduler_bot.git

WORKDIR /my_scheduler_bot

CMD [ "python3", "main.py" ]