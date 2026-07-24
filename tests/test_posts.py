import pytest

from app.schemas.posts import ResponsePost, Post

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return ResponsePost(**post)

    post_map = map(validate, res.json())

    posts_list = list(post_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200  


def test_unathorized_get_all_post(client, test_posts):
    res = client.get("/posts")

    assert res.status_code == 401

def test_unathorized_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].post_id}")

    assert res.status_code == 401

def test__get_one_post_not_exits(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/737")

    assert res.status_code == 404

def test__get_all_post_not_exits(authorized_client):
    res = authorized_client.get(f"/posts/")

    assert res.status_code == 404

def test__get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].post_id}")
    print(res.json())

    post = ResponsePost(**res.json())

    assert res.status_code == 200
    assert post.post.post_id == test_posts[0].post_id
    assert post.post.content == test_posts[0].content
    assert post.post.title == test_posts[0].title

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})

    created_post = Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user['userid']

def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"})

    created_post = Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "aasdfjasdf"
    assert created_post.published == True
    assert created_post.user_id == test_user['userid']


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post(
        "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"})
    assert res.status_code == 401


def test_unauthorized_user_delete_Post(client, test_user, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].post_id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].post_id}")

    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/8000000")

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].post_id}")
    
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].post_id

    }
    res = authorized_client.put(f"/posts/{test_posts[0].post_id}", json=data)
    updated_post = Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].post_id

    }
    res = authorized_client.put(f"/posts/{test_posts[3].post_id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].post_id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].post_id

    }
    res = authorized_client.put(
        f"/posts/8000000", json=data)

    assert res.status_code == 404