
import os
import types
import contextlib
import mysql.connector
from contextlib import contextmanager

# SSL désactivé par défaut (BD locale) ; DB_SSL=true pour une BD distante
def ssl_active():
    return os.getenv("DB_SSL", "false").strip().lower() in ("1", "true", "yes", "oui")

# Connexion à la bd
@contextlib.contextmanager
def creer_connexion():
    options_ssl = {"ssl_disabled": False, "ssl_verify_cert": False} if ssl_active() else {"ssl_disabled": True}
    conn = mysql.connector.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        database=os.getenv("DB_NAME"),
        raise_on_warnings=True,
        **options_ssl
    )

    conn.get_curseur = types.MethodType(get_curseur, conn)

    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()
    finally:
        conn.close()

@contextlib.contextmanager
def get_curseur(self, **kwargs):
    curseur = self.cursor(dictionary=True, buffered=True)
    try:
        yield curseur
    finally:
        curseur.close()