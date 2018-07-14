from rvb import application
from rvb.models import *
from flask import Flask, request, json
from rvb.controllers.helpers import authenticate, parse_data, validate_data
from rvb.controllers.exceptions import ApiError

@application.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        player = authenticate(request,['Alpha','Bravo'])
        data = parse_data(request)
        validate_data(data,['channel_id', 'content'])
        message = Message.create(data['content'], int(data['channel_id']), player.name)
        return json.jsonify(
            id=message.id,
            content=message.content,
            sender=message.sender,
            channel_id=message.channel_id,
            created_at=message.created_at
        )

    elif request.method == 'GET':
        player = authenticate(request,['Alpha','Bravo'])
        channel_id = request.args.get('channel_id')
        message = Message.query.filter(Message.channel_id == channel_id).order_by(Message.id.desc()).first()
        if message:
            return json.jsonify(
                id=message.id,
                content=message.content,
                sender=message.sender,
                channel_id=message.channel_id,
                created_at=message.created_at
                )
        else:
            return json.jsonify(
                id=None,
                content=None,
                sender=None,
                created_at=None
                )
