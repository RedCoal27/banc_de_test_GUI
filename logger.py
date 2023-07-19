import os
import logging
import logging.handlers


class log():
    def __init__(self):
        self.logger = self.create_logger()


    def create_logger(self):
        # Vérifier si le dossier "logs" existe, sinon le créer
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Créer le gestionnaire de rotation des fichiers de log
        log_filename = os.path.join('logs', 'app.log')
        handler = logging.handlers.TimedRotatingFileHandler(log_filename, when='midnight', backupCount=30)
        handler.suffix = "%Y-%m-%d"

        # Configurer le format du log
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Créer le logger et ajouter le gestionnaire
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

        return self.logger

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

logger = log()