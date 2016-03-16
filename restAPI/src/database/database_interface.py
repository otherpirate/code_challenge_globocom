import abc

class DatabaseInterface(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def clear(self):
        pass

    @abc.abstractmethod
    def candidate_get(self, id):
        pass

    @abc.abstractmethod
    def candidate_update(self, candidate):
        pass

    @abc.abstractmethod
    def candidate_add(self, candidate):
        pass

    @abc.abstractmethod
    def is_candidate_in_wall(self, candidate, wall):
        pass

    @abc.abstractmethod
    def wall_get_active(self):
        pass

    @abc.abstractmethod
    def wall_get(self, id):
        pass

    @abc.abstractmethod
    def wall_add(self, wall):
        pass

    @abc.abstractmethod
    def wall_update(self, wall):
        pass

    @abc.abstractmethod
    def wall_get_currently(self):
        pass

    @abc.abstractmethod
    def vote_add(self, wall, candidate):
        pass

    @abc.abstractmethod
    def vote_get_by_candidate(self, wall):
        pass

    @abc.abstractmethod
    def vote_get_by_hour(self, wall):
        pass