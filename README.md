# Casting Agency Fullstack Capstone Project

## Testing the API locally

### Installing Python Dependencies

Navigate to the fullstack_capstone folder and install python package dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

### Database Setup

The `db_backup.sql` file can be used to restore a backup of the test database.

### Running the server

To run the server, execute:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

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

## Testing

A Postman collection is included with the project: `Fullstack Capstone.postman_collection.json`. After importing the collection to Postman, the test suite can be run on a fresh database created from the backup file.

The test suite is divided into three folders based on the RBAC roles of the project. Each folder contains a token request, which can be used to request a new bearer token if the one included in the collection has expired. Click `Send`, then copy the token returned in the payload, and paste it under the `Authorization` tab of the folder. Note that each folder requires a token specific to the corresponding role.

By changing the `url` variable on the collection level to the [Heroku URL](#testing-the-api-on-heroku), you can use the requests to communicate with the deployed application.
