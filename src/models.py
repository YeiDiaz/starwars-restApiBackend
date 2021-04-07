from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

               
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(550))
    diameter = db.Column(db.String(100))
    rotation_period = db.Column(db.String(100))
    orbital_period = db.Column(db.String(100))
    gravity = db.Column(db.String(100))
    population = db.Column(db.String(100))
    Climate = db.Column(db.String(100))
    terrain = db.Column(db.String(100))
    surface_water = db.Column(db.String(100))
    imgPlanet = db.Column(db.String(300))
    entity = db.Column(db.String(100))
    

    def __repr__(self):
        return '<Planets %r>' % self.full_name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "Climate": self.Climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "imgPlanet": self.imgPlanet,
            "entity": self.entity,
                             
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(550))
    height = db.Column(db.String(100))
    mass = db.Column(db.String(100))
    hair_color = db.Column(db.String(100))
    eye_color = db.Column(db.String(100))
    skin_color = db.Column(db.String(100))
    birth_year = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    imgCharacter = db.Column(db.String(300))
    entity = db.Column(db.String(100))
 

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "skin_color": self.skin_color,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "imgCharacter": self.imgCharacter,
            "entity": self.entity,
           
            # do not serialize the password, its a security breach
        }

   

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)
    favorites = db.relationship("Favorites", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "favorites": list(map(lambda x: x.serialize(), self.favorites))
            # do not serialize the password, its a security breach
        }
        

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tipo = db.Column(db.String(100))
    object_id = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id":self.user_id,
            "tipo": self.tipo,
            "object_id": self.object_id, #PARA QUE SIRVE ESTO
                    
            # do not serialize the password, its a security breach
        }
