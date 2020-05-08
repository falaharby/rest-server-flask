from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="falahwebservice",
    password="arbystrong12",
    hostname="falahwebservice.mysql.pythonanywhere-services.com",
    databasename="falahwebservice$books",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db=SQLAlchemy(app)

class Books(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String)
    first_sentence = db.Column(db.String)
    published = db.Column(db.String)

    def __init__(self, title, author, first_sentence, published):
        self.title = title
        self.author = author
        self.first_sentence = first_sentence
        self.published = published

    def serialize(self):
        return {"id": self.id,
                "title": self.title,
                "author": self.author,
                "first_sentence": self.first_sentence,
                "published": self.published}

@app.route('/', methods=['GET'])
def home():
    return '<h1>Web Service Unisbank !</h1><p>Latihan membuat API dengan Python dan Flask</p>'

@app.route('/books/', methods=['GET'])
def books():
    return jsonify({'data': list(map(lambda dev: dev.serialize(), Books.query.all()))})

@app.route('/books/<int:id>/')
def get_books(id):
    return jsonify({'data': Books.query.get(id).serialize()})

@app.route('/books', methods=['POST'])
def add_books():
    title = request.json['title']
    author = request.json['author']
    first_sentence = request.json['first_sentence']
    published = request.json['published']

    dev = Books(title, author, first_sentence, published)

    db.session.add(dev)
    db.session.commit()
    return jsonify({'data': dev.serialize()}), 201

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_books(id):
    db.session.delete(Books.query.get(id))
    db.session.commit()
    return jsonify({'result': True})

@app.route('/books/<int:id>/', methods=['PUT'])
def update_books(id):
    dev = Books.query.get(id)

    title = request.json['title']
    author = request.json['author']
    first_sentence = request.json['first_sentence']
    published = request.json['published']

    dev.title = title
    dev.author = author
    dev.first_sentence = first_sentence
    dev.published = published

    db.session.commit()
    return jsonify({'dev': dev.serialize()})
