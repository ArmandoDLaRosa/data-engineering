from ..extensions import db, ma
from datetime import datetime

class Consumer(db.Model):
    # Each record is a robot's stats of a match
    __tablename__ = 'consumer'
    # ID    
    consumer_id = db.Column(db.Integer, primary_key=True, nullable=False)
    # ATTRIBUTES    
    consumer_first_name = db.Column(db.String(50), nullable=False)
    consumer_last_name = db.Column(db.String(50), nullable=False)        
    # Standard attributes    
    created_at = db.Column(db.DateTime,  default=datetime.utcnow, nullable=False)
    created_by = db.Column(db.String(100), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_by = db.Column(db.String(100), nullable=False)
    available = db.Column(db.Boolean, nullable=False)      
    
class ConsumerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Consumer

    # ID    
    consumer_id = ma.auto_field()
    # ATTRIBUTES    
    consumer_first_name = ma.auto_field()
    consumer_last_name = ma.auto_field()    
    # Standard attributes    
    created_at = ma.DateTime(format='%Y-%m-%d %H:%M:%S.%f')
    created_by = ma.auto_field()
    updated_at = ma.DateTime(format='%Y-%m-%d %H:%M:%S.%f')
    updated_by = ma.auto_field()
    available = ma.auto_field()    