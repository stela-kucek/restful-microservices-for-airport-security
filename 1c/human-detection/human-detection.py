import base64

import requests
from flask import Flask, request, json
from typing_json import *

app = Flask(__name__)

API_key_param = "?key=AIzaSyCKoKxqgOdSyz1ErIYDnS8b8hYWMqHgkl8"
default_dest = "https://vision.googleapis.com/v1/images:annotate"
default_URL = default_dest + API_key_param

face_recognition = "http://face-recognition:80/frame"
image_analysis = "http://image-analysis:80/frame"
collector_persons = "http://collector:80/persons"
collector_known_persons = "http://collector:80/known-persons"


@app.route('/frame', methods=['POST'])
def forward_request():
    if request.is_json:
        print("Received valid JSON from user.", flush=True)
        req = json.loads(request.json)
        gv_res = forward_to_gv(req)
        create_final_response(req, gv_res)
        # forward to ia and fd
        return {"success": {"code": 200, "status": "OK"}}
    return {"error": {"code": 403, "message": "Contents of the request body are not in valid JSON format",
                      "status": "DENIED"}}


def create_final_response(original_req: Any, res: Any) -> Any:
    if 'responses' in res:
        detected_objects = res['responses'][0]['localizedObjectAnnotations']
        person_counter = 0
        for obj in detected_objects:
            if obj['name'] == "Person":
                person_counter += 1
        field_to_add = {
            "person-count": person_counter
        }
        original_req.update(field_to_add)
        if person_counter > 0:
            # forward to other services
            print(f"{person_counter} human(s) detected! Forwarding...", flush=True)
            forward_to_image_analysis(original_req)
            forward_to_face_recognition(original_req)
            return {"success": {"code": 200, "status": "OK"}}
            # original_req['destination'] = face_recognition
        else:
            original_req.pop('destination')
    else:
        print("\n------------NO RESPONSES KEY --------------")
        return {"error": {"code": 403, "message": "No 'responses' key", "status": "DENIED"}}
    return original_req


def forward_to_gv(req):
    gv_json = prep_gv_json(req)
    print("Forwarding request to Google Cloud Vision...", flush=True)
    res = requests.post(default_URL, json=gv_json)
    print("Received response from Google Cloud Vision:\n" + res.text, flush=True)
    print("\n-----TYPE:", flush=True)
    print(type(res), flush=True)
    return json.loads(res.text)


def forward_to_image_analysis(req):
    req['destination'] = collector_persons
    try:
        requests.post(image_analysis, json=req)
    except Exception as e:
        print(json.dumps({"error": {"code": 403, "message": str(e), "status": "DENIED"}}))


def forward_to_face_recognition(req):
    req['destination'] = collector_known_persons
    try:
        requests.post(face_recognition, json=req)
    except Exception as e:
        print(json.dumps({"error": {"code": 403, "message": str(e), "status": "DENIED"}}))


def prep_gv_json(req):
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


@app.route('/', methods=['GET'])
def hello() -> str:
    return "Hi there! You reached the human-detection service. Congrats!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
