from restAPI import web_server
import unittest


class TestCandidateRest(unittest.TestCase):
    def setUp(self):
        web_server.app.config['TESTING'] = True
        web_server.app.database.clear()
        self.app = web_server.app.test_client()

    def tearDown(self):
        web_server.app.config['TESTING'] = False


    def test_add_empty(self):
        response = self.app.post('/candidate/',
                                 data='{}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_add_without_id(self):
        response = self.app.post('/candidate/',
                                 data='{"name": "Mauro Murari", "id": ""}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_add_without_name(self):
        response = self.app.post('/candidate/',
                                 data='{"name": "", "id": "other_pirate"}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_add(self):
        response = self.app.post('/candidate/',
                                 data='{"name": "Mauro Murari", "id": "other_pirate"}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)
        response = self.app.post('/candidate/',
                                 data='{"name": "Bruce Wayne", "id": "batman"}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)

    def test_add_duplicate(self):
        response = self.app.post('/candidate/',
                                 data='{"name": "Mauro Murari", "id": "other_pirate"}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)
        response = self.app.post('/candidate/',
                                 data='{"name": "Mauro Murari", "id": "other_pirate"}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 409)

    def test_remove_not_added(self):
        response = self.app.post('/candidate/',
                                 data='{"name": "Mauro Murari", "id": "other_pirate"}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)

        response = self.app.delete('/candidate/batman')
        self.assertEqual(response.status_code, 404)

    def test_remove(self):
        response = self.app.post('/candidate/',
                                 data='{"name": "Mauro Murari", "id": "other_pirate"}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)

        response = self.app.delete('/candidate/other_pirate')
        self.assertEqual(response.status_code, 202)

    def test_remove_removed(self):
        response = self.app.post('/candidate/',
                                 data='{"name": "Mauro Murari", "id": "other_pirate"}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)

        response = self.app.delete('/candidate/other_pirate')
        self.assertEqual(response.status_code, 202)

        response = self.app.delete('/candidate/other_pirate')
        self.assertEqual(response.status_code, 409)

if __name__ == '__main__':
    unittest.main()
