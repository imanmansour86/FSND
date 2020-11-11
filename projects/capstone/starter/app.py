import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from controllers.auth import AuthError, requires_auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={"/*": {"origins": "*", "supports_credentials": True}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS"
        )
        return response

    """
    GET /movies
    Get all movies 
    """

    @app.route("/movies", methods=["GET"])
    @requires_auth("view:movie")
    def get_movies(payload):

        all_movies = Movie.query.all()
        movies = [movie.format() for movie in all_movies]
        if len(all_movies) == 0:
            abort(404, "no movies found")

        return jsonify({"success": "True", "movies": movies})

    """
    GET /actors
    Get all actors 
    """

    @app.route("/actors", methods=["GET"])
    @requires_auth("view:actor")
    def get_actors(payload):

        all_actors = Actor.query.all()
        actors = [actor.format() for actor in all_actors]
        if len(all_actors) == 0:
            abort(404, "no actors found")

        return jsonify({"success": "True", "actors": actors})

    """
    DELETE /movies/<int:id>
    Deletes movie by id
    """

    @app.route("/movies/<int:id>", methods=["Delete"])
    @requires_auth("delete:movie")
    def delete_movies(payload,id):

        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie is None:
            abort(404, "movie " + str(id) + " not found")

        movie.delete()

        return jsonify({"success": "True", "deleted": id})

    """
    DELETE /actors/<int:id>
    Deletes actors by id
    """

    @app.route("/actors/<int:id>", methods=["Delete"])
    @requires_auth("delete:actor")
    def delete_actors(payload,id):

        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor is None:
            abort(404, "actor " + str(id) + " not found")

        actor.delete()

        return jsonify({"success": "True", "deleted": id})

    """
    POST /movies
    Create a new movie
    """

    @app.route("/movies", methods=["POST"])
    @requires_auth("post:movie")
    def add_movie(payload):
        body = request.get_json()
        if "title" and "release_date" not in body:
            abort(422, "Missing field")

        title = body.get("title")
        release_date = body.get("release_date")

        movie = Movie(title=title, release_date=release_date)
        movie.insert()

        return jsonify({"success": True, "movie": movie.format()})

    """
    POST /actors
    Create a new actor
    """

    @app.route("/actors", methods=["POST"])
    @requires_auth("post:actor")
    def add_actor(payload):
        body = request.get_json()
        if "name" and "age" and 'gender' and 'movie_id' not in body:
            abort(422, "Missing field")

        name = body.get("name")
        age = body.get("age")
        gender = body.get("gender")
        movie_id = body.get("movie_id")

        actor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)
        actor.insert()

        return jsonify({"success": True, "actor": actor.format()})
    
    '''
    PATCH /movies/<int:id>
    Update movie with given id 
    '''
    @app.route("/movies//<int:id>", methods=["PATCH"])
    @requires_auth("patch:movie")
    def update_movie(payload,id):
        body = request.get_json()
        
        movie= Movie.query.filter(Movie.id == id).one_or_none()
        if movie is None:
            abort(404, "No movie with given id")
            
        if "title" in body:
            movie.title = body.get('title')
        if 'release_date' in body:
            movie.release_date = body.get('release_date')
        
        movie.update()
        
        return jsonify({"success": True, "updated": movie.format()})
    
    
    '''
    PATCH /actors/<int:id>
    Update actor with given id 
    '''
    @app.route("/actors//<int:id>", methods=["PATCH"])
    @requires_auth("patch:actor")
    def update_actor(payload,id):
        body = request.get_json()
        
        actor= Actor.query.filter(Actor.id == id).one_or_none()
        if actor is None:
            abort(404, "No actor with given id")
            
        if "name" in body:
            actor.name = body.get('name')
        if 'age' in body:
            actor.age = body.get('age')
        if 'gender' in body:
            actor.gender = body.get('gender')
        if 'movie_id' in body:
             actor.movie_id = body.get('movie_id')
        
        actor.update()
        
        return jsonify({"success": True, "updated": actor.format()})
    
    """
    Error Handling
    Example error handling for unprocessable entity
    """ 
    
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422
    
    @app.errorhandler(401)
    def unauthorized(error):
        return (
        jsonify({"success": False, "error": 401, "message": "unauthorized"}),
        401,
    )


    @app.errorhandler(404)
    def not_found(error):
        return (
        jsonify({"success": False, "error": 404, "message": "resource not found"}),
        404,
    )
    
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):

        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response
    
    

    return app


APP = create_app()

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=8080, debug=True)
