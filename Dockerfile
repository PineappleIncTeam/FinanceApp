FROM python:3.11

RUN apt-get update && apt-get install -y telnet tcpdump iputils-ping dnsutils
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/FinanceApp

COPY . /opt/FinanceApp


RUN pip install -r /opt/FinanceApp/requirements.txt

CMD ["python3", "/manage.py", "runserver", "0.0.0.0:8000"]


