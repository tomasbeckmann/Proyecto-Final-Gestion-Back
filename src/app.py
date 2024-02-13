"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from datetime import timedelta
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, User_rol, Document, Activity, Task
from flask_jwt_extended import JWTManager,create_access_token, get_jwt_identity, jwt_required
from flask_bcrypt import Bcrypt
from flask_cors import CORS


app = Flask(__name__)
app.url_map.strict_slashes = False
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app)

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
else:
  app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY']= "SUPER-CLAVE_SECRETA"
app.config['SECRET_KEY']= "PALABRA_SECRETA"

app.config['SQLALCHEMY_ECHO'] = True   #ESTO SE DEBE ELIMINAR DESPUES

expire_jwt= timedelta(minutes=5)

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return generate_sitemap(app)

#User CRUD
@app.route('/user', methods=['POST'])
def create_user():
  get_from_body = request.json.get("email")
  user = User() 
  user_exist = User.query.filter_by(email=get_from_body).first()
  if user_exist is not None:
    return f"The User already exist", 409
  else:
    user.name= request.json.get("name")
    user.last_name= request.json.get("lastname")
    user.rut=  request.json.get("rut")
    user.deleted=  request.json.get("deleted")
    user.email=  request.json.get("email")
    password=  request.json.get("password")
    passwordHash= bcrypt.generate_password_hash(password)
    user.password = passwordHash
    user.user_rol_id= request.json.get("userrol_id")
    db.session.add(user)
    db.session.commit()
    
    return f"The user was created", 201
  
  #Login 
@app.route('/login', methods=['POST'])
def login():
  print(request.get_json())
  user= request.json.get("email")
  password= request.json.get("password")
  
  user_exist = User.query.filter_by(email= user).first()
  if user_exist is not None:
    if bcrypt.check_password_hash(user_exist.password, password):
        token= create_access_token(identity= user, expires_delta= expire_jwt)
        
        return jsonify({
          "token": token,
          "status": "success",
          "user": user_exist.serialize()
        }), 200
    else: 
       return f"Incorrect password", 400
  else:  
       return f"The user doesn't exist", 401
  

@app.route("/users", methods=['GET'])
def get_user():
  users = User.query.all()
  users= list(map(lambda user: user.serialize(), users))
  

  return jsonify({
    "data": users,
    "status": 'success'
  }),200

@app.route("/user/<int:id>", methods=['GET'])
def get_oneuser(id):
  user = User.query.filter_by(id=id).first()
  if user is not None:
    return jsonify(user.serialize()), 200
  else:
    return jsonify({"error":"User not found"}),404


@app.route("/user/<int:id>", methods=['DELETE'])
def delete_user(id):
  user = User.query.filter_by(id=id).first()
  if user is not None:
    db.session.delete(user)
    db.session.commit()
    return jsonify({
      "msg": "User deleted",
      "status": "Success"
    }), 203
  else:
    return jsonify({"error":"User not found"}),404

@app.route('/user', methods=["PUT"])
def update_user():
  email_to_search = request.json.get("email")
  user = User.query.filter_by(email=email_to_search).first()
  if user is None:
    return "The user does not exist", 401
  else:
    user.name= request.json.get("name")
    user.last_name= request.json.get("lastname")
    user.rut=  request.json.get("rut")
    user.deleted=  request.json.get("deleted")
    user.email=  request.json.get("email")
    user.password=  request.json.get("password")
    user.userrol_id= request.json.get("userrol_id")

    db.session.add(user)
    db.session.commit()

    return f"User updated", 201

#UserRol CRUD

@app.route('/user_rol', methods=['POST'])
def create_user_rol():
  get_from_body = request.json.get("id")
  user_rol = User_rol() 
  user_rol_exist = User_rol.query.filter_by(id=get_from_body).first()
  if user_rol_exist is not None:
    return "The User Role already exist"
  else:
    user_rol.name= request.json.get("name")
    db.session.add(user_rol)
    db.session.commit()
    
    return f"The user role was created", 201

@app.route("/user_rol/<int:id>", methods=['GET'])
def get_user_rol(id):
  user_rol = User_rol.query.filter_by(id=id).first()
  if user_rol is not None:
    return jsonify(user_rol.serialize()), 200
  else:
    return jsonify({"error":"User role not found"}),404

@app.route("/user_rol/<int:id>", methods=['DELETE'])
def delete_user_rol(id):
  user_rol = User_rol.query.filter_by(id=id).first()
  if user_rol is not None:
    db.session.delete(user_rol)
    db.session.commit()
    return jsonify({
      "msg": "User role deleted",
      "status": "Success"
    }), 203
  else:
    return jsonify({"error":"User role not found"}),404

@app.route("/user_rol", methods=["PUT"])
def update_user_rol():
  id_to_search = request.json.get("id")
  user_rol = User_rol.query.filter_by(id=id_to_search).first()
  if user_rol is None:
    return "The user role does not exist", 401
  else:
    user_rol.name= request.json.get("name")

    db.session.add(user_rol)
    db.session.commit()

    return f"User updated", 201

#Document CRUD

@app.route('/document', methods=['POST'])           
def create_document():
  search_for_id =request.json.get("user_id")
  search_for_name =request.json.get("name")
  document = Document() 
  document_exist = Document.query.filter_by(user_id=search_for_id ,name= search_for_name).first()
  if document_exist is not None:
    return jsonify({
       "success": False
    }),401
  else:
   document.name= request.json.get("name")
   document.description= request.json.get("description")
   document.link= request.json.get("link")
   document.user_id= request.json.get("user_id")

  db.session.add(document)
  db.session.commit()

  return f"The document was created", 201


@app.route("/document/<int:id>", methods=['GET'])
def get_document(id):
  document = Document.query.filter_by(id=id).first()
  if document is not None:
    return jsonify(document.serialize()), 200
  else:
    return jsonify({"error":"Document not found"}),404

@app.route("/document/<int:id>", methods=['DELETE'])
def delete_document(id):
  document = Document.query.filter_by(id=id).first()
  if document is not None:
    db.session.delete(document)
    db.session.commit()
    return jsonify({
      "msg": "Document deleted",
      "status": "Success"
    }), 203
  else:
    return jsonify({"error":"Document not found"}),404

@app.route('/document', methods=["PUT"])
def update_document():
  id_to_search = request.json.get("id")
  document= Document()
  document = Document.query.filter_by(id=id_to_search).first()
  if document is None:
    return "The document does not exist", 401
  else:
    document.name= request.json.get("name")
    document.description= request.json.get("description")
    document.link= request.json.get("link")
    document.user_id= request.json.get("user_id")
   

    db.session.add(document)
    db.session.commit()

    return f"Document updated", 201   


#Task CRUD

@app.route('/task', methods=['POST'])
def create_task():
  task = Task() 
  #search_id = request.json.get("id")
  #task_exist = Task.query.filter_by(user_id=search_id).first()
  #if task_exist is not None:
    #return "The task already exist"
  #else:
  task.name= request.json.get("name")
  task.description= request.json.get("description")
  
  db.session.add(task)
  db.session.commit()

  return jsonify({"msg": "The task was created",
                  "success": True
  }),201

@app.route("/task/<int:id>", methods=['GET'])
def get_task(id):
  task = Task.query.filter_by(id=id).first()
  if task is not None:
    return jsonify(task.serialize()), 200
  else:
    return jsonify({"error":"Task not found"}),404

@app.route("/task/<int:id>", methods=['DELETE'])
def delete_task(id):
  task = Task.query.filter_by(id=id).first()
  if task is not None:
    db.session.delete(task)
    db.session.commit()
    return jsonify({
      "msg": "Task deleted",
      "status": "Success"
    }), 203
  else:
    return jsonify({"error":"Task not found"}),404

@app.route('/task', methods=["PUT"])
def update_task():
  id_to_search = request.json.get("id")
  task = Task.query.filter_by(id=id_to_search).first()
  if task is None:
    return "The task does not exist", 401
  else:
    task.name= request.json.get("name")
    task.description= request.json.get("description")
    
    db.session.add(task)
    db.session.commit()

    return f"Task updated", 201        


#Activity CRUD

@app.route('/activity', methods=['POST'])
def create_activity():
  #get_from_body = request.json.get("id")
  activity = Activity() 
  #activity_exist = Activity.query.filter_by(user_id=get_from_body).first()
  #if activity_exist is not None:
   #return "The activity already exist"
  #else:
  activity.name= request.json.get("name")
  activity.place= request.json.get("place")
  activity.description= request.json.get("description")
  activity.date= request.json.get("date")
  activity.status= request.json.get("status")
  activity.user_id =request.json.get("user_id")
  activity.task_id =request.json.get("task_id")

  
  db.session.add(activity)
  db.session.commit()

  return f"The activity was created", 201

@app.route("/activity/<int:id>", methods=['GET'])
def get_activity(id):
  activity = Activity.query.filter_by(id=id).first()
  if activity is not None:
    return jsonify(activity.serialize()), 200
  else:
    return jsonify({"error":"Activity not found"}),404

@app.route("/activity/<int:id>", methods=['DELETE'])
def delete_activity(id):
  activity = Activity.query.filter_by(id=id).first()
  if activity is not None:
    db.session.delete(activity)
    db.session.commit()
    return jsonify({
      "msg": "Activity deleted",
      "status": "Success"
    }), 203
  else:
    return jsonify({"error":"Activity not found"}),404

@app.route('/activity', methods=["PUT"])
def update_activity():
  id_to_search = request.json.get("id")
  activity = Activity.query.filter_by(id=id_to_search).first()
  if activity is None:
    return "The activity does not exist", 401
  else:
    activity.name= request.json.get("name")
    activity.description= request.json.get("description")
    activity.date= request.json.get("date")
    activity.status= request.json.get("status")
    activity.user_id= request.json.get("user_id")
    activity.task_id= request.json.get("task_id")
    
    db.session.add(activity)
    db.session.commit()

    return f"Activity updated", 201


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
