from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from passlib.hash import sha256_crypt
import datetime
import bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this to a random secret key

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

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

@app.route('/get', methods=['GET'])
def get_articles():
    all_articles = Articles.query.all()
    results = [article_to_dict(article) for article in all_articles]
    return jsonify(results)

@app.route('/get/<int:id>/', methods=['GET'])
def get_article(id):
    article = Articles.query.get(id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404
    return jsonify
