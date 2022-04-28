import requests
from flask import Flask, request, json
import base64

app = Flask(__name__)

API_key_param = "?key=AIzaSyCKoKxqgOdSyz1ErIYDnS8b8hYWMqHgkl8"
default_dest = "https://vision.googleapis.com/v1/images:annotate"
default_URL = default_dest + API_key_param
own_URL = "http://service-1a:80/frame"


@app.route('/frame', methods=['POST'])
def forward_request() -> json:
    if request.is_json:
        print("Received valid JSON from user.")
        return forward_to_dest(request.json)
    return {"error": {"code": 403, "message": "Contents of the request body are not in valid JSON format",
                      "status": "DENIED"}}


def forward_to_dest(req_json: json) -> json:
    try:
        if 'destination' in req_json:
            destination = req_json['destination']
            if destination == own_URL:
                return forward_to_gv(req_json)
            print("Attempting to forward request to " + destination + "...")
            res = requests.post(destination, json=req_json)
        else:
            return forward_to_gv(req_json)
        print("Received response:\n" + res.text)
        return res.json()

    except Exception as e:
        return {"error": {"code": 403, "message": str(e), "status": "DENIED"}}


def forward_to_gv(req: json) -> json:
    gv_json = prep_gv_json(req)
    print("Forwarding request to Google Cloud Vision...")
    res = requests.post(default_URL, json=gv_json)
    print("Received response from Google Cloud Vision:\n" + res.text)
    return res.json()


def prep_gv_json(req: json) -> json:
    gv_json = {
        "requests": [
            {
                "image": {
                    "content": ""
                },
                "features": [
                    {
                        "maxResults": 10,
                        "type": "OBJECT_LOCALIZATION"
                    },
                ]
            }]

    }
    image = req['image']
    gv_json['requests'][0]['image']['content'] = image
    return gv_json


@app.route('/convert', methods=['POST'])
def convert_to_base64() -> json:
    res = {"image": base64.b64encode(request.data).decode('utf-8')}
    return res


@app.route('/', methods=['GET', 'POST'])
def hello() -> str:
    return "Hi there! You reached the 1A forwarding service. Congrats!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
