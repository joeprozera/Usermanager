from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///followed_users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class FollowedUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)

@app.route('/submit', methods=['POST'])
def submit():
    username = request.json.get('username')
    if FollowedUser.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already followed'}), 400
    new_user = FollowedUser(username=username)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Followed successfully'}), 200

@app.route('/list', methods=['GET'])
def list_users():
    users = FollowedUser.query.all()
    return jsonify([user.username for user in users])

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
