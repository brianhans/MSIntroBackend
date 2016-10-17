from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

petList = []

def findPet(name):
    if(len(petList) < 1):
        return None, None
    for i in range(0, len(petList)):
        if(petList[i].name == name):
            return petList[i], i

class Pet():
    name = ""
    age = 0
    species = ""

    def __init__(self, name, age, species):
        self.name = name
        self.age = age
        self.species = species

    def __eq__(self, other):
        return self.name.lower() == other.name.lower()

    def toDict(self):
        return {'name' : self.name, 'age' : self.age, 'species' : self.species}




@app.route('/hello')
def hello():
    return 'hello'

@app.route('/pets/', methods=['POST', 'GET'])
def pets():
    if(request.method == 'POST'):
        json = request.get_json()
        if('name' in json and 'age' in json and 'species' in json):
            pet, _ = findPet(json['name'])
            if(pet):
                return jsonify({'code' : 409, 'error' : 'That pet already exists. You need to give your pet a unique name'}), 409
            else:
                pet = Pet(json['name'], json['age'], json['species'])
                petList.append(pet)
                return jsonify({'code' : 200})
        else:
            return jsonify({'error' : 'Please include a name, age, and species'}), 400
    elif(request.method == 'GET'):
        return jsonify(map((lambda x: x.toDict()), petList))


@app.route('/pets/<name>', methods=['GET', 'PUT', 'DELETE'])
def getPet(name):
    if(request.method == 'GET'):
        pet, _ = findPet(name)
        if(pet):
            return jsonify(pet.toDict())
        return jsonify({'error' : 'Not in database'}), 404
    elif(request.method == 'PUT'):
        json = request.get_json()
        if(not 'name' in json or not 'age' in json or not 'species' in json):
            return jsonify({'error' : 'Please include a name, age, and species'}), 400
        pet, _ = findPet(name)
        if(pet):
            pet.name = json['name']
            pet.age = json['age']
            pet.species = json['species']
            return jsonify({'code' : 200})
        else:
            return jsonify({'error' : 'Not in database'}), 404
    else:
        json = request.get_json()

        pet, index = findPet(name)
        if(pet):
            del petList[index]
            return jsonify(pet.toDict())
        return jsonify({'error' : 'Not in database'}), 404

if __name__ == '__main__':
    app.run()
