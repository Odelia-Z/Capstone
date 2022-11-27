import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from models import db_drop_and_create_all, setup_db, Actor, Movie
from auth import AuthError, requires_auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    !! Running this function will add one
    '''
    db_drop_and_create_all()

    # Endpoints
    # GET /actors
    @app.route('/actors', methods=['GET'])
    def get_actors():
        actors = Actor.query.all()

        if len(actors) == 0 or actors is None:
            abort(404, "No actors found!")

        return jsonify({
            "success": True,
            "actors": [actor.long() for actor in actors]
        })

    # GET /movies
    @app.route('/movies', methods=['GET'])
    def get_movies():
        movies = Movie.query.all()

        if len(movies) == 0 or movies is None:
            abort(404, "No movies found!")

        return jsonify({
            "success": True,
            "movies": [movie.long() for movie in movies]
        })

    # DELETE /actors
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, id):
        actor = Actor.query.get(id)

        if not actor:
            abort(404, f"No actor found with id: {id}")

        try:
            actor.delete()

            return jsonify({
                "success": True,
                "delete": id
            })
        except Exception as e:
            abort(422, f"{str(e)}")

    # DELETE /movies
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, id):
        movie = Movie.query.get(id)

        if not movie:
            abort(404, f"No movie found with id: {id}")

        try:
            movie.delete()

            return jsonify({
                "success": True,
                "delete": id
            })
        except Exception as e:
            abort(422, f"{str(e)}")

    # POST /actors
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(jwt):
        j = request.get_json()

        if 'name' not in j:
            abort(422, "no name supplied")

        n = j['name']
        a = j['age']
        g = j['gender']

        try:
            actor = Actor(name=n, age=a, gender=g)
            actor.insert()

            return jsonify({
                "success": True,
                "actor": actor.long()
            })

        except Exception as e:
            abort(422, f"{str(e)}")

    # POST /movies
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(jwt):
        j = request.get_json()

        if 'title' not in j:
            abort(422, "no movie title supplied")

        t = j['title']
        d = j['release_date']

        try:
            movie = Movie(title=t, release_date=d)
            movie.insert()

            return jsonify({
                "success": True,
                "movie": movie.long()
            })

        except Exception as e:
            abort(422, f"{str(e)}")

    # PATCH /actors/
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, id):
        actor = Actor.query.get(id)

        if not actor:
            abort(404, f"No actor found with id {id}")

        j = request.get_json()
    
        try:
            if 'name' in j.keys():
                actor.name = j['name']
            if 'age' in j.keys():
                actor.age = j['age']
            if 'gender' in j.keys():
                actor.gender = j['gender']
            if not any(item in ['age', 'name', 'gender'] for item in list(j.keys())):
                raise Exception("Please specify name, age, and / or gender.")
        
            actor.update()

            return jsonify({
                "success": True,
                "actor": actor.long()
            })
        except Exception as e:
            abort(422, f"{str(e)}")

    # PATCH /movies/
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, id):
        movie = Movie.query.get(id)

        if not movie:
            abort(404, f"No movie found with id {id}")

        j = request.get_json()
        
        try:
            if 'title' in j.keys():
                movie.title = j['title']
            if 'release_date' in j.keys():
                movie.release_date = j['release_date']
            if not any(item in ['title', 'release_date'] for item in list(j.keys())):
                raise Exception("Please specify title and / or release_date.")

            movie.update()

            return jsonify({
                "success": True,
                "movie": movie.long()
            })
        except Exception as e:
            abort(422, f"{str(e)}")



    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": f"unprocessable, {error.description}"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": f"resource not found, {error.description}"
        })

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": f"Authentication error"
        })

    return app

app = create_app()

if __name__ == "__main__":
    # app = create_app
    app.debug = True
    app.run(host='0.0.0.0', port=8080, debug=True)
