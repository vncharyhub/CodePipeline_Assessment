import json
import boto3
import os
import logging
from botocore.exceptions import ClientError
import requests  # For actual API calls (example)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

secrets_client = boto3.client('secretsmanager')
SECRET_NAME = os.environ.get("SECRET_NAME")

def get_secrets():
    try:
        response = secrets_client.get_secret_value(SecretId=SECRET_NAME)
        secret = json.loads(response['SecretString'])
        return secret
    except ClientError as e:
        logger.error(f"Error retrieving secrets: {e}")
        raise e

def call_bedrock_api(prompt, api_key):
    # Example of a call to Amazon Bedrock API (mocked)
    # Normally you'd use boto3 or requests to call the API
    logger.info(f"Calling Bedrock API with prompt: {prompt}")
    # Here we simulate a response
    return {"model": "bedrock", "reply": f"Simulated Bedrock response to '{prompt}'"}

def call_azure_openai(prompt, api_key, endpoint):
    # Placeholder Azure OpenAI API call
    logger.info(f"Calling Azure OpenAI at {endpoint} with prompt: {prompt}")
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    data = {
        "prompt": prompt,
        "max_tokens": 100
    }
    # In real usage, you would do:
    # response = requests.post(endpoint, headers=headers, json=data)
    # return response.json()
    # Here we just simulate:
    return {"model": "azure_openai", "reply": f"Simulated Azure OpenAI response to '{prompt}'"}

def lambda_handler(event, context):
    try:
        if event.get('httpMethod') != 'POST':
            return {
                "statusCode": 405,
                "body": json.dumps({"error": "Method Not Allowed, only POST supported"})
            }

        body = json.loads(event.get('body', '{}'))
        prompt = body.get('prompt')
        target_model = body.get('target_model')

        if not prompt or not target_model:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'prompt' or 'target_model' in request body"})
            }

        secrets = get_secrets()

        if target_model.lower() == 'bedrock':
            response = call_bedrock_api(prompt, secrets['bedrock_api_key'])
        elif target_model.lower() == 'azure':
            response = call_azure_openai(prompt, secrets['azure_api_key'], secrets['azure_endpoint'])
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid target_model, choose 'bedrock' or 'azure'"})
            }

        return {
            "statusCode": 200,
            "body": json.dumps(response)
        }
    except Exception as e:
        logger.error(f"Exception: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"})
        }
