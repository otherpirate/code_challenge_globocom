import json

from flask import Flask, request, abort, Response
app = Flask(__name__)

from restAPI.src.database.database import Database
from restAPI.src.controllers.controller_candidate import CandidateController
from restAPI.src.controllers.controller_wall import WallController
from restAPI.src.controllers.controller_vote import VoteController

from restAPI.src.exceptions.exceptions_vote import VoteInvalid
from restAPI.src.exceptions.exceptions_candidate import CandidateAlreadyAdded, CandidateDoNotExist, CandidateIsOut, \
    CandidateIsNotInWall, CandidateInvalidData
from restAPI.src.exceptions.exceptions_wall import WallAlreadyRunning, WallInsufficientCandidates, WallInvalidData, \
    WallDoNotExist, WallIsEnded, WallAlreadyAdded

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

@app.route("/candidate/", methods=["POST"])
def candidate_add():
    try:
        new_candidate = app.candidate.add(request.json["name"], request.json["id"])
        if not new_candidate:
            abort(500)
    except (CandidateInvalidData, KeyError):
        abort(400)
    except CandidateAlreadyAdded:
        abort(409)

    return Response(response=new_candidate.to_json(), status=201, mimetype="application/json")

@app.route("/candidate/<id>", methods=["DELETE"])
def candidate_remove(id):
    try:
        if not app.candidate.remove(id):
            abort(500)
    except CandidateDoNotExist:
        abort(404)
    except CandidateIsOut:
        abort(409)

    return Response(status=202)

@app.route("/wall/", methods=["POST"])
def wall_add():
    try:
        new_wall = app.wall.add(request.json["id"], request.json["candidates"])
        if not new_wall:
            abort(500)
    except (WallAlreadyRunning, WallAlreadyAdded):
        abort(409)
    except (WallInvalidData, WallInsufficientCandidates, CandidateDoNotExist, CandidateIsOut, KeyError):
        abort(400)

    return Response(response=new_wall.to_json(), status=201, mimetype="application/json")

@app.route("/wall/<id>", methods=["DELETE"])
def wall_remove(id):
    try:
        if not app.wall.remove(id):
            abort(500)
    except WallDoNotExist:
        abort(404)
    except WallIsEnded:
        abort(409)

    return Response(status=202)

@app.route("/wall/", methods=["GET"])
def vote_get():
    wall = app.wall.get_currently()
    if not wall:
        abort(404)

    return Response(response=wall.to_json(), status=200, mimetype="application/json")

@app.route("/wall/<id>/candidate/", methods=["GET"])
def wall_report_candidate(id):
    try:
        wall = app.wall.get(id)
    except WallDoNotExist:
        abort(404)

    resume = app.vote.resume_candidate(wall)
    return Response(response=json.dumps(resume, indent=4), status=200, mimetype="application/json")

@app.route("/wall/<id>/hour/", methods=["GET"])
def wall_report_hour(id):
    try:
        wall = app.wall.get(id)
    except WallDoNotExist:
        abort(404)

    resume = app.vote.resume_hour(wall)
    return Response(response=json.dumps(resume, indent=4), status=200, mimetype="application/json")

@app.route("/vote/", methods=["POST"])
def vote_add():
    try:
        wall = app.wall.get(request.json["wall"])
        candidate = app.candidate.get(request.json["candidate"])

        if not app.vote.add(wall, candidate):
            abort(500)
    except (CandidateDoNotExist, WallDoNotExist):
        abort(404)
    except (VoteInvalid, WallIsEnded, CandidateIsOut, CandidateIsNotInWall, KeyError):
        abort(400)

    return Response(status=201)

def start():
    app.run(host='0.0.0.0')

if app.config['TESTING']:
    app.database = Database("testing")
else:
    app.database = Database()

app.candidate = CandidateController(app.database)
app.wall = WallController(app.database)
app.vote = VoteController(app.database)