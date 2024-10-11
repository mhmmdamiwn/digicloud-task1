import jwt
import datetime
from nameko.rpc import rpc
from nameko_sqlalchemy import DatabaseSession
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, User

class AuthService:
    name = "auth_service"

    db = DatabaseSession(Base)
    secret_key = "supersecretkey"  

    def __init__(self):
        engine = create_engine("mysql+pymysql://myuser:mypassword@mysql/mydatabase")
        Base.metadata.create_all(engine)
    
    @rpc
    def register(self, username, password):
        """Register a new user by saving hashed password"""
        if self.db.query(User).filter_by(username=username).first():
            return {"message": "User already exists!"}
        
        password_hash = generate_password_hash(password)
        new_user = User(username=username, password_hash=password_hash)
        self.db.add(new_user)
        self.db.commit()
        return {"message": "User registered successfully!"}

    @rpc
    def login(self, username, password):
        """Login user and return JWT token if successful"""
        user = self.db.query(User).filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            return {"message": "Invalid username or password!"}
        
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, self.secret_key, algorithm="HS256")

        return {"token": token}

    @rpc
    def verify_token(self, token):
        """Verify JWT token and return user_id if valid"""
        try:
            decoded = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return {"user_id": decoded['user_id']}
        except jwt.ExpiredSignatureError:
            return {"message": "Token expired!"}
        except jwt.InvalidTokenError:
            return {"message": "Invalid token!"}