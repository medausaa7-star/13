from flask import Flask, jsonify, request

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop", "price": 50000},
    {"id": 2, "name": "Mobile Phone", "price": 20000},
    {"id": 3, "name": "Headphones", "price": 2000},
    {"id": 4, "name": "Keyboard", "price": 1500}
]

cart = []


# Get all products
@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)


# Add product to cart
@app.route("/cart", methods=["POST"])
def add_to_cart():

    data = request.get_json()

    product_id = data["product_id"]

    for product in products:
        if product["id"] == product_id:
            cart.append(product)
            return jsonify({
                "message": "Product added to cart",
                "cart": cart
            })

    return jsonify({"message": "Product not found"}), 404


# View cart
@app.route("/cart", methods=["GET"])
def get_cart():

    total = sum(item["price"] for item in cart)

    return jsonify({
        "items": cart,
        "total": total
    })


# AI recommendation
@app.route("/recommend", methods=["GET"])
def recommend():

    product_name = request.args.get("product")

    recommendations = []

    if product_name.lower() == "laptop":
        recommendations = [
            "Keyboard",
            "Headphones"
        ]

    elif product_name.lower() == "mobile":
        recommendations = [
            "Headphones"
        ]

    else:
        recommendations = [
            "Laptop",
            "Mobile Phone"
        ]

    return jsonify({
        "recommendations": recommendations
    })


if __name__ == "__main__":
    app.run(debug=True)