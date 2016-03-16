from restAPI.src.database.database import Database

from restAPI.src.controllers.controller_candidate import CandidateController
from restAPI.src.entitys.entity_candidate import Candidate

from restAPI.src.exceptions.exceptions_candidate import CandidateDoNotExist, CandidateAlreadyAdded, \
    CandidateInvalidData, CandidateIsOut

import unittest

class TestCandidateController(unittest.TestCase):

    def setUp(self):
        db = Database("testing")
        db.clear()

        self.candidates = CandidateController(db)
        self.batman = Candidate("Bruce Wayne", "batman", True)


    def test_validate_empty(self):
        self.assertFalse(self.candidates.is_valid("", ""))

    def test_validate_without_name(self):
        self.assertFalse(self.candidates.is_valid("", "1"))

    def test_validate_without_id(self):
        self.assertFalse(self.candidates.is_valid("Mario", ""))

    def test_validate_with_data(self):
        self.assertTrue(self.candidates.is_valid(self.batman.name, self.batman.id))

    def test_get_not_added(self):
        with self.assertRaises(CandidateDoNotExist):
            self.candidates.get(self.batman.id)

    def test_get_added(self):
        self.candidates.add(self.batman.name, self.batman.id)
        self.assertEqual(self.batman, self.candidates.get(self.batman.id))

    def test_not_exist(self):
        self.assertFalse(self.candidates.exist(self.batman.id))

    def test_exist(self):
        self.candidates.add(self.batman.name, self.batman.id)
        self.assertTrue(self.candidates.exist(self.batman.id))

    def test_add_invalid(self):
        with self.assertRaises(CandidateInvalidData):
            self.candidates.add("", "")

    def test_add_invalid_name(self):
        with self.assertRaises(CandidateInvalidData):
            self.candidates.add("", "123")

    def test_add_invalid_id(self):
        with self.assertRaises(CandidateInvalidData):
            self.candidates.add("Mario", "")

    def test_add_duplicated(self):
        self.candidates.add(self.batman.name, self.batman.id)
        with self.assertRaises(CandidateAlreadyAdded):
            self.candidates.add(self.batman.name, self.batman.id)

    def test_add(self):
        new_candidate = self.candidates.add(self.batman.name, self.batman.id)
        self.assertEqual(self.batman, new_candidate)

    def test_remove_not_added(self):
        with self.assertRaises(CandidateDoNotExist):
            self.candidates.remove(self.batman.id)

    def test_remove_removed(self):
        self.candidates.add(self.batman.name, self.batman.id)
        self.candidates.remove(self.batman.id)

        with self.assertRaises(CandidateIsOut):
            self.candidates.remove(self.batman.id)

    def test_remove_added(self):
        self.candidates.add(self.batman.name, self.batman.id)
        self.assertTrue(self.batman.active)

        removed = self.candidates.remove(self.batman.id)
        self.assertFalse(removed.active)

if __name__ == '__main__':
    unittest.main()
