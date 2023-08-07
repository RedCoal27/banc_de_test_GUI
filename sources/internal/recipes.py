from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QThread, QEventLoop, pyqtSlot
import yaml
import os
import threading
from time import sleep


class Recipes(QObject):
    finished = pyqtSignal()
    warning = pyqtSignal(str)
    request_timer_stop = pyqtSignal()
    recipe_folder = "recipes"

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
            self.current_recipe = self.recipes[recipe_name]
            self.thread.start()

    def is_running(self):
        return self.thread.isRunning()

    def run_recipe(self):
        recipe = self.current_recipe
        print(recipe)
        for step_name, step in recipe.items():
            if self.stop_event.is_set():
                break
            print(f"Executing {step_name}")
            for action in step['actions']:
                print(f"  Action: {action['action']}, Value: {action['valeur']}")

            if 'condition' in step:
                print(f"  Condition: {step['condition']}")
                self.current_condition = step['condition']
                self.current_error_message = step['message_erreur']
                condition_met = self.check_condition(self.current_condition)
                self.timer.start(int(step['temps']) * 1000)  # QTimer expects milliseconds

                while not condition_met and self.timer.isActive() and not self.stop_event.is_set():
                    loop = QEventLoop()
                    QTimer.singleShot(1000, loop.quit)  # Check the condition every second
                    loop.exec_()
                    condition_met = self.check_condition(self.current_condition)

                if not condition_met:
                    break
            else:
                print(f"  Time: {step['temps']}")
                loop = QEventLoop()
                QTimer.singleShot(int(step['temps']) * 1000, loop.quit)  # QTimer expects milliseconds
                loop.exec_()

            print(f"  Error message: {step['message_erreur']}")

        self.stop()

        
    def stop(self):
        self.timer.stop()
        self.stop_event.set()
        self.thread.quit()
        sleep(0.1)
        self.stop_event.clear()
        self.parent.custom_widgets["chamber_label"].button_stop()



    @pyqtSlot()
    def stop_recipes(self):
        self.stop()

    def check_condition(self, condition):
        # Replace this with the actual code to check the condition
        return False

    def check_timeout(self):
        print("Checking timeout")
        condition_met = self.check_condition(self.current_condition)
        error_message = self.current_error_message
        if not condition_met:
            self.warning.emit(f"Warning: {error_message}")
            self.stop()
