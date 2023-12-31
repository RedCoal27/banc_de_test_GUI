from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QSpinBox
from PyQt5.QtCore import QTimer, QDate, QDateTime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT
from matplotlib.figure import Figure
import csv
import os

from internal.logger import Logger

class CycleGui(QMainWindow):
    def __init__(self, parent, state_up_key='ascent', state_down_key='descent'):
        """
        Constructeur de la classe CycleGui.

        Args:
            parent: Objet parent.
            state_up_key: Clé d'état pour la montée.
            state_down_key: Clé d'état pour la descente.
        """
        super().__init__()

        self.parent = parent
        self.main_parent = parent.parent

        self.state_up_key = state_up_key  # ou 'open'
        self.state_down_key = state_down_key  # ou 'close'

        self.tempo_high = self.main_parent.config.get_constant_value("tempo_high")
        self.tempo_low = self.main_parent.config.get_constant_value("tempo_low")

        # Initialize widget dictionaries
        self.labels = {}
        self.edits = {}
        self.layouts = {}

        # Initialize timers
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer)
        self.sensor_check_timer = QTimer()
        self.sensor_check_timer.timeout.connect(self.check_sensor)
        self.is_running = False

        # Create widgets and layouts
        self.create_top_widgets()
        self.create_start_button()
        self.create_max_min_widgets()
        self.create_graph()
        self.create_pn_sn_widgets()
        self.create_main_layout()

        # Initialize data list for the graph
        self.time_data = []
        self.component_state = []
        self.cycle_durations = []


        self.setCentralWidget(self.widget)

        self.setMinimumSize(750, 500)
        self.setMaximumSize(1000, 700)

        #name of the window
        try:
            self.setWindowTitle(self.parent.translator.translate(self.parent.key, number=self.parent.FourWay_number))
        except:
            self.setWindowTitle(self.parent.translator.translate(self.parent.key))


        self.setWindowIcon(self.parent.parent.icon)
        self.resize(900, 700)


    def create_top_widgets(self):
        """
        Crée les widgets pour les options en haut de la fenêtre.
        """
        self.labels['cycle'] = QLabel(self.parent.translator.translate('cycles'), self)
        self.edits['cycle'] = QSpinBox(self)
        self.edits['cycle'].setRange(0, 100)
        self.edits['cycle'].setValue(20)

        self.labels['status'] = QLabel(self.parent.translator.translate('status'), self)
        self.edits['status'] = QLineEdit(self)
        self.edits['status'].setReadOnly(True)
        self.edits['status'].setFixedWidth(50)  # set a smaller default width

        self.layouts['top'] = QHBoxLayout()
        for widget in ['cycle', 'status']:
            self.layouts['top'].addWidget(self.labels[widget])
            self.layouts['top'].addWidget(self.edits[widget])

    def create_start_button(self):
        """
        Crée le bouton de démarrage/arrêt des cycles.
        """
        self.start_button = QPushButton(self.parent.translator.translate('start'), self)
        self.start_button.clicked.connect(self.on_start_button)
        self.start_button.setEnabled(False)  # initially disabled until a CSV file name is defined

    def create_max_min_widgets(self):
        """
        Crée les widgets pour les valeurs maximales et minimales.
        """
        for label in ['max', 'min']:
            self.labels[label] = QLabel(self.parent.translator.translate(label), self)
            self.edits[label] = QSpinBox(self)
            self.edits[label].setRange(0, 100)
            self.layouts[label] = QHBoxLayout()
            self.layouts[label].addWidget(self.labels[label])
            self.layouts[label].addWidget(self.edits[label])
            self.layouts[label].addStretch()
        self.edits['max'].setValue(5)  # set a default value for the maximum
        self.layouts['max_min'] = QVBoxLayout()
        for layout in ['max', 'min']:
            self.layouts['max_min'].addLayout(self.layouts[layout])

    def create_graph(self):
        """
        Crée le graphique et les labels de valeurs associées.
        """
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax1 = self.figure.add_subplot(211)  # the first subplot for the ascent times
        self.ax1.set_title(self.parent.translator.translate('time', state=self.state_up_key))
        self.ax2 = self.figure.add_subplot(212)  # the second subplot for the descent times
        self.ax2.set_title(self.parent.translator.translate('time', state=self.state_down_key))
        self.figure.subplots_adjust(hspace=0.5)  # adjust vertical spacing between subplots
        self.toolbar = NavigationToolbar2QT(self.canvas, self)


        self.layouts['graph'] = QVBoxLayout()
        self.layouts['graph'].addWidget(self.toolbar)
        self.layouts['graph'].addWidget(self.canvas)
        
        self.layouts['values'] = QVBoxLayout()
        self.layouts['values'].addStretch(2)  # add stretch before the labels

        # Create min_val, max_val, and avg_val labels for both graphs
        for label in ['min_val', 'max_val', 'avg_val', 'last_val']:
            self.labels[label + '_ascent'] = QLabel(self.parent.translator.translate(label, state=self.state_up_key, value=0), self)
            self.labels[label + '_ascent'].setFixedWidth(200)  # set a fixed width for the label
            self.layouts['values'].addWidget(self.labels[label + '_ascent'])
        self.layouts['values'].addStretch(2)  # add stretch before the labels

        for label in ['min_val', 'max_val', 'avg_val', 'last_val']:
            self.labels[label + '_descent'] = QLabel(self.parent.translator.translate(label, state=self.state_down_key, value=0), self)
            self.labels[label + '_descent'].setFixedWidth(200)  # set a fixed width for the label
            self.layouts['values'].addWidget(self.labels[label + '_descent'])
        self.layouts['values'].addStretch(1)  # add stretch after the labels
                
        self.values_widget = QWidget()  # create a new widget for the values
        self.values_widget.setLayout(self.layouts['values'])  # set the layout of the widget
        self.values_widget.setFixedWidth(self.values_widget.sizeHint().width())  # set the widget to its preferred width


    def create_pn_sn_widgets(self):
        """
        Crée les widgets pour entrer le PN, le SN et le nom du fichier CSV.
        """
        for label in ['PN', 'SN']:
            self.labels[label] = QLabel(self.parent.translator.translate(label), self)
            self.edits[label] = QLineEdit(self)
            self.edits[label].setMaximumWidth(400)  # set a maximum width
            self.edits[label].textChanged.connect(self.update_csv_file)
            self.layouts[label] = QHBoxLayout()
            self.layouts[label].addWidget(self.labels[label])
            self.layouts[label].addWidget(self.edits[label])
            self.layouts[label].addStretch()

        self.labels['CSV File'] = QLabel(self.parent.translator.translate('CSV File'), self)
        self.edits['CSV File'] = QLineEdit(self)
        self.edits['CSV File'].setReadOnly(True)
        self.edits['CSV File'].setMaximumWidth(400)  # set a maximum width
        self.layouts['CSV'] = QHBoxLayout()
        self.layouts['CSV'].addWidget(self.labels['CSV File'])
        self.layouts['CSV'].addWidget(self.edits['CSV File'])
        self.layouts['CSV'].addStretch()
        self.layouts['pn_sn'] = QVBoxLayout()
        for layout in ['PN', 'SN', 'CSV']:
            self.layouts['pn_sn'].addLayout(self.layouts[layout])

    def create_main_layout(self):
        """
        Crée la mise en page principale de la fenêtre.
        """
        self.widget = QWidget()
        self.layouts['main'] = QVBoxLayout(self.widget)

        self.layouts['upper'] = QHBoxLayout()
        self.layouts['main'].addLayout(self.layouts['upper'])

        self.layouts['left'] = QVBoxLayout()
        self.layouts['upper'].addLayout(self.layouts['left'])

        self.layouts['left'].addLayout(self.layouts['top'])
        self.layouts['left'].addWidget(self.start_button)
        self.layouts['left'].addLayout(self.layouts['max_min'])

        self.layouts['right'] = QHBoxLayout()
        self.layouts['upper'].addLayout(self.layouts['right'])

        self.layouts['right'].addLayout(self.layouts['graph'])
        self.layouts['right'].addWidget(self.values_widget)

        self.layouts['upper'].setStretch(0, 0)  # make the left part keep its minimum size
        self.layouts['upper'].setStretch(1, 1)  # make the right part (graph) stretch
        self.layouts['upper'].setStretch(2, 0)  # make the right part (graph) stretch
        self.layouts['right'].addStretch(100)  # add stretch after the graph

        self.layouts['main'].addLayout(self.layouts['pn_sn'])


    def change_widget_state(self,state):
        """
        Active ou désactive certains widgets en fonction de l'état spécifié.

        Args:
            state: État pour activer ou désactiver les widgets.
        """
        self.edits['PN'].setEnabled(state)
        self.edits['SN'].setEnabled(state)
        self.edits['cycle'].setEnabled(state)
        self.edits['max'].setEnabled(state)
        self.edits['min'].setEnabled(state)

    def on_start_button(self):
        """
        Gère l'événement de clic sur le bouton de démarrage/arrêt des cycles.
        """
        if self.is_running:
            Logger.info("Stopping the cycles")
            self.stop_cycle()
            self.edits['status'].setText('stopped')  # update status to show that the cycles are stopped
            self.change_widget_state(True)
            
        else:
            Logger.info(f"Starting the cycles with {self.edits['cycle'].value()} cycles, filename: {self.edits['CSV File'].text()}")
            self.cycle_count = 0  # initialize cycle counter
            self.starting_time = QDateTime.currentMSecsSinceEpoch()  # initialize starting time
            self.time_data = []
            self.component_state = []
            self.cycle_durations = []
            self.start_button.setText(self.parent.translator.translate('stop'))
            self.edits['status'].setText('home')
            self.is_running = True  # set is_running to True to start the pre_start_cycle loop
            self.pre_start_cycle()
            self.change_widget_state(False)
                    
    def pre_start_cycle(self):
        """
        Prépare le cycle en activant le composant et en attendant qu'il soit dans la position souhaitée par défaut.
        """
        self.activate_component()
        if not self.is_sensor_reached():  # wait that the component is down
            if self.is_running:  # check if the cycles are running
                QTimer.singleShot(100, self.pre_start_cycle)
        else:
            QTimer.singleShot(100, self.start_cycle)

    def start_cycle(self):
        """
        Démarre un cycle en activant le composant et en commençant à vérifier le capteur.
        """
        self.deactivate_component()  # activate component
        self.component_state.append(0)
        self.sensor_check_start_time = QDateTime.currentMSecsSinceEpoch()/1000 # initialize sensor check start time
        self.sensor_check_timer.start(25)  # start checking the sensor every 25 ms


    def stop_cycle(self):
        """
        Arrête les cycles en cours.
        """
        if self.timer.isActive():
            self.timer.stop()
        if self.sensor_check_timer.isActive():
            self.sensor_check_timer.stop()
        self.start_button.setText(self.parent.translator.translate('start'))
        self.is_running = False


    def on_timer(self):
        """
        Gère l'événement de fin du minuteur de 15 secondes.
        """
        # This method is called when the 15-second timer expires
        self.timer.stop()  # stop the timer
        self.sensor_check_timer.stop()  # stop checking the sensor
        self.start_button.setText(self.parent.translator.translate('start'))
        self.edits['status'].setText('error')  # update status to show that the sensor was not reached

        

    def check_sensor(self):
        """
        Vérifie périodiquement si le capteur a été atteint.
        """
        # This method is called every 25 ms to check the sensor
        if self.is_sensor_reached():
            self.sensor_check_timer.stop()  # stop checking the sensor
            self.timer.stop()  # stop the 15-second timer

            # Record the time the sensor was reached
            sensor_reached_time = QDateTime.currentMSecsSinceEpoch()/1000
            self.time_data.append(sensor_reached_time - self.sensor_check_start_time)  # record the time in seconds

            # Calculate cycle duration
            cycle_duration = sensor_reached_time - self.sensor_check_start_time
            self.cycle_durations.append(cycle_duration)

            # Add corresponding component state
            if self.component_state[-1] == 1:  # if the component is up
                self.component_state.append(0)
                self.deactivate_component()
                QTimer.singleShot(self.tempo_low * 1000, self.start_sensor_check)  # wait for tempo_low seconds before starting sensor check

            else:  # if the component is down
                self.component_state.append(1)
                self.activate_component()
                self.cycle_count += 1  # increment cycle counter only after a complete ascent and descent
                QTimer.singleShot(self.tempo_high * 1000, self.start_sensor_check)  # wait for tempo_high seconds before starting sensor check

            self.update_graph_and_labels()

            if self.cycle_count > self.edits['cycle'].value():
                self.finish_cycles()
            else:
                self.timer.start(15000)  # start a timer to stop the cycle if it takes more than 15 seconds
                self.edits['status'].setText(f'{self.cycle_count}')


    def start_sensor_check(self):
        """
        Démarre la vérification du capteur pour le prochain cycle.
        """
        if self.cycle_count <= self.edits['cycle'].value():
            self.sensor_check_start_time = QDateTime.currentMSecsSinceEpoch()/1000 # reset sensor check start time
            self.sensor_check_timer.start(25)  # start checking the sensor every 25 ms
            self.timer.start(15000)  # start a timer to stop the cycle if it takes more than 15 seconds



    def update_graph_and_labels(self):
        """
        Met à jour le graphique et les labels de valeurs affichées.
        """
        # Update the graphs
        self.ax1.clear()
        self.ax2.clear()
        self.ax1.set_title(self.parent.translator.translate('time', state=self.state_up_key))  # reset title after clearing
        self.ax2.set_title(self.parent.translator.translate('time', state=self.state_down_key))  # reset title after clearing
        self.ax1.step([i for i in range(len(self.cycle_durations[::2])+1)], [0]+[duration for duration in self.cycle_durations[::2]])  # plot ascent times in seconds
        self.ax1.axhline(y=self.edits['max'].value(), color='r', linestyle='--')
        self.ax1.axhline(y=self.edits['min'].value(), color='r', linestyle='--')
        self.ax2.step([i for i in range(len(self.cycle_durations[1::2])+1)], [0]+[duration for duration in self.cycle_durations[1::2]])  # plot descent times in seconds
        self.ax2.axhline(y=self.edits['max'].value(), color='r', linestyle='--')
        self.ax2.axhline(y=self.edits['min'].value(), color='r', linestyle='--')

        if self.cycle_durations[::2]:  # check if the list of ascent durations is not empty
            self.labels['min_val_ascent'].setText(self.parent.translator.translate('min_val', state=self.state_up_key, value=f'{min(self.cycle_durations[::2]):.2f}'))
            self.labels['max_val_ascent'].setText(self.parent.translator.translate('max_val', state=self.state_up_key, value=f'{max(self.cycle_durations[::2]):.2f}'))
            self.labels['avg_val_ascent'].setText(self.parent.translator.translate('avg_val', state=self.state_up_key, value=f'{sum(self.cycle_durations[::2]) / len(self.cycle_durations[::2]):.2f}'))
            self.labels['last_val_ascent'].setText(self.parent.translator.translate('last_val', state=self.state_up_key, value=f'{self.cycle_durations[::2][-1]:.2f}'))
        if self.cycle_durations[1::2]:  # check if the list of descent durations is not empty
            self.labels['min_val_descent'].setText(self.parent.translator.translate('min_val', state=self.state_down_key, value=f'{min(self.cycle_durations[1::2]):.2f}'))
            self.labels['max_val_descent'].setText(self.parent.translator.translate('max_val', state=self.state_down_key, value=f'{max(self.cycle_durations[1::2]):.2f}'))
            self.labels['avg_val_descent'].setText(self.parent.translator.translate('avg_val', state=self.state_down_key, value=f'{sum(self.cycle_durations[1::2]) / len(self.cycle_durations[1::2]):.2f}'))
            self.labels['last_val_descent'].setText(self.parent.translator.translate('last_val', state=self.state_down_key, value=f'{self.cycle_durations[1::2][-1]:.2f}'))

        self.canvas.draw()

    def finish_cycles(self):
        """
        Termine les cycles en enregistrant les données et en réinitialisant les valeurs.
        """
        # If the requested number of cycles is reached, stop everything
        self.start_button.setText(self.parent.translator.translate('start'))
        self.save_to_csv(self.cycle_durations)
        self.deactivate_component()  # deactivate component
        self.change_widget_state(True)
        self.edits['status'].setText('finished')  # update status to show that the cycles are finished
        Logger.info("Cycles finished and saved to CSV file")
        self.sensor_check_timer.stop()  # stop checking the sensor
        self.timer.stop()  # stop the 15-second timer

    def activate_component(self):
        """
        Active le composant (le fait monter).
        """
        self.parent.update_DO(True)

    def deactivate_component(self):
        """
        Désactive le composant (le fait descendre).
        """
        self.parent.update_DO(False)


    def is_sensor_reached(self):
        """
        Vérifie si le capteur a été atteint.

        Returns:
            bool: True si le capteur est atteint, False sinon.
        """
        if self.parent.serial_reader.busy == False:

            self.parent.serial_reader.busy = True # tell to serial_reader that it will be busy for some time
            self.parent.serial_reader.send_data(1,self.parent.cmd.Port)
            data = self.parent.serial_reader.wait_and_read_data(1)
            self.parent.serial_reader.busy = False # free the serial reader
            if len(self.component_state) == 0 or self.component_state[-1] == 1:  # if the component is up
                return not (data[0] & self.parent.cmd.Down)
            else:  # if the component is down
                return not (data[0] & self.parent.cmd.Up)
        else:
            return False

        
    def update_csv_file(self):
        """
        Met à jour le nom du fichier CSV en fonction des entrées PN et SN.
        """
        pn = self.edits['PN'].text()
        sn = self.edits['SN'].text()
        if pn and sn:
            date = QDate.currentDate().toString("yyyy-MM-dd")
            filename = f"{pn}-{sn}-{date}.csv"
            self.edits['CSV File'].setText(filename)
            self.start_button.setEnabled(True)
        else:
            self.edits['CSV File'].clear()
            self.start_button.setEnabled(False)

    def save_to_csv(self, cycle_durations):
        """
        Enregistre les durées des cycles dans un fichier CSV.

        Args:
            cycle_durations: Liste des durées des cycles.
        """
        filename = self.edits['CSV File'].text()
        path = f"data/{self.parent.key}/{filename}"

        #create data folder if it doesn't exist
        os.makedirs("data",exist_ok= True)
        os.makedirs(f"data/{self.parent.key}",exist_ok= True)


        with open(path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Cycle Number', 'Ascent Time', 'Descent Time'])
            ascent_times = cycle_durations[1::2]
            descent_times = cycle_durations[::2]
            for i in range(len(ascent_times)):
                writer.writerow([i + 1, round(ascent_times[i],3), round(descent_times[i],3)])

    def closeEvent(self, event):
        """
        Gère l'événement de fermeture de la fenêtre.
        """
        self.stop_cycle()
        event.accept()
