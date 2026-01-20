from flask import Flask, redirect, url_for
from apis.chat import apis

app = Flask(__name__)

# Register Blueprint
app.register_blueprint(apis, url_prefix="/chat")

# Root route
@app.route("/")
def home():
    return redirect(url_for("apis.dashboard_aerochat"))

if __name__ == "__main__":
    app.run(debug=True)
