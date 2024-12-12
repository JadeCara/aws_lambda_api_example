from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import boto3
from botocore.exceptions import ClientError

from app.routes.users import is_existing_user_id

router = APIRouter()

# Initialize the DynamoDB client
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("posts")


class Post(BaseModel):
    Id: str
    title: str
    content: str
    author_id: str


def is_existing_post_id(post_Id: str):
    try:
        response = table.scan(FilterExpression="Id = :i", ExpressionAttributeValues={":i": post_Id})
        return len(response["Items"]) == 1
    except ClientError as e:
        raise HTTPException(status_code=500, detail=e.response["Error"]["Message"])


@router.get("/")
def read_posts():
    """
    Gets all posts from the DynamoDB table "posts"

    Example call:
    ``curl -X GET "http://127.0.0.1:8000/posts/" -H "accept: application/json"``

    Response:
    ``[{"Id": "1", "title": "First Post", ... "author_id": "1"}]``
    """
    try:
        response = table.scan()
        return response["Items"]
    except ClientError as e:
        raise HTTPException(status_code=500, detail=e.response["Error"]["Message"])


@router.get("/{Id}")
def read_post(Id: str):
    """
    Gets a post from the DynamoDB table "posts" by Id

    Example call:
    ``curl -X GET "http://127.0.0.1:8000/posts/1" -H "accept: application/json"``

    Response:
    ``{"content":"This is the first post","author_id":"1","Id":"1","title":"First Post"}``
    """
    try:
        response = table.get_item(Key={"Id": Id})
        if "Item" not in response:
            raise HTTPException(status_code=404, detail="Post not found")
        return response["Item"]
    except ClientError as e:
        raise HTTPException(status_code=500, detail=e.response["Error"]["Message"])


@router.post("/")
def create_post(post: Post):
    """
    Creates a post in the DynamoDB table "posts"

    Example call:
    ``curl -X POST "http://127.0.0.1:8000/posts/" -H "accept: application/json" -H "Content-Type: application/json" -d '{  # noqa E501
      "Id": "1",
      "title": "First Post",
      "content": "This is the first post",
      "author_id": "1"
    }'``

    Response:
    ``{"message": "Post created"}``
    """
    try:
        if not is_existing_user_id(post.author_id):
            raise HTTPException(status_code=400, detail="Cannot create post for unknown User Id.")
        if is_existing_post_id(post.Id):
            raise HTTPException(status_code=400, detail="Cannot create post for duplicate Id.")
        table.put_item(Item={k: v for k, v in post.model_dump().items()})

        return {"message": "Post created"}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=e.response["Error"]["Message"])


@router.put("/{Id}")
def update_post(Id: str, post: Post):
    """
    Updates a post in the DynamoDB table "posts" by Id

    Example call:
    ``curl -X PUT "http://127.0.0.1:8000/posts/1" -H "accept: application/json" -H "Content-Type: application/json" -d  # noqa E501
    '{
        "Id": "1",
        "title": "Updated Post",
        "content": "This is the updated post",
        "author_id": "1"
    }'

    Response:
    ``{"message": "Post with id {Id} updated", "updated_attributes": {updated_attributes}}``
    """
    try:
        if not is_existing_post_id(post.Id):
            raise HTTPException(status_code=400, detail="Cannot update post for unknown Id.")
        response = table.update_item(
            Key={"Id": Id},
            UpdateExpression="set title=:t, content=:c, author_id=:a",
            ExpressionAttributeValues={":t": post.title, ":c": post.content, ":a": post.author_id},
            ReturnValues="UPDATED_NEW",
        )
        return {
            "message": f"Post with id {Id} updated",
            "updated_attributes": response["Attributes"],
        }
    except ClientError as e:
        raise HTTPException(status_code=500, detail=e.response["Error"]["Message"])


@router.delete("/{Id}")
def delete_post(Id: str):
    """
    Deletes a post from the DynamoDB table "posts" by Id

    Example call:
    ``curl -X DELETE "http://127.0.0.1:8000/posts/1" -H "accept: application/json"``

    Response:
    ``{"message":"Post with id 1 deleted"}
    """
    try:
        if not is_existing_post_id(Id):
            raise HTTPException(status_code=400, detail="Cannot delete post for unknown Id.")
        table.delete_item(Key={"Id": Id})
        return {"message": f"Post with id {Id} deleted"}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=e.response["Error"]["Message"])
