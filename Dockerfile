FROM python:3.9

RUN apt-get update && apt-get install -y telnet tcpdump iputils-ping dnsutils

WORKDIR /opt/FinanceApp

COPY . /opt/FinanceApp

RUN pip install -r /opt/FinanceApp/requirements.txt

# RUN python manage.py collectstatic --noinput


CMD ["python", "/opt/FinanceApp/manage.py", "runserver", "0.0.0.0:8000"]
