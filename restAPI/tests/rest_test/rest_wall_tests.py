from restAPI import web_server
from restAPI.src.database.database import Database
import unittest


class TestWallRest(unittest.TestCase):
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
        self.app.delete('/candidate/master')

    def tearDown(self):
        web_server.app.config['TESTING'] = False


    def test_add_empty(self):
        response = self.app.post('/wall/',
                                 data='{}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_add_without_id(self):
        response = self.app.post('/wall/',
                                 data='{"candidates": ["other_pirate", "batman", "john"], "id": ""}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_add_without_candidates(self):
        response = self.app.post('/wall/',
                                 data='{"candidates": "", "id": "june_8"}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_add_insufficient_candidates(self):
        response = self.app.post('/wall/',
                                 data='{"id": "june_8", "candidates": ["other_pirate"]}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_add_removed_candidates(self):
        response = self.app.post('/wall/',
                                 data='{"id": "june_8", "candidates": ["other_pirate", "master"]}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_add_not_added_candidates(self):
        response = self.app.post('/wall/',
                                 data='{"id": "june_8", "candidates": ["other_pirate", "jedi"]}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_add(self):
        response = self.app.post('/wall/',
                                 data='{"id": "june_8", "candidates": ["john", "other_pirate", "batman"]}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)

    def test_add_duplicated(self):
        response = self.app.post('/wall/',
                                 data='{"id": "june_8", "candidates": ["john", "other_pirate", "batman"]}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)

        response = self.app.delete('/wall/june_8')
        self.assertEqual(response.status_code, 202)

        response = self.app.post('/wall/',
                                 data='{"id": "june_8", "candidates": ["john", "batman"]}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 409)

    def test_add_with_active(self):
        response = self.app.post('/wall/',
                                 data='{"id": "june_8", "candidates": ["john", "other_pirate", "batman"]}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)

        response = self.app.post('/wall/',
                                 data='{"id": "june_12", "candidates": ["john", "batman"]}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 409)

    def test_remove_not_added(self):
        response = self.app.post('/wall/',
                                 data='{"id": "june_8", "candidates": ["john", "other_pirate", "batman"]}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)

        response = self.app.delete('/wall/june_12')
        self.assertEqual(response.status_code, 404)

    def test_remove(self):
        response = self.app.post('/wall/',
                                 data='{"id": "june_8", "candidates": ["john", "other_pirate", "batman"]}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)

        response = self.app.delete('/wall/june_8')
        self.assertEqual(response.status_code, 202)

    def test_remove_removed(self):
        response = self.app.post('/wall/',
                                 data='{"id": "june_8", "candidates": ["john", "other_pirate", "batman"]}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)

        response = self.app.delete('/wall/june_8')
        self.assertEqual(response.status_code, 202)

        response = self.app.delete('/wall/june_8')
        self.assertEqual(response.status_code, 409)

    def test_get_not_added(self):
        response = self.app.get('/wall/')
        self.assertEqual(response.status_code, 404)

        response = self.app.post('/wall/',
                                 data='{"id": "june_8", "candidates": ["john", "other_pirate", "batman"]}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)

        response = self.app.delete('/wall/june_8')
        self.assertEqual(response.status_code, 202)

        response = self.app.get('/wall/')
        self.assertEqual(response.status_code, 404)

    def test_get_added(self):
        response = self.app.post('/wall/',
                                 data='{"id": "june_8", "candidates": ["john", "other_pirate", "batman"]}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)

        response = self.app.get('/wall/')
        self.assertEqual(response.status_code, 200)

    def test_report_candidate_not_added(self):
        response = self.app.get('/wall/june_8/candidate/')
        self.assertEqual(response.status_code, 404)

    def test_report_candidate(self):
        response = self.app.post('/wall/',
                                 data='{"id": "june_8", "candidates": ["john", "other_pirate", "batman"]}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)

        response = self.app.get('/wall/june_8/candidate/')
        self.assertEqual(response.status_code, 200)

    def test_report_hour_not_added(self):
        response = self.app.get('/wall/june_8/hour/')
        self.assertEqual(response.status_code, 404)

    def test_report_hour(self):
        response = self.app.post('/wall/',
                                 data='{"id": "june_8", "candidates": ["john", "other_pirate", "batman"]}',
                                 headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)

        response = self.app.get('/wall/june_8/hour/')
        self.assertEqual(response.status_code, 200)

    def test_report_candidate(self):
        pass

    def test_report_hour(self):
        pass


if __name__ == '__main__':
    unittest.main()
