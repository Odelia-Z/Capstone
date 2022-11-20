import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()


# binds a flask application and a SQLAlchemy service
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


# initialize a clean database
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # add one demo row which is helping in POSTMAN test
    #actor
    actor = Actor(
        name='Leonardo Wilhelm DiCaprio',
        age=48,
        gender='male',
    )
    actor.insert()
    #movie
    movie = Movie(
        title='Catch Me If You Can',
        release_date = '2002',
    )
    movie.insert()


# extends the base SQLAlchemy Model
# actor
class Actor(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    name = Column(String(180), unique=True, nullable=True)
    age = Column(String(80), nullable=True)
    gender = Column(String(80), nullable=True)

    # long()
    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }
    
    # insert()
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    # delete()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
  
    # update()
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.long())



# movie
class Movie(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(180), nullable=True)
    release_date = Column(String(180), nullable=True)

    # long()
    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }
    
    # insert()
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    # delete()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
  
    # update()
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.long())