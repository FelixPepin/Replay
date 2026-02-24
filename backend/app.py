from flask import Flask
import bd
from routes.authentification import bp_auth
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "une_clé_secrète"
CORS(app)
app.register_blueprint(bp_auth)

if __name__ == "__main__":
    app.run(debug=True, port=5000)