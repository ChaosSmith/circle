from rvb import application
from rvb.models import *
from flask import Flask, request, json
from rvb.controllers.helpers import authenticate, parse_data, validate_data
from rvb.exceptions import ResourceMissing, InvalidUsage, Unauthenticated

@application.route('/packages', methods=['GET'])
def packages():
    if request.method == 'GET':
        player = authenticate(request,['Alpha'])
        return json.jsonify(packages=[package.serialize() for package in Package.all()])
