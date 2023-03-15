#from api import db
from api.extensions import db
from api import create_app
from api.models import *

with create_app().app_context():
    db.create_all()
    
