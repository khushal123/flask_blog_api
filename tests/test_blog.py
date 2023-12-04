from faker import Faker

faker = Faker()


def test_create_post(client, access_token):
    post_data = {
        "title": faker.name(),
        "content": faker.text(),
    }
    response = client.post(
        "/posts/create",
        headers={"Authorization": f"Bearer {access_token}"},
        json=post_data,
    )
    assert response.status_code == 201


def test_get_all_posts(client, access_token, fake_posts):
    # Get all posts
    response = client.get(
        "/posts?limit=2",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert len(response.json) == 2


def test_get_single_post(client, fake_post, access_token):
    fake_post_id = fake_post.get("id")
    response = client.get(
        f"/posts/{fake_post_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json["id"] == fake_post_id


def test_get_comments(client, fake_post, access_token):
    fake_post_id = fake_post.get("id")
    response = client.get(
        f"/posts/{fake_post_id}/comments?limit=2",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200


def test_add_comment(
    client,
    access_token,
    fake_post,
):
    comment_data = {
        "content": "This is a test comment",
    }
    fake_post_id = fake_post.get("id")
    response = client.post(
        f"/posts/{fake_post_id}/comments",
        headers={"Authorization": f"Bearer {access_token}"},
        json=comment_data,
    )
    assert response.status_code == 201
