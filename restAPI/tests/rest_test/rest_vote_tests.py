from restAPI import web_server
import unittest
import time
import threading

class TestVoteRest(unittest.TestCase):
    def setUp(self):
        web_server.app.config['TESTING'] = True
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
        for _ in xrange(400):
            requests.append(add_vote_thread(self.app, "john"))

        for _ in xrange(600):
            requests.append(add_vote_thread(self.app, "other_pirate"))

        for request in requests:
            request.start()

        ini_time = time.time()
        time.sleep(.99)
        end_time = time.time()

        self.assertLess((end_time-ini_time), 1)

class add_vote_thread(threading.Thread):
    def __init__(self, app, name):
        threading.Thread.__init__(self)
        self.app = app
        self.name = name

    def run(self):
        response = self.app.post('/vote/',
                                data='{"wall": "june_12", "candidate": "' + self.name + '"}',
                                headers={'content-type': 'application/json'})
        assert response.status_code == 201


if __name__ == '__main__':
    unittest.main()
