from flask import Flask, request, jsonify
import logging
import uuid

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['POST'])
def receive_otlp():
    # Check if there is data in the request
    if request.data:
        # Generate a unique filename for each payload
        filename = f"otlp_payload_{uuid.uuid4()}.bin"

        # Write the binary data directly to a file
        with open(filename, 'wb') as f:
            f.write(request.data)
        
        logging.info(f"Received OTLP data, saved to {filename}")
        return jsonify({"message": "OTLP data received", "filename": filename}), 200
    else:
        return jsonify({"message": "No data received"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4317, debug=True)
