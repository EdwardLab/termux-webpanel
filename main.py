from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

def get_device_info():
    info = {}
    commands = {
        'Battery Status': 'termux-battery-status',
        'Wifi Connection': 'termux-wifi-connectioninfo',
        'Storage Info': 'termux-storage-get'
    }

    for key, command in commands.items():
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                info[key] = result.stdout
            else:
                info[key] = 'Error: ' + result.stderr
        except Exception as e:
            info[key] = 'Exception: ' + str(e)

    return info

@app.route('/', methods=['GET'])
def device_info():
    info = get_device_info()
    return jsonify(info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5540)
