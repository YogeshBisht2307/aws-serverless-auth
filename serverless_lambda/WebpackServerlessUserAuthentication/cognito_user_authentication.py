import json
import logging
from datetime import datetime
from multiprocessing.connection import Client

import boto3

from credentials import cognito_client_id
from credentials import cognito_user_pool_id
from constants import ApiRouteEnum

from auth_helper import send_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

cognito_client = boto3.client(
    "cognito-idp",
    region_name="ap-south-1"
)

dynamodb_client = boto3.client(
    "dynamodb",
    region_name="ap-south-1"
)

def _auth_user_resend_confirmation_code(event):
    try:
        json_data = json.loads(event['body'])
        response = cognito_client.resend_confirmation_code(
            ClientId=cognito_client_id,
            Username=json_data['email'].lower().strip()
        )
        logger.info(response)
        return send_response(200, {'message': 'Confirmation code has been sent.'})
    except (KeyError, ValueError, cognito_client.exceptions.InvalidParameterException) as error:
        logger.error(str(error))
        return send_response(400, {'message': "Invalid Parameter"})
    except cognito_client.exceptions.NotAuthorizedException as error:
        logger.error(str(error))
        return send_response(400, {'message': "Unauthorized access."})
    except cognito_client.exceptions.UserNotFoundException as error:
        logger.error(str(error))
        return send_response(400, {'message': "User doesn't exists."})

def _auth_user_signup_handler(event):
    try:
        json_data = json.loads(event['body'])
        response = cognito_client.list_users(
            UserPoolId=cognito_user_pool_id,
            AttributesToGet=['sub', 'email', 'name'],
            Limit=60,
            Filter="email = '{}'".format(json_data['email'].lower().strip())
        )

        if response['Users']:
            if response['Users'][0]['UserStatus'] == "UNCONFIRMED":
                return _auth_user_resend_confirmation_code(event)
            else:
                return send_response(409, {'message': 'User Already Exist'})

        signup_response = cognito_client.sign_up(
            ClientId=cognito_client_id,
            Username=json_data['email'].lower().strip(),
            Password=json_data['password'],
            UserAttributes=[
                {'Name': 'name', 'Value': json_data['name']},
                {'Name': 'updated_at', 'Value': str(int(datetime.timestamp(datetime.utcnow()) * 1000))},
                {'Name': 'profile', 'Value': '/'},
                {'Name': 'custom:permissions', 'Value': '[]'}
            ],
        )
        logger.info("signup response %s", signup_response)
        return send_response(200, signup_response)
    except (KeyError, ValueError) as error:
        logger.error(str(error))
        return send_response(400, {'message': "Invalid Parameter"})
    except cognito_client.exceptions.InvalidPasswordException as error:
        logger.error(error)
        return send_response(400, {'message': "Invalid password"})
    except cognito_client.exceptions.NotAuthorizedException as error:
        logger.error(error)
        return send_response(400, {'message': "Not Authorized."})

def _auth_user_confirm_signup_handler(event):
    try:
        json_data = json.loads(event['body'])
        response = cognito_client.confirm_sign_up(
            ClientId=cognito_client_id,
            Username=json_data['email'].lower().strip(),
            ConfirmationCode=json_data['confirmation_code']
        )

        put_item_response = dynamodb_client.put_item(
            TableName='wp_user_profile',
            Item={
                'email': {'S': json_data['email'].lower().strip()},
                'bio': {'S': '-'},
                'is_married': {'BOOL': False},
                'location': {'S': '-'},
                'occupation': {'S': '-'},
                'user_id': {'S': json_data['user_id']},
                'skills': {'SS': ['']},
                'social': {
                    'M': {
                        'facebook': {'S': '-'},
                        'instagram': {'S': '-'},
                        'linkedin': {'S': '-'},
                        'website': {'S': '-'}
                    }
                }
            }
        )
        logger.info("put item response %s", put_item_response)
        return send_response(200, response)
    except (KeyError, ValueError) as error:
        logger.error(str(error))
        return send_response(400, {'message': "Invalid Parameters"})
    except (cognito_client.exceptions.CodeMismatchException, cognito_client.exceptions.ExpiredCodeException) as error:
        logger.error(error)
        return send_response(400, {'message': "Invalid Confirmation Code."})
    except (cognito_client.exceptions.UserNotFoundException) as error:
        logger.error(error)
        return send_response(400, {'message': "User doesn't exists."})

def _auth_user_login_handler(event):
    try:
        json_data = json.loads(event['body'])
        response = cognito_client.initiate_auth(
            ClientId=cognito_client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": json_data['auth_id'].lower().strip(),
                "PASSWORD": json_data['password']
            },
        )
        access_token = response['AuthenticationResult']['AccessToken']
        return send_response(200, {'access_token': access_token})
    except (KeyError, ValueError, cognito_client.exceptions.InvalidParameterException) as error:
        logger.error(str(error))
        return send_response(400, {'message': "Invalid request paramters."})
    except cognito_client.exceptions.PasswordResetRequiredException as error:
        logger.error(error)
        return send_response(400, {'message': "Password reset required."})
    except (cognito_client.exceptions.UserNotFoundException, cognito_client.exceptions.UserNotConfirmedException) as error:
        logger.error(error)
        return send_response(400, {'message': "User Doesn't exists."})

def _get_user_access_handler(event):
    try:
        json_data = json.loads(event['body'])
        user = cognito_client.get_user(AccessToken=json_data['access_token'])
        if not user:
            return {
            'statusCode': 400,
            'body': json.dumps({'message': 'User not Found'})
        }
        return {
            'statusCode': 200,
            'body': json.dumps({'user': user})
        }
            
    except Exception as error:
        logger.error(error)
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'User not Found'})
        }

def user_auth_request_handler(event, context):
    print(event)
    api_request_route = event['requestContext']['http']['path']
    
    if api_request_route == ApiRouteEnum.SIGNUP_ROUTE.value:
        return _auth_user_signup_handler(event)
    
    elif api_request_route == ApiRouteEnum.CONFIRM_SIGNUP_ROUTE.value:
        return _auth_user_confirm_signup_handler(event)

    elif api_request_route == ApiRouteEnum.LOGIN_ROUTE.value:
        return _auth_user_login_handler(event)

    elif api_request_route == ApiRouteEnum.GET_USER_ACCESS_ROUTE.value:
        return _get_user_access_handler(event)
    
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid Request Endpoint.'})
        }

    
