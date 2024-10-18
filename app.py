from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__, template_folder='src', static_folder='src/styles')
app.config["MONGO_URI"] = "mongodb+srv://storage:*****@cluster0.vw0gowi.mongodb.net/"
mongo = PyMongo(app)

@app.route('/')
def index():
    products = mongo.db.products.find()
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    id = request.form['productId']
    name = request.form['productName']
    quantity = int(request.form['productQuantity'])
    mongo.db.products.insert_one({'id':id,'name': name, 'quantity': quantity})
    return redirect(url_for('index'))

@app.route('/decrease/<product_id>', methods=['POST'])
def decrease(product_id):
    mongo.db.products.update_one({'_id': ObjectId(product_id)}, {'$inc': {'quantity': -1}})
    return redirect(url_for('index'))

@app.route('/increase/<product_id>', methods=['POST'])
def increase(product_id):
    mongo.db.products.update_one({'_id': ObjectId(product_id)}, {'$inc': {'quantity': 1}})
    return redirect(url_for('index'))

@app.route('/edit/<product_id>', methods=['GET', 'POST'])
def edit(product_id):
    product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
    if request.method == 'POST':
        id = request.form['productId']
        name = request.form['productName']
        quantity = int(request.form['productQuantity'])
        mongo.db.products.update_one({'_id': ObjectId(product_id)}, {'$set': {'id':id,'name': name, 'quantity': quantity}})
        return redirect(url_for('index'))
    return render_template('edit.html', product={**product, "_id": str(product["_id"])})

@app.route('/delete/<product_id>', methods=['POST'])
def delete(product_id):
    mongo.db.products.delete_one({'_id': ObjectId(product_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,port=8080)