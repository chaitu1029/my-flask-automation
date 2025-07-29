from flask import Flask, jsonify, send_from_directory
import time

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/run_automation')
def run_automation():
    print("Automation started")
    # Replace this with your actual automation code (e.g., Selenium)
    time.sleep(3)  # Simulating work
    print("Automation finished")
    return jsonify({"message": "Automation triggered successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
