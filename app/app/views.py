from app import app, db
from flask import render_template, request, redirect
from app.models import Product, Location, ProductMovement


@app.route('/')
def index():
    locations = Location.query.all()
    return render_template('index.html',locations = locations)

@app.route('/products', methods=['GET','POST'])
def create_product():
    if request.method == 'POST':
        product_id = request.form['product_id']

        product = Product(product_id=product_id)
        db.session.add(product)
        db.session.commit()

        return redirect('/')
    else:
        return render_template('add_product.html')

# Create a new location
@app.route('/locations', methods=['GET','POST'])
def create_location():
    if request.method == 'POST':
        location_id = request.form['location_id']
        location = Location(location_id=location_id)
        db.session.add(location)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('add_location.html')

# Create a new product movement
@app.route('/<location>', methods=['GET','POST'])
def create_movement(location):
    current_location = Location.query.get(location)
    if request.method == 'POST':
        from_location = request.form['from_location']
        to_location = request.form['to_location']
        product_id = request.form['product_id']
        qty = request.form['qty']
        movement = ProductMovement(
            from_location=from_location,
            to_location=to_location,
            product_id=product_id,
            qty=qty
        )
        db.session.add(movement)
        db.session.commit()
        return redirect('/')
    else :
        locations = Location.query.all()
        products = Product.query.all()
        return render_template('location.html',locations = locations,products = products,
                            current_location = current_location)
    

@app.route('/product-balances-report')
def product_balances_report():
    # Query all locations and products
    locations = Location.query.all()
    products = Product.query.all()
    product_balances = {}

    for location in locations:
        product_balances[location.location_id] = {}
        
        for product in products:
            balance = 0
            
            # Calculate balance for movements to the location
            to_movements = ProductMovement.query.filter_by(to_location=location.location_id,
                                                        product_id=product.product_id).all()
            for movement in to_movements:
                balance += movement.qty
            
            # Calculate balance for movements from the location
            from_movements = ProductMovement.query.filter_by(from_location=location.location_id,
                                                            product_id=product.product_id).all()
            for movement in from_movements:
                balance -= movement.qty
            
            product_balances[location.location_id][product.product_id] = balance

    return render_template('report.html', locations=locations, products=products, product_balances=product_balances)





