from restAPI.src.database.database import Database

from restAPI.src.controllers.controller_candidate import CandidateController
from restAPI.src.controllers.controller_wall import WallController
from restAPI.src.controllers.controller_vote import VoteController

from restAPI.src.exceptions.exceptions_vote import VoteInvalid
from restAPI.src.exceptions.exceptions_wall import WallIsEnded
from restAPI.src.exceptions.exceptions_candidate import CandidateIsOut, CandidateIsNotInWall

import unittest

class TestVoteController(unittest.TestCase):

    def setUp(self):
        db = Database("bbb_3000_testing")
        db.clear()

        self.candidates = CandidateController(db)
        self.batman = self.candidates.add("Bruce Wayne", "batman")
        self.mario = self.candidates.add("Mario", 1)
        self.john = self.candidates.add("John Snow", "John")
        self.jedi = self.candidates.add("Master Yoda", "Jedi")

        self.walls = WallController(db)
        self.april_05 = self.walls.add("april_05", ["John", "batman", 1])

        self.votes = VoteController(db)


    def test_validate_empty(self):
        self.assertFalse(self.votes.is_valid(None, None))

    def test_validate_without_wall(self):
        self.assertFalse(self.votes.is_valid(None, self.batman))

    def test_validate_without_candidate(self):
        self.assertFalse(self.votes.is_valid(self.april_05, None))

    def test_validate_valid(self):
        self.assertTrue(self.votes.is_valid(self.april_05, self.batman))

    def test_add_empty(self):
        with self.assertRaises(VoteInvalid):
            self.votes.add(None, None)

    def test_add_without_wall(self):
        with self.assertRaises(VoteInvalid):
            self.votes.add(None, self.batman)

    def test_add_without_candidate(self):
        with self.assertRaises(VoteInvalid):
            self.votes.add(self.april_05, None)

    def test_add_with_wall_ended(self):
        self.april_05 = self.walls.remove(self.april_05.id)
        with self.assertRaises(WallIsEnded):
            self.votes.add(self.april_05, self.batman)

    def test_add_with_candidate_out(self):
        self.batman = self.candidates.remove(self.batman.id)
        with self.assertRaises(CandidateIsOut):
            self.votes.add(self.april_05, self.batman)

    def test_add_with_not_wall_candidate(self):
        with self.assertRaises(CandidateIsNotInWall):
            self.votes.add(self.april_05, self.jedi)

    def test_add(self):
        self.assertTrue(self.votes.add(self.april_05, self.batman))
        self.assertTrue(self.votes.add(self.april_05, self.batman))
        self.assertTrue(self.votes.add(self.april_05, self.john))
        self.assertTrue(self.votes.add(self.april_05, self.john))
        self.assertTrue(self.votes.add(self.april_05, self.batman))
        self.assertTrue(self.votes.add(self.april_05, self.john))
        self.assertTrue(self.votes.add(self.april_05, self.mario))
        self.assertTrue(self.votes.add(self.april_05, self.batman))
        self.assertTrue(self.votes.add(self.april_05, self.mario))
        self.assertTrue(self.votes.add(self.april_05, self.batman))
        self.assertTrue(self.votes.add(self.april_05, self.batman))
        self.assertTrue(self.votes.add(self.april_05, self.batman))

    def test_resume(self):
        self.test_add()

        report = self.votes.resume_candidate(self.april_05)
        self.assertEqual(7, report[self.batman.id])
        self.assertEqual(3, report[self.john.id])
        self.assertEqual(2, report[self.mario.id])
        self.assertEqual(12, report["total"])

    def test_add_two_walls(self):
        self.test_add()
        self.april_05 = self.walls.remove(self.april_05.id)
        self.mario = self.candidates.remove(self.mario.id)

        self.june_03 = self.walls.add("june_03", ["John", "batman", "Jedi"])
        self.assertTrue(self.votes.add(self.june_03, self.jedi))
        self.assertTrue(self.votes.add(self.june_03, self.jedi))
        self.assertTrue(self.votes.add(self.june_03, self.john))
        self.assertTrue(self.votes.add(self.june_03, self.batman))
        self.assertTrue(self.votes.add(self.june_03, self.john))
        self.assertTrue(self.votes.add(self.june_03, self.jedi))
        self.assertTrue(self.votes.add(self.june_03, self.jedi))
        self.assertTrue(self.votes.add(self.june_03, self.jedi))
        self.assertTrue(self.votes.add(self.june_03, self.john))
        self.assertTrue(self.votes.add(self.june_03, self.batman))
        self.assertTrue(self.votes.add(self.june_03, self.batman))
        self.assertTrue(self.votes.add(self.june_03, self.batman))
        self.assertTrue(self.votes.add(self.june_03, self.jedi))
        self.assertTrue(self.votes.add(self.june_03, self.jedi))
        self.assertTrue(self.votes.add(self.june_03, self.john))
        self.assertTrue(self.votes.add(self.june_03, self.batman))
        self.assertTrue(self.votes.add(self.june_03, self.batman))

        report = self.votes.resume_candidate(self.june_03)
        self.assertEqual(6, report[self.batman.id])
        self.assertEqual(4, report[self.john.id])
        self.assertEqual(7, report[self.jedi.id])
        self.assertEqual(17, report["total"])


if __name__ == '__main__':
    unittest.main()
