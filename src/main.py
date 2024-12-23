from flask import Flask
import routes.analyze_loss as analyze_loss

app = Flask(__name__)
app.register_blueprint(analyze_loss.api)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(port=8000, debug=True)