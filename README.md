# Fuzzy API

## Introduction
Fuzzy API is a simple CRUD API built with Python Flask and Postgresql. It is implemented over a single table to perform CRUD operations on that table.

## Prerequisite
- You must have python and poetry installed
- You should be running a local or remote instance of postgresql that is accessible.
- You must have git installed on your machine.

## Setup
1. Clone the repository
```sh
$ git clone https://github.com/BenFaruna/fuzzy-api.git
$ cd fuzzy-api
```

2. Install packages using poetry
```sh
$ poetry install
```

3. Copy the content of `sample.env` into `.env` and provide the details for your database.
```sh
$ cp sample.env .env        # Linux/Mac
$
$ copy sample.env .env      # windows
```

4. Start the application
```sh
$ poetry run python api_endpoint/main.py
```

You can visit the API endpoint at http://localhost:5000/api.

## Testing
To test the API endpoint using tests written in the tests folder, take the following step:

1. Start the flask server (if it isn't running)
```sh
$ poetry run python api_endpoint/main.py
```

2. Open a new terminal window and run the command
```sh
$ poetry run pytest
$   # OR
$ poetry run python -m unittest
```

## API Routes
* `POST` `api/` -> Accepts request with a body containing the `name` field, creates a new database entry and return a response on the request status.
* `GET` `api/<string:name>` -> Return a json containing user `name` and `id`
* `PUT` `api/<string:name>` -> Accepts request with a body containing the field `new_name` and updates the database entry with the name specified in the route, or return an error response if the name doesn't exist.
* `DELETE` `api/<string:name>` -> Delete database entry with name equal `name` and return a response. If the name is not found, and error response is returned.

**NB: POST, PUT and DELETE queries to the API endpoints should have a `Content-Type` of `application/json`.**