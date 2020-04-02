# Configuration

Pour fonctionner, le server nécessite quelques configurations supplémentaires dans un fichier `.env` à placer à la racine du projet

    SECRET_KEY = 'clé de l'application'
    VERSION = "dev" # si version de dev ou de prod, influe sur la possibilité de CORS
    DEBUG = "1" # 1 si debug a True, 0 si False # pas de prod avec DEBUG = True
    SERVER_IP = "your IP"
    DTB_ENGINE = "django.db.backends.sqlite3"
    DTB_NAME = "db.sqlite3"
    DTB_USER = ''
    DTB_PASSWORD = ""
    DTB_HOST = "localhost"
    DTB_PORT = ""
