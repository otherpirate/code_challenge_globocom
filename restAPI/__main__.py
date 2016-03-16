from web_server import *
from restAPI.src.database.database import Database
from restAPI.src.controllers.controller_candidate import CandidateController
from restAPI.src.controllers.controller_wall import WallController
from restAPI.src.controllers.controller_vote import VoteController


if __name__ == "__main__":
    database = Database()
    database.clear()
    app.candidate = CandidateController(database)
    app.wall = WallController(database)
    app.vote = VoteController(database)
    app.run(host='0.0.0.0')