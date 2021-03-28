import os
import unittest
import json
import requests
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import DB_PATH, setup_db, Movie, Actor
from auth import AUTH0_DOMAIN, API_AUDIENCE


def get_user_token(username, password):
    url = f'https://{AUTH0_DOMAIN}/oauth/token'
    headers = {'content-type': 'application/json'}
    parameter = {"client_id": "5eXy5EwbCL5jq2jQZYA2xPdygRVj5AsM",
                 "client_secret": "-ho1au3-CbB09VsjagzvXDHqBAkQqNFadD4VcKRPZ0qPhAAGLh_C3MWB353MIzfA",
                 "audience": API_AUDIENCE,
                 "grant_type": "password",
                 "username": username,
                 "password": password}
    response_dict = json.loads(requests.post(
        url, json=parameter, headers=headers).text)
    return {'authorization': "Bearer " + response_dict['access_token']}


class ApiTestCase(unittest.TestCase):
    """This class represents all possible endpoints in the API"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        setup_db(self.app, DB_PATH)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies_success(self):
        """Successful GET /movies"""
        res = self.client().get('/movies', headers=producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']))

    def test_get_movies_failure(self):
        """Unsuccessful GET /movies?page=1000"""
        res = self.client().get('/movies?page=1000', headers=producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_actors_success(self):
        """Successful GET /actors"""
        res = self.client().get('/actors', headers=producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))

    def test_get_actors_failure(self):
        """Unsuccessful GET /actors?page=1000"""
        res = self.client().get('/actors?page=1000', headers=producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_post_movies_success(self):
        """Successful POST /movies"""
        res = self.client().post('/movies', headers=producer_token,
            json={
                "title": "Iron Man 4",
                "release_date": "2023-04-14"
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_post_movies_failure(self):
        """Unsuccessful POST /movies"""
        res = self.client().post('/movies', headers=producer_token,
            json={
                "title": "Iron Man 5",
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_post_actors_success(self):
        """Successful POST /actors"""
        res = self.client().post('/actors', headers=producer_token,
                                 json={
                                     "name": "Charlie Chaplin",
                                     "age": 44,
                                     "gender": "male"
                                 })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_post_movies_failure(self):
        """Unsuccessful POST /actors"""
        res = self.client().post('/actors', headers=producer_token,
                                 json={
                                     "name": "Bud Spencer",
                                 })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_patch_movies_success(self):
        """Successful PATCH /movies/2"""
        res = self.client().patch('/movies/2', headers=producer_token,
            json={
                "title": "Iron Man 6",
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movies_failure(self):
        """Unsuccessful PATCH /movies/1000"""
        res = self.client().patch('/movies/1000', headers=producer_token,
            json={
                "title": "Iron Man 5",
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_patch_actors_success(self):
        """Successful PATCH /actors/2"""
        res = self.client().patch('/actors/2', headers=producer_token,
            json={
                "name": "Bud Spencer",
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actors_failure(self):
        """Unsuccessful PATCH /actors/1000"""
        res = self.client().patch('/actors/1000', headers=producer_token,
            json={
                "name": "Sharon Stone",
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_movies_success(self):
        """Successful DELETE /movies/1"""
        res = self.client().delete('/movies/1', headers=producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movies_failure(self):
        """Unsuccessful DELETE /movies/1000"""
        res = self.client().delete('/movies/1000', headers=producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_actors_success(self):
        """Successful DELETE /actors/1"""
        res = self.client().delete('/actors/1', headers=producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors_failure(self):
        """Unsuccessful DELETE /actors/1000"""
        res = self.client().delete('/actors/1000', headers=producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

class RoleTestCase(unittest.TestCase):
    """This class represents RBAC accesses"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        setup_db(self.app, DB_PATH)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_assistant_get_movies(self):
        """Successful assistant access for endpoint GET /movies"""
        res = self.client().get('/movies', headers=assistant_token)

        self.assertEqual(res.status_code, 200)

    def test_assistant_post_actors(self):
        """Unsuccessful assistant access for endpoint POST /actors"""
        res = self.client().post('/actors', headers=assistant_token,
                                 json={
                                     "name": "Terence Hill",
                                     "age": 80,
                                     "gender": "male"
                                 })

        self.assertEqual(res.status_code, 403)

    def test_assistant_post_movies(self):
        """Unsuccessful assistant access for endpoint POST /movies"""
        res = self.client().post('/movies', headers=assistant_token,
                                 json={
                                     "title": "Star Wars",
                                     "release_date": "1978-09-15"
                                 })

        self.assertEqual(res.status_code, 403)

    def test_director_get_movies(self):
        """Successful director access for endpoint GET /movies"""
        res = self.client().get('/movies', headers=director_token)

        self.assertEqual(res.status_code, 200)

    def test_director_post_actors(self):
        """Successful director access for endpoint POST /actors"""
        res = self.client().post('/actors', headers=director_token,
                                 json={
                                     "name": "Terence Hill",
                                     "age": 80,
                                     "gender": "male"
                                 })

        self.assertEqual(res.status_code, 201)

    def test_director_post_movies(self):
        """Unsuccessful director access for endpoint POST /movies"""
        res = self.client().post('/movies', headers=director_token,
                                 json={
                                     "title": "Star Wars",
                                     "release_date": "1978-09-15"
                                 })

        self.assertEqual(res.status_code, 403)

    def test_producer_get_movies(self):
        """Successful producer access for endpoint GET /movies"""
        res = self.client().get('/movies', headers=producer_token)

        self.assertEqual(res.status_code, 200)

    def test_producer_post_actors(self):
        """Successful producer access for endpoint POST /actors"""
        res = self.client().post('/actors', headers=producer_token,
                                 json={
                                     "name": "Keira Knightly",
                                     "age": 41,
                                     "gender": "female"
                                 })

        self.assertEqual(res.status_code, 201)

    def test_producer_post_movies(self):
        """Successful producer access for endpoint POST /movies"""
        res = self.client().post('/movies', headers=producer_token,
                                 json={
                                     "title": "Star Wars",
                                     "release_date": "1978-09-15"
                                 })

        self.assertEqual(res.status_code, 201)

if __name__ == "__main__":
    assistant_token = get_user_token("assistant@example.com", "Assistant!")
    director_token = get_user_token("director@example.com", "Director!")
    producer_token = get_user_token("producer@example.com", "Producer!")
    unittest.main()