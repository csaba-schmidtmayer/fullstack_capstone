# IMPORTS
from flask import Flask, request, abort, jsonify
from flask_migrate import Migrate
from flask_cors import CORS

from models import setup_db, db, Movie, Actor
from auth import AuthError, requires_auth

PAGE_LENGTH = 10


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # ENDPOINTS

    # MOVIES

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_paginated_movies():
        page = request.args.get('page', 1, type=int)
        movies = Movie.query.order_by('release_date').all()
        paginated_movies = movies[
                           (page - 1) * PAGE_LENGTH : page * PAGE_LENGTH
                           ]
        if len(paginated_movies) > 0:
            return jsonify({
                'success': True,
                'movies': [movie.format() for movie in paginated_movies],
                'total_movies': len(movies),
                'current_page': page
            })
        else:
            abort(404, 'The requested page is beyond the valid range.')

    @app.route('/movies/<int:movie_id>')
    @requires_auth('get:movies')
    def get_specific_movie(movie_id):
        movie = Movie.query.get(movie_id)
        if movie is not None:
            return jsonify({
                'success': True,
                'movie': movie.format()
            })
        else:
            abort(404, f'Movie with id {movie_id} does not exist.')

    @app.route('/movies', methods=['POST'])
    @requires_auth('add:movies')
    def add_new_movie():
        success = True

        title = request.json.get('title', None)
        if title is None:
            abort(400, 'Missing field \'title\'.')

        release_date = request.json.get('release_date', None)
        if release_date is None:
            abort(400, 'Missing field \'release_date\'.')

        existing_movie = Movie.query.filter(
            Movie.title.ilike(title)).first()
        if existing_movie is not None:
            abort(409, 'The movie already exists.')

        try:
            new_movie = Movie(
                title=title,
                release_date=release_date
            )
            new_movie.insert()
        except Exception as e:
            db.session.rollback()
            success = False
        finally:
            db.session.close()

        if success:
            return jsonify({
                'success': True
            }), 201
        else:
            abort(500, 'Adding the movie to the database was unsuccessful.')

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('modify:movies')
    def update_movie(movie_id):
        success = True
        upd_movie = Movie.query.get(movie_id)

        if upd_movie is None:
            abort(404, f'Movie id {movie_id} does not exist.')

        title = request.json.get('title', None)
        if title is not None:
            upd_movie.title = title

        release_date = request.json.get('release_date', None)
        if release_date is not None:
            upd_movie.release_date = release_date

        try:
            upd_movie.update()
        except Exception as e:
            db.session.rollback()
            err_msg = str(e)
            success = False
        else:
            response = jsonify({
                'success': True,
                'movie': upd_movie.format()
            })
        finally:
            db.session.close()

        if success:
            return response, 200
        else:
            abort(500, err_msg)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(movie_id):
        success = True
        del_movie = Movie.query.get(movie_id)

        if del_movie is None:
            abort(404, f'Movie id {movie_id} does not exist')

        try:
            del_movie.delete()
        except Exception as e:
            db.session.rollback()
            err_msg = str(e)
            success = False
        else:
            response = jsonify({
                'success': True,
                'delete': movie_id
            })
        finally:
            db.session.close()

        if success:
            return response, 200
        else:
            abort(500, err_msg)

    # ACTORS

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_paginated_actors():
        page = request.args.get('page', 1, type=int)
        actors = Actor.query.order_by('id').all()
        paginated_actors = actors[
                           (page - 1) * PAGE_LENGTH : page * PAGE_LENGTH
                           ]
        if len(paginated_actors) > 0:
            return jsonify({
                'success': True,
                'actors': [actor.format() for actor in paginated_actors],
                'total_actors': len(actors),
                'current_page': page
            })
        else:
            abort(404, 'The requested page is beyond the valid range.')

    @app.route('/actors/<int:actor_id>')
    @requires_auth('get:actors')
    def get_specific_actor(actor_id):
        actor = Actor.query.get(actor_id)
        if actor is not None:
            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        else:
            abort(404, f'Actor with id {actor_id} does not exist.')

    @app.route('/actors', methods=['POST'])
    @requires_auth('add:actors')
    def add_new_actor():
        success = True

        name = request.json.get('name', None)
        if name is None:
            abort(400, 'Missing field \'name\'.')

        age = request.json.get('age', None)
        if age is None:
            abort(400, 'Missing field \'age\'.')

        gender = request.json.get('gender', None)
        if gender is None:
            abort(400, 'Missing field \'gender\'.')
        elif gender not in ['male', 'female']:
            abort(400, 'The value of the field \'gender\' must be either of ' +
                  '\'male\' or \'female\'.')

        existing_actor = Actor.query.filter(
            Actor.name.ilike(name)).first()
        if existing_actor is not None:
            abort(409, 'The actor already exists.')

        try:
            new_actor = Actor(
                name=name,
                age=age,
                gender=gender
            )
            new_actor.insert()
        except Exception as e:
            db.session.rollback()
            success = False
        finally:
            db.session.close()

        if success:
            return jsonify({
                'success': True
            }), 201
        else:
            abort(500, 'Adding the actor to the database was unsuccessful.')

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('modify:actors')
    def update_actor(actor_id):
        success = True
        upd_actor = Actor.query.get(actor_id)

        if upd_actor is None:
            abort(404, f'Actor id {actor_id} does not exist.')

        name = request.json.get('name', None)
        if name is not None:
            existing_actor = Actor.query.filter(
                Actor.name.ilike(name)).first()
            if existing_actor is not None:
                abort(409, 'Another actor with the same name already exists.')
            upd_actor.name = name

        age = request.json.get('age', None)
        if age is not None:
            upd_actor.age = age

        gender = request.json.get('gender', None)
        if gender is not None:
            upd_actor.gender = gender

        try:
            upd_actor.update()
        except Exception as e:
            db.session.rollback()
            err_msg = str(e)
            success = False
        else:
            response = jsonify({
                'success': True,
                'actor': upd_actor.format()
            })
        finally:
            db.session.close()

        if success:
            return response, 200
        else:
            abort(500, err_msg)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(actor_id):
        success = True
        del_actor = Actor.query.get(actor_id)

        if del_actor is None:
            abort(404, f'Actor id {actor_id} does not exist')

        try:
            del_actor.delete()
        except Exception as e:
            db.session.rollback()
            err_msg = str(e)
            success = False
        else:
            response = jsonify({
                'success': True,
                'delete': actor_id
            })
        finally:
            db.session.close()

        if success:
            return response, 200
        else:
            abort(500, err_msg)

    # ERROR HANDLING

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': error.description
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': error.description
        }), 404

    @app.errorhandler(409)
    def conflict(error):
        return jsonify({
            'success': False,
            'error': 409,
            'message': error.description
        }), 409

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': error.description
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(e):
        return jsonify({
            'success': False,
            'error': e.status_code,
            'message': e.error['description']
        }), e.status_code

    return app
