import datetime
import pymongo
from pymongo import MongoClient

import database_interface
from restAPI.src.entitys.entity_candidate import Candidate
from restAPI.src.entitys.entity_wall import Wall


class DatabaseMongoDB(database_interface.DatabaseInterface):

    def __init__(self, address, port, db_name, user, password):
        self.connection = MongoClient(address, port)
        self.database = self.connection.get_database(db_name)
        if user and password:
            self.database.authenticate(user, password)

    def clear(self):
        super(DatabaseMongoDB, self).clear()
        for collection in self.database.collection_names(False):
            self.database.drop_collection(collection)

    def candidate_get(self, id):
        super(DatabaseMongoDB, self).candidate_get(id)

        search = self.database.candidates.find({"id": id})
        if search.count() == 1:
            found = search[0]
            return Candidate(found["name"],
                             found["id"],
                             found["active"])
        return None

    def candidate_add(self, candidate):
        super(DatabaseMongoDB, self).candidate_add(candidate)
        self.database.candidates.insert_one(candidate.__dict__)
        return self.candidate_get(candidate.id)

    def candidate_update(self, candidate):
        super(DatabaseMongoDB, self).candidate_update(candidate)
        self.database.candidates.update_one({"id": candidate.id}, {'$set': candidate.__dict__})
        return self.candidate_get(candidate.id)

    def is_candidate_in_wall(self, candidate, wall):
        super(DatabaseMongoDB, self).is_candidate_in_wall(candidate, wall)

        search = self.database.walls.find({"id": wall.id},
                                          {"candidates": {"$elemMatch": {"$eq": candidate.id}}})
        if search.count() == 1:
            found = search[0]
            if "candidates" in found:
                return len(found["candidates"]) == 1
        return False

    def wall_get_active(self):
        super(DatabaseMongoDB, self).wall_get_active()
        filtered = []
        for wall in self.database.walls.find({"active": True}):
            filtered.append(Wall(wall["id"], wall["active"], wall["candidates"]))
        return filtered

    def wall_get(self, id):
        super(DatabaseMongoDB, self).wall_get(id)

        search = self.database.walls.find({"id": id})
        if search.count() == 1:
            found = search[0]
            return Wall(found["id"],
                        found["active"],
                        found["candidates"])
        return None

    def wall_add(self, wall):
        super(DatabaseMongoDB, self).wall_add(wall)
        self.database.walls.insert_one(wall.__dict__)
        return self.wall_get(wall.id)

    def wall_update(self, wall):
        super(DatabaseMongoDB, self).wall_update(wall)
        self.database.walls.update_one({"id": wall.id}, {'$set': wall.__dict__})
        return self.wall_get(wall.id)

    def wall_get_currently(self):
        super(DatabaseMongoDB, self).wall_get_currently()
        search = self.database.walls.find({"active": True}).limit(1).sort('$natural', pymongo.ASCENDING)
        if search.count() == 1:
            found = search[0]
            return Wall(found["id"],
                        found["active"],
                        found["candidates"])
        return None

    def vote_add(self, wall, candidate):
        super(DatabaseMongoDB, self).vote_add(wall, candidate)
        return bool(
                self.database.votes.insert_one({"wall_id": wall.id,
                                                "candidate_id": candidate.id,
                                                "created_at": datetime.datetime.now()}))

    def vote_get_by_candidate(self, wall):
        super(DatabaseMongoDB, self).vote_get_by_candidate(wall)
        return self.__vote_get_by(wall, "$candidate_id")

    def vote_get_by_hour(self, wall):
        super(DatabaseMongoDB, self).vote_get_by_hour(wall)
        return self.__vote_get_by(wall, {"$hour": "$created_at"})

    def __vote_get_by(self, wall, group):
        pipe = []
        pipe.append({"$match": {"wall_id": wall.id}})
        pipe.append({
            "$group": {
                "_id": group,
                "votes": {"$sum": 1}
            }
        })

        result = {}
        result["total"] = 0
        search = list(self.database.votes.aggregate(pipeline=pipe))
        if search:
            for item in search:
                result[item["_id"]] = item["votes"]
                result["total"] += item["votes"]

        return result