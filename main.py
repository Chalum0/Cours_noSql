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
def redirect_to_counts():
    return redirect(url_for("list_counts_on_page", page=1))

@app.route('/api/v1/<page>')
def list_counts_on_page(page):
    db = get_db("Transilien")
    stations = []
    fields = {'_id': 1, 'nom_gare': 1}

    # checkboxes
    selected_values = request.args.getlist('options')
    for value in selected_values:
        fields[value] = 1

    page = int(page)
    num_items = int(request.args.get('num_items', '20'))
    sort_order = request.args.get('sort_order', '')

    query = {}
    cursor = db.find(query, fields)

    if sort_order:
        if 'somme_de_montants' in fields:
            sort_direction = -1 if sort_order == 'desc' else 1
            cursor = cursor.sort('somme_de_montants', sort_direction)

    limit = num_items
    skip = (page - 1) * limit
    cursor = cursor.skip(skip).limit(limit)

    for document in cursor:
        stations.append(document)

    query_sting = str(request.query_string)[2:-1]
    return render_template('list.html', stations=stations, fields=fields, page=int(page), nbitems=num_items, query=query_sting, sort_order=sort_order)


@app.route('/api/v1/edit', methods=["GET", "POST"])
def add_counting():
    global columns
    if request.method == 'POST':

        # get content from posst
        item_data = {}
        for item_name in columns:
            item_data[item_name] = request.form.get(item_name)

        db = get_db("Transilien")
        db.insert_one(item_data)

        return redirect(url_for("list_counts_on_page"))

    return render_template("edit.html", item=None)


@app.route('/api/v1/edit/<item_id>', methods=['GET', 'POST'])
def edit_count(item_id):
    db = get_db("Transilien")

    if request.method == 'POST':
        item_data = {}
        for item_name in columns:
            item_data[item_name] = request.form.get(item_name)

        db.update_one({"_id": ObjectId(item_id)}, {'$set': item_data})

        return redirect(url_for('list_counts_on_page'))
    item = db.find_one({'_id': ObjectId(item_id)})
    return render_template("edit.html", item=item)

@app.route('/api/v1/delete/<item_id>', methods=['GET'])
def delete_count(item_id):
    db = get_db("Transilien")

    db.delete_one({"_id": ObjectId(item_id)})
    return redirect(url_for('list_counts'))

@app.route("/api/v1/search", methods=['GET', 'POST'])
def search_counts():
    global columns
    db = get_db("Transilien")
    if request.method == 'POST':
        search_term = request.form.get('search_term', '')
        query = {"nom_gare": {"$regex": search_term, "$options": "i"}}

        fields = {'_id': 1}
        for value in columns:
            fields[value] = 1

        cursor = db.find(query, fields)
        stations = []
        for document in cursor:
            stations.append(document)

        return render_template('search_results.html', stations=stations, search_term=search_term, fields=fields)
    return render_template('search.html')



if __name__ == "__main__":
    app.run(port=5001)
