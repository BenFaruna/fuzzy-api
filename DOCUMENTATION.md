# Fuzzy API Endpoints, Usage and Setup

## API Routes request and response

**NB: POST, PUT and DELETE queries to the API endpoints should have a `Content-Type` of `application/json`.**

### POST /api

Creates a new database entry

Request body:
```
{
    "name": string
}
```

Response:

Status code: `201`
```
{
    "Success": "New user added",
    "user": {
        "id": integer,
        "name": string
    }
}
```

Error Response:

- For duplicate name

Response:

Status code: `403`
```
{
    "Error": "Name already exists"
}
```

- For request without body

Response:

Status code: `400`
```
{
    "Error": "body data not supplied or name key not found"
}
```

### GET /api/<string:name>

Fetch user details matching `name`

Response:

Status code: `200`
```
{
    "id": integer,
    "name": string
}
```

Error Response:

- `name` not in database

Response:

Status code: `404`
```
{
    "Error": "<name> not found"
}
```

### PUT /api/<string:name>

Update user name in database matching `name`

Request body:
```
{
    "new_name": string
}
```

Response:

Status code: `200`
```
{
    "Success": "Name updated",
    "user": {
        "id": integer,
        "name": string
    }
}
```

Error Response:

- `name` not in database

Response:

Status code: `404`
```
{
    "Error": "<name> not found"
}
```

- `new_name` not in request body

Response:

Status code: `400`
```
{
    "Error": "new_name data not supplied"
}
```

- Updating to an existing name

Response:

Status code: `403`
```
{
    "Error": "Name already exists"
}
```

### DELETE /api/<string:name>

Removes database entry matching `name`

Request body:
```
{}
```

Response:

Status code: `200`
```
{
    "Success": "<name> deleted"
}
```

Error Response:

- `name` not in database

Response:

Status code: `404`
```
{
    "Error": "<name> not found"
}
```

## Setup of API locally
### Prerequisite
- You must have python and poetry installed
- You should be running a local or remote instance of postgresql that is accessible.
- You must have git installed on your machine.

### Setup
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
