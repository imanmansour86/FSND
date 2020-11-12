
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
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
         # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_movie= {
            'title': 'testmovie',
            'release_date': '2023-1-2'
        }
        
        self.fail_movie= {
            'title': 'testmovie',
        }
        
        self.fail_actor= {
            'name': 'testactor',
            'age': '33',
            'gender': 'female',
        }
        
        self.new_actor= {
            'name': 'testactor',
            'age': '33',
            'gender': 'female',
            'movie_id': 20
           
        }
        
        self.casting_assistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFfY292YUo5bG9QNEx6OTJsbTM1MiJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLXByb2plY3QxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZmFiMGE0NzlhYjJkMDAwNzZmNWIyZjUiLCJhdWQiOiJjYXN0IiwiaWF0IjoxNjA1MTU1MDMzLCJleHAiOjE2MDUyNDE0MzMsImF6cCI6ImE0WnFNbEFLbXhXYjJJODFnVVFxekNWYkxjMWl1dTM3Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJ2aWV3OmFjdG9yIiwidmlldzptb3ZpZSJdfQ.mCt5HJooc-Gyf4jsSTVsn7R9Q26ExVAnKlSDIfOUZeo5aaWlCI_OseZ_5VVR_ucMjViHANWwefvG45GeNM3BNeacuwMj2ZfIf53UyfQ40lQIwibyFcJuoNP_Fq-3wE3Y7CyRG_34D-5lNTWIyDJV53v6CjRFI7O4cs145X90OQOY464V-P4WMZcXF7uksaJYRGk5kS2clXmOl1wAATmlXurfx2SpGoR243I0ZmXpD8EM82RDeSQ3JnBvBioM9FXv0GHVfCPO8vQH59vmygGcwqQoqE202zGythUtMF3uRPfRbTxZ060X5AcPTTLh5v-j53Ax2uZLS0XAAi5akWfWAQ'
        self.casting_director='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFfY292YUo5bG9QNEx6OTJsbTM1MiJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLXByb2plY3QxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZmFiMDkxZTc1ODg0NzAwNjkyOWIzYzAiLCJhdWQiOiJjYXN0IiwiaWF0IjoxNjA1MTYwMTQzLCJleHAiOjE2MDUyNDY1NDMsImF6cCI6ImE0WnFNbEFLbXhXYjJJODFnVVFxekNWYkxjMWl1dTM3Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IgIiwiZGVsZXRlOmFjdG9ycyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwidmlldzphY3RvciIsInZpZXc6bW92aWUiXX0.p7rehdmgc4yAHiK13h4vzBY6f64MCRehv2jpJeVBM9sxT1hcOwWOmi1JY32hrCZeaoxkOrAn2Y0VOCT8cLl16TE8xNoQ7zpZxgSDJjUjpzoKm8toQE7AYWTdecaHodl1JPTsP_2pgvAfwrGEich-C1wflURaD2JFXA3Ej8Kr_1HKyKR6mU8Ibm6oHYvClSNI7rIAoQEhMKlQHpC0cwPZTkGIpGd-IKdbtHMnTxwCcpUyL58ogknYydLyB3cZm6MI8gm6e5QSmBwJUo-lJKfHB-b4LCC7qNemPd9JmrGxFx_LKzOeQZqcawMb-YsWE85yVs1f0il9Wb_K6q_ex1FbUw'
        self.executive_producer='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFfY292YUo5bG9QNEx6OTJsbTM1MiJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLXByb2plY3QxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZmFiMDQ0ODFhMzBhZjAwNmYzMTM4MjEiLCJhdWQiOiJjYXN0IiwiaWF0IjoxNjA1MTU5NzI4LCJleHAiOjE2MDUyNDYxMjgsImF6cCI6ImE0WnFNbEFLbXhXYjJJODFnVVFxekNWYkxjMWl1dTM3Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IgIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZSIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSIsInZpZXc6YWN0b3IiLCJ2aWV3Om1vdmllIl19.FCttjiEJx0e7sv4XHZLJhKEOlTplIce4_960pcqagGjnKT8247ql2k4HbJaw3VxEnfZQxBd20u-5owiQoSyX5JtWdlRBySDHJJ9ZdhqpNf2tUEuVnmqXeuXBPNya4r4klWpUaVcsIXJwmPMPbwCsCHhghbc-qz5dvquupDDgf6fsIdd3hAfG_twF8OeWKJFPjzWzJETJdJhH6snk440PNAoJk1oT--ywIABWJpkaP2JH1YiWQRewVVwGKVw9aHLB08V43W647XaAt77rSfi08dEgAfF6PSXgCqIRf-u8PWGxo0u0nkgoFxG5F-ipmrob1hdgjtW-xN7155U3ydxGxg'
        
    def tearDown(self):
        """Executed after reach test"""
        pass
        
    def test_get_movies(self):
        auth_header= {"Authorization": "Bearer " +self.casting_assistant}
        res = self.client().get('/movies', headers=auth_header)
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertTrue(data['movies'])
        
    def test_401_get_movies_fail(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
    
    
    def test_get_actors(self):
        auth_header= {"Authorization": "Bearer " +self.casting_assistant}
        res = self.client().get('/actors', headers=auth_header)
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertTrue(data['actors'])
    
    
    def test_401_get_actors_fail(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
   
   
    def test_get_actors_directors(self):
        auth_header= {"Authorization": "Bearer " +self.casting_director}
        res = self.client().get('/actors', headers=auth_header)
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertTrue(data['actors'])
        
    def test_get_actors_producer(self):
        auth_header= {"Authorization": "Bearer " +self.executive_producer}
        res = self.client().get('/actors', headers=auth_header)
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertTrue(data['actors'])
        
    
    def test_delete_movies(self):
        auth_header= {"Authorization": "Bearer " +self.executive_producer}
        
        movie= Movie(title='newtitle',release_date='2021-1-2')
        movie.insert()
        id= movie.id
        movie= Movie.query.filter(Movie.id == id).one_or_none()
        
        res = self.client().delete(f'/movies/{str(id)}', headers=auth_header)
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertEqual(data['deleted'], id)
        
    def test_404_delete_movies(self):
        auth_header= {"Authorization": "Bearer " +self.executive_producer}
        
        res = self.client().delete('/movies/17856465', headers=auth_header)
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
       
        
    def test_404_delete_movies_fail(self):
        auth_header= {"Authorization": "Bearer " +self.casting_director}
        
        movie= Movie(title='newtitle',release_date='2021-1-2')
        movie.insert()
        id= movie.id
        movie= Movie.query.filter(Movie.id == id).one_or_none()
        
        
        res = self.client().delete(f'/movies/{str(id)}', headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'Permission not found')
        
    def test_404_delete_movies_fail(self):
        auth_header= {"Authorization": "Bearer " +self.casting_assistant}
        
        movie= Movie(title='newtitle',release_date='2021-1-2')
        movie.insert()
        id= movie.id
        movie= Movie.query.filter(Movie.id == id).one_or_none()
        
        
        res = self.client().delete(f'/movies/{str(id)}', headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'Permission not found')
        
    
    def test_delete_actors(self):
        auth_header= {"Authorization": "Bearer " +self.executive_producer}
        
        actor= Actor(name='newname',age= '24', gender='female',movie_id= '20')
        actor.insert()
        id= actor.id
        actor= Actor.query.filter(Actor.id == id).one_or_none()
        
        res = self.client().delete(f'/actors/{str(id)}', headers=auth_header)
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertEqual(data['deleted'], id)
        
    def test_404_delete_actors_fail(self):
        auth_header= {"Authorization": "Bearer " +self.executive_producer}
        
        res = self.client().delete('/actors/806767', headers=auth_header)
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], 'True')
      
        
    def test_delete_actors(self):
        auth_header= {"Authorization": "Bearer " +self.casting_director}
        
        actor= Actor(name='newname',age= '24', gender='female',movie_id= '20')
        actor.insert()
        id= actor.id
        actor= Actor.query.filter(Actor.id == id).one_or_none()
        
        res = self.client().delete(f'/actors/{str(id)}', headers=auth_header)
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], 'True')
        self.assertEqual(data['deleted'], id)
        
        
    def test_404_delete_actors_fail(self):
        auth_header= {"Authorization": "Bearer " +self.casting_assistant}
        
        actor= Actor(name='newname',age= '24', gender='female',movie_id= '20')
        actor.insert()
        id= actor.id
        actor= Actor.query.filter(Actor.id == id).one_or_none()
        
        res = self.client().delete(f'/actors/{str(id)}', headers=auth_header)
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], 'True')
        self.assertEqual(data['description'], 'Permission not found')
        
    def test_404_delete_actors_fail(self):
        auth_header= {"Authorization": "Bearer " +self.casting_director}
        
        actor= Actor(name='newname',age= '24', gender='female',movie_id= '20')
        actor.insert()
        id= actor.id
        actor= Actor.query.filter(Actor.id == id).one_or_none()
        
        res = self.client().delete(f'/actor/{str(id)}', headers=auth_header)
        data = json.loads(res.data)
        print(data)
    
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        
    
    def test_create_movies(self):
        auth_header= {"Authorization": "Bearer " +self.executive_producer}
        
        res = self.client().post(f'/movies',json=self.new_movie, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    def test_404_create_movies(self):
        auth_header= {"Authorization": "Bearer " +self.executive_producer}
    

        res = self.client().post(f'/movies/',json=self.fail_movie, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        
   
    def test_404_create_movie_fail(self):
        auth_header= {"Authorization": "Bearer " +self.casting_assistant}
    

        res = self.client().post(f'/movies/',json=self.new_movie, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        
    def test_404_create_movie_fail(self):
        auth_header= {"Authorization": "Bearer " +self.casting_director}
    

        res = self.client().post(f'/movies/',json=self.new_movie, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        
        
    
    def test_create_actor(self):
        auth_header= {"Authorization": "Bearer " +self.executive_producer}
        
        res = self.client().post(f'/actors',json=self.new_actor, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        
    def test_422_create_actor_fail(self):
        auth_header= {"Authorization": "Bearer " +self.executive_producer}
        
        res = self.client().post(f'/actors',json=self.fail_actor, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        
    def test_create_actor(self):
        auth_header= {"Authorization": "Bearer " +self.casting_director}
        
        res = self.client().post(f'/actors',json=self.new_actor, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    def test_create_actor_fail(self):
        auth_header= {"Authorization": "Bearer " +self.casting_assistant}
        
        res = self.client().post(f'/actors',json=self.new_actor, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        
    def test_update_movies(self):
        auth_header= {"Authorization": "Bearer " +self.executive_producer}
        
        movie= Movie(title='newtitle',release_date='2021-1-2')
        movie.insert()
        id= movie.id
        movie= Movie.query.filter(Movie.id == id).one_or_none()
        new_title="test1"
        
        res = self.client().patch(f'/movies/{str(id)}', json={ 'title': new_title},headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    def test_404_update_movies_fail(self):
        auth_header= {"Authorization": "Bearer " +self.executive_producer}
        
        new_title="test1"
        
        res = self.client().patch('/movies/780087', json={ 'title': new_title}, headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
    
    def test_update_movies(self):
        auth_header= {"Authorization": "Bearer " +self.casting_director}
        
        movie= Movie(title='newtitle',release_date='2021-1-2')
        movie.insert()
        id= movie.id
        movie= Movie.query.filter(Movie.id == id).one_or_none()
        new_title="test1"
        
        res = self.client().patch(f'/movies/{str(id)}', json={ 'title': new_title},headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
       
    def test_update_actor(self):
        auth_header= {"Authorization": "Bearer " +self.executive_producer}
        
        actor= Actor(name='testactor',age='33',gender='female',movie_id= 20)
        actor.insert()
        id= actor.id
        actor= Actor.query.filter(Actor.id == id).one_or_none()
        
        res = self.client().patch(f'/actors/{str(id)}', json=self.new_actor, headers=auth_header)
        print(res)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        
            
        
    def test_404_update_actor_fail(self):
        auth_header= {"Authorization": "Bearer " +self.executive_producer}
        
        new_name='test'
        res = self.client().patch(f'/actors/{str(id)}', json={ 'name': new_name},headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        
    def test_404_update_actor_fail(self):
        auth_header= {"Authorization": "Bearer " +self.casting_assistant}
        
        new_name='test'
        res = self.client().patch(f'/actors/{str(id)}', json={ 'name': new_name},headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        
        
        
if __name__ == "__main__":
    unittest.main()