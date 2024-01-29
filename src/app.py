"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

#db_url = os.getenv("DATABASE_URL")
#if db_url is not None:
   # app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
#else:
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#Creating an user
@app.route('/user', methods=['POST'])
def creating_user():
  get_from_body = request.json.get("email")
  user = User() 
  user_exist = User.query.filter_by(email=get_from_body).first()
  if user_exist is not None:
    return "The User already exist"
  else:
    user.name= request.json.get("name")
    user.last_name= request.json.get("lastname")
    user.rut=  request.json.get("rut")
    user.deleted=  request.json.get("deleted") #Verificar si se deja
    user.email=  request.json.get("email")
    user.password=  request.json.get("password")
    user.userrol_id= request.json.get("userrol_id")


    return f"The user was created", 201

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
