import io
import os
import sys
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS, cross_origin
from PIL import Image
import numpy as np
import time
import logging

import basnet
import transform

logging.basicConfig(level=logging.INFO)
logging.getLogger('flask_cors').level = logging.DEBUG

# Initialize the Flask application
app = Flask(__name__)
CORS(app)


# Simple probe.
@app.route('/', methods=['GET'])
@cross_origin()
def hello():
    return 'Photo Stickers is running!'


# Route http posts to this method
@app.route('/', methods=['POST'])
@cross_origin()
def run():
    start = time.time()

    # Convert string of image data to uint8
    if 'data' not in request.files:
        return jsonify({'error': 'missing file param `data`'}), 400
    data = request.files['data'].read()
    if len(data) == 0:
        return jsonify({'error': 'empty image'}), 400

    # Convert string data to PIL Image
    try:
        img = Image.open(io.BytesIO(data))
    except:
        return jsonify({'error': 'image could not be processed'}), 400

    # Ensure i,qge size is under 1024
    if img.size[0] > 1024 or img.size[1] > 1024:
        img.thumbnail((1024, 1024))

    # Process Image
    res = basnet.run(np.array(img))

    # Segment the original image
    masked = transform.segment(img, res)
    cropped_mask = transform.crop_bbox(masked)
    # Save to buffer
    buff = io.BytesIO()
    cropped_mask.save(buff, 'PNG')
    buff.seek(0)

    # Print stats
    logging.info(f'Completed in {time.time() - start:.2f}s')

    # Return data
    return send_file(buff, mimetype='image/png')


if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
