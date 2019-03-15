from flask_restplus import Api, Resource, fields
from flask import abort, json, make_response, request, url_for
from sqlalchemy import func
from movie import Movie
import random


def init_api_routes(app, session):
    if app:
        api = Api(app)
        movie_api = api.namespace('', description='Operations on movies')

        movie_model = api.model('Movie', {
                                'title': fields.String,
                                'genre': fields.String,
                                'year': fields.Integer})

        def getRandom():
                query = session.query(Movie)
                rowCount = int(query.count())
                randomRow = query.offset(int(rowCount*random.random())) \
                                 .first().movie_id
                return randomRow

        def getRandomGenre(genre):
                query = session.query(Movie)
                try:
                        randomRow = query.filter(Movie.genre == genre) \
                                 .order_by(func.random()) \
                                 .limit(1) \
                                 .one().movie_id
                except Exception as e:
                        randomRow = -1
                return randomRow

        @movie_api.route('/recommendation')
        class GetMovie(Resource):
                @movie_api.response(200, 'Success')
                @movie_api.response(404, 'Not Found')
                def get(self):
                        '''Gets a random movie'''
                        id = getRandom()
                        mv = session.query(Movie).filter_by(movie_id=id) \
                                                 .first()
                        if mv:
                                mv.recommended_count += 1
                                session.commit()
                                return mv.serialize(), 200
                        return "No movies in the database", 404

                @movie_api.response(200, 'Success')
                @movie_api.response(400, 'Bad Request')
                @movie_api.response(500, 'Internal Server Error')
                @movie_api.expect(movie_model)
                def post(self):
                        '''Creates a movie in the database'''
                        data = request.json
                        title = data["title"]
                        genre = data["genre"]
                        year = int(data["year"])
                        exists = session.query(Movie) \
                                        .filter_by(title=title,
                                                   genre=genre,
                                                   year=year).first()
                        if exists:
                                return "Movie already exists", 400
                        new_mv = Movie(title=title, genre=genre, year=year)
                        try:
                                session.add(new_mv)
                                session.commit()
                        except Exception as e:
                                return str(e), 500
                        return "Movie added to the database", 200

        @movie_api.route('/recommendation/<string:genre>')
        class GetMovieGenre(Resource):
                @movie_api.response(200, 'Success')
                @movie_api.response(404, 'Not Found')
                def get(self, genre):
                        '''Gets a random movie of a given Genre'''
                        id = getRandomGenre(genre)
                        mv = session.query(Movie).filter_by(movie_id=id) \
                                                 .first()
                        if mv:
                                mv.recommended_count += 1
                                session.commit()
                                return mv.serialize(), 200
                        return "No movies of genre: "+genre, 404

        @movie_api.route('/statistics')
        class GetMovieStatistics(Resource):
                @movie_api.response(200, 'Success')
                def get(self):
                        '''Gets the statistics'''
                        tot = session.query(func.sum(Movie.recommended_count))\
                                     .scalar()
                        count = session.query(func.count(Movie.movie_id))\
                                       .scalar()
                        if tot is None:
                                tot = 0
                        if count is None:
                                count = 0

                        data = {
                                        'total_recommendations': tot,
                                        'total_movies': count
                                }
                        response = json.dumps(data)
                        return data, 200
