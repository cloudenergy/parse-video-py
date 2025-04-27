import json
import asyncio
import traceback
import sys
from urllib.parse import parse_qs
from parser import parse_video_share_url


def handler(environ, start_response):
    # Parse query string parameters
    query_string = environ.get('QUERY_STRING', '')
    params = parse_qs(query_string)
    
    if 'url' in params and params['url']:
        url = params['url'][0]
        
        # Run the async function in a synchronous context
        try:
            # Print some debug info
            print(f"Processing URL: {url}")
            
            result = asyncio.run(parse_video_share_url(url))
            
            # Convert VideoInfo to dict
            video_dict = {}
            for k, v in result.__dict__.items():
                if hasattr(v, '__dict__'):
                    video_dict[k] = v.__dict__
                else:
                    video_dict[k] = v
            
            response_data = {"code": 200, "msg": "解析成功", "data": video_dict}
            response_body = json.dumps(response_data).encode('utf-8')
            status = '200 OK'
            
            print(f"Successfully parsed video URL: {url}")
        except Exception as e:
            # Get the full traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error_details = traceback.format_exception(exc_type, exc_value, exc_traceback)
            
            # Log the error
            print(f"Error parsing URL {url}: {str(e)}")
            print(f"Traceback: {''.join(error_details)}")
            
            error_response = {
                "code": 500,
                "msg": f"Error: {str(e)}",
                "traceback": error_details[-3:] if error_details else []
            }
            response_body = json.dumps(error_response).encode('utf-8')
            status = '500 Internal Server Error'
    else:
        print("Missing URL parameter")
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