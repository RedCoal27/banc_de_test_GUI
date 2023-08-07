from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QThread, QEventLoop, pyqtSlot
import yaml
import os
import threading
from time import sleep


class Recipes(QObject):
    dictionnaire = {
        "on":0,
        "off":1,
        "open":0,
        "close":1,
        "at_speed": 0
    }
    finished = pyqtSignal()
    warning = pyqtSignal(str)
    request_timer_stop = pyqtSignal()
    recipe_folder = "recipes"

    action = pyqtSignal(object, object)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
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

    def load_recipes(self):
        recipes = {}
        for filename in os.listdir(self.recipe_folder):
            if filename.endswith('.yaml'):
                with open(os.path.join(self.recipe_folder, filename), 'r', encoding="utf-8") as f:
                    recipe_name = os.path.splitext(filename)[0]
                    recipes[recipe_name] = yaml.safe_load(f)
        return recipes

    def execute_recipe(self, recipe_name):
        if self.thread.isRunning():
            print("A recipe is already running. Please wait for it to finish or stop it before starting a new one.")
            return
        if recipe_name in self.recipes:
            self.stop_event.clear()
            self.current_recipe = self.recipes[recipe_name]
            self.thread.start()

    def is_running(self):
        return self.thread.isRunning()

    def run_recipe(self):
        recipe = self.current_recipe
        for index, (step_name, step) in enumerate(recipe.items()):
            print(step_name,step)
            if self.stop_event.is_set():
                break
            self.parent.custom_widgets["chamber_label"].update_step(step_name, index + 1, len(recipe))
            for action in step['actions']:
                if action["value"] in self.dictionnaire.keys():
                    action["value"] = self.dictionnaire[action["value"]]
                self.action.emit(action["action"], action["value"])
            if 'conditions' in step:
                print(f"  Condition: {step['conditions']}")
                self.current_conditions = step['conditions']
                self.current_error_message = step['message_erreur']
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
                print(f"  No condition")
                print(f"  Time: {step['timeout']}")
                for time in range(int(step['timeout']), 0, -1):
                    self.parent.custom_widgets["chamber_label"].update_time("time_left", time)
                    loop = QEventLoop()
                    QTimer.singleShot(1000, loop.quit)  # Check the condition every second
                    loop.exec_()
                    print(time)
                    if self.stop_event.is_set():
                        print("stop")
                        break
            if self.stop_event.is_set():
                break
        self.stop()

        
    def stop(self):
        print("stop")
        self.timer.stop()
        self.stop_event.set()
        self.thread.quit()
        print(self.stop_event.is_set())
        self.parent.custom_widgets["chamber_label"].button_stop()



    @pyqtSlot()
    def stop_recipes(self):
        self.stop()

    def check_conditions(self, conditions):
        '''
        Checks if the conditions are met.
        Condition can be a single condition or a list of conditions.
        A condition is a dictionary with the name of the widget as key and a test to perform as value.
        The test can be:
        - a boolean: the state of the widget must be equal to the boolean
        - < or > followed by a number: the value of the widget must be less than or greater than the number
        '''
        for condition in conditions:
            value = self.parent.custom_widgets[condition["condition"]].get_value()
            if value in self.dictionnaire.keys():
                value = self.dictionnaire[condition]
            condition = condition["value"]
            if isinstance(condition, bool) or isinstance(condition, int):
                return value == condition
            elif isinstance(condition, str):
                if condition[0] == '<':
                    return value < float(condition[1:])
                elif condition[0] == '>':
                    return value > float(condition[1:])
                

    def check_timeout(self):
        condition_met = self.check_conditions(self.current_conditions)
        error_message = self.current_error_message
        if not condition_met:
            self.warning.emit(f"Warning: {error_message}")
            self.stop()
