from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QThread, QEventLoop, pyqtSlot
import yaml
import os
import threading
from time import sleep
from internal.logger import Logger
import sys

class Recipes(QObject):
    """
    La classe Recipes gère l'exécution des recettes du système. Elle charge les recettes à partir de fichiers YAML et exécute les étapes spécifiées.

    Attributes:
        valid_actions: Liste des actions valides.
        valid_conditions: Liste des conditions valides.
        dictionnaire: Dictionnaire pour la correspondance des valeurs.
        finished: Signal émis lorsque l'exécution d'une recette est terminée.
        warning: Signal émis en cas d'avertissement.
        request_timer_stop: Signal émis pour demander l'arrêt des recettes en cours.
        recipe_folder: Chemin du dossier contenant les fichiers de recettes.
        action: Signal émis pour déclencher une action.
        parent: Référence à l'objet parent.
        translator: Référence à l'objet Translator.
        recipes: Dictionnaire contenant les recettes.
        thread: Référence au thread de la classe.
        timer: Référence au timer de la classe.
        warning: Signal émis en cas d'avertissement.
        action: Signal émis pour déclencher une action.
        stop_event: Objet Event pour arrêter l'exécution d'une recette.


    Methods:
        __init__(self, parent):
            Constructeur de la classe Recipes.

        verify_yaml(self, yaml_path):
            Vérifie la validité d'un fichier YAML de recette.

        handle_error(self, error_key, **kwargs):
            Gère les erreurs rencontrées lors de la vérification des recettes.

        load_recipes(self):
            Charge les recettes à partir des fichiers YAML.

        execute_recipe(self, recipe_name):
            Exécute une recette spécifique.

        is_running(self):
            Vérifie si une recette est en cours d'exécution.

        run_recipe(self):
            Exécute les étapes d'une recette.

        stop(self):
            Arrête l'exécution de la recette en cours.

        stop_recipes(self):
            Arrête toutes les recettes en cours.

        check_conditions(self, conditions):
            Vérifie si les conditions sont remplies pour l'exécution de l'étape.

        check_timeout(self):
            Vérifie si le temps imparti pour une étape est écoulé.
    """
    valid_actions = ['wafer_lift1','wafer_lift2','wafer_lift3','SV','throttle_valve','motor_lift','MFC1','MFC2', 'roughing_pump', 'turbo_pump_ch', 'turbo_pump_rga', 'turbo_pump_gate','nupro_final','nupro_MFC1','nupro_MFC2','nupro_vent','iso_rga_ch','iso_rga_pump', 'iso_turbo','turbo_pump_gate', 'iso_chamber']
    valid_conditions = ['interlock','wafer_lift1','wafer_lift2','wafer_lift3','SV','baratron1','baratron2','MFC1','MFC2','chamber_pressure','pump_pressure','ion_gauge','roughing_pump','turbo_pump_ch','turbo_pump_rga','turbo_pump_gate']

    dictionnaire = {
        "on":False,
        "off":True,
        "open":False,
        "close":True,
        "at_speed": False,
        "slow":True,
        "up": True,
        "down":False,
    }
    
    finished = pyqtSignal()
    warning = pyqtSignal(str)
    request_timer_stop = pyqtSignal()
    recipe_folder = "recipes"

    action = pyqtSignal(object, object)

    def __init__(self, parent):
        """
        Constructeur de la classe Recipes.

        Args:
            parent: Référence à l'objet parent.
        """
        super().__init__()
        self.parent = parent
        self.translator = self.parent.translator
        self.recipes = self.load_recipes()
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.run_recipe)

        self.request_timer_stop.connect(self.stop_recipes)

        self.timer = QTimer()
        self.timer.moveToThread(self.thread)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.check_timeout)

        self.warning.connect(parent.show_error_message)

        self.action.connect(parent.set_value)

        self.stop_event = threading.Event()  # Ajout de cette ligne


    def verify_yaml(self, yaml_path):
        """
        Vérifie la validité d'un fichier YAML de recette.

        Args:
            yaml_path: Chemin du fichier YAML de recette.
        """
        with open(yaml_path, 'r') as f:
            content = yaml.safe_load(f)

        filename = os.path.basename(yaml_path)
        if not isinstance(content, dict):
            self.handle_error('invalid_yaml', filename=filename)
            
        for step_num, step in content.items():
            # Vérification de 'name'
            if "name" not in step:
                self.handle_error('missing_name', filename=filename, step_num=step_num)

            # Vérification des 'actions'
            if "actions" in step:
                for action_name in step["actions"].keys():
                    if action_name not in self.valid_actions:
                        self.handle_error('invalid_action', filename=filename, step_num=step_num, action_name=action_name)

            # Vérification des 'conditions'
            if "conditions" in step:
                for condition_name in step["conditions"].keys():
                    if condition_name not in self.valid_conditions:
                        self.handle_error('invalid_condition', filename=filename, step_num=step_num, condition_name=condition_name)

                # Vérification de 'error_message' si 'conditions' est présent
                if "error_message" not in step:
                    self.handle_error('missing_error_message', filename=filename, step_num=step_num)

            # Vérification de 'timeout'
            if "timeout" not in step:
                self.handle_error('missing_timeout', filename=filename, step_num=step_num)

    def handle_error(self, error_key, **kwargs):
        """
        Gère les erreurs rencontrées lors de la vérification des recettes.

        Args:
            error_key: Clé de l'erreur.
            **kwargs: Arguments spécifiques à l'erreur.
        """
        error_message = self.translator.translate(error_key, **kwargs)
        Logger.error(error_message)
        raise ValueError(error_message)  # Lève une exception avec le message d'erreur

    def load_recipes(self):
        """
        Charge les recettes à partir des fichiers YAML.
        """
        recipes = {}
        for filename in os.listdir(self.recipe_folder):
            path = os.path.join(self.recipe_folder, filename)
            try:  # Essaye de vérifier et de charger le fichier
                self.verify_yaml(path)
                if filename.endswith('.yaml'):
                    with open(path, 'r', encoding="utf-8") as f:
                        recipe_name = os.path.splitext(filename)[0]
                        recipes[recipe_name] = yaml.safe_load(f)
            except ValueError as e:  # Gère l'exception si une erreur est trouvée
                Logger.error(f"Erreur lors du chargement de {filename}: {str(e)}")
        return recipes


    def execute_recipe(self, recipe_name):
        """
        Exécute une recette spécifique.

        Args:
            recipe_name: Nom de la recette à exécuter.
        """
        if self.thread.isRunning():
            Logger.info("A recipe is already running. Please wait for it to finish or stop it before starting a new one.")
            return
        if recipe_name in self.recipes:
            self.stop_event.clear()
            self.current_recipe = self.recipes[recipe_name]
            self.thread.start()

    def is_running(self):
        """
        Vérifie si une recette est en cours d'exécution.

        Returns:
            True si une recette est en cours d'exécution, False sinon.
        """
        return self.thread.isRunning()

    def run_recipe(self):
        """
        Exécute les étapes d'une recette.
        """
        recipe = self.current_recipe
        for index, step in enumerate(recipe.values()):  # On utilise values() pour obtenir seulement les valeurs
            step_name = step["name"]
            if self.stop_event.is_set():
                break
            self.parent.custom_widgets["chamber_label"].update_step(step_name, index + 1, len(recipe))
            if 'actions' in step:
                for action_name, action_value in step['actions'].items():
                    if action_value in self.dictionnaire.keys():
                        action_value = self.dictionnaire[action_value]
                    self.action.emit(action_name, action_value)
            if 'conditions' in step:
                self.current_conditions = step['conditions']
                if 'error_message' in step:
                    self.current_error_message = step['error_message']
                else:
                    self.current_error_message = "Error"
                condition_met = self.check_conditions(self.current_conditions)
                self.timer.start(int(step['timeout']) * 1000)  # Timeouts

                while not condition_met and self.timer.isActive() and not self.stop_event.is_set():
                    self.parent.custom_widgets["chamber_label"].update_time("timeout", int(float(self.timer.remainingTime())/1000))
                    loop = QEventLoop()
                    QTimer.singleShot(1000, loop.quit)  # Check the condition every second
                    loop.exec_()
                    condition_met = self.check_conditions(self.current_conditions)
                if not condition_met:
                    break
            else:
                for time in range(int(step['timeout']), 0, -1):
                    self.parent.custom_widgets["chamber_label"].update_time("time_left", time)
                    loop = QEventLoop()
                    QTimer.singleShot(1000, loop.quit)  # Check the condition every second
                    loop.exec_()
                    if self.stop_event.is_set():
                        break
            if self.stop_event.is_set():
                break
        self.stop()

        
    def stop(self):
        """
        Arrête l'exécution de la recette en cours.
        """
        self.timer.stop()
        self.stop_event.set()
        self.thread.quit()
        self.parent.custom_widgets["chamber_label"].button_stop()


    @pyqtSlot()
    def stop_recipes(self):
        """
        Permet d'arrêter l'exécution de la recette en cours depuis un autre thread.
        """
        self.stop()

    def check_conditions(self, conditions):
        """
        Vérifie si les conditions sont remplies pour l'exécution de l'étape.

        Args:
            conditions: Conditions à vérifier. Une condition doit être un nombre, un booléen ou une chaîne de caractères contenant < ou > suivi d'un nombre.

        Returns:
            True si les conditions sont satisfaites, False sinon.
        """
        for condition_name, condition_value in conditions.items():
            value = self.parent.custom_widgets[condition_name].get_value()
            if condition_value in self.dictionnaire.keys():
                condition_value = self.dictionnaire[condition_value]
            if isinstance(condition_value, bool) or isinstance(condition_value, int):
                if value != condition_value:
                    return False
            elif isinstance(condition_value, str):
                if condition_value[0] == '<':
                    if value >= float(condition_value[1:]):
                        return False
                elif condition_value[0] == '>':
                    if value <= float(condition_value[1:]):
                        return False
        return True

                

    def check_timeout(self):
        """
        Vérifie si le temps imparti pour une étape est écoulé.
        """
        condition_met = self.check_conditions(self.current_conditions)
        error_message = self.current_error_message
        if not condition_met:
            self.warning.emit(f"Warning: {error_message}")
            self.stop()
