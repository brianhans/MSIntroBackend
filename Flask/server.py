from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

pet_list = []

#Takes a name as a parameter and returns the index of the item or None if it
#doesn't exist
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

    #Allows for the == operator to work between two Pet objects
    def __eq__(self, other):
        return self.name.lower() == other.name.lower()

    #Convert the object into a dictionary so it is easier to turn into JSON
    def to_dict(self):
        return {'name' : self.name, 'age' : self.age, 'species' : self.species}


@app.route('/hello')
@app.route('/hello/<name>')
def hello_name(name=None):
    if(name):
        return 'hello ' + name
    return 'hello'

@app.route('/pets/', methods=['POST', 'GET'])
def pets():
    if(request.method == 'POST'):
        #get_json returns a dictionary object representing body data
        json = request.get_json()

        #Make sure all the values are provided in the JSON
        if('name' in json and 'age' in json and 'species' in json):
            index = find_pet(json['name'])
            if(index is not None):
                return jsonify({'error' : 'That pet already exists. You need to give your pet a unique name','code' : 409}), 409
            else:
                pet = Pet(json['name'], json['age'], json['species'])
                pet_list.append(pet)
                return jsonify({'pet' : pet.to_dict(), 'code' : 201}), 201
        else:
            return jsonify({'error' : 'Please include a name, age, and species', 'code' : 400}), 400
    elif(request.method == 'GET'):
        #Maps all the pet objects into an array of Python dictionaries and then
        #converts those into a JSON string
        return jsonify(map((lambda x: x.to_dict()), pet_list))


@app.route('/pets/<name>', methods=['GET', 'PUT', 'DELETE'])
def get_pet(name):
    if(request.method == 'GET'):
        index = find_pet(name)
        if(index is not None):
            return jsonify(pet_list[index].to_dict())
        return jsonify({'error' : 'Not in database', 'code' : 404}), 404
    elif(request.method == 'PUT'):
        json = request.get_json()
        #Make sure all the values are provided in the JSON
        if(not 'name' in json or not 'age' in json or not 'species' in json):
            return jsonify({'error' : 'Please include a name, age, and species', 'code': 400}), 400
        index = find_pet(name)
        if(index is not None):
            pet_list[index].name = json['name']
            pet_list[index].age = json['age']
            pet_list[index].species = json['species']
            return jsonify({'code' : 200})
        else:
            return jsonify({'error' : 'Not in database', 'code': 404}), 404
    elif(request.method == 'DELETE'):
        json = request.get_json()
        index = find_pet(name)
        if(index is not None):
            #Store pet in temp variable so it can be returned 
            tempPet = pet_list[index]
            del pet_list[index]
            return jsonify(tempPet.to_dict())
        return jsonify({'error' : 'Not in database', 'code': 404}), 404

if __name__ == '__main__':
    app.run()
