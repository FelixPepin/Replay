import os

from dotenv import load_dotenv
from flask import Flask, send_from_directory
from flask_cors import CORS

from routes.authentification import bp_auth
from routes.location import bp_location
from routes.vente import bp_vente

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "une_clé_secrète_dev")
CORS(app)
app.register_blueprint(bp_auth, url_prefix='/api')
app.register_blueprint(bp_vente, url_prefix='/api')
app.register_blueprint(bp_location, url_prefix='/api')

app.config['MORCEAUX_VERS_AJOUTS'] = ['static', 'images', 'ajouts']
app.config['ROUTE_VERS_AJOUTS'] = "/".join(app.config['MORCEAUX_VERS_AJOUTS'])
app.config['CHEMIN_VERS_AJOUTS'] = os.path.join(app.root_path, *app.config['MORCEAUX_VERS_AJOUTS'])

FRONTEND_DIST = os.path.join(os.path.dirname(app.root_path), 'frontend', 'dist')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path and os.path.exists(os.path.join(FRONTEND_DIST, path)):
        return send_from_directory(FRONTEND_DIST, path)
    return send_from_directory(FRONTEND_DIST, 'index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
