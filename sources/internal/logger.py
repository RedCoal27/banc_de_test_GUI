import os
import logging
import logging.handlers
import time


class CustomTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """
    Cette classe étend la classe TimedRotatingFileHandler du module logging.handlers pour personnaliser le nom des fichiers de logs lors de la rotation.

    Methods:
        __init__(self, dir, when='s', backupCount=0, encoding=None, delay=False, utc=False, atTime=None):
            Constructeur de la classe CustomTimedRotatingFileHandler.

        custom_namer(self, default_name):
            Fonction de personnalisation du nom de fichier lors de la rotation.
    """
    def __init__(self, dir, when= 's', backupCount=0, encoding=None, delay=False, utc=False, atTime=None):
        """
        Constructeur de la classe CustomTimedRotatingFileHandler.

        Args:
            dir: Répertoire où les fichiers de log seront stockés.
            when: Fréquence de rotation ('s' pour secondes, 'D' pour jours, etc.).
            backupCount: Nombre maximal de fichiers de log à conserver.
            encoding: Encodage des caractères à utiliser.
            delay: Retard l'ouverture du fichier jusqu'à ce qu'un enregistrement soit effectué.
            utc: Utiliser le temps universel coordonné (UTC).
            atTime: Heure précise de rotation.
        """
        filename = os.path.join(dir, 'app.log')
        super().__init__(filename, when=when, backupCount=backupCount, encoding=encoding, delay=delay, utc=utc, atTime=atTime)
        self.namer = self.custom_namer
        self.prefix = "%Y-%m-%d-%M"

    def custom_namer(self, default_name):
        """
        Fonction de personnalisation du nom de fichier lors de la rotation.

        Args:
            default_name: Nom de fichier par défaut.

        Returns:
            Nouveau nom de fichier avec la date formatée ajoutée avant le app.log
        """
        t = self.rolloverAt - self.interval
        # Obtenir la date courante formatée comme une chaîne de caractères
        date_str = time.strftime(self.prefix, time.localtime(t))
        # Remplacer "app.log" avec "date_str_app.log"
        return default_name.replace("app.log", f"{date_str}_app.log")


class log():
    """
    Cette classe gère la création et la gestion des fichiers de logs.

    Methods:
        __init__(self):
            Constructeur de la classe Log.

        create_logger(self):
            Crée et configure le logger.

        debug(self, message):
            Enregistre un message de débogage.

        info(self, message):
            Enregistre un message d'information.

        warning(self, message):
            Enregistre un message d'avertissement.

        error(self, message):
            Enregistre un message d'erreur.
    """
    def __init__(self):
        """
        Constructeur de la classe Log.
        """
        self.Logger = self.create_logger()


    def create_logger(self):
        """
        Crée et configure le logger.

        Returns:
            Objet Logger configuré.
        """
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
        """
        Enregistre un message de débogage.

        Args:
            message: Message à enregistrer.
        """
        self.Logger.debug(message)

    def info(self, message):
        """
        Enregistre un message d'information.

        Args:
            message: Message à enregistrer.
        """
        self.Logger.info(message)
        print(message)

    def warning(self, message):
        """
        Enregistre un message d'avertissement.

        Args:
            message: Message à enregistrer.
        """
        self.Logger.warning(message)

    def error(self, message):
        """
        Enregistre un message d'erreur.

        Args:
            message: Message à enregistrer.
        """
        self.Logger.error(message)
        print(message)

Logger = log()
