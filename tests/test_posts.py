from app import schemas
import pytest


def test_get_all_posts(client, test_posts):
    res = client.get('/posts')

    def validate(post):
        return schemas.PostWithVotes(**post)

    posts_map = map(validate, res.json())
    posts_l = list(posts_map)

    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)


def test_get_1_post_not_exist(client, test_posts):
    res = client.get('posts/8988888')
    assert res.status_code == 404


def test_get_1_post(client, test_posts):
    res = client.get(f'posts/{test_posts[0].id}')
    post = schemas.PostWithVotes(**res.json())
    assert post.Post.id == test_posts[0].id


@pytest.mark.parametrize('title, content', [
    ("new post", "new post c."),
    ("np2", "np2 c.")
])
def test_create_post(authorized_client, test_user, test_posts, title, content):
    res = authorized_client.post("/posts/", json={"title": title, "content": content})

    cr_post = schemas.PostUser(**res.json())

    assert res.status_code == 201
    assert cr_post.title == title
    assert cr_post.content == content
    assert cr_post.owner_id == int(test_user['id'])


def test_unauthorized_create_post(client):
    res = client.post("/posts/", json={"title": "title", "content": "content"})
    assert res.status_code == 401


def test_unauthorized_delete_post(client, test_posts):
    res = client.delete(f'posts/{test_posts[0].id}')
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f'posts/{test_posts[0].id}')
    assert res.status_code == 204


def test_delete_1_post_not_exist(authorized_client, test_posts):
    res = authorized_client.delete('posts/8988888')
    assert res.status_code == 404


