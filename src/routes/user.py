from flask import Blueprint, request, jsonify
from repository.models import db, User

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

@bp.route('/<int:id>', methods=['GET']) # type: ignore
def get_name(id:int):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({"error": "ユーザーが見つかりません"}), 404

    return jsonify({"name": user.name}), 200

@bp.route('/<int:id>/ateList', methods=['Get']) # type: ignore
def get_ateList(id:int):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({"error": "ユーザーが見つかりません"}), 404

    ateList = user.jiro_calls
    ateList = [{"shopName": jiro_call.shopName, "amountOfnoodles": jiro_call.amountOfnoodles, "amountOfBegetables": jiro_call.amountOfBegetables, "amountOfNinniku": jiro_call.amountOfNinniku, "amountOfKarame": jiro_call.amountOfKarame, "ammountOfAbura": jiro_call.ammountOfAbura} for jiro_call in ateList]
    return jsonify(ateList), 200