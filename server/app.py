from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from passlib.hash import sha256_crypt
import bcrypt
from uuid import uuid4
from extensions import db
import datetime
from auth import auth_bp

def create_app():

    app = Flask(__name__)

    app.config.from_prefixed_env()

    #initialize ext
    db.init_app(app)

    #register blueprints
    app.register_blueprint(auth_bp,url_prefix='/auth')

    return app



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this to a random secret key

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(), primary_key=True, default =(uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email =db.Column(db.String(),nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User('{self.username}>"

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

class Articles(db.Model):
    __tablename__ = 'Articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25))
    body = db.Column(db.String(25))
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, title, body):
        self.title = title
        self.body = body

def article_to_dict(article):
    return {
        'id': article.id,
        'title': article.title,
        'body': article.body,
        'date': article.date.strftime('%Y-%m-%d %H:%M:%S')
    }

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({"msg": "Invalid username or password"}), 401
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@app.route('/get', methods=['GET'])
@jwt_required()
def get_articles():
    all_articles = Articles.query.all()
    results = [article_to_dict(article) for article in all_articles]
    return jsonify(results)

@app.route('/get/<int:id>/', methods=['GET'])
@jwt_required()
def get_article(id):
    article = Articles.query.get(id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404
    return jsonify(article_to_dict(article))

if __name__ == '__main__':
    app.run(debug=True)
