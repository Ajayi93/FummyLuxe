from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import urllib.parse

app = Flask(__name__)
import os

app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key')

# Example product data
products = [
    {'id': 1, 'name': 'Miral Boubou', 'description': 'Fits up to size 18.', 'price': 55000, 'image': 'product6.jpg'},
    {'id': 2, 'name': 'Miyaki Boubou', 'description': 'Fits up to size 18.', 'price': 60000, 'image': 'product3.jpg'},
    {'id': 3, 'name': 'Miral Boubou', 'description': 'Fits up to size 18.', 'price': 55000, 'image': 'product8.jpg'},
    {'id': 4, 'name': 'Adire Silk Boubou', 'description': 'Fits up to size 14.', 'price': 25000, 'image': 'product5.jpg'},
    {'id': 5, 'name': 'Mixed Adire Crep Gown', 'description': 'Fits up to size 16.', 'price': 35000, 'image': 'product4.jpg'},
    {'id': 6, 'name': 'Cotton Adire Kaftan', 'description': 'Fits up to size 18.', 'price': 35000, 'image': 'product2.jpg'},
    {'id': 7, 'name': 'Mixed Adire Crep Gown', 'description': 'Fits up to size 16.', 'price': 35000, 'image': 'product1.jpg'},
    {'id': 8, 'name': 'Miral Boubou', 'description': 'Fits up to size 18.', 'price': 55000, 'image': 'product7.jpg'},
    {'id': 9, 'name': 'Miyaki Boubou', 'description': 'Fits up to size 18.', 'price': 60000, 'image': 'product9.jpg'},
    {'id': 10, 'name': 'Pleated Silk Boubou', 'description': 'Fits up to size 16.', 'price': 25000, 'image': 'product10.jpg'},
    {'id': 11, 'name': 'Pleated Silk Boubou', 'description': 'Fits up to size 18.', 'price': 25000, 'image': 'product11.jpg'},
    {'id': 12, 'name': 'Pleated Silk Boubou', 'description': 'Fits up to size 16.', 'price': 25000, 'image': 'product12.jpg'},
    {'id': 13, 'name': 'Pattern Silk Boubou', 'description': 'Fits up to size 18.', 'price': 25000, 'image': 'product13.jpg'},    
    {'id': 14, 'name': 'Pattern Silk Boubou', 'description': 'Fits up to size 18.', 'price': 25000, 'image': 'product14.jpg'},
    {'id': 15, 'name': 'Pleated Silk Boubou', 'description': 'Fits up to size 18.', 'price': 30000, 'image': 'Product15.jpg'},
    {'id': 16, 'name': 'Pleated Silk Boubou', 'description': 'Fits up to size 16.', 'price': 25000, 'image': 'product16.jpg'}
]

@app.route('/')
def home():
    return render_template('index.html')

# Shop page
@app.route('/shop')
def shop():
    return render_template('shop.html', products=products)

# Add to Cart
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    
    if product:
        cart = session.get('cart', [])

        # Check if item already exists in cart
        for item in cart:
            if item['id'] == product_id:
                item['quantity'] += 1  # Increase quantity
                session['cart'] = cart
                session.modified = True
                return redirect(url_for('cart'))

        # If item is not in cart, add it with quantity 1
        product['quantity'] = 1
        cart.append(product)
        session['cart'] = cart
        session.modified = True
    
    return redirect(url_for('cart'))

# View Cart
@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total_price = sum(item['price'] * item['quantity'] for item in session.get('cart', []))
    return render_template('cart.html', cart=cart, total_price=total_price)

@app.route('/cart-count')
def cart_count():
    cart = session.get('cart', [])
    total_items = sum(item['quantity'] for item in cart)
    return jsonify({'total_items': total_items})

# Clear Cart (POST only)
@app.route('/clear-cart', methods=['POST'])
def clear_cart():
    print("🛒 Clearing cart...")  # Debugging in the console
    session.pop('cart', None)  # Use ` pop` to remove cart safely
    session.modified = True 
    return jsonify({"message": "Cart cleared successfully"}), 200  # Ensure correct JSON response

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # You can handle or save the message here if needed.
        return 'Thank you for your message!'
    return render_template('contact.html')

@app.route('/confirmation')
def confirmation():
    cart = session.get('cart', [])
    total = sum(item['price'] for item in cart)
    # Clear the cart after order
    session['cart'] = []
    return render_template('confirmation.html', cart=cart, total=total)

@app.route('/manual_payment')
def manual_payment():
    cart = session.get('cart', [])

    if not cart:
        return "Your cart is empty."

    # Generate order summary
    order_summary = "Order Summary:\n"
    total_price = 0

    for item in cart:  # ✅ Iterate over the list directly
        item_name = item['name']
        quantity = item['quantity']
        price = item['price'] * quantity
        total_price += price

        order_summary += f"- {quantity}x {item_name} - ₦{price:,}\n"

    order_summary += f"\nTotal: ₦{total_price:,}"

    # Encode for WhatsApp
    message = f"{order_summary}\n\nPlease send your payment proof here."
    whatsapp_url = f"https://wa.me/2347018692863?text={message}"

    return render_template('manual_payment.html', whatsapp_url=whatsapp_url, cart=cart, total_price=total_price)

if __name__ == '__main__':
    app.run(debug=True)