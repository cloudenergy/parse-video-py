import json
import asyncio
from urllib.parse import parse_qs
from main import share_url_parse


def handler(environ, start_response):
    # Parse query string parameters
    query_string = environ.get('QUERY_STRING', '')
    params = parse_qs(query_string)
    
    if 'url' in params and params['url']:
        url = params['url'][0]
        
        # Run the async function in a synchronous context
        try:
            result = asyncio.run(share_url_parse(url))
            response_body = json.dumps(result).encode('utf-8')
            status = '200 OK'
        except Exception as e:
            error_response = {
                "code": 500,
                "msg": str(e),
            }
            response_body = json.dumps(error_response).encode('utf-8')
            status = '500 Internal Server Error'
    else:
        error_response = {
            "code": 400,
            "msg": "Missing required parameter: url",
        }
        response_body = json.dumps(error_response).encode('utf-8')
        status = '400 Bad Request'
    
    # Set headers and start response
    headers = [('Content-Type', 'application/json')]
    start_response(status, headers)
    
    return [response_body] 