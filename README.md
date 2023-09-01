![FLASK](https://img.shields.io/badge/flask-%2320232a.svg?style=for-the-badge&logo=flask&logoColor=%2361DAFB)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%2320232a.svg?style=for-the-badge&logo=PostgreSQL&logoColor=green)
![Jinja](https://img.shields.io/badge/Jinja-%2320232a.svg?style=for-the-badge&logo=Jinja&logoColor=green)

## § Website

[Admin Platform](https://shownbooking-a10ea6e13f6b.herokuapp.com/admin)

[User Platform](https://show-booking.netlify.app/)

[User Platform Repo](https://github.com/elle-n-lu/movie-booking-front)

*admin login details in login_info.txt

## § Backend App Introduction

This is a movie booking management application allowing admin to login, create and update cinemas, movies, schedules and sessions in webpage supported by Jinja.
This app uses Flask-login to do admin login and logout session management.

*The project is based on the api project for Code Academy's flask assignment. 

## § Local Setup Instructions

1. git clone this repo

2. install python venv

        python3 -m venv .venv && source .venv/bin/activate 

3. install packages

        python3 -m pip install -r requirements.txt

4. create .env file according to .env.example

5. generate models and admin

        flask db create
        flask db seed
    
6. run app

        flask run



