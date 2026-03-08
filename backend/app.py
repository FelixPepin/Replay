from flask import Flask
import bd
from routes.authentification import bp_auth
from routes.vente import bp_vente
from routes.location import bp_location
from flask_cors import CORS
import os


app = Flask(__name__)
app.secret_key = "une_clé_secrète"
CORS(app)
app.register_blueprint(bp_auth)
app.register_blueprint(bp_vente)
app.register_blueprint(bp_location)

app.config['MORCEAUX_VERS_AJOUTS'] = ['static', 'images', 'ajouts']
app.config['ROUTE_VERS_AJOUTS'] = "/".join(app.config['MORCEAUX_VERS_AJOUTS'])
app.config['CHEMIN_VERS_AJOUTS'] = os.path.join(app.root_path, *app.config['MORCEAUX_VERS_AJOUTS'])

if __name__ == "__main__":
    app.run(debug=True, port=5000)