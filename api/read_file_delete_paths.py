from http.server import BaseHTTPRequestHandler
import os
from pymongo import MongoClient
import json
from flask import Flask, Response
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    from flask import request
    if request.headers.get('Content-Type') != 'application/json': return Response("Content-Type must be application/json", mimetype='text/plain', status=400)
    body = request.json
    args = {}
    if "_id" in body.keys():
        args["_id"] = body["_id"]
    if "name" in body.keys():
        args["name"] = body["name"]
    if "path" in body.keys():
        args["path"] = body["path"]
    if "redirect" in body.keys():
        args["redirect"] = body["redirect"]
    client = MongoClient(os.environ['MONGODB_URI'])
    data = [{
        "_id": str(i["_id"]),
        "name": i["name"] if "name" in i.keys() else None,
        "path": i["path"],
        "redirect": i["redirect"] if "redirect" in i.keys() else None
        } for i in client.data.file_delete_paths.find(args)]
    return Response(json.dumps([{j:i[j] for j in i.keys() if i[j] != None} for i in data]), mimetype='application/json')