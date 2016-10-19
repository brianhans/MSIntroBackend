import server
import unittest
import json

class FlaskServerTest(unittest.TestCase):

    def setUp(self):
        #Run app in testing mode to retrieve exceptions and stack traces
        server.app.testing = True
        self.app = server.app.test_client()
        self.initArray()

    def initArray(self):
        dog = server.Pet('Doggy', 'Dog', 5)
        cat = server.Pet('Spot', 'Cat', 1)
        fish = server.Pet('Fishy', 'Fish', 0)
        server.pet_list = [dog, cat, fish]

    def test_hello(self):
        response = self.app.get('/hello')
        assert response.status_code == 200, 'status_code was not OK'
        assert response.data == 'hello'

    def test_hello_name(self):
        response = self.app.get('/hello/Julia')
        assert response.status_code == 200, 'status_code was not OK'
        assert response.data == 'hello Julia'

    def test_getPets(self):
        #Test to see if you can get all pets
        response = self.app.get('/pets/')
        assert response.status_code == 200, 'status_code was not OK'
        pets = json.loads(response.data)
        assert len(pets) == 3, 'not all pets returned'
        assert pets[0]['name'] == 'Doggy', 'wrong pet returned'

    def test_postPet(self):
        #Test to make sure you can create pets
        response = self.app.post('/pets/', data=json.dumps(dict(name='Piggy', species='Pig', age=5)),
                       content_type='application/json')
        assert response.status_code == 201, 'status_code was not OK'
        pets = json.loads(response.data)
        assert pets['pet']['name'] == 'Piggy', 'pet was not returned'

    def test_getPet(self):
        #Test to make sure you can get a pet by name
        response = self.app.get('/pets/Doggy')
        assert response.status_code == 200, 'status_code was not OK'
        pet = json.loads(response.data)
        assert pet['name'] == 'Doggy', 'wrong pet returned'

    def test_putPet(self):
        #Test to see if you can update pet by name
        response = self.app.put('/pets/Doggy', data=json.dumps(dict(name='Piggy', species='Pig', age=5)),
                       content_type='application/json')
        assert response.status_code == 200, 'status_code was not OK'
        assert server.find_pet('Piggy') is not None, 'name not changed'

    def test_delPet(self):
        #Test to make sure you can delete pets
        response = self.app.delete('/pets/Doggy')
        assert response.status_code == 200, 'status_code was not OK'
        pet = json.loads(response.data)
        assert pet['name'] == 'Doggy', 'wrong pet returned'
        assert server.find_pet('Doggy') is None, 'pet not deleted'


    def test_postPetFail(self):
        #Test to see that you can't duplicate a pet
        response = self.app.post('/pets/', data=json.dumps(dict(name='Doggy', species='Pig', age=5)),
                       content_type='application/json')
        assert response.status_code == 409, 'status_code was not OK'
        error = json.loads(response.data)
        assert error['code'] == 409, 'wrong error type returned'
        #Test to see if passing in invalid arguments works
        response = self.app.post('/pets/', data=json.dumps(dict(name='Piggy', age=5)),
                       content_type='application/json')
        assert response.status_code == 400, 'status_code was not OK'
        error = json.loads(response.data)
        assert error['code'] == 400, 'wrong error type returned'

    def test_getPetFail(self):
        #Test to make sure the sever doesn't return anything for pets that don't exists
        response = self.app.get('/pets/Floggy')
        assert response.status_code == 404, 'status_code was not OK'
        error = json.loads(response.data)
        assert error['code'] == 404, 'wrong code returned'

    def test_putPetFail(self):
        #Test to make sure you can't post with incomplete data
        response = self.app.put('/pets/Doggy', data=json.dumps(dict(species='Pig', age=5)),
                       content_type='application/json')
        assert response.status_code == 400, 'status_code was not ERROR'
        error = json.loads(response.data)
        assert error['code'] == 400, 'wrong code returned'
        #Test to make sure you can post a pet through the put method
        response = self.app.put('/pets/Piggy', data=json.dumps(dict(name='Piggy', species='Pig', age=5)),
                       content_type='application/json')
        assert response.status_code == 404, 'status_code was not NOT FOUND'

    def test_delPetFail(self):
        #Test to make sure you can't delete something that isn't there
        response = self.app.delete('/pets/Floggy')
        assert response.status_code == 404, 'status_code was not NOT FOUND'
        error = json.loads(response.data)
        assert error['code'] == 404, 'wrong code returned'




if __name__ == '__main__':
    unittest.main()
