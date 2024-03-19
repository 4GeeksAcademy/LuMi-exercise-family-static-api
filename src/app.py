"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

John = {
    "id": jackson_family._generateId(),
    "name":"John Jackson",
    "age": "33 Years old",
    "lucky_numbers": [7, 13, 22]
}

Jane = {
    "id": jackson_family._generateId(),
    "name":"Jane Jackson",
    "age":"35 Years old",
    "lucky_numbers": [10, 14, 3]
}

Jimmy = {
    "id": jackson_family._generateId(),
    "name": "Jimmy  Jackson",
    "age": "5 Years old",
    "lucky_numbers": 1
}

jackson_family.add_member(John)
jackson_family.add_member(Jane)
jackson_family.add_member(Jimmy)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():

    members = jackson_family.get_all_members()
    response_body = members

    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def add_members():
    body = request.json
    if "id" not in body:
        body["id"] = jackson_family._generateId()
    
    jackson_family.add_member(body)
    return "Family member added", 200

@app.route('/member/<int:id>', methods=['GET'])
def get_one_member(id):
    member = jackson_family.get_member(id)
    if member is None:
        return jsonify({"error": "Member not found"}), 404
    else:
        return jsonify(member), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_one_member(id):
    member = jackson_family.delete_member(id)
    if member == True:
        return {"done": True}, 200
    if member == False:
        return 'member doesnt exist', 400
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
