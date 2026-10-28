"""Réinitialise la base de données locale (schema.sql puis seed.sql).

Pour ceux qui ont MySQL installé sans Docker. Utilise le client `mysql`
en ligne de commande et un compte ayant le droit de créer la base
(root par défaut).

Utilisation (depuis le dossier backend) :
    python db/reset_db.py                 # utilisateur root, mot de passe demandé
    python db/reset_db.py -u root -p monMdp
"""
import argparse
import getpass
import os
import shutil
import subprocess
import sys

from dotenv import load_dotenv

DOSSIER_DB = os.path.dirname(os.path.abspath(__file__))
FICHIERS = ["schema.sql", "seed.sql"]


def main():
    load_dotenv(os.path.join(DOSSIER_DB, "..", ".env"))

    parser = argparse.ArgumentParser(description="Réinitialise la BD Replay")
    parser.add_argument("-u", "--user", default="root")
    parser.add_argument("-p", "--password")
    parser.add_argument("--host", default=os.getenv("DB_HOST", "localhost"))
    parser.add_argument("--port", default=os.getenv("DB_PORT", "3306"))
    parser.add_argument("--mysql", default="mysql", help="chemin vers le client mysql")
    args = parser.parse_args()

    if not shutil.which(args.mysql) and not os.path.isfile(args.mysql):
        sys.exit(f"Client MySQL introuvable : {args.mysql} (utilisez --mysql <chemin vers mysql.exe>)")

    mot_de_passe = args.password if args.password is not None else getpass.getpass(f"Mot de passe MySQL pour {args.user} : ")
    env = dict(os.environ, MYSQL_PWD=mot_de_passe)
    commande = [args.mysql, "-h", args.host, "-P", str(args.port), "-u", args.user, "--default-character-set=utf8mb4"]

    for nom in FICHIERS:
        print(f"Exécution de {nom}...")
        with open(os.path.join(DOSSIER_DB, nom), "rb") as fichier:
            resultat = subprocess.run(commande, stdin=fichier, env=env)
        if resultat.returncode != 0:
            sys.exit(f"Échec lors de l'exécution de {nom}")

    # Compte utilisé par l'application (valeurs du .env), comme le fait docker-compose
    db_user = os.getenv("DB_USER", "replay")
    if db_user != args.user:
        db_name = os.getenv("DB_NAME", "replay")
        db_password = os.getenv("DB_PASSWORD", "replay").replace("'", "''")
        print(f"Création de l'utilisateur {db_user}...")
        # mysql_native_password : permet la connexion sans SSL (DB_SSL=false)
        sql = (
            f"CREATE USER IF NOT EXISTS '{db_user}'@'localhost' IDENTIFIED WITH mysql_native_password BY '{db_password}';"
            f"GRANT ALL PRIVILEGES ON `{db_name}`.* TO '{db_user}'@'localhost';"
            "FLUSH PRIVILEGES;"
        )
        resultat = subprocess.run(commande + ["-e", sql], env=env)
        if resultat.returncode != 0:
            sys.exit(f"Échec lors de la création de l'utilisateur {db_user}")

    print("Base de données réinitialisée.")


if __name__ == "__main__":
    main()
