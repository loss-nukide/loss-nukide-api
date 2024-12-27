from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    jiro_calls = db.relationship("JiroCall", back_populates="user")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        
class JiroCall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shopName = db.Column(db.String(150), nullable=False)
    amountOfnoodles = db.Column(db.Integer, nullable=False)
    amountOfBegetables = db.Column(db.String(150), nullable=False)
    amountOfNinniku = db.Column(db.String(150), nullable=False)
    amountOfKarame = db.Column(db.String(150), nullable=False)
    ammountOfAbura = db.Column(db.String(150), nullable=False)

    user = db.relationship("User", back_populates="jiro_calls")

    
    def __init__(self,user_id, shopName, amountOfnoodles, amountOfBegetables, amountOfNinniku, amountOfKarame, ammountOfAbura):
        self.user_id = user_id
        self.shopName = shopName
        self.amountOfnoodles = amountOfnoodles
        self.amountOfBegetables = amountOfBegetables
        self.amountOfNinniku = amountOfNinniku
        self.amountOfKarame = amountOfKarame
        self.ammountOfAbura = ammountOfAbura