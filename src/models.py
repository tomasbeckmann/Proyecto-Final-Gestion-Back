from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User_rol(db.Model):
    __tablename__= "user_rol"
    id=  db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(250), nullable=False)
    
    def serialize(self):
        return {
          "name": self.name  
          }


class User(db.Model):
    __tablename__= "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    rut= db.Column(db.String(13), nullable=False)
    deleted= db.Column(db.Boolean(5), nullable=False, default= False)
    email = db.Column(db.String(250), unique= True)
    url_img = db.Column(db.String(250), unique= True, nullable=True)
    password = db.Column(db.String(250),unique=False, nullable=False)
    user_rol_id = db.Column(db.Integer, db.ForeignKey('user_rol.id'))
    user_rol= db.relationship(User_rol)

    def serialize(self):
        return {
        "id": self.id,
        "rol": self.user_rol_id,
        "name": self.name,
        "last_name": self.last_name,
        "email": self.email, 
        "url_img": self.url_img, 
        "rut":self.rut,
        "deleted": self.deleted
        }

class Document(db.Model):
    __tablename__="document"    
    id = db.Column(db.Integer, primary_key=True)   
    name = db.Column(db.String(250), nullable=False)  
    description = db.Column(db.String(250), nullable=False)
    link = db.Column(db.String(450), nullable=False)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)


    def serialize(self):
        return {
          "id": self.id,
          "user_name": self.user.name,
          "name": self.name, 
          "description": self.description,
          "link": self.link
          
          }



class Task(db.Model):
    tablename = "task"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250), nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    start_date = db.Column(db.String(10), nullable=False)
    end_date = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(1), nullable=False)
      
    def serialize(self):
        return {
          "id": self.id,
          "user_id": self.user_id,    
          "description": self.description,
          "start_date": self.start_date,
          "end_date": self.end_date,
          "status": self.status,
          "name": self.user.name,
          "last_name": self.user.last_name
          }


