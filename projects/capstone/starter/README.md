# Casting Agency API Backend
Udacity Full-Stack Web Developer Nanodegree Program Capstone Project

## Project Motivation
This is the final project to complete Udacity Full-Stack Web Developer Nanodegree Program. Project is about a casting agency that has 3 roles: Executive director, Casting director and Casting assistant. Depending on the role, the user can modfiy movies and actors. For each movie, there can be many actors assigned, thus database models a one to many relationship. The completion of the project demnostrates ability to model data, setup relationship, API design, authentication and cloud deploymnet. 

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/starter` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the capstone.psql file provided. From the backend folder in terminal run:
```bash
createdb capstone
psql capstone < capstone.psql
```
## Running tests Setup
With Postgres running, create a test database and restore contents from a database using the capstone.psql file provided. From the backend folder in terminal run:
```bash
createdb capstone_test
psql capstone_test < capstone.psql
python test_app.py
```
## Auth0 Setup

To login or set up an account, go to the following url:

https://capstone-project1.us.auth0.com/authorize?audience=cast&response_type=token&client_id=a4ZqMlAKmxWb2I81gUQqzCVbLc1iuu37&redirect_uri=http://localhost:8080/login-results

AUTH0_DOMAIN = "capstone-project1.us.auth0.com"
ALGORITHMS = ["RS256"]
API_AUDIENCE = "cast"

## Roles

Casting Assistant

    Can view actors and movies

Casting Director

    All permissions a Casting Assistant has and…
    Add or delete an actor from the database
    Modify actors or movies

Executive Producer

    All permissions a Casting Director has and…
    Add or delete a movie from the database

## Permissions
Created in API settings as follows:

    view:actors
    view:movies
    delete:actors
    delete:movies
    post:actors
    post:movies
    update:actors
    update:movies
    



## Running the server

From within the `starter` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to app.y  directs flask to find the application. 


## API Documentation

## Endpoints

GET /movies
- Get all movies 
- Require view:movies permission
- Return exmaple:

{
    "movies": [
        {
            "actors": [
                {
                    "age": 5,
                    "gender": "f",
                    "id": 26,
                    "movie_id": 12,
                    "name": "rtr"
                }
            ],
            "id": 12,
            "release_date": "Mon, 05 Jan 2015 00:00:00 GMT",
            "title": "d"
                    }
    ],
    "success": "True"
}


GET /movies
- Get all actors 
- Require view:movies actors
- Return exmaple:

{
    "actors": [
        {
            "age": 5,
            "gender": "f",
            "id": 26,
            "movie_id": 12,
            "name": "rtr"
        }

],
    "success": "True"
}


DELETE /movies/<int:id>
- Deletes the movie with given id
- Require delete:movies permission
- Return exmaple:
{
    "deleted": 12,
    "success": "True"
}

DELETE /actors/<int:id>
- Deletes the actor with given id
- Require delete:actors permission
- Return exmaple:
{
    "deleted": 12,
    "success": "True"
}


POST /movies
- Create a new movie
- Require post:movies permission
- Return exmaple:
{
    "movie": {
        "actors": [],
        "id": 26,
        "release_date": "Sun, 02 Jan 2022 00:00:00 GMT",
        "title": "newpost"
    },
    "success": true
}

POST /actors
- Create a new actor
- Require post:actor permission
- Return exmaple:
{
    "actor": {
        "age": 102,
        "gender": "female",
        "id": 43,
        "movie_id": 10,
        "name": "newactor postman"
    },
    "success": true
}

PATCH /movies/<int:id>
- Update movie with given id 
- Require patch:movie
- Return exmaple:
{
    "success": true,
    "updated": {
        "actors": [
            {
                "age": 102,
                "gender": "female",
                "id": 31,
                "movie_id": 10,
                "name": "newactor postman"
            },
            {
                "age": 102,
                "gender": "female",
                "id": 36,
                "movie_id": 10,
                "name": "newactor postman"
            },
           
        ],
        "id": 10,
        "release_date": "Sat, 03 Jan 2015 00:00:00 GMT",
        "title": "updated"
    }
}


PATCH /actors/<int:id>
- Update actor with given id 
- Require patch:actor
- Return exmaple:
{
    "success": true,
    "updated": {
        "age": 102,
        "gender": "female",
        "id": 22,
        "movie_id": 10,
        "name": "updated-newactor postman"
    }
}

## Error Handling

API will return these error in case request fails:

404: resource not found
401: Unauthorized
403: Forbidden
404: Resource Not Found
422: unprocessable
500: Internal Server Error