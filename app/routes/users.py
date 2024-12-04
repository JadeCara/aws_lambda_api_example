from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import boto3
from botocore.exceptions import ClientError

router = APIRouter()

# Initialize the DynamoDB client to connect to AWS DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("users")


class User(BaseModel):
    Id: str  # Change user_id to Id to match the DynamoDB table schema
    user_name: str
    password: str
    email_address: str


@router.post("/")
def create_user(user: User):
    """
    Creates a new user in the DynamoDB table "users"

    Example call:
    ``curl -X POST "http://127.0.0.1:8000/users/" -H "accept: application/json" -H "Content-Type: application/json" -d '{  # noqa E501
      "Id": "1",
      "user_name": "johndoe",
      "password": "password",
      "email_address": "john@example.com"
    }'``

    Response: ``{"message":"User created"}``
    """
    try:
        table.put_item(
            Item={
                "Id": user.Id,
                "user_name": user.user_name,
                "password": user.password,
                "email_address": user.email_address,
            }
        )
        return {"message": "User created"}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=e.response["Error"]["Message"])


@router.get("/{Id}")
def read_user(Id: str):
    """
    Reads a user from the DynamoDB table "users" by Id

    Example call:
    ``curl -X GET "http://127.0.0.1:8000/users/1" -H "accept: application/json"``

    Response: ``{"Id": "1", "user_name": "johndoe", "password": ...``
    """
    try:
        response = table.get_item(Key={"Id": Id})
        if "Item" not in response:
            raise HTTPException(status_code=404, detail="User not found")
        return response["Item"]
    except ClientError as e:
        raise HTTPException(status_code=500, detail=e.response["Error"]["Message"])


@router.get("/")
def read_users():
    """
    Reads all users from the DynamoDB table "users"

    Example call:
    ``curl -X GET "http://127.0.0.1:8000/users/" -H "accept: application/json"``

    Response: ``[{"Id": "1", "user_name": "johndoe", "password": "password", "email_address": ...``
    """
    try:
        response = table.scan()
        return response["Items"]
    except ClientError as e:
        raise HTTPException(status_code=500, detail=e.response["Error"]["Message"])


@router.put("/{Id}")
def update_user(Id: str, user: User):
    """
    Updates a user in the DynamoDB table "users" by Id

    Example call:
    ``curl -X PUT "http://127.0.0.1:8000/users/{Id}" -H "accept: application/json" -H "Content-Type: application/json" -d '{  # noqa E501
      "Id": "1",
      "user_name": "johndoeupdated",
      "password": "newpassword",
      "email_address": "johnupdated@example.com"
    }'

    Response: ``{"message":"User with id 1 updated","updated_attributes": ...}``
    """
    try:
        response = table.update_item(
            Key={"Id": Id},
            UpdateExpression="set user_name=:u, password=:p, email_address=:e",
            ExpressionAttributeValues={
                ":u": user.user_name,
                ":p": user.password,
                ":e": user.email_address,
            },
            ReturnValues="UPDATED_NEW",
        )
        return {
            "message": f"User with id {Id} updated",
            "updated_attributes": response["Attributes"],
        }
    except ClientError as e:
        raise HTTPException(status_code=500, detail=e.response["Error"]["Message"])


@router.delete("/{Id}")
def delete_user(Id: str):
    """
    Deletes a user from the DynamoDB table "users" by Id

    Example call: ``curl -X DELETE "http://127.0.0.1:8000/users/1" -H "accept: application/json"``

    Response: ``{"message":"User with id 1 deleted"}``
    """
    try:
        table.delete_item(Key={"Id": Id})
        return {"message": f"User with id {Id} deleted"}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=e.response["Error"]["Message"])
