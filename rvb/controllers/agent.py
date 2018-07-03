from rvb import application
from rvb.models import *
from flask import Flask, request, json
from rvb.controllers.helpers import authenticate, parse_data, validate_data
from rvb.exceptions import ResourceMissing, InvalidUsage

@application.route('/agent/<listener_id>', methods=['GET','POST'])
def listener(listener_id):
    if request.method == 'POST':
        player = authenticate(request,['Charlie'])
        data = parse_data(request)
        validate_data(data,['channel_id'])
        listener = Listener.find(int(listener_id))
        if listener:
            listener.listen_to(data['channel_id'])
            return "Listener {listener_id} is now listening to channel {channel_id}".format(
                listener_id = listener_id,
                channel_id = data['channel_id']
                )
        else:
            raise ResourceMissing("No listener found with id %r" % listener_id,404)

    elif request.method == 'GET':
        player = authenticate(request,['Charlie'])
        listener = Listener.find(int(listener_id))

        if listener:
            return json.jsonify(
                id=listener.id,
                channel_id=listener.channel_id,
                intercepted_messages=len(listener.messages),
                messages = listener.serialize_messages()
                )
        else:
            raise ResourceMissing("No listener found with id %r" % listener_id,404)
