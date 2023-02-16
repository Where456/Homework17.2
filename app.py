# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class MovieSchema(Schema):
    # id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Int()
    genre_id = fields.Int()
    genre = fields.Str()
    director_id = fields.Int()
    director = fields.Str()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

api = Api(app)
movie_ns = api.namespace('movies')


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


@movie_ns.route('/')
class ClassView(Resource):
    def get(self):
        note = db.session.query(Movie).all()
        return movies_schema.dump(note), 200


@movie_ns.route("/<int:bid>")
class ClassView(Resource):
    def get(self, bid: int):
        try:
            note = Movie.query.get(bid)
            return movie_schema.dump(note), 200
        except Exception as e:
            return "", 404

@movie_ns.route("/")
class ClassView(Resource):
    def get(self):
        result = []
        note = db.session.query(Movie).all()
        movies = movies_schema.dump(note)
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        if director_id:
            for i in movies:
                if i['director_id'] == director_id:
                    result.append(i)
        if genre_id:
            for i in movies:
                if i['genre_id'] == director_id:
                    result.append(i)
        return result


if __name__ == '__main__':
    app.run(debug=True)
