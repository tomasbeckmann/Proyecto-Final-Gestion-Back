from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__= "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    rut= db.Column(db.String(13), nullable=False)
    deleted= db.Column(db.Boolean(5), nullable=False)
    email = db.Column(db.String(250), unique= True)
    password = db.Column(db.String(250),unique=False, nullable=False)
    userrol_id = Column(Integer, ForeignKey('userrol.id'))
    user_rol= db.relationship(UserRol)

    

    def serialize(self):
        return {
        "id": self.id,
        "name": self.name,
        "last_name": self.last_name,
        "email": self.email, 
        "rut":self.rut
        }

class UserRol(db.Model):
    __tablename__= "userrol"
    id=  db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(250), nullable=False)
    
    def serialize(self):
        return {
          "name": self.name  
          }

class Document(db.Model):
    __tablename__="document"    
    id = db.Column(db.Integer, primary_key=True)   
    name = db.Column(db.String(250), nullable=False)  
    description = db.Column(db.String(250), nullable=False)
    link = db.Column(db.String(450), nullable=False)
    user_id= db.Column(Integer, ForeignKey('user.id'))
    user = db.relationship(User)


    def serialize(self):
        return {
          "id": self.id,
          "name": self.name, 
          "description": self.description,
          "link": self.link
          }

class Activity(db.Model):
    __tablename__="activity"     
     id= db.Column(db.Integer, primary_key=True) 
     name = db.Column(db.String(250), nullable=False)  
     place = db.Column(db.String(250), nullable=False)  
     description= db.Column(db.String(250), nullable=False)
     date= db.Column(db.datetime.now(), nullable=False)
     status= db.Column(db.Integer, nullable=False)


class Task(db.Model):
    tablename = "task"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)  