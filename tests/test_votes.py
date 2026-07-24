import pytest

from app.models.posts import Vote

@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = Vote(post_id=test_posts[3].post_id, user_id=test_user["userid"])

    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        '/vote/',
        json={
            "post_id": test_posts[0].post_id,
            "dir": 1
        }
    )

    assert res.status_code == 201

def test_vote_on_multiple(authorized_client, test_vote, test_posts):

    res = authorized_client.post(
        '/vote/',
        json={
            "post_id": test_posts[3].post_id,
            "dir": 1
        }
    )

    assert res.status_code == 409

def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        '/vote/',
        json={
            "post_id": test_posts[3].post_id,
            "dir": 0
        }
    )

    assert res.status_code == 201

def test_delet_not_exit(authorized_client, test_posts):
    res = authorized_client.post(
        '/vote/',
        json={
            "post_id": test_posts[3].post_id,
            "dir": 0
        }
    )

    assert res.status_code == 404

def test_vote_on_post_not_exit(authorized_client):
    res = authorized_client.post(
        '/vote/',
        json={
            "post_id": 30000,
            "dir": 1
        }
    )

    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_posts):
    res = client.post(
        '/vote/',
        json={
            "post_id": test_posts[3].post_id,
            "dir": 1
        }
    )

    assert res.status_code == 401