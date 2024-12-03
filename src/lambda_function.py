import boto3
import json
import logging

logging.basicConfig(level=logging.INFO)


dynamo = boto3.client("dynamodb", region_name="us-east-1")
table_name = "my-table" # Replace with your table name

def lambda_handler(event, context):
    """
    Lambda handler function

    Args:
        event (dict): Event data
        context (object): Runtime information

    """
    logging.info(f"Received event: {json.dumps(event, indent=2)}")

    http_method = event["requestContext"]["http"]["method"]
    path = event["requestContext"]["http"]["path"]

    response = {}

    # Call the appropriate function based on the HTTP method
    try:
        logging.info("Update with API values here")
        body = {"message": "Hello from Lambda!"}
    except Exception as e:
        logging.error(f"Error: {e}")
        response["statusCode"] = 500,
        body = json.dumps({"error": str(e)}),
    
    response["headers"] = {"Content-Type": "application/json"}
    response["body"] = json.dumps(body)