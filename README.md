# Full Stack Casting Agency

## Casting Agency Specifications

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Motivation for the Project

This project forms the capstone project for the Udacity Fullstack Nanodegree program. It is designed to model a casting agency, which stores information on both actors and movies. The motivation behind this project is to create a host API using Flask, JWT permissions, and tests.

## URL Location for API

## Installing Dependencies

### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Set up instructions

### Database setup

This project uses SQLite for the database. In order to setup the database first uncomment the line in `app.py`:

```python
db_drop_and_create_all()
```

This will delete all records and the database and re-create it.

### Running the app

In order to run the app first run the following commands:

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Behaviour & RBAC controls

The application has the following API behaviours:

* `get:movies`: return movies details (avialable for assistant role)
* `get:actors`: return actor details (available for assistant role)
* `post:movies`: insert a movie (available for executive producer)
* `post:actors`: insert an actor (available for casting director)
* `patch:actors/<int:id>`: modify an actor with id `id` (available for casting director)
* `patch:movies/<int:id>`: modify a movie with id `id` (available for executive producer)
* `delete:actors/<int:id>`: delete an actor with id `id` (avialable for casting director)
* `delete:movies/<int:id>`: delete a movie with id `id` (availabel for executive producer)