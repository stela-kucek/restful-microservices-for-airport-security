import requests
from flask import Flask, request, json
import time

app = Flask(__name__)

service1a_dest = "http://service-1a:80/frame"


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
            if destination != service1a_dest:
                destination = service1a_dest
        else:
            destination = service1a_dest

        print("Forwarding request to Service-1a...")
        res = requests.post(destination, json=req_json)
        print("Received response from Google Vision:\n" + res.text)
        return res.json()
    except Exception as e:
        return {"error": {"code": 403, "message": str(e), "status": "DENIED"}}


@app.route('/', methods=['GET', 'POST'])
def hello() -> str:
    return "Hi there! You reached the 1B forwarding service. Congrats!"


@app.route('/test', methods=['POST'])
def time_to_respond() -> json:
    res = {
        "time": str
    }
    if request.is_json:
        if 'times' in request.json:
            times = request.json['times']
        else: times = 20
        start = time.time()
        i = 0
        while i < times:
            forward_to_dest(request.json)
            i += 1
        end = time.time()
        res['time'] = end - start
        return res

    return {"error": {"code": 403, "message": "Contents of the request body are not in valid JSON format",
                      "status": "DENIED"}}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
