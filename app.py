from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(80), nullable=False)
    item_name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'item_name': self.item_name,
            'quantity': self.quantity
        }

def create_tables():
    with app.app_context():
        db.create_all()
    
def insert_test_data():
    test_orders = [
        {'customer_name': 'John Doe', 'item_name': 'Laptop', 'quantity': 1},
        {'customer_name': 'Jane Smith', 'item_name': 'Keyboard', 'quantity': 2},
        {'customer_name': 'Alice Johnson', 'item_name': 'Monitor', 'quantity': 1}
    ]

    with app.app_context():
        for order_data in test_orders:
            order = Order(**order_data)
            db.session.add(order)

        db.session.commit()

create_tables()
insert_test_data()

@app.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if order is None:
        return jsonify({'error': 'Order not found'}), 404

    return jsonify(order.to_dict())

if __name__ == '__main__':
    app.run(debug=True)