from models.conn import db
from datetime import datetime
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    # Relationship with LeafImage
    leaf_images = db.relationship('LeafImage', back_populates='user', order_by='LeafImage.id')

    def set_password(self, password):
        self.password = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class LeafImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    classification_result = db.Column(db.String(100), nullable=False)
    
    # Back reference from LeafImage to User
    user = db.relationship('User', back_populates='leaf_images')

    def __repr__(self):
        return f'<LeafImage {self.id}>'
