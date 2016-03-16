import json

class Candidate():
    def __init__(self, name, id, active):
        self.name = name
        self.id = id
        self.active = active

    def to_json(self):
        return json.dumps(self.__dict__, indent=4)

    def __eq__(self, other):
        return self.id == other.id and \
               self.name == self.name and \
               self.active == other.active