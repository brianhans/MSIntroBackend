from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

petList = []

def findPet(name):
    for pet in petList:
        if(pet['name'] == name):
            return pet


@app.route('/hello')
def hello():
    return 'hello'

@app.route('/pets/', methods=['POST', 'GET'])
def pets():
    if(request.method == 'POST'):
        json = request.get_json()
        if('name' in json and 'age' in json and 'species' in json):
            if(findPet(json['name'])):
                return jsonify({'code' : 409, 'error' : 'That pet already exists. You need to give your pet a unique name'}), 409
            else:
                petList.append({'name' : json['name'], 'age' : json['age'], 'species' : json['species']})
                return jsonify({'code' : 200})
        else:
            return jsonify({'error' : 'Please include a name, age, and species'}), 400
    elif(request.method == 'GET'):
        return jsonify(petList)

@app.route('/pets/<name>', methods=['GET', 'PUT', 'DELETE'])
def getPet(name):
    if(request.method == 'GET'):
        pet = findPet(name)
        if(pet):
            return jsonify(pet)
        return jsonify({'error' : 'Not in database'}), 404
    elif(request.method == 'PUT'):
        json = request.get_json()
        for i in range(0, len(petList)):
            if(petList[i]['name'] == name):
                if('name' in json and 'age' in json and 'species' in json):
                    petList[i] = {'name' : json['name'], 'age' : json['age'], 'species' : json['species']}
                    return jsonify({'code' : 200})
                else:
                    return jsonify({'error' : 'Please include a name, age, and species'}), 400
        return jsonify({'error' : 'Not in database'}), 404
    else:
        json = request.get_json()
        for i in range(0, len(petList)):
            if(petList[i]['name'] == name):
                temp = petList[i]
                del petList[i]
                return jsonify(temp)
        return jsonify({'error' : 'Not in database'}), 404

if __name__ == '__main__':
    app.run()

def Pet():
    name = ""
    age = 0
    species = ""

     def __init__(self, name, age, species):
        self.name = name
        self.age = age
        self.species = species

    def __eq__(self, other):
        return self.name.lower() == other.name.lower()

    def toJSON():
        return {'name' : name, 'age' : age, 'species' : species}
