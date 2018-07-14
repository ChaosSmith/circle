from rvb.models import *
from flask import request, json
from rvb.exceptions import ApiError

def authenticate(request, expect):
    api_key = request.args.get('api_key')
    player = Player.current_user(api_key)
    if player and player.name in expect:
        return player
    else:
        raise ApiError('Access Denied', status_code=401)

def parse_data(request):
    data = request.get_data().decode('utf8')
    return json.loads(data)

def validate_data(data,expected_keys):
    missing_keys = [key for key in expected_keys if key not in data.keys()]
    if len(missing_keys) == 0:
        return True
    else:
        raise ApiError("Improper request, missing -> [{keys}]".format(keys=",".join(missing_keys)),400)
