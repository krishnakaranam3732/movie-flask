from sqlalchemy import Column, String, Integer
from model import Model

from pyld import jsonld


class Movie(Model):
    """
        The movie model
    """
    __tablename__ = 'movies'

    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=True)
    genre = Column(String(50), nullable=True)
    year = Column(Integer, nullable=False)
    recommended_count = Column(Integer, nullable=False, default=0)

    def __init__(self, title, genre, year):
        self.title = title
        self.genre = genre
        self.year = year

    def serialize(self):
        compacted_json = jsonld.compact({
            "http://schema.org/movie_id": self.movie_id,
            "http://schema.org/title": self.title,
            "http://schema.org/genre": self.genre,
            "http://schema.org/year": self.year,
            "http://schema.org/recommended_count": self.recommended_count
        }, self.get_context())
        del compacted_json['@context']
        return compacted_json

    def get_context(self):
        return {
            "@context": {
                "movie_id": "http://schema.org/movie_id",
                "title": "http://schema.org/title",
                "genre": "http://schema.org/genre",
                "year": "http://schema.org/year",
                "recommended_count": "http://schema.org/recommended_count"
            }
        }