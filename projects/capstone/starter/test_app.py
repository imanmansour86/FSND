import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format(
            "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_movie = {"title": "testmovie", "release_date": "2023-1-2"}

        self.fail_movie = {
            "title": "testmovie",
        }

        self.fail_actor = {
            "name": "testactor",
            "age": "33",
            "gender": "female",
        }

        self.new_actor = {
            "name": "testactor",
            "age": "33",
            "gender": "female",
            "movie_id": 20,
        }

        self.casting_assistant = os.environ["casting_assistant"]
        self.casting_director = os.environ["casting_director"]
        self.executive_producer = os.environ["executive_producer"]

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies(self):
        auth_header = {"Authorization": "Bearer " + self.casting_assistant}
        res = self.client().get("/movies", headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], "True")
        self.assertTrue(data["movies"])

    def test_401_get_movies_fail(self):
        res = self.client().get("/movies")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], "authorization_header_missing")

    def test_get_actors(self):
        auth_header = {"Authorization": "Bearer " + self.casting_assistant}
        res = self.client().get("/actors", headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], "True")
        self.assertTrue(data["actors"])

    def test_401_get_actors_fail(self):
        res = self.client().get("/actors")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], "authorization_header_missing")

    def test_get_actors_directors(self):
        auth_header = {"Authorization": "Bearer " + self.casting_director}
        res = self.client().get("/actors", headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], "True")
        self.assertTrue(data["actors"])

    def test_get_actors_producer(self):
        auth_header = {"Authorization": "Bearer " + self.executive_producer}
        res = self.client().get("/actors", headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], "True")
        self.assertTrue(data["actors"])

    def test_delete_movies(self):
        auth_header = {"Authorization": "Bearer " + self.executive_producer}

        movie = Movie(title="newtitle", release_date="2021-1-2")
        movie.insert()
        id = movie.id
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        res = self.client().delete(f"/movies/{str(id)}", headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], "True")
        self.assertEqual(data["deleted"], id)

    def test_404_delete_movies(self):
        auth_header = {"Authorization": "Bearer " + self.executive_producer}

        res = self.client().delete("/movies/17856465", headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])

    def test_404_delete_movies_fail(self):
        auth_header = {"Authorization": "Bearer " + self.casting_director}

        movie = Movie(title="newtitle", release_date="2021-1-2")
        movie.insert()
        id = movie.id
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        res = self.client().delete(f"/movies/{str(id)}", headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["description"], "Permission not found")

    def test_404_delete_movies_fail(self):
        auth_header = {"Authorization": "Bearer " + self.casting_assistant}

        movie = Movie(title="newtitle", release_date="2021-1-2")
        movie.insert()
        id = movie.id
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        res = self.client().delete(f"/movies/{str(id)}", headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["description"], "Permission not found")

    def test_delete_actors(self):
        auth_header = {"Authorization": "Bearer " + self.executive_producer}

        actor = Actor(name="newname", age="24", gender="female", movie_id="20")
        actor.insert()
        id = actor.id
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        res = self.client().delete(f"/actors/{str(id)}", headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], "True")
        self.assertEqual(data["deleted"], id)

    def test_404_delete_actors_fail(self):
        auth_header = {"Authorization": "Bearer " + self.executive_producer}

        res = self.client().delete("/actors/806767", headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], "True")

    def test_delete_actors(self):
        auth_header = {"Authorization": "Bearer " + self.casting_director}

        actor = Actor(name="newname", age="24", gender="female", movie_id="20")
        actor.insert()
        id = actor.id
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        res = self.client().delete(f"/actors/{str(id)}", headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], "True")
        self.assertEqual(data["deleted"], id)

    def test_404_delete_actors_fail(self):
        auth_header = {"Authorization": "Bearer " + self.casting_assistant}

        actor = Actor(name="newname", age="24", gender="female", movie_id="20")
        actor.insert()
        id = actor.id
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        res = self.client().delete(f"/actors/{str(id)}", headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], "True")
        self.assertEqual(data["description"], "Permission not found")

    def test_404_delete_actors_fail(self):
        auth_header = {"Authorization": "Bearer " + self.casting_director}

        actor = Actor(name="newname", age="24", gender="female", movie_id="20")
        actor.insert()
        id = actor.id
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        res = self.client().delete(f"/actor/{str(id)}", headers=auth_header)
        data = json.loads(res.data)
        print(data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_create_movies(self):
        auth_header = {"Authorization": "Bearer " + self.executive_producer}

        res = self.client().post(f"/movies",
                                 json=self.new_movie, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_404_create_movies(self):
        auth_header = {"Authorization": "Bearer " + self.executive_producer}

        res = self.client().post(f"/movies/",
                                 json=self.fail_movie, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])

    def test_404_create_movie_fail(self):
        auth_header = {"Authorization": "Bearer " + self.casting_assistant}

        res = self.client().post(f"/movies/",
                                 json=self.new_movie, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])

    def test_404_create_movie_fail(self):
        auth_header = {"Authorization": "Bearer " + self.casting_director}

        res = self.client().post(f"/movies/",
                                 json=self.new_movie, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])

    def test_create_actor(self):
        auth_header = {"Authorization": "Bearer " + self.executive_producer}

        res = self.client().post(f"/actors",
                                 json=self.new_actor, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_422_create_actor_fail(self):
        auth_header = {"Authorization": "Bearer " + self.executive_producer}

        res = self.client().post(f"/actors",
                                 json=self.fail_actor, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])

    def test_create_actor(self):
        auth_header = {"Authorization": "Bearer " + self.casting_director}

        res = self.client().post(f"/actors",
                                 json=self.new_actor, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_create_actor_fail(self):
        auth_header = {"Authorization": "Bearer " + self.casting_assistant}

        res = self.client().post(f"/actors",
                                 json=self.new_actor, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_update_movies(self):
        auth_header = {"Authorization": "Bearer " + self.executive_producer}

        movie = Movie(title="newtitle", release_date="2021-1-2")
        movie.insert()
        id = movie.id
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        new_title = "test1"

        res = self.client().patch(
            f"/movies/{str(id)}",
            json={
                "title": new_title},
            headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_404_update_movies_fail(self):
        auth_header = {"Authorization": "Bearer " + self.executive_producer}

        new_title = "test1"

        res = self.client().patch(
            "/movies/780087", json={"title": new_title}, headers=auth_header
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_update_movies(self):
        auth_header = {"Authorization": "Bearer " + self.casting_director}

        movie = Movie(title="newtitle", release_date="2021-1-2")
        movie.insert()
        id = movie.id
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        new_title = "test1"

        res = self.client().patch(
            f"/movies/{str(id)}",
            json={
                "title": new_title},
            headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_update_actor(self):
        auth_header = {"Authorization": "Bearer " + self.executive_producer}

        actor = Actor(name="testactor", age="33", gender="female", movie_id=20)
        actor.insert()
        id = actor.id
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        res = self.client().patch(
            f"/actors/{str(id)}", json=self.new_actor, headers=auth_header
        )
        print(res)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_404_update_actor_fail(self):
        auth_header = {"Authorization": "Bearer " + self.executive_producer}

        new_name = "test"
        res = self.client().patch(
            f"/actors/{str(id)}", json={"name": new_name}, headers=auth_header
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])

    def test_404_update_actor_fail(self):
        auth_header = {"Authorization": "Bearer " + self.casting_assistant}

        new_name = "test"
        res = self.client().patch(
            f"/actors/{str(id)}", json={"name": new_name}, headers=auth_header
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])


if __name__ == "__main__":
    unittest.main()
