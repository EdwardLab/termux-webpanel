from flask import Flask, render_template_string
import subprocess
import json

app = Flask(__name__)

def get_device_info():
    info = {}
    commands = {
        'Battery Status': 'termux-battery-status',
        'Wifi Connection': 'termux-wifi-connectioninfo'
    }

    for key, command in commands.items():
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                info[key] = json.loads(result.stdout)
            else:
                info[key] = {'Error': result.stderr}
        except Exception as e:
            info[key] = {'Exception': str(e)}

    return info

@app.route('/', methods=['GET'])
def device_info():
    info = get_device_info()
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <title>Device Info</title>
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="mb-4">Device Information</h1>
            {% for key, value in info.items() %}
                <h2>{{ key }}</h2>
                <table class="table table-striped">
                    <thead class="thead-dark">
                        <tr>
                            <th>Property</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for prop, val in value.items() %}
                            <tr>
                                <td>{{ prop }}</td>
                                <td>{{ val }}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            {% endfor %}
        </div>
    </body>
    </html>
    ''', info=info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5540)
