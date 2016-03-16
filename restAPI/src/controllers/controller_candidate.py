from restAPI.src.entitys.entity_candidate import Candidate
from restAPI.src.exceptions.exceptions_candidate import CandidateDoNotExist, CandidateAlreadyAdded, CandidateInvalidData, CandidateIsOut

class CandidateController:
    def __init__(self, database):
        self.db = database

    def is_valid(self, name, id):
        if not name:
            return False

        if not id:
            return False

        return True

    def get(self, id):
        candidate = self.db.candidate_get(id)

        if not candidate:
            raise CandidateDoNotExist()

        return candidate

    def exist(self, id):
        return bool(self.db.candidate_get(id))

    def add(self, name, id):
        if not self.is_valid(name, id):
            raise CandidateInvalidData()

        if self.exist(id):
            raise CandidateAlreadyAdded()
        return self.db.candidate_add(Candidate(name, id, True))

    def remove(self, id):
        candidate = self.get(id)
        if not candidate.active:
            raise CandidateIsOut()

        candidate.active = False
        return self.db.candidate_update(candidate)