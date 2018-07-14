import os
import tempfile

import pytest

from rvb import application
from rvb import db


@pytest.fixture
def client():
    db_fd, application.config['DATABASE'] = tempfile.mkstemp()
    application.config['TESTING'] = True
    client = application.test_client()

    with application.app_context():
        db.init_db()

    yield client

    os.close(db_fd)
    os.unlink(application.config['DATABASE'])

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data
