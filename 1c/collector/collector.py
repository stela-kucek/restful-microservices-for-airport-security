import json
from typing import Any

import requests
from flask import Flask, request

app = Flask(__name__)

# URLs of service to forward to
face_recognition = "http://face-recognition:80/frame"
human_detection = "http://human-detection:80/frame"
image_analysis = "http://image-analysis:80/frame"
section = "http://section:80/persons"
alert = "http://alert:80/alerts"
cpanel = "http://cpanel:80/"


@app.route('/frame', methods=['POST'])
def forward_request() -> Any:
    if request.is_json:
        print("Received valid JSON from user.", flush=True)
        return get_service_response(request.get_json())
    else:
        return {"error": {"code": 403, "message": "Contents of the request body are not in valid JSON format",
                "status": "DENIED"}}


def get_service_response(req: Any) -> Any:
    try:
        forward_to_human_detection(json.dumps(req))
        return {"success": {"code": 200, "status": "OK"}}
    except Exception as e:
        return {"error": {"code": 403, "message": str(e), "status": "DENIED"}}


def forward_to_human_detection(req_json: Any) -> Any:
    try:
        res = requests.post(human_detection, json=req_json)
        return res.json()
    except Exception as e:
        return {"error": {"code": 403, "message": str(e), "status": "DENIED"}}


@app.route('/persons', methods=['POST'])
def persons():
    if request.is_json:
        print("Received valid JSON.", flush=True)
        req = request.get_json()
        if 'persons' in req:
            if req['persons']:
                return forward_to_section(req)
            else:
                return {"error": {"code": 403, "message": "Gender and age of persons could not be estimated.",
                                  "status": "DETECTION-ERROR"}}
        else:
            return {"error": {"code": 403, "message": "No 'persons' key found in JSON object.",
                              "status": "DENIED"}}
    else:
        return {"error": {"code": 403, "message": "Contents of the request body are not in valid JSON format",
                "status": "DENIED"}}


@app.route('/known-persons', methods=['POST'])
def known_persons():
    if request.is_json:
        print("Received valid JSON.", flush=True)
        req = request.get_json()
        if 'known-persons' in req:
            if req['known-persons']:
                return forward_to_alert(req)
            else:
                return {"error": {"code": 200, "message": "No 'known-persons' were detected on the image.",
                                  "status": "OK"}}
        else:
            return {"error": {"code": 403, "message": "No 'known-persons' key found in JSON object.",
                              "status": "DENIED"}}
    else:
        return {"error": {"code": 403, "message": "Contents of the request body are not in valid JSON format",
                "status": "DENIED"}}


def forward_to_section(req):
    try:
        res = requests.post(section, json=req)
        return res.json()
    except Exception as e:
        return {"error": {"code": 403, "message": str(e), "status": "DENIED"}}


def forward_to_alert(req):
    try:
        res = requests.post(alert, json=req)
        return res.json()
    except Exception as e:
        return {"error": {"code": 403, "message": str(e), "status": "DENIED"}}

# def forward_to_image_analysis(req_json: Any) -> Any:
#     try:
#         res = requests.post(image_analysis, json=req_json)
#         print("Received response:\n" + res.text)
#         return res.json()
#     except Exception as e:
#         return {"error": {"code": 403, "message": str(e), "status": "DENIED"}}
#
#
# def forward_to_face_recognition(req_json: Any) -> Any:
#     try:
#         res = requests.post(face_recognition, json=req_json)
#         print("Received response:\n" + res.text)
#         return res.json()
#     except Exception as e:
#         return {"error": {"code": 403, "message": str(e), "status": "DENIED"}}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
