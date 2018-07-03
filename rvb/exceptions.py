from rvb import application
from flask import Flask, request, json

class Unauthenticated(Exception):
    status_code = 401

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class FullGame(Exception):
    status_code = 423

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class ResourceMissing(Exception):
    status_code = 404

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class IsDead(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class IllegalMove(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@application.errorhandler(Unauthenticated)
def handle_invalid_usage(error):
    response = json.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@application.errorhandler(IllegalMove)
def handle_invalid_usage(error):
    response = json.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@application.errorhandler(IsDead)
def handle_invalid_usage(error):
    response = json.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@application.errorhandler(FullGame)
def handle_invalid_usage(error):
    response = json.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@application.errorhandler(ResourceMissing)
def handle_invalid_usage(error):
    response = json.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@application.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = json.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
