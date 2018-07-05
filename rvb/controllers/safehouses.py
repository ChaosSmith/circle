from rvb import application
from rvb.models import *
from flask import Flask, request, json
from rvb.controllers.helpers import authenticate, parse_data, validate_data
from rvb.exceptions import ResourceMissing, InvalidUsage, Unauthenticated

@application.route('/safehouses', methods=['GET'])
def safehouses():
    if request.method == 'GET':
        player = authenticate(request,['Bravo'])
        return json.jsonify(safehouses=[safehouse.serialize() for safehouse in Safehouse.all()])
