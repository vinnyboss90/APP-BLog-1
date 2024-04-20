# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# import datetime
# from flask_migrate import Migrate
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# class Articles(db.Model):
#     __tablename__ = 'Articles'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(25))
#     body = db.Column(db.String(25))
#     date = db.Column(db.DateTime, default=datetime.datetime.now)

#     def __init__(self, title, body):
#         self.title = title
#         self.body = body

# def article_to_dict(article):
#     return {
#         'id': article.id,
#         'title': article.title,
#         'body': article.body,
#         'date': article.date.strftime('%Y-%m-%d %H:%M:%S')
#     }

# @app.route('/get', methods=['GET'])
# def get_articles():
#     all_articles = Articles.query.all()
#     if not all_articles:
#         return jsonify([])  # Return an empty list if there are no articles

#     results = [article_to_dict(article) for article in all_articles]
#     return jsonify(results)


# @app.route('/get/<int:id>/', methods=['GET'])
# def get_article(id):
#     article = Articles.query.get(id)
#     if not article:
#         return jsonify({'error': 'Article not found'}), 404

#     return jsonify(article_to_dict(article))

# from flask import jsonify, request

# @app.route('/add', methods=['POST'])
# def add_article():
#     title = request.json.get('title')
#     body = request.json.get('body')

#     article = Articles(title=title, body=body)
#     db.session.add(article)
#     db.session.commit()
#     db.create_all()
#     return jsonify(article_to_dict(article))

# @app.route('/update/<int:id>/', methods=['PUT'])
# def update_article(id):
#     article = Articles.query.get(id)
#     if not article:
#         return jsonify({'error': 'Article not found'}), 404

#     article.title = request.json.get('title', article.title)
#     article.body = request.json.get('body', article.body)
#     db.session.commit()

#     return jsonify(article_to_dict(article))

# @app.route('/delete/<int:id>/', methods=['DELETE'])
# def delete_article(id):
#     article = Articles.query.get(id)
#     if not article:
#         return jsonify({'error': 'Article not found'}), 404

#     db.session.delete(article)
#     db.session.commit()

#     return jsonify(article_to_dict(article))


# if __name__ == '__main__':
#     app.run(debug=True)















# from flask import Flask, jsonify, request
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required
# from flask_cors import CORS

# app = Flask(__name__)
# app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a random secret key
# jwt = JWTManager(app)
# CORS(app)

# users = {
#     "test@example.com": {
#         "password": "password123"
#     }
# }

# @app.route('/login', methods=['POST'])
# def login():
#     email = request.json.get('email', None)
#     password = request.json.get('password', None)
#     if email not in users or users[email]['password'] != password:
#         return jsonify({"message": "Invalid credentials"}), 401
#     access_token = create_access_token(identity=email)
#     return jsonify({"token": access_token}), 200

# @app.route('/signup', methods=['POST'])
# def signup():
#     email = request.json.get('email', None)
#     password = request.json.get('password', None)
#     if email in users:
#         return jsonify({"message": "Email already exists"}), 400
#     users[email] = {"password": password}
#     access_token = create_access_token(identity=email)
#     return jsonify({"token": access_token}), 200

# @app.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     email = get_jwt_identity()
#     return jsonify(logged_in_as=email), 200

# if __name__ == '__main__':
#     app.run(debug=True)
















from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
import jwt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration for JWT
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a random secret key
jwt = JWTManager(app)

# Configuration for SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Model for articles
class Articles(db.Model):
    __tablename__ = 'Articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25))
    body = db.Column(db.String(25))
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S')
        }

# Routes for articles
@app.route('/get', methods=['GET'])
def get_articles():
    all_articles = Articles.query.all()
    if not all_articles:
        return jsonify([])  # Return an empty list if there are no articles

    results = [article.to_dict() for article in all_articles]
    return jsonify(results)

@app.route('/get/<int:id>/', methods=['GET'])
def get_article(id):
    article = Articles.query.get(id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404

    return jsonify(article.to_dict())

@app.route('/add', methods=['POST'])
def add_article():
    data = request.get_json()
    title = data.get('title')
    body = data.get('body')

    article = Articles(title=title, body=body)
    db.session.add(article)
    db.session.commit()
    return jsonify(article.to_dict()), 201

@app.route('/update/<int:id>/', methods=['PUT'])
def update_article(id):
    article = Articles.query.get(id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404

    data = request.get_json()
    article.title = data.get('title', article.title)
    article.body = data.get('body', article.body)
    db.session.commit()

    return jsonify(article.to_dict())

@app.route('/delete/<int:id>/', methods=['DELETE'])
def delete_article(id):
    article = Articles.query.get(id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404

    db.session.delete(article)
    db.session.commit()

    return jsonify(article.to_dict())

# Routes for user authentication
users = {
    "test@example.com": {
        "password": "password123"
    }
}

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if email not in users or users[email]['password'] != password:
        return jsonify({"message": "Invalid credentials"}), 401
    access_token = create_access_token(identity=email)
    return jsonify({"token": access_token}), 200

@app.route('/signup', methods=['POST'])
def signup():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if email in users:
        return jsonify({"message": "Email already exists"}), 400
    users[email] = {"password": password}
    access_token = create_access_token(identity=email)
    return jsonify({"token": access_token}), 200

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    email = get_jwt_identity()
    return jsonify(logged_in_as=email), 200

if __name__ == '__main__':
    app.run(debug=True)




