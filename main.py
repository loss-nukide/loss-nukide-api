from flask import Flask, request, jsonify
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# アップロード先ディレクトリ
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 写真のアップロードエンドポイント
@app.route('/upload', methods=['POST'])
def upload_photos():
    if 'after' not in request.files:
        return jsonify({"error": "食べる前と食べた後の写真をアップロードしてください"}), 400
    
    after = request.files['after']
    
    if after.filename == None:
        return jsonify({"error": "ファイル名が無効です"}), 400
    
    # ファイルの保存
    after_filename = secure_filename(after.filename)
    after_path = os.path.join(UPLOAD_FOLDER, after_filename)
    after.save(after_path)
    
    # 画像処理
    score = calculate_score(after_path)
    return jsonify({"score": score})


if __name__ == '__main__':
    app.run(debug=True)