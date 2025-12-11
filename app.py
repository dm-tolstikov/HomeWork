import os
import json
import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)


def get_ip_from_ipapi():
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        data = response.json()
        return data.get('query')
    except:
        return None


def get_ip_from_jsonip():
    try:
        response = requests.get('https://jsonip.com/', timeout=5)
        data = response.json()
        return data.get('ip')
    except:
        return None


@app.route('/')
def index():
    api_type = os.environ.get('TYPE', 'ipapi').lower()

    if api_type == 'jsonip':
        ip_address = get_ip_from_jsonip()
        api_name = 'JSONIP.com'
    else:
        ip_address = get_ip_from_ipapi()
        api_name = 'IP-API.com'

    return render_template('index.html',
                           ip_address=ip_address,
                           api_name=api_name,
                           env_api=api_type)


@app.route('/json')
def get_ip_json():
    api_type = os.environ.get('TYPE', 'ipapi').lower()

    if api_type == 'jsonip':
        ip_address = get_ip_from_jsonip()
    else:
        ip_address = get_ip_from_ipapi()

    if ip_address:
        return jsonify({"myIP": ip_address})
    else:
        return jsonify({"error": "Ошибка"}), 500


@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)