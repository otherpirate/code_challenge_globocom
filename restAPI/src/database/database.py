from database_mongoDB import DatabaseMongoDB
from decouple import config

class Database:
    def __init__(self, db_name=config("DB_NAME")):
        self.connection = DatabaseMongoDB(config('DB_ADDRESS'),
                                          config('DB_PORT', cast=int),
                                          db_name,
                                          config('DB_USER'),
                                          config('DB_PASSWORD'))

    def clear(self):
        self.connection.clear()

    def candidate_get(self, id):
        return self.connection.candidate_get(id)

    def candidate_add(self, candidate):
        return self.connection.candidate_add(candidate)

    def candidate_update(self, candidate):
        return self.connection.candidate_update(candidate)

    def is_candidate_in_wall(self, candidate, wall):
        return self.connection.is_candidate_in_wall(candidate, wall)

    def wall_get_active(self):
        return self.connection.wall_get_active()

    def wall_get(self, id):
        return self.connection.wall_get(id)

    def wall_add(self, wall):
        return self.connection.wall_add(wall)

    def wall_update(self, wall):
        return self.connection.wall_update(wall)

    def wall_get_currently(self):
        return self.connection.wall_get_currently()

    def vote_add(self, wall, candidate):
        return self.connection.vote_add(wall, candidate)

    def vote_get_by_candidate(self, wall):
        return self.connection.vote_get_by_candidate(wall)

    def vote_get_by_hour(self, wall):
        return self.connection.vote_get_by_hour(wall)