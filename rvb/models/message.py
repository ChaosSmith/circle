from rvb import db
from rvb.models import *
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.exc import *
from rvb.exceptions import ApiError
import random
import math

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    channel = db.relationship('Channel', back_populates='messages')
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
    listener = db.relationship('Listener', back_populates='messages')
    listener_id = db.Column(db.Integer, db.ForeignKey('listeners.id'))
    content = db.Column(db.Text, nullable=False)
    encrypted_content = db.Column(db.Text, nullable=False)
    sender = db.Column(db.String, nullable=False)
    intercepted_at = db.Column(db.TIMESTAMP)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(),onupdate=func.current_timestamp())

    def __repr__(self):
        return '<Message %r>' % self.id

    def create(content, channel_id, sender):
        message = Message(channel_id=channel_id,content=content,sender=sender, encrypted_content= Message.encrypt(content, 0))
        db.session.add(message)
        try:
            db.session.commit()
        except IntegrityError as e:
            print(str(e))
            raise ApiError("Could not find channel {channel_id}, message was not delivered".format(channel_id=channel_id), 404)

        if message.channel.has_listeners():
            # Assuming there is only one listener
            message.listener = message.channel.listeners[0]
            message.intercepted_at = datetime.now()
            message.encrypted_content = Message.encrypt(content, message.listener.decrypt_level())
            db.session.commit()

        return message

    def serialize(self):
        # Return the encrypted messages to red team, not for blue team use
        return {
            'id': self.id,
            'channel_id': self.channel_id,
            'intercepted_at': self.intercepted_at,
            'created_at': self.created_at,
            'sender': self.sender,
            'content': self.encrypted_content
        }

    def encrypt(content, decrypt_level):
        length = len(content)
        decrypted_chars = []
        for _ in range(math.ceil(length * (1-decrypt_level))):
            char_index = random.randint(0, length)
            if char_index not in decrypted_chars:
                decrypted_chars.append(char_index)

        return "".join([('*' if index in decrypted_chars else char) for index, char in enumerate(content)])
