from flask import Flask, send_from_directory
from flask_cors import CORS
import os
app = Flask(__name__)

allowed_origins = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:8080').split(',')
CORS(app, resources={r"/*": {"origins": allowed_origins}})

@app.route('/data/food/banks/coordinates.json')
def serve_json():
    return send_from_directory('./data/food', 'coordinates_all_banks.json')

#health checks
@app.route('/health')
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8100)