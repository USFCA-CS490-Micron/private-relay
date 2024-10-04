from flask import Flask, request, jsonify
from PIL import Image
import io

from ..internal import QueryProcessor

server = Flask(__name__)
qp = QueryProcessor.QueryProcessor()

# Here's an example of accepting a vision request
@server.route('/vision', methods=['POST'])
def vision():
    pass

# Run the server
if __name__ == '__main__':
    server.run(debug=True) # TODO remove "debug=True" once stable