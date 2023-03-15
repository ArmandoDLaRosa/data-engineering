from flask import Flask
from .extensions import crs, db, ma
from .routes.beneficiary import app_be
from .routes.consumer import app_co
from .routes.transaction import app_tr



def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:01570376@192.168.1.109:5432/ria"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CORS_HEADERS'] = 'Content-Type'
    
    db.init_app(app)            
    ma.init_app(app)
    crs.init_app(app)
    
    app.register_blueprint(app_tr)
    app.register_blueprint(app_co)
    app.register_blueprint(app_be)
    return app
