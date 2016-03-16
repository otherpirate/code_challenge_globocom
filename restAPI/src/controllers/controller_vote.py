from restAPI.src.exceptions.exceptions_vote import VoteInvalid
from restAPI.src.exceptions.exceptions_wall import WallIsEnded
from restAPI.src.exceptions.exceptions_candidate import CandidateIsOut, CandidateIsNotInWall

class VoteController:
    def __init__(self, database):
        self.db = database

    def is_valid(self, wall, candidate):
        if not wall:
            return False

        if not candidate:
            return False

        return True

    def add(self, wall, candidate):
        if not self.is_valid(wall, candidate):
            raise VoteInvalid()

        if not wall.active:
            raise WallIsEnded()

        if not candidate.active:
            raise CandidateIsOut()

        if not self.db.is_candidate_in_wall(candidate, wall):
            raise CandidateIsNotInWall()

        return self.db.vote_add(wall, candidate)

    def resume_candidate(self, wall):
        return self.db.vote_get_by_candidate(wall)

    def resume_hour(self, wall):
        return self.db.vote_get_by_hour(wall)