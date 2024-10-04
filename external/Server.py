from flask import Flask, request, jsonify
from PIL import Image
import io

from ..internal import QueryProcessor

server = Flask(__name__)
qp = QueryProcessor.QueryProcessor()

# Here's an example of accepting a vision request
@server.route('/vision', methods=['POST'])
def vision():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided.'}), 400

    image = request.files['image']

    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'Missing query'}), 400

    try:
        image_stream = io.BytesIO(image.read())
        image = Image.open(image_stream)
    except Exception as e:
        return jsonify({'error': f'Invalid image file: {str(e)}'}), 400

    try:
        result = qp.query_vision(image)
    except Exception as e:
        return jsonify({'error': f'Error processing image: {str({e})}'}), 500

    return jsonify({'result': result}), 200


# Run the server
if __name__ == '__main__':
    server.run(debug=True) # TODO remove "debug=True" once stable