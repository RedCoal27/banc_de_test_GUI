import os
import logging
import logging.handlers
import time


class CustomTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, dir, when= 's', backupCount=0, encoding=None, delay=False, utc=False, atTime=None):
        filename = os.path.join(dir, 'app.log')
        super().__init__(filename, when=when, backupCount=backupCount, encoding=encoding, delay=delay, utc=utc, atTime=atTime)
        self.namer = self.custom_namer
        self.prefix = "%Y-%m-%d-%M"

    def custom_namer(self, default_name):
        t = self.rolloverAt - self.interval
        # Obtenir la date courante formatée comme une chaîne de caractères
        date_str = time.strftime(self.prefix, time.localtime(t))
        # Remplacer "app.log" avec "date_str_app.log"
        return default_name.replace("app.log", f"{date_str}_app.log")


class log():
    def __init__(self):
        self.Logger = self.create_logger()


    def create_logger(self):
        # Vérifier si le dossier "logs" existe, sinon le créer
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Créer le gestionnaire de rotation des fichiers de log
        handler = CustomTimedRotatingFileHandler('logs', when= 'midnight', backupCount=30)
        handler.suffix = ""


        # Configurer le format du log
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Créer le Logger et ajouter le gestionnaire
        self.Logger = logging.getLogger(__name__)
        self.Logger.addHandler(handler)
        self.Logger.setLevel(logging.DEBUG)

        return self.Logger

    def debug(self, message):
        self.Logger.debug(message)

    def info(self, message):
        self.Logger.info(message)
        print(message)

    def warning(self, message):
        self.Logger.warning(message)

    def error(self, message):
        self.Logger.error(message)
        print(message)

Logger = log()
