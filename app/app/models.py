from app import db
class Product(db.Model):
    product_id = db.Column(db.String, primary_key=True)

class Location(db.Model):
    location_id = db.Column(db.String, primary_key=True)

class ProductMovement(db.Model):
    movement_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    from_location = db.Column(db.String, db.ForeignKey('location.location_id'))
    to_location = db.Column(db.String, db.ForeignKey('location.location_id'))
    product_id = db.Column(db.String, db.ForeignKey('product.product_id'))
    qty = db.Column(db.Integer)

    from_location_rel = db.relationship('Location', foreign_keys=[from_location])
    to_location_rel = db.relationship('Location', foreign_keys=[to_location])
    product_rel = db.relationship('Product')

db.create_all()