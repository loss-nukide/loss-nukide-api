import os
from flask import Blueprint, jsonify, request

from image_processing import calculate_score
api = Blueprint('analyze-loss',
                __name__,
                url_prefix='/api/analyze-loss')
from flask import Response
from werkzeug.utils import secure_filename

# アップロード先ディレクトリ
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
from flask import current_app

@api.before_request
def before_request():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@api.route("", methods=['POST', 'GET'])
def index() -> Response:
    if request.method == 'POST':
        if 'after' not in request.files:
            response = jsonify({"error": "食べる前と食べた後の写真をアップロードしてください"})
            response.status_code = 400
            return response

        after = request.files['after']

        if after.filename == None:
            response = jsonify({"error": "ファイル名が無効です"})
            response.status_code = 400
            return response

        # ファイルの保存
        after_filename = secure_filename(after.filename)
        after_path = os.path.join(UPLOAD_FOLDER, after_filename)
        after.save(after_path)

        # 画像処理
        score = calculate_score(after_path)
        return jsonify({"score": score})

    else:
        response = jsonify(message="Not implemented")
        response.status_code = 501
        return response

