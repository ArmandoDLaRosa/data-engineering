from ..extensions import db, ma
from datetime import datetime

class Beneficiary(db.Model):
    __tablename__ = 'beneficiary'
    # ID
    beneficiary_id = db.Column(db.String(50), primary_key=True)
    # ATTRIBUTES
    beneficiary_first_name = db.Column(db.String(50), nullable=False)
    beneficiary_last_name = db.Column(db.String(50), nullable=False)
    # Standard attributes
    created_at = db.Column(db.DateTime,  default=datetime.utcnow, nullable=False)
    created_by = db.Column(db.String(100), nullable=False)
    updated_at = db.Column(db.DateTime,  default=datetime.utcnow, nullable=False)
    updated_by = db.Column(db.String(100), nullable=False)
    available = db.Column(db.Boolean, nullable=False)     
    
class BeneficiarySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Beneficiary

    # ID    
    beneficiary_id = ma.auto_field()
    # ATTRIBUTES    
    beneficiary_first_name = ma.auto_field()
    beneficiary_last_name = ma.auto_field()    
    # Standard attributes    
    created_at = ma.DateTime(format='%Y-%m-%d %H:%M:%S.%f')
    created_by = ma.auto_field()
    updated_at = ma.DateTime(format='%Y-%m-%d %H:%M:%S.%f')
    updated_by = ma.auto_field()
    available = ma.auto_field()    
    