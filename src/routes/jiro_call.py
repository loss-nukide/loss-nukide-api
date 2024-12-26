from flask import Blueprint, request, jsonify
from repository.models import JiroCall, db, User

bp = Blueprint('jiroCall', __name__, url_prefix='/jiroCall')

@bp.route('', methods=['POST', 'GET']) # type: ignore
def create_jiroCall():
    if request.method == 'POST':
        # フォームデータを取得
        shopName = request.form.get('shopName')
        amountOfnoodles = request.form.get('amountOfnoodles')
        amountOfBegetables = request.form.get('amountOfBegetables')
        amountOfNinniku = request.form.get('amountOfNinniku')
        amountOfKarame = request.form.get('amountOfKarame')
        ammountOfAbura = request.form.get('ammountOfAbura')

        if not shopName or not amountOfnoodles or not amountOfBegetables or not amountOfNinniku or not amountOfKarame or not ammountOfAbura:
            return jsonify({"error": "店名、麺の量、野菜の量、ニンニクの量、カラメの量、アブラの量は必須です"}), 400

        new_jiroCall = JiroCall(shopName=shopName, amountOfnoodles=amountOfnoodles, amountOfBegetables=amountOfBegetables, amountOfNinniku=amountOfNinniku, amountOfKarame=amountOfKarame, ammountOfAbura=ammountOfAbura)
        db.session.add(new_jiroCall)
        db.session.commit()

        return jsonify({"message": "created jiroCall!"}), 201
    
    elif request.method == 'GET':
        jiroCalls = JiroCall.query.all()
        jiroCalls = [{"shopName": jiroCall.shopName, "amountOfnoodles": jiroCall.amountOfnoodles, "amountOfBegetables": jiroCall.amountOfBegetables, "amountOfNinniku": jiroCall.amountOfNinniku, "amountOfKarame": jiroCall.amountOfKarame, "ammountOfAbura": jiroCall.ammountOfAbura} for jiroCall in jiroCalls]
        return jsonify(jiroCalls), 200

@bp.route('/<int:id>', methods=['GET']) # type: ignore
def get_jiroCall(id:int):
    jiroCall = JiroCall.query.filter_by(id=id).first()
    if not jiroCall:
        return jsonify({"error": "二郎のコールが見つかりません"}), 404

    return jsonify({"Noodles": jiroCall.amountOfnoodles, 
                    "Vegetable": jiroCall.amountOfBegetables,
                    "Ninniku": jiroCall.amountOfNinniku,
                    "Karame": jiroCall.amountOfKarame,
                    "Abura": jiroCall.ammountOfAbura}), 200