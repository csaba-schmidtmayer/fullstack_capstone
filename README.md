# Casting Agency Fullstack Capstone Project

This repository is the project code for the final capstone project of the Udacity Fullstack Nanodegree. It follows the default specification for creating a management interface for a casting agency.

## Testing the API locally

### Installing Python Dependencies

Navigate to the fullstack_capstone folder and install python package dependencies by running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

#### Key dependencies

**Flask:** The web framework for handling requests and responses.
**SQLAlchemy:** ORM tool for handling database connections and queries.
**Flask-Jose:** A toolkit for decoding Javascript Web Tokens for authorization.

### Database Setup

Create a PostgreSQL database with the name `casting_agency`. Use the `db_backup.sql` file to restore a backup of the test database.

You can also set up the database structure by using the included migrations by running the following commands:

```bash
flask db init
flask db migrate
flask db upgrade
```

In this case, you have to populate the database manually to perform any tests. Make sure to add at least two entries for each category, as ids 1 and 2 for both movies and actors are required for all tests to pass.

### Setting up and running the local development server

To run the development server, execute one of the following command stacks, depending on your operating system:

On Linux:

```bash
export FLASK_APP=app
export FLASK_ENV=development

export AUTH0_DOMAIN=schmiczy.eu.auth0.com
export ALGORITHMS=RS256
export API_AUDIENCE=https://api.casting-agency.schmiczy.eu

flask run
```

On Windows:

```bash
set FLASK_APP=app
set FLASK_ENV=development

set AUTH0_DOMAIN=schmiczy.eu.auth0.com
set ALGORITHMS=RS256
set API_AUDIENCE=https://api.casting-agency.schmiczy.eu

flask run
```

For convenience, you can also run either `local_setup.sh` or `local_setup.bat`.

### Unit tests

Run `tests.py` for unit tests.

Two TestCase classes are included:

**ApiTestCase:** Uses an executive producer role to test that all endpoints are working correctly.
**RoleTestCase:** Tests that a representative selection of endpoints (GET /movies, POST /actors, POST /movies) can be accessed with the correct roles only.

## Testing the API on Heroku

The host address of the Heroku deployment is `https://casting-agency-schmiczy-eu.herokuapp.com`.

## Endpoints

The backend API uses the following endpoints:

| HTTP method | Route | Link |
| --- | --- | --- |
| GET | /movies | [Read more](#get-movies) |
| GET | /actors | [Read more](#get-actors) |
| GET | /movies/<movie_id> | [Read more](#get-moviesmovie_id) |
| GET | /actors/<actor_id> | [Read more](#get-actorsactor_id) |
| POST | /movies | [Read more](#post-movies) |
| POST | /actors | [Read more](#post-actors) |
| PATCH | /movies/<movie_id> | [Read more](#patch-movies) |
| PATCH | /actors/<actor_id> | [Read more](#patch-actors) |
| DELETE | /movies/<movie_id> | [Read more](#delete-moviesmovie_id) |
| DELETE | /actors/<actor_id> | [Read more](#delete-actorsactor_id) |

### GET /movies

Fetches a paginated list of movies. A page contains ten objects or less if the last page is requested.

#### Required permission

`get:movies`

#### Request arguments

`page`: Determines the slice of all objects that is returned. Default value is 1.

#### Response payload

An array of movie objects.

### GET /actors

Fetches a paginated list of questions. A page contains ten objects or less if the last page is requested.

#### Require permission

`get:actors`

#### Request arguments

`page`: Determines the slice of all objects that is returned. Default value is 1.

#### Response payload

An array of actor objects.

### GET /movies/<movie_id>

Fetches a single movie with the provided id.

#### Required permission

`get:movies`

#### Request arguments

None

#### Response payload

A single movie object.

### GET /actors/<actor_id>

Fetches a single movie with the provided id.

#### Requied permission

`get:actors`

#### Request arguments

None

#### Response payload

A single actor object.

### POST /movies

Creates a new movie in the database.

#### Required permission

`add:movies`

#### Request payload

| Key | Type | Data |
| --- | --- | --- |
| `title` | str | The title of the movie |
| `release_date` | str | The release date of the movie in the form of `yyyy-mm-dd` |

All of the keys and their corresponding data must be included in the request.

#### Response payload of submitting new questions

Success message.

### POST /actors

Creates a new actor in the database.

#### Required permission

`add:actors`

#### Request payload

| Key | Type | Data |
| --- | --- | --- |
| `name` | str | The name of the actor |
| `age` | int | The age of the actor |
| `gender` | str | The gender of the actor |

All of the keys and their corresponding data must be included in the request.

#### Response payload

Success message.

### PATCH /movies

Updates a movie in the database.

#### Required permission

`modify:movies`

#### Request payload

| Key | Type | Data |
| --- | --- | --- |
| `title` | str | The title of the movie |
| `release_date` | str | The release date of the movie in the form of `yyyy-mm-dd` |

At least one of the keys and their corresponding data must be included in the request.

#### Response payload of submitting new questions

Success message.

### PATCH /actors

Updates an actor in the database.

#### Required permission

`modify:actors`

#### Request payload

| Key | Type | Data |
| --- | --- | --- |
| `name` | str | The name of the actor |
| `age` | int | The age of the actor |
| `gender` | str | The gender of the actor |

At least one of the keys and their corresponding data must be included in the request.

#### Response payload

Success message.

### DELETE /movies/<movie_id>

Deletes the specified movie.

#### Required permission

`delete:movies`

#### Request arguments

None

#### Response payload

Success message.

### DELETE /actors/<actor_id>

Deletes the specified actor.

#### Required permission

`delete:actors`

#### Request arguments

None

#### Response payload

Success message.

## Role-based Access Control

The API uses [Auth0](https://auth0.com) to authenticate users with Javascript Web Tokens.

Three roles are defined with the following permissions:

| Role | Permissions |
| --- | --- |
| Casting assistant | `get:movies` `get:actors` |
| Casting director | `get:movies` `get:actors` `modify:movies` `modify:actors` `add:actors` `delete:actors` |
| Executive producer | `get:movies` `get:actors` `modify:movies` `modify:actors` `add:movies` `add:actors` `delete:movies` `delete:actors` |

Tokens can be requested by sending a POST message to `https://schmiczy.eu.auth0.com/oauth/token` with the following JSON payload:

```json
{
    "client_id": "5eXy5EwbCL5jq2jQZYA2xPdygRVj5AsM",
    "client_secret": "-ho1au3-CbB09VsjagzvXDHqBAkQqNFadD4VcKRPZ0qPhAAGLh_C3MWB353MIzfA",
    "audience": "https://api.casting-agency.schmiczy.eu",
    "grant_type": "password",
    "username": <username>,
    "password": <password>
}
```

The following username and password pairs can be used for the roles defined above:

| Role | Username | Password |
| --- | --- | --- |
| Casting assistant | assistant@example.com | Assistant! |
| Casting director | director@example.com | Director! |
| Executive producer | producer@example.com | Producer! |

The tokens recieved this way must be included in the `Authorization` header of a request sent towards the API endpoints.

The token requests are included in the attached Postman collection as request templates. To use them, simply choose one under its respective role folder, and click `Send`.

## Postman collection

A Postman collection is included with the project: `Fullstack Capstone.postman_collection.json`. After importing the collection to Postman, the test suite can be run on a fresh database created from the backup file.

The test suite is divided into three folders based on the RBAC roles of the project. Each folder contains a token request, which can be used to request a new bearer token if the one included in the collection has expired. Click `Send`, then copy the token returned in the payload, and paste it under the `Authorization` tab of the folder. Note that each folder requires a token specific to the corresponding role.

By changing the `url` variable on the collection level to the [Heroku URL](#testing-the-api-on-heroku), you can use the requests to communicate with the deployed application.

## Credits

The authentication token retreival code for unit tests are from [this Stackoverflow post](https://stackoverflow.com/questions/48552474/auth0-obtain-access-token-for-unit-tests-in-python).
