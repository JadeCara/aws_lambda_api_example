import pytest
from pytest import param

from app.routes.posts import is_existing_post_id

from tests.routes.test_users import user_data_1, user_data_2, generate_users

post_data_1 = {"Id": "1", "title": "First", "content": "The first post", "author_id": "1"}
post_data_2 = {"Id": "2", "title": "Second", "content": "The second post", "author_id": "2"}
post_data_3 = {"Id": "2", "title": "Updated Post", "content": "The updated post", "author_id": "2"}

post_not_found = {"detail": "Post not found"}
post_created = {"message": "Post created"}
unknown_user_id = {"detail": "Cannot create post for unknown User Id."}


def generate_posts(client, posts):
    for post_data in posts:
        client.post("/posts/", json=post_data)


def test_is_existing_post_id(client):
    assert is_existing_post_id("1") is False

    client.post("/users/", json=user_data_1)
    client.post("/posts/", json=post_data_1)
    assert is_existing_post_id("1") is True


@pytest.mark.parametrize(
    "posts",
    [
        param([], id="reads_no_posts"),
        param([post_data_1], id="reads1_post"),
        param([post_data_1, post_data_2], id="reads_multiple_posts"),
    ],
)
def test_read_posts(client, posts):
    generate_users(client, [user_data_1, user_data_2])
    generate_posts(client, posts)
    response = client.get("/posts/")

    assert response.status_code == 200
    assert response.json() == posts


@pytest.mark.parametrize(
    "post_Id, posts, expected_status, expected_response",
    [
        param("1", [post_data_1], 200, post_data_1, id="post_found_only_user"),
        param("1", [post_data_1, post_data_2], 200, post_data_1, id="post1_found_multiple_users"),
        param("2", [post_data_1, post_data_2], 200, post_data_2, id="post2_found_multipl_users"),
        param("75", [], 404, post_not_found, id="post75_not_found_no_posts"),
        param(
            "75",
            [post_data_1, post_data_2],
            404,
            post_not_found,
            id="post75_not_found_multiple_users",
        ),
    ],
)
def test_read_user(client, post_Id, posts, expected_status, expected_response):
    generate_users(client, [user_data_1, user_data_2])
    generate_posts(client, posts)

    response = client.get(f"/posts/{post_Id}")
    assert response.status_code == expected_status
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "post, existing_posts, users, expected_status, expected_response",
    [
        param(post_data_1, [], [user_data_1], 200, post_created, id="post_created_successfully"),
        param(
            post_data_1,
            [],
            [user_data_1, user_data_2],
            200,
            post_created,
            id="post_created_successfully_multiple_users",
        ),
        param(
            post_data_1,
            [],
            [],
            400,
            unknown_user_id,
            id="cannot_create_post_without_author_id_in_users",
        ),
        param(
            post_data_1,
            [post_data_1],
            [user_data_1],
            400,
            {"detail": "Cannot create post for duplicate Id."},
            id="cannot_create_post_with_existing_id",
        ),
    ],
)
def test_create_post(client, post, existing_posts, users, expected_response, expected_status):
    generate_users(client, users)
    generate_posts(client, existing_posts)
    response = client.post("/posts/", json=post)
    assert response.status_code == expected_status
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "post, existing_posts, users, expected_status, expected_response",
    [
        param(
            post_data_3,
            [post_data_2],
            [user_data_2],
            200,
            {
                "message": "Post with id 2 updated",
                "updated_attributes": {"content": "The updated post", "title": "Updated Post"},
            },
            id="successfully_updated_response_single_post",
        ),
        param(
            post_data_3,
            [post_data_1, post_data_2],
            [user_data_1, user_data_2],
            200,
            {
                "message": "Post with id 2 updated",
                "updated_attributes": {"content": "The updated post", "title": "Updated Post"},
            },
            id="successfully_updated_post_multiple_posts",
        ),
        param(
            post_data_3,
            [post_data_1],
            [user_data_1, user_data_2],
            400,
            {"detail": "Cannot update post for unknown Id."},
            id="failed_to_updated_post_unknown_id",
        ),
    ],
)
def test_update_post(client, post, existing_posts, users, expected_response, expected_status):
    generate_users(client, users)
    generate_posts(client, existing_posts)
    response = client.put(f"/posts/{post['Id']}", json=post)
    assert response.status_code == expected_status
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "post_id, existing_posts, users, expected_status, expected_response",
    [
        param(
            "1",
            [post_data_1],
            [user_data_1],
            200,
            {"message": "Post with id 1 deleted"},
            id="deleted-post",
        ),
        param(
            "1",
            [],
            [],
            400,
            {"detail": "Cannot delete post for unknown Id."},
            id="failed_to_delete_unknown_id",
        ),
    ],
)
def test_delete_post(client, post_id, existing_posts, users, expected_response, expected_status):
    generate_users(client, users)
    generate_posts(client, existing_posts)
    response = client.delete(f"/posts/{post_id}")
    print(response.json())  # Print the response content for debugging
    assert response.status_code == expected_status
    assert response.json() == expected_response
