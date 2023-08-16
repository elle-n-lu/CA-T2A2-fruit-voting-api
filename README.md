![FLASK](https://img.shields.io/badge/flask-%2320232a.svg?style=for-the-badge&logo=flask&logoColor=%2361DAFB)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%2320232a.svg?style=for-the-badge&logo=PostgreSQL&logoColor=green)
![Jinja](https://img.shields.io/badge/Jinja-%2320232a.svg?style=for-the-badge&logo=Jinja&logoColor=green)

## R1

This is a movie booking management application allowing admin to login and update cinemas, movies, schedules and sessions in webpage supported by Jinja.
This app uses Flask-login to do admin login and logout session management.

The project is based on the Code Academy's flask api assignment. 

## § Instructions

1. git clone this repo

2. install python venv

        python3 -m venv .venv && source .venv/bin/activate 

3. install packages

        python3 -m pip install -r requirements.txt

4. create .env file and set up DATABASE_URL and SECRET_KEY, MAILTRAP_SERVER, MAILTRAP_USERNAME, MAILTRAP_PASSWORD

5. generate models and admin

        flask db create
        flask db seed
    
6. run app

        flask run



