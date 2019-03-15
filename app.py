from flask import Flask, json, Response
from flask_cors import CORS

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from routes import init_api_routes
from model import Model

db_string = ("postgres://vywhwbzvzxprkq:"
             "2f7083fed0106103e25ce5300750f5a8af50678ae11710731e61692e7deab729"
             "@ec2-54-225-76-201.compute-1.amazonaws.com:5432/d58h3832oj43d6")

db_engine = create_engine(db_string)
Model.metadata.create_all(db_engine)
db_session = sessionmaker(bind=db_engine)
session = db_session()
app = Flask(__name__)

print(session)

init_api_routes(app, session)

app.config['SECRET_KEY'] = 'PythonFlaskMovieRecommedationByKrishnaKaranam'
CORS(app)

if __name__ == '__main__':
    app.run()
