import json

class Wall():
    def __init__(self, id, active, candidates):
        self.id = id
        self.active = active
        self.candidates = candidates

    def to_json(self):
        return json.dumps(self.__dict__, indent=4)

    def __eq__(self, other):
        return self.id == self.id and \
               self.active == other.active and \
               set(self.candidates) == set(other.candidates)