import requests
from flask import Flask, request, render_template
import json

app = Flask(__name__)

# camera addresses
cam1 = "http://camera-1:80/"
cam2 = "http://camera-2:80/"
sec = "http://section:80/"
alert = "http://alert:80/"

configuration = {
    'cameras':
        [
            {
                'id': 1,
                'event': 'entry',
                'section': 1,
                'url': 'http://camera-1:80/'
            },
            {
                'id': 2,
                'event': 'exit',
                'section': 1,
                'url': 'http://camera-2:80/'
            }
        ]
}


@app.route('/', methods=['GET'])
def index():
    config = configure_cameras()
    return render_template('index.html', result=f"Cameras have been successfully configured.\n{json.dumps(config)}",
                           change_1=False, show_results=True)


@app.route('/change-cam1-config', methods=['POST'])
def change_config_1():
    section = request.form['section']
    event = request.form['event']
    cam_name = request.form['cam_name']
    if not section:
        return render_template('index.html', result="Section id is required.", show_results=True)
    if not cam_name:
        cam_name = "Camera 1"
    config1 = {
        'section': section,
        'event': event,
        'name': cam_name
    }
    try:
        requests.put(cam1 + "config", json=config1)
        print("Successfully configured camera1.", flush=True)
        config = {
            'Config for the 1st camera': config1,
        }
        info = f"Camera 1 has been successfully reconfigured.\n" \
               f"{json.dumps(config, sort_keys=True, indent=4, check_circular=True)}"
        configuration['cameras'][0]['event'] = event
        configuration['cameras'][0]['section'] = section
        return render_template('index.html', result=info, show_results=True)
    except Exception as e:
        print(json.dumps({"error": {"code": 403, "message": str(e), "status": "DENIED"}}))


@app.route('/change-cam2-config', methods=['POST'])
def change_config_2():
    section = request.form['section']
    event = request.form['event']
    cam_name = request.form['cam_name']
    if not section:
        return render_template('index.html', result="Section id is required.", show_results=True)
    if not cam_name:
        cam_name = "Camera 2"
    config2 = {
        'section': section,
        'event': event,
        'name': cam_name
    }
    try:
        requests.put(cam2 + "config", json=config2)
        print("Successfully configured camera1.", flush=True)
        config = {
            'Config for the 1st camera': config2,
        }
        info = f"Camera 2 has been successfully reconfigured.\n" \
               f"{json.dumps(config, sort_keys=True, indent=4, check_circular=True)}"
        configuration['cameras'][1]['event'] = event
        configuration['cameras'][1]['section'] = section
        return render_template('index.html', result=info, show_results=True)
    except Exception as e:
        print(json.dumps({"error": {"code": 403, "message": str(e), "status": "DENIED"}}))


def configure_cameras():
    config1 = {
        'section': 1,
        'event': 'entry',
        'name': 'Camera 1'
    }
    config2 = {
        'section': 1,
        'event': 'exit',
        'name': 'Camera 2'
    }
    try:
        requests.put(cam1 + "config", json=config1)
        requests.put(cam2 + "config", json=config2)
        print("Successfully configured cameras.", flush=True)
        config = {
            'Config for the 1st camera': config1,
            'Config for the 2nd camera': config2
        }
        return config
    except Exception as e:
        print(json.dumps({"error": {"code": 403, "message": str(e), "status": "DENIED"}}))


@app.route('/cameras', methods=['GET'])
def get_cameras():
    return render_template("index.html", result=json.dumps(configuration, sort_keys=True, indent=4,
                                                           check_circular=True), show_results=True)


@app.route('/cameras/<camera_id>/<path:u_path>', methods=['GET'])
def get_camera_by_id(camera_id, u_path=''):
    if camera_id == "1":
        url = cam1 + u_path
    elif camera_id == "2":
        url = cam2 + u_path
    else:
        return render_template("index.html", result="The available cameras have the ids '1' and '2'.",
                               show_results=True)
    res = ''
    if request.method == 'GET':
        res = requests.get(url, request.data)
    return render_template("index.html", result=json.dumps(res.json(), sort_keys=True, indent=4, check_circular=True),
                           show_results=True)


@app.route('/stream1')
def stream_cam1():
    url = cam1 + "stream?toggle=on"
    setup = {
        "destination": "http://collector:80/frame",
        "max-frames": 5,
        "delay": 1
    }
    res = requests.post(url, json=setup)
    return render_template("index.html", result=json.dumps(res.json(), sort_keys=True, indent=4),
                           show_results=True)


@app.route('/stream2')
def stream_cam2():
    url = cam2 + "stream?toggle=on"
    setup = {
        "destination": "http://collector:80/frame",
        "max-frames": 5,
        "delay": 1
    }
    res = requests.post(url, json=setup)
    return render_template("index.html", result=json.dumps(res.json(), sort_keys=True, indent=4, check_circular=True),
                           show_results=True)


@app.route('/section/<section_id>/<path:u_path>', methods=['GET'])
def get_section_by_id(section_id, u_path='') -> json:
    if section_id == "1":
        url = sec + request.url[32::]
    else:
        return render_template("index.html", result="The available section has the id '1'.",
                               show_results=True)
    res = ''
    if request.method == 'GET':
        res = requests.get(url, request.data)
    return render_template("index.html", result=json.dumps(res.json(), sort_keys=True, indent=4, check_circular=True),
                           show_results=True)


@app.route('/alerts/<alert_id>/<path:u_path>', methods=['GET'])
def get_alerts(alert_id, u_path='') -> json:
    if alert_id == "1":
        url = alert + request.url[31::]
    else:
        return render_template("index.html", result="The available alert service has the id '1'.",
                               show_results=True)
    res = requests.get(url, request.data)
    return render_template("index.html", result=json.dumps(res.json(), sort_keys=True, indent=4, check_circular=True),
                           show_results=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
