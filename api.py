from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from bson import ObjectId
from flask import render_template

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Electronics'
app.config['MONGO_URI'] = 'mongodb+srv://ibk2510:deathbychocolate@cluster0.u4lph.mongodb.net/Electronics?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
def get_home():
    return render_template('index.html')

@app.route('/docs')
def api_docs():
    return render_template('docs.html')

@app.route('/getAll', methods=['GET'])
def get_all_data():
    collection = mongo.db.smartphones #data here is collection name in mongo
    output = []
    for s in collection.find():
        s['_id']=str(s['_id'])
        output.append(s)
    return jsonify(output)

@app.route('/get', methods=['GET'])
def get_one():
    data = request.json
    try:
        oid = ObjectId(data['oid'])
    except:
        return jsonify({"msg": "Invalid ObjectId, must be a 24-character hex string."})
    collection = mongo.db.smartphones #data here is collection name in mongo
    try:
        get_record = collection.find_one({'_id': oid})
        get_record['_id']=str(get_record['_id'])
        return jsonify(get_record)
    except:
        return jsonify({"msg": "An error occured. ObjectId not found. Check if your ObjectId is valid."})

@app.route('/insert', methods=['POST'])
def insert_data():
    #pass array of json for single/multiple insert
    data = request.json
    collection = mongo.db.smartphones #data here is collection name in mongo
    try:
        inserted_oids = collection.insert_many(data).inserted_ids
        return jsonify({
            "inserted_oids": str(inserted_oids)
        })
    except:
        return jsonify({"msg": "An error occured. Data must be an array of json objects."})

@app.route('/update', methods=['PUT'])
def update_one():
    data = request.json
    oid = ObjectId(data['oid'])
    newvalues = data['newvalues']
    collection = mongo.db.smartphones #data here is collection name in mongo
    filter = {'_id': oid}
    update_query = {
        "$set": newvalues
    }
    update_data = collection.update_one(filter, update_query)
    return jsonify({
        "msg": "Update request received. Check status by querying /get with ObjectId."
    })

@app.route('/delete', methods=['DELETE'])
def delete_one():
    data = request.json
    oid = ObjectId(data['oid'])
    collection = mongo.db.smartphones #data here is collection name in mongo
    delete_data = collection.delete_one({'_id': oid})
    return jsonify({
        "msg": "Delete request received. Check status by querying /get with ObjectId."
    })


@app.route('/table')
def table():
    return render_template('table.html')

if __name__ == '__main__':
    app.run(debug=True)
