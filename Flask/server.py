from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

petList = []

@app.route('/hello')
def hello():
    return 'hello'

@app.route('/pets', methods=['POST', 'GET'])
def pets():
    if(request.method == 'POST'):
        json = request.get_json()
        try:
            if('name' in json and 'age' in json and 'species' in json):
                petList.append({'name' : json['name'], 'age' : json['age'], 'species' : json['species']})

        except:
            print('error')
            return jsonify({'error' : 'Please include a name, age, and species'})
    elif(request.method == 'GET'):
        return jsonify(petList)


if __name__ == '__main__':
    app.run()
