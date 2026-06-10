from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/v1/messages', methods=['POST', 'OPTIONS'])
def proxy():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        return response
    
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    resp = requests.post(
        'https://api.anthropic.com/v1/messages',
        headers={
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01'
        },
        json=request.json
    )
    response = jsonify(resp.json())
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, resp.status_code

if __name__ == '__main__':
    app.run()