import json

def send_response(http_code, data):
    return {
            'statusCode': http_code,
            'body': json.dumps(data)
        }