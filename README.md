# Project: FinanceApp

<p style="text-align: center;">
<kbd>
<image src="src/staticfiles/LogoSVG.svg" alt='logo' width='150'/>
</kbd>
</p>
FinanceApp is an API that implements a service for financial accounting.

___
 

## Contents:

- [Technologies](#technologies)
- [Description](#description)
- [Installation and starting](#installation-and-starting)

---

## Technologies


**Programming languages and modules:**

[![Python](https://img.shields.io/badge/-python_3.10^-464646?logo=python)](https://www.python.org/)


**Frameworks:**

[![Django](https://img.shields.io/badge/-Django-464646?logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?logo=Django)](https://www.django-rest-framework.org/)

**Databases:**

[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)


**Containerization:**

[![docker](https://img.shields.io/badge/-Docker-464646?logo=docker)](https://www.docker.com/)
[![docker_compose](https://img.shields.io/badge/-Docker%20Compose-464646?logo=docker)](https://docs.docker.com/compose/)

[⬆️Contents](#contents)

---
## Description:

***FinanceApp is an API that implements a service for financial accounting.***

[⬆️Contents](#contents)

---

## Installation and starting

<details><summary>Pre-conditions</summary>

It is assumed that the user has installed [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) on the local machine or on the server where the project will run. You can check if they are installed using the command:

```bash
docker --version && docker-compose --version
```
</details>


Local launch:

1. Clone the repository from GitHub:
```bash
git clone https://github.com/PineappleIncTeam/FinanceApp
```

1.1 Enter the data for the environment variables in the [.env] file:

```
    SECRET_KEY=

    EMAIL_HOST=
    EMAIL_PORT=
    EMAIL_USE_TLS=
    EMAIL_USE_SSL=

    EMAIL_HOST_USER=
    EMAIL_HOST_PASSWORD=
    DEFAULT_FROM_EMAIL=
    
    DOMAIN=
```

1.2 To generate SECRET_KEY run the command:
```bash
make secretkey
```

<details><summary>Local launch: Django/PostgreSQL</summary><br>

***!!! It is assumed that the user has installed [PostgreSQL](https://www.postgresql.org/) and [poetry](https://python-poetry.org/) !!!***


1.3* Create a new PostgreSQL database and pass the credentials to the [.env] file.

2. All required dependencies described in **pyproject.toml** file. To install all required libraries and packages, run the command:
```bash
poetry install
```

3. To activate the virtual environment:
```bash
poetry shell
```

4. Run the migrations and launch the application:
```bash
python tree_menu/manage.py makemigrations && \
python tree_menu/manage.py migrate && \
python tree_menu/manage.py runserver
```
The project will run locally at `http://127.0.0.1:8000/`

</details>

<details><summary>Lounch via Docker: Docker Compose</summary>

2. From the root directory of the project, execute the command:
```bash
docker-compose -f docker-compose.dev.yml up -d --build
```
The project will be hosted in two docker containers (db, app) at `http://localhost:8000/`.

3. You can stop docker and delete containers with the command from the root directory of the project:
```bash
docker-compose -f docker-compose.dev.yml down
```
add flag -v to delete volumes ```docker-compose -f docker-compose.dev.yml down -v```
</details><h1></h1>

[⬆️Contents](#contents)
