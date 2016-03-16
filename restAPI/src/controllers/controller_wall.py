from restAPI.src.entitys.entity_wall import Wall
from restAPI.src.exceptions.exceptions_wall import WallInsufficientCandidates, WallAlreadyRunning, WallInvalidData, \
    WallAlreadyAdded, WallIsEnded, WallDoNotExist
from restAPI.src.exceptions.exceptions_candidate import CandidateIsOut, CandidateDoNotExist

class WallController:
    def __init__(self, database):
        self.db = database

    def is_valid(self, id, candidates):
        if not id:
            return False

        if not candidates:
            return False

        if len(candidates) <= 1:
            raise WallInsufficientCandidates()

        for id in candidates:
            candidate = self.db.candidate_get(id)

            if not candidate:
                raise CandidateDoNotExist

            if not candidate.active:
                raise CandidateIsOut

        return True

    def exist_active(self):
        return bool(self.db.wall_get_active())

    def exist(self, id):
        return bool(self.db.wall_get(id))

    def get(self, id):
        wall = self.db.wall_get(id)

        if not wall:
            raise WallDoNotExist()

        return wall

    def add(self, id, candidates):
        if self.exist_active():
            raise WallAlreadyRunning()

        candidates = list(set(candidates)) if candidates else []
        if not self.is_valid(id, candidates):
            raise WallInvalidData()

        if self.exist(id):
            raise WallAlreadyAdded()

        return self.db.wall_add(Wall(id, True, candidates))

    def remove(self, id):
        wall = self.get(id)
        if not wall.active:
            raise WallIsEnded()

        wall.active = False
        return self.db.wall_update(wall)

    def get_currently(self):
        return self.db.wall_get_currently()