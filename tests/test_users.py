import jwt 

from app.schemas.users import ResponseUser, Token
from app.core.config import settings

def test_root(client):
    res = client.get("/")

    assert res.json().get("data") == "Home page"

def test_create_User(client):
    
    res = client.post(
        "/resister/",
        data={
            "username": "arian",
            "email": "arian@gmail.com",
            "password": "arian12345"
        }
    )

    new_user = ResponseUser(**res.json())
    assert new_user.email == "arian@gmail.com"
    assert res.status_code == 201


def test_login(test_user, client):

    res = client.post(
        "/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    sec_key = res.json().get('access_token')
    toK_type = res.json().get('token_type')

    login_res = Token(access_token=sec_key, token_type=toK_type)

    payload = jwt.decode(
        login_res.access_token, 
        settings.secret_key.get_secret_value(), 
        algorithms=[settings.algorithm]
    )

    id = payload.get("user_id")

    assert id == test_user['userid']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200