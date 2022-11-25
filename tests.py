import os
import json
import unittest
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app import create_app
from models import setup_db, Actor, Movie, db_drop_and_create_all

load_dotenv()

# ASSISTANT_TOKEN = os.getenv('ASSISTANT_TOKEN')
DIRECTOR_TOKEN = os.getenv('DIRECTOR_TOKEN')
# PRODUCER_TOKEN = os.getenv('PRODUCER_TOKEN')


class CastingTestCase(unittest.TestCase):
    """This class represents the casting test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)
        # self.assistant_token = ASSISTANT_TOKEN
        self.director_token = DIRECTOR_TOKEN
        # self.producer_token = PRODUCER_TOKEN

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # # create all tables
            # self.db.create_all()
            db_drop_and_create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def get_response_payload(self, url, token):
        """Get HTTP response and json payload"""
        response = self.client().get(
            url,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        payload = json.loads(response.data)
        return response, payload

    def post_payload(self, url, post, token):
        """Post payload"""
        response = self.client().post(
            url,
            headers={
                "Authorization": f"Bearer {token}"
            },
            json=post
        )
        payload = json.loads(response.data)
        return response, payload

    def patch_payload(self, url, patch, token):
        """Patch payload"""
        response = self.client().patch(
            url,
            headers={
                "Authorization": f"Bearer {token}"
            },
            json=patch
        )
        payload = json.loads(response.data)
        return response, payload

    def delete_payload(self, url, token):
        """Delete payload"""
        response = self.client().delete(
            url,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        payload = json.loads(response.data)
        return response, payload

    def assert_status(self, response, payload, status_code, success):
        """Helper function for asserting status of http request"""
        self.assertEqual(response.status_code, status_code)
        self.assertEqual(payload['success'], success)

    def test_movies(self):
        """Test movies"""
        response, payload = self.get_response_payload(
            '/movies',
            token=self.director_token
        )
        self.assert_status(response, payload, 200, True)

        self.assertTrue(len(payload['movies']) > 0)

    def test_actors(self):
        """Test actors"""
        response, payload = self.get_response_payload(
            '/actors',
            token=self.director_token
        )
        self.assert_status(response, payload, 200, True)
        self.assertTrue(len(payload['actors']) > 0)

    def test_post_actor(self):
        """Test posting actor"""
        pre_test = Actor.query.all()

        test_actor = {
            "name": "Timothée Chalamet",
            "age": 26,
            "gender": "Male"
        }

        response, payload = self.post_payload(
            '/actors',
            token=self.director_token,
            post=test_actor
        )
        CastingTestCase.actor_added = payload['actor']['id']

        post_test = Actor.query.all()

        self.assert_status(response, payload, 200, True)
        self.assertTrue(len(post_test) - len(pre_test) == 1)

    def test_post_movie(self):
        """Test posting movies"""
        pre_test = Movie.query.all()

        test_movie = {
            "title": "Call Me By Your Name",
            "release_date": 2018
        }

        response, payload = self.post_payload(
            '/movies',
            token=self.director_token,
            post=test_movie
        )
        CastingTestCase.movie_added = payload['movie']['id']

        post_test = Movie.query.all()

        self.assert_status(response, payload, 200, True)
        self.assertTrue(len(post_test) - len(pre_test) == 1)

    def test_y_modify_actor(self):
        """Test modify actor"""
        modify_actor = {
            "name": "Timothy Chalamet"
        }

        response, payload = self.patch_payload(
            f'/actors/{1}',
            token=self.director_token,
            patch=modify_actor
        )

        self.assert_status(response, payload, 200, True)
        self.assertTrue(payload['actor']['name'] == modify_actor['name'])

    def test_y_modify_movies(self):
        """Test modify movies"""
        modify_movie = {
            "title": "Call Me By My Name"
        }

        response, payload = self.patch_payload(
            f'/movies/{1}',
            token=self.director_token,
            patch=modify_movie
        )

        self.assert_status(response, payload, 200, True)
        self.assertTrue(payload['movie']['title'] == modify_movie['title'])

    def test_z_delete_actor(self):
        """Test delete actors"""
        response, payload = self.delete_payload(
            f"/actors/1",
            token=self.director_token
        )

        self.assert_status(response, payload, 200, True)
        self.assertEqual(payload['delete'], 1)

    def test_z_delete_movie(self):
        """Test delete actors"""
        response, payload = self.delete_payload(
            f"/movies/1",
            token=self.director_token
        )

        self.assert_status(response, payload, 200, True)
        self.assertEqual(payload['delete'], 1)

    # Error test cases

    def test_malformed_post_actor(self):
        """Test malformed post for actor"""
        test_actor = {
            "title": "This is a test"
        }

        response, payload = self.post_payload(
            '/actors',
            token=self.director_token,
            post=test_actor
        )

        self.assert_status(response, payload, 422, False)

    def test_malformed_post_movie(self):
        """Test malformed post for movie """
        test_movie = {
            "name": "Jurassic Park"
        }

        response, payload = self.post_payload(
            '/movies',
            token=self.director_token,
            post=test_movie
        )

        self.assert_status(response, payload, 422, False)

    def test_malformed_modify_actor(self):
        """Test malformed modify actor """
        test_actor = {
            "title": "Big Ben"
        }

        response, payload = self.patch_payload(
            '/actors/1',
            token=self.director_token,
            patch=test_actor
        )

        self.assert_status(response, payload, 422, False)

    def test_malformed_modify_movie(self):
        """Test malformed modify movie """
        test_movie = {
            "name": "Jurassic Park"
        }

        response, payload = self.patch_payload(
            '/movies/1',
            token=self.director_token,
            patch=test_movie
        )

        self.assert_status(response, payload, 422, False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
