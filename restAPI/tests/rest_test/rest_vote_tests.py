from restAPI import web_server
from restAPI.src.database.database import Database
import unittest
import time
import threading
from flask import json

class TestVoteRest(unittest.TestCase):
    def setUp(self):
        web_server.load_modules(Database("bbb_3000_testing"))
        web_server.app.database.clear()
        self.app = web_server.app.test_client()

        self.app.post('/candidate/',
                      data='{"name": "Mauro Murari", "id": "other_pirate"}',
                      headers={'content-type': 'application/json'})
        self.app.post('/candidate/',
                      data='{"name": "Bruce Wayne", "id": "batman"}',
                      headers={'content-type': 'application/json'})
        self.app.post('/candidate/',
                      data='{"name": "John Snow", "id": "john"}',
                      headers={'content-type': 'application/json'})
        self.app.post('/candidate/',
                      data='{"name": "Macgyver", "id": "master"}',
                      headers={'content-type': 'application/json'})

        self.app.post('/wall/',
                      data='{"id": "june_8", "candidates": ["master", "other_pirate", "batman"]}',
                      headers={'content-type': 'application/json'})
        self.app.delete('/wall/june_8')
        self.app.delete('/candidate/master')

        self.app.post('/wall/',
                      data='{"id": "june_12", "candidates": ["john", "other_pirate"]}',
                      headers={'content-type': 'application/json'})

    def tearDown(self):
        web_server.app.config['TESTING'] = False


    def test_add_empty(self):
        response = self.app.post('/vote/',
                                 data='{}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_add_without_wall(self):
        response = self.app.post('/vote/',
                                 data='{"candidate": "other_pirate"}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_add_without_candidate(self):
        response = self.app.post('/vote/',
                                 data='{"wall": "june_12"}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_add_candidate_not_added(self):
        response = self.app.post('/vote/',
                                 data='{"wall": "june_12", "candidate": "jedi"}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 404)

    def test_add_wall_not_added(self):
        response = self.app.post('/vote/',
                                 data='{"wall": "june_20", "candidate": "batman"}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 404)

    def test_add_wall_ended(self):
        response = self.app.post('/vote/',
                                 data='{"wall": "june_8", "candidate": "batman"}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_add_candidate_out(self):
        response = self.app.post('/vote/',
                                 data='{"wall": "june_12", "candidate": "master"}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_add_candidate_out_of_wall(self):
        response = self.app.post('/vote/',
                                 data='{"wall": "june_12", "candidate": "batman"}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_add(self):
        response = self.app.post('/vote/',
                                 data='{"wall": "june_12", "candidate": "other_pirate"}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)

        response = self.app.post('/vote/',
                                 data='{"wall": "june_12", "candidate": "other_pirate"}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)

        response = self.app.post('/vote/',
                                 data='{"wall": "june_12", "candidate": "john"}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)

    def test_add_stress(self):
        requests = []
        for _ in xrange(2):
            request = add_vote_thread(self.app, "john")
            request.start()
            requests.append(request)

        for _ in xrange(3):
            request = add_vote_thread(self.app, "other_pirate")
            request.start()
            requests.append(request)

        time.sleep(1)
        has_active = True
        while has_active:
            has_active = False
            for request in requests:
                if request.is_alive():
                    time.sleep(0.25)
                    has_active = True
                    break
                requests.remove(request)

        response = self.app.get('/wall/june_12/candidate/')
        response_data = json.loads(response.data)
        self.assertEqual(response_data["total"], 1000)

class add_vote_thread(threading.Thread):
    def __init__(self, app, name, votes=200):
        threading.Thread.__init__(self)
        self.app = app
        self.name = name
        self.votes = votes

    def run(self):
        while self.votes > 0:
            response = self.app.post('/vote/',
                                    data='{"wall": "june_12", "candidate": "' + self.name + '"}',
                                    headers={'content-type': 'application/json'})
            assert response.status_code == 201
            self.votes -= 1


if __name__ == '__main__':
    unittest.main()
