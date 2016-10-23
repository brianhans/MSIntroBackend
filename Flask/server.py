from flask import Flask
from flask import request
from flask import jsonify
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

# Connects to a mongoDB database
client = MongoClient()
db = client.pet_database


pet_list = []

# Takes a name as a parameter and returns the index of the item or None if it
# doesn't exist


def find_pet(name):
    if(len(pet_list) < 1 or not name):
        return None
    for i in range(0, len(pet_list)):
        if(pet_list[i].name == name):
            return i


class Pet():
    name = ""
    age = 0
    species = ""

    def __init__(self, name, age, species):
        self.name = name
        self.age = age
        self.species = species

    @classmethod
    def from_database(cls, json):
        # Make sure all the values are provided in the JSON
        if(not ('name' in json and 'age' in json and 'species' in json)):
            raise PetJsonError
        return cls(json['name'], json['age'], json['species'])

    # Allows for the == operator to work between two Pet objects
    def __eq__(self, other):
        return self.name.lower() == other.name.lower()

    # Convert the object into a dictionary so it is easier to turn into JSON
    def to_dict(self):
        return {'name': self.name, 'age': self.age, 'species': self.species}

    def save_to_database(self, db):
        db.pets.insert_one(self.to_dict())


class PetJsonError(Exception):

    def __init__(self, message):
        self.message = message


@app.route('/hello')
@app.route('/hello/<name>')
def hello_name(name=None):
    if(name):
        return 'hello ' + name
    return 'hello'


@app.route('/pets/', methods=['POST', 'GET'])
def pets():
    if(request.method == 'POST'):
        # get_json returns a dictionary object representing body data
        json = request.get_json()
        # Make sure all the values are provided in the JSON
        try:
            db_pet = db.pets.find_one({'name': json['name']})
            if(db_pet):
                return jsonify({'error': 'That pet already exists. You need to give your pet a unique name', 'code': 409}), 409
            else:
                pet = Pet(json['name'], json['age'], json['species'])
                pet.save_to_database(db)
                return jsonify({'pet': pet.to_dict(), 'code': 201}), 201
        except PetJsonError:
            return jsonify({'error': 'Please include a name, age, and species', 'code': 400}), 400
    elif(request.method == 'GET'):
        # Maps all the pet objects into an array of Python dictionaries and then
        # converts those into a JSON string
        return jsonify(map(lambda x: Pet(x).to_dict(), db.pets.find()))


@app.route('/pets/<name>', methods=['GET', 'PUT', 'DELETE'])
def get_pet(name):
    if(request.method == 'GET'):
        db_pet = db.pets.find_one({'name': name})
        if(db_pet):
            return jsonify(Pet.from_database(db_pet).to_dict())
        return jsonify({'error': 'Not in database', 'code': 404}), 404
    elif(request.method == 'PUT'):
        json = request.get_json()
        pet = None
        try:
            pet = Pet.from_database(json)
        except PetJsonError:
            return jsonify({'error': 'Please include a name, age, and species', 'code': 400}), 400

        db_pet = db.pets.update_one({'name': json['name']}, {
            '$set': {
                'name' : json['name'],
                'age' : json['age'],
                'species' : json['species']
            }
        }, upsert = False)

        if(db_pet.matched_count < 1):
            return jsonify({'error': 'Not in database', 'code': 404}), 404
        else:
            return jsonify({'code' : 200})
    elif(request.method == 'DELETE'):
        json = request.get_json()
        db_pet = db.pets.find_one({'name': name})
        if(db_pet):
            db.pets.delete_one({'name': name})
            return jsonify(Pet.from_database(db_pet).to_dict())
        return jsonify({'error': 'Not in database', 'code': 404}), 404

if __name__ == '__main__':
    app.run()
