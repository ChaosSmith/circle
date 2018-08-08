
from flask import request, json
from rvb.exceptions import ApiError

def parse_data(request):
    data = request.get_data().decode('utf8')
    return json.loads(data)

def validate_data(data,expected_keys):
    missing_keys = [key for key in expected_keys if key not in data.keys()]
    if len(missing_keys) == 0:
        return True
    else:
        raise ApiError("Improper request, missing -> [{keys}]".format(keys=",".join(missing_keys)),400)
