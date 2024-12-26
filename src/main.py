from flask import Flask
from routes import jiro_call
import routes.user as user
import routes.analyze_loss as analyze_loss
from repository.models import db  # 修正

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lossnuki.db'  # データベースURIを設定
db.init_app(app)

app.register_blueprint(analyze_loss.api)
app.register_blueprint(user.bp)
app.register_blueprint(jiro_call.bp)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # データベーステーブルを作成
    app.run(port=8000, debug=True)