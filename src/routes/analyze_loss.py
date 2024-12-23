from flask import Blueprint, jsonify
api = Blueprint('analyze-loss',
                __name__,
                url_prefix='/api/analyze-loss')
from flask import Response

@api.route("", methods=['POST', 'GET'])
def index() -> Response:
    response = jsonify(message="Not implemented")
    response.status_code = 501
    return response

