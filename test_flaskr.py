import os
import tempfile

import pytest

from rvb import application
from rvb import db
from rvb.controls import clear_rows

@pytest.fixture
def client():
    application.config['DATABASE'] = tempfile.mkstemp()
    application.config['TESTING'] = True
    client = application.test_client()

    clear_rows()

    yield client

def test_blank_route(client):
    rv = client.get('/')
    assert b'Hello :)! You have found the rvb api!' in rv.data
