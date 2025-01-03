from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


# Initialize the db object here
db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__)
    
#     # Configure the app
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
#     # Initialize the SQLAlchemy object with the app
#     db.init_app(app)
    
#     # Register routes (blueprint) here
#     with app.app_context():
#         from app import routes  # Import the routes after app initialization
#         db.create_all()  # Creates the database tables
    
#     return app
def create_app():
    app = Flask(__name__)
    CORS(app) 
    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the SQLAlchemy object with the app
    db.init_app(app)

    # Register the blueprint here
    from app.routes import bp  # Import the blueprint from routes
    app.register_blueprint(bp)  # Register the blueprint

    # Create all the database tables
    with app.app_context():
        db.create_all()

    return app

