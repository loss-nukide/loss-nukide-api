from flask import Blueprint, request, jsonify
from models import db, User

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('', methods=['POST', 'GET']) # type: ignore
def create_user():
    if request.method == 'POST':
        # フォームデータを取得
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not name or not email or not password:
            return jsonify({"error": "名前、メールアドレス、パスワードは必須です"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "このメールアドレスは既に登録されています"}), 400

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "created user!"}), 201

    elif request.method == 'GET':
        users = User.query.all()
        users = [{"name": user.name, "email": user.email} for user in users]
        return jsonify(users), 200