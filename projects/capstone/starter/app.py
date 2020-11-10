import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor


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
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    GET /movies
    Get all movies 
    """

    @app.route("/movies", methods=["GET"])
    def get_movies():

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
    def get_actors():

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
    def delete_movies(id):

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
    def delete_actors(id):

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
    def add_movie():
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
    def add_actor():
        body = request.get_json()
        if body is None:
            abort(400, "Missing field")

        name = body.get("name")
        age = body.get("age")
        gender = body.get("gender")
        movie_id = body.get("movie_id")

        actor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)
        actor.insert()

        return jsonify({"success": True, "actor": actor})

    return app


APP = create_app()

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=8080, debug=True)
