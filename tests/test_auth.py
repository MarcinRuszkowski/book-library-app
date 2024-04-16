import pytest

from book_library_app import db


def test_registration(client, clean_up_db):
    response = client.post('/api/v1/auth/register',
                           json={  # content-type zostanie autom. na application/json
                               'username': 'test',
                               'password': '123456',
                               'email': 'test@gmail.com'
                           })
    response_data = response.get_json()
    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['token']


@pytest.mark.parametrize(
    'data,missing_field',
    [
        ({'username': 'test', 'password': '123456'}, 'email'),
        ({'username': 'test', 'email': 'test@gmail.com'}, 'password'),
        ({'password': '123456', 'email': 'test@gmail.com'}, 'username')
    ]
)
def test_registration_invalid_data(client, data, missing_field, clean_up_db):
    response = client.post('/api/v1/auth/register',
                           json=data)
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data
    assert missing_field in response_data['message']
    assert 'Missing data for required field.' in response_data['message'][missing_field]


def test_registration_invalid_content_type(client, clean_up_db):
    response = client.post('/api/v1/auth/register',
                           data={  # nie ma application/json
                               'username': 'test',
                               'password': '123456',
                               'email': 'test@gmail.com'
                           })
    response_data = response.get_json()
    assert response.status_code == 415
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data


def test_registration_already_used_username(client, user, clean_up_db):
    response = client.post('/api/v1/auth/register',
                           json={
                               'username': user['username'],
                               'password': '123456',
                               'email': 'test123@gmail.com'
                           })
    response_data = response.get_json()
    assert response.status_code == 409
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data


def test_registration_already_used_email(client, user, clean_up_db):
    response = client.post('/api/v1/auth/register',
                           json={
                               'username': 'new_user',
                               'password': '123456',
                               'email': user['email']
                           })
    response_data = response.get_json()
    assert response.status_code == 409
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data


def test_get_current_user(client, user, token, clean_up_db):
    response = client.get('/api/v1/auth/me',
                           headers={
                               'Authorization': f'Bearer {token}'
                           })
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data']['username'] == user['username']
    assert response_data['data']['email'] == user['email']
    assert 'id' in response_data['data']


def test_get_current_user_missing_token(client, clean_up_db):
    response = client.get('/api/v1/auth/me')
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data