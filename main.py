# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os

from flask import Flask, jsonify, Request, request, make_response
from flask_cors import CORS  # Import CORS

from calculator import calculate

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/', methods=['POST'])
def process_gcode(req: Request = None):
    try:
        # Check if running on Cloud Functions
        if 'FUNCTION_TARGET' in os.environ:
            r = req  # Get the request object for Cloud Functions
        else:
                    r = request  # Get the request object for local dev

        file = r.files['file']
        gcode_data = file.read().decode('utf-8')
        # Get cut_length from the request
        cut_length = float(request.form.get('cutLength', 1.1))  # Default to 1.1 if not provided

        result = calculate(gcode_data, cut_length)  # Pass the G-code data to your calculate function
        resp = make_response(jsonify(result))
        resp.headers['Content-Type'] = 'application/json'

        h = resp.headers
        # prepare headers for CORS authentication
        h['Access-Control-Allow-Origin'] = r.environ['HTTP_ORIGIN']
        h['Access-Control-Allow-Methods'] = 'POST'
        h['Access-Control-Allow-Headers'] = 'X-Requested-With'

        resp.headers = h
        return resp
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
