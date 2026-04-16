import os

from dotenv import load_dotenv
from flask import Flask, send_file
from flask_cors import CORS

from routes.authentification import bp_auth
from routes.location import bp_location
from routes.vente import bp_vente
from routes.reservations import bp_reservation;
from routes.utilisateur import bp_users
from routes.paiement import bp_paiement
from routes.forum import bp_forum
from routes.evaluation import bp_evaluation


load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "une_clé_secrète_dev")
CORS(app)
app.register_blueprint(bp_auth, url_prefix='/api')
app.register_blueprint(bp_vente, url_prefix='/api')
app.register_blueprint(bp_location, url_prefix='/api')
app.register_blueprint(bp_reservation, url_prefix='/api')
app.register_blueprint(bp_users, url_prefix='/api')
app.register_blueprint(bp_paiement, url_prefix='/api')
app.register_blueprint(bp_forum,url_prefix='/api')
app.register_blueprint(bp_evaluation, url_prefix='/api')

app.config['MORCEAUX_VERS_AJOUTS'] = ['static', 'images', 'ajouts']
app.config['ROUTE_VERS_AJOUTS'] = "/".join(app.config['MORCEAUX_VERS_AJOUTS'])
app.config['CHEMIN_VERS_AJOUTS'] = os.path.join(app.root_path, *app.config['MORCEAUX_VERS_AJOUTS'])

FRONTEND_DIST = os.path.join(os.path.dirname(app.root_path), 'frontend', 'dist')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    target = os.path.join(FRONTEND_DIST, path)
    if path and os.path.isfile(target):
        return send_file(target)
    return send_file(os.path.join(FRONTEND_DIST, 'index.html'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
