import os
from flask import Blueprint, jsonify, request, Response, current_app, Flask
from werkzeug.utils import secure_filename
from services.analyze import analyze_loss  
import cv2

# Blueprintの定義
api = Blueprint('analyze-loss', __name__, url_prefix='/api/analyze-loss')

# アップロードディレクトリの設定
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# before_requestフックの設定
@api.before_request
def before_request():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ルートの定義
@api.route("", methods=['POST'])
def index() -> Response:
    if 'img' not in request.files:
        response = jsonify({"error": "画像をアップロードしてください"})
        response.status_code = 400
        return response

    img = request.files['img']

    if not img.filename:
        response = jsonify({"error": "ファイル名が無効です"})
        response.status_code = 400
        return response

    # ファイルの保存
    img_filename = secure_filename(img.filename)
    img_path = os.path.join(UPLOAD_FOLDER, img_filename)
    img.save(img_path)

    # 画像処理
    image = cv2.imread(img_path)
    if image is None:
        response = jsonify({"error": "画像の読み込みに失敗しました"})
        response.status_code = 500
        return response

    score = analyze_loss(image)
    return jsonify({"score": str(score)})

# FlaskアプリケーションにBlueprintを登録
app = Flask(__name__)
app.register_blueprint(api)

if __name__ == "__main__":
    app.run(port=8000, debug=True)