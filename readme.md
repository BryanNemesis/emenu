# eMenu

A REST API for managing restaurant menus.

## Tools used
* Django Rest Framework for API implementation
* Postgresql database engine
* Swagger UI for documentation
* drf-spectacular package for automatic generation of Swagger UI schema
* docker-compose for app deployment
* Mailtrap for email functionality testing

## Requirements
Docker, docker-compose.

## Installation guide
Clone the repository.
```
git clone https://github.com/BryanNemesis/emenu.git emenu
```
Change the working directory to the repository root.
```
cd emenu
```
Make sure the line endings in dailyreport&#46;sh were not changed to CRLF, if you're on Windows. If so, do `git config --global core.autocrlf false` and checkout the repo again.

Build and run.
 ```
 docker-compose up -d
 ```
After first run, perform db migrations inside 'web' container.
```
docker-compose run web python manage.py migrate
```
API will be available under http://localhost:8000/.

Documentation of endpoints will be available under http://localhost:8001/.

To update Swagger UI schema after making changes in the API, run `python manage.py spectacular --file schema.yml` inside the working directory or in the 'web' app and restart the 'docs' container.