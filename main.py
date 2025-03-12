import os
from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId


app = Flask(__name__)
columns = ["nom_gare", "code_gare", "type_jour", "date", "annee", "ligne", "axe", "tranche_horaire", "somme_de_montants"]


def get_db(collection):
    mongo_uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri)

    db = client["MyDataBase"]
    return db[collection]

@app.route('/api/v1')
def list_counts():
    db = get_db("Transilien")
    stations = []
    for document in db.find():  # .limit(20):
        stations.append(document)
    return render_template('list.html', stations=stations)


@app.route('/api/v1/edit', methods=["GET", "POST"])
def add_counting():
    global columns
    if request.method == 'POST':

        item_data = {}
        for item_name in columns:
            item_data[item_name] = request.form.get(item_name)

        db = get_db("Transilien")
        db.insert_one(item_data)

        return redirect(url_for("list_counts"))

    return render_template("edit.html", item=None)


@app.route('/api/v1/edit/<item_id>', methods=['GET', 'POST'])
def edit_count(item_id):
    db = get_db("Transilien")

    if request.method == 'POST':
        item_data = {}
        for item_name in columns:
            item_data[item_name] = request.form.get(item_name)

        db.update_one({"_id": ObjectId(item_id)}, {'$set': item_data})

        return redirect(url_for('list_counts'))
    item = db.find_one({'_id': ObjectId(item_id)})
    return render_template("edit.html", item=item)

@app.route('/api/v1/delete/<item_id>', methods=['GET'])
def delete_count(item_id):
    db = get_db("Transilien")

    db.delete_one({"_id": ObjectId(item_id)})
    return redirect(url_for('list_counts'))



if __name__ == "__main__":
    app.run(port=5001)
