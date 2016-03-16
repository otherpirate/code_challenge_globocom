from restAPI.src.database.database import Database

from restAPI.src.controllers.controller_candidate import CandidateController
from restAPI.src.controllers.controller_wall import WallController
from restAPI.src.entitys.entity_wall import Wall

from restAPI.src.exceptions.exceptions_candidate import CandidateDoNotExist, CandidateIsOut
from restAPI.src.exceptions.exceptions_wall import WallAlreadyRunning, WallAlreadyAdded, WallInvalidData, WallDoNotExist, \
    WallIsEnded, WallInsufficientCandidates

import unittest

class TestWallController(unittest.TestCase):

    def setUp(self):
        db = Database("testing")
        db.clear()

        self.walls = WallController(db)
        self.candidates = CandidateController(db)
        self.candidates.add("Bruce Wayne", "batman")
        self.candidates.add("Mario", 1)
        self.candidates.add("John Snow", "John")


    def test_validate_empty(self):
        self.assertFalse(self.walls.is_valid("", None))

    def test_validate_without_candidates(self):
        self.assertFalse(self.walls.is_valid("march", None))

    def test_validate_without_id(self):
        self.assertFalse(self.walls.is_valid("", ["batman", "John", 1]))

    def test_validate_insufficient_candidates(self):
        with self.assertRaises(WallInsufficientCandidates):
            self.walls.is_valid("march", ["batman"])

    def test_validate_invalid_candidates(self):
        with self.assertRaises(CandidateDoNotExist):
            self.walls.is_valid("march", ["batman", "joker"])

    def test_validate_removed_candidates(self):
        self.candidates.remove("batman")

        with self.assertRaises(CandidateIsOut):
            self.walls.is_valid("march", ["batman", "John"])

    def test_exist_active(self):
        self.walls.add("march", ["batman", "John"])
        self.assertTrue(self.walls.exist_active())

    def test_no_exist_active(self):
        self.assertFalse(self.walls.exist_active())
        self.walls.add("march", ["batman", 1, "John"])
        self.assertTrue(self.walls.exist_active())
        self.walls.remove("march")
        self.assertFalse(self.walls.exist_active())

    def test_wall_add_with_active(self):
        self.walls.add("march", ["batman", 1, "John"])

        with self.assertRaises(WallAlreadyRunning):
            self.walls.add("march", ["batman", "John"])

    def test_add_duplicated_candidates(self):
        wall = self.walls.add("march", ["batman", "batman", "John"])
        self.assertEqual(2, len(wall.candidates))

    def test_add_empty(self):
        with self.assertRaises(WallInvalidData):
            self.walls.add("", None)

    def test_add_without_candidates(self):
        with self.assertRaises(WallInvalidData):
            self.walls.add("march", None)

    def test_add_without_id(self):
        with self.assertRaises(WallInvalidData):
            self.walls.add("", ["batman", "John", 1])

    def test_add_insufficient_candidates(self):
        with self.assertRaises(WallInsufficientCandidates):
            self.walls.add("march", ["batman"])

    def test_add_invalid_candidates(self):
        with self.assertRaises(CandidateDoNotExist):
            self.walls.add("march", ["batman", "joker"])

    def test_add_removed_candidates(self):
        self.candidates.remove("batman")

        with self.assertRaises(CandidateIsOut):
            self.walls.add("march", ["batman", "John"])

    def test_add_duplicated(self):
        self.walls.add("march", ["batman", 1, "John"])
        self.walls.remove("march")

        with self.assertRaises(WallAlreadyAdded):
            self.walls.add("march", ["batman", "John"])

    def test_add_two_candidates(self):
        self.walls.add("march", ["batman", "John"])

    def test_add_many_candidates(self):
        wall = self.walls.add("march", ["batman", 1, "John"])
        self.assertEqual(Wall("march", True, ["batman", 1, "John"]), wall)

    def test_remove_not_added(self):
        with self.assertRaises(WallDoNotExist):
            self.walls.remove("march")

    def test_remove_removed(self):
        self.walls.add("march", ["batman", 1, "John"])
        self.walls.remove("march")
        with self.assertRaises(WallIsEnded):
            self.walls.remove("march")

    def test_remove(self):
        self.walls.add("march", ["batman", 1, "John"])
        wall = self.walls.remove("march")
        self.assertEqual(Wall("march", False, ["batman", 1, "John"]), wall)

    def test_get_currently_empty(self):
        self.assertIsNone(self.walls.get_currently())

    def test_get_currently_removed(self):
        self.walls.add("march", ["batman", 1, "John"])
        self.walls.remove("march")
        self.assertIsNone(self.walls.get_currently())

    def test_get_currently(self):
        wall = self.walls.add("march", ["batman", 1, "John"])
        self.assertEqual(wall, self.walls.get_currently())

if __name__ == '__main__':
    unittest.main()
