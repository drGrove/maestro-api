def test_ping(client):
    rv = client.get('/')
    assert rv.status_code == 200
