import os
import unittest
import json
import requests
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import DB_PATH, setup_db, Movie, Actor
from auth import AUTH0_DOMAIN, API_AUDIENCE


def get_user_token():
    url = f'https://{AUTH0_DOMAIN}/oauth/token'
    headers = {'content-type': 'application/json'}
    parameter = {"client_id": "5eXy5EwbCL5jq2jQZYA2xPdygRVj5AsM",
                 "client_secret": "-ho1au3-CbB09VsjagzvXDHqBAkQqNFadD4VcKRPZ0qPhAAGLh_C3MWB353MIzfA",
                 "audience": API_AUDIENCE,
                 "grant_type": "password",
                 "username": "producer",
                 "password": "Producer!"}
    response_dict = json.loads(requests.post(
        url, json=parameter, headers=headers).text)
    return {'authorization': "Bearer " + response_dict['access_token']}


class ProducerTestCase(unittest.TestCase):
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
        res = self.client().get('/movies', headers=token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']))

    def test_get_movies_failure(self):
        """Unsuccessful GET /movies?page=1000"""
        res = self.client().get('/movies?page=1000', headers=token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_actors_success(self):
        """Successful GET /actors"""
        res = self.client().get('/actors', headers=token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))

    def test_get_actors_failure(self):
        """Unsuccessful GET /actors?page=1000"""
        res = self.client().get('/actors?page=1000', headers=token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_post_movies_success(self):
        """Successful POST /movies"""
        res = self.client().post('/movies', headers=token,
            json={
                "title": "Iron Man 4",
                "release_date": "2023-04-14"
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_post_movies_failure(self):
        """Unsuccessful POST /movies"""
        res = self.client().post('/movies', headers=token,
            json={
                "title": "Iron Man 5",
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_post_actors_success(self):
        """Successful POST /actors"""
        res = self.client().post('/actors', headers=token,
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
        res = self.client().post('/actors', headers=token,
                                 json={
                                     "name": "Bud Spencer",
                                 })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_patch_movies_success(self):
        """Successful PATCH /movies/1"""
        res = self.client().patch('/movies/1', headers=token,
            json={
                "title": "Iron Man 6",
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movies_failure(self):
        """Unsuccessful PATCH /movies/1000"""
        res = self.client().post('/movies/1000', headers=token,
            json={
                "title": "Iron Man 5",
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_patch_actors_success(self):
        """Successful PATCH /actors/1"""
        res = self.client().patch('/movies/1', headers=token,
            json={
                "name": "Bud Spencer",
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_movies_failure(self):
        """Unsuccessful PATCH /actors/1000"""
        res = self.client().post('/actors/1000', headers=token,
            json={
                "name": "Sharon Stone",
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_movies_success(self):
        """Successful DELETE /movies/1"""
        res = self.client().delete('/movies/1', headers=token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movies_failure(self):
        """Unsuccessful DELETE /movies/1000"""
        res = self.client().delete('/movies/1000', headers=token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_actors_success(self):
        """Successful DELETE /actors/1"""
        res = self.client().delete('/actors/1', headers=token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors_failure(self):
        """Unsuccessful DELETE /actors/1000"""
        res = self.client().delete('/actors/1000', headers=token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


if __name__ == "__main__":
    token = get_user_token()
    unittest.main()