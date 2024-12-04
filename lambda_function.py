import json
import logging
from app.main import handler

logging.basicConfig(level=logging.INFO)


def lambda_handler(event, context):
    """
    Lambda handler function

    Args:
        event (dict): Event data
        context (object): Runtime information
    """
    logging.info(f"Received event: {json.dumps(event, indent=2)}")

    try:
        response = handler(event, context)
    except Exception as e:
        logging.error(f"Error: {e}")
        response = {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)}),
        }

    return response
