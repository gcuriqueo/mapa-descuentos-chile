from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/data/food/scotiabank/coordinates.json')
def serve_json():
    return send_from_directory('./data/food', 'coordinates_scotiabank.json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8100)