from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adoption'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Track what is happening during dev
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "hihihi333"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

# HOME PAGE ROUTE
@app.route('/')
def get_home():
    return render_template('home.html')

# GET all cupcakes
@app.route('/api/cupcakes')
def get_cupcakes():
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]

    return jsonify(cupcakes=all_cupcakes)

# GET single cupcake
@app.route('/api/cupcakes/<int:cupcake_id>')
def get_single_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id).serialize()

    return jsonify(cupcake=cupcake)

# POST [CREATE] cupcake
@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():

    new_cupcake = Cupcake(
        flavor=request.json["flavor"], 
        rating=request.json["rating"], 
        size=request.json["size"],
        image=request.json["image"] or None)

    db.session.add(new_cupcake)
    db.session.commit()
    return (jsonify(cupcake=new_cupcake.serialize()), 201)

# UPDATE cupcake
@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

# DELETE cupcake
@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")