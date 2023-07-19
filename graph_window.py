from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QSpinBox
from PyQt5.QtCore import QTimer, QDate, Qt, QTime,QDateTime
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT
from matplotlib.figure import Figure
import csv
import os
import random
from time import sleep

class GraphWindow(QMainWindow):
    def __init__(self, translator):
        super().__init__()

        self.translator = translator

        # Initialize widget dictionaries
        self.labels = {}
        self.edits = {}
        self.layouts = {}

        # Initialize timers
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer)
        self.sensor_check_timer = QTimer()
        self.sensor_check_timer.timeout.connect(self.check_sensor)


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

        self.setCentralWidget(self.widget)

        self.setMinimumSize(750, 500)
        self.setMaximumSize(1000, 700)

        base_path = os.environ.get('_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        self.setWindowIcon(QIcon(base_path + "\\images\\xfab.jpg"))
        self.resize(800, 600)


    def create_top_widgets(self):
        self.labels['cycle'] = QLabel(self.translator.translate('cycles'), self)
        self.edits['cycle'] = QSpinBox(self)
        self.edits['cycle'].setRange(0, 100)

        self.labels['status'] = QLabel(self.translator.translate('status'), self)
        self.edits['status'] = QLineEdit(self)
        self.edits['status'].setReadOnly(True)
        self.edits['status'].setFixedWidth(50)  # set a smaller default width

        self.layouts['top'] = QHBoxLayout()
        for widget in ['cycle', 'status']:
            self.layouts['top'].addWidget(self.labels[widget])
            self.layouts['top'].addWidget(self.edits[widget])

    def create_start_button(self):
        self.start_button = QPushButton(self.translator.translate('start'), self)
        self.start_button.clicked.connect(self.on_start_button)
        self.start_button.setEnabled(False)  # initially disabled until a CSV file name is defined

    def create_max_min_widgets(self):
        for label in ['max', 'min']:
            self.labels[label] = QLabel(self.translator.translate(label), self)
            self.edits[label] = QSpinBox(self)
            self.edits[label].setRange(0, 100)
            self.layouts[label] = QHBoxLayout()
            self.layouts[label].addWidget(self.labels[label])
            self.layouts[label].addWidget(self.edits[label])
            self.layouts[label].addStretch()
        self.layouts['max_min'] = QVBoxLayout()
        for layout in ['max', 'min']:
            self.layouts['max_min'].addLayout(self.layouts[layout])

    def create_graph(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        # self.canvas.setFixedHeight(300)  # adjust as needed
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title(self.translator.translate('time'))
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        self.labels['min_val'] = QLabel(self.translator.translate('min_val'), self)
        self.labels['min_val'].setFixedWidth(100)  # set a fixed width for the label
        self.labels['max_val'] = QLabel(self.translator.translate('max_val'), self)
        self.labels['max_val'].setFixedWidth(100)  # set a fixed width for the label
        self.labels['avg_val'] = QLabel(self.translator.translate('avg_val'), self)
        self.labels['avg_val'].setFixedWidth(100)  # set a fixed width for the label

        self.layouts['graph'] = QVBoxLayout()
        self.layouts['graph'].addWidget(self.toolbar)
        self.layouts['graph'].addWidget(self.canvas)
        
        self.layouts['values'] = QVBoxLayout()
        self.layouts['values'].addStretch()  # add stretch before the labels
        for label in ['min_val', 'max_val', 'avg_val']:
            self.layouts['values'].addWidget(self.labels[label])
        self.layouts['values'].addStretch()  # add stretch after the labels
        self.values_widget = QWidget()  # create a new widget for the values
        self.values_widget.setLayout(self.layouts['values'])  # set the layout of the widget
        self.values_widget.setFixedWidth(self.values_widget.sizeHint().width())  # set the widget to its preferred width



    def create_pn_sn_widgets(self):
        for label in ['PN', 'SN']:
            self.labels[label] = QLabel(self.translator.translate(label), self)
            self.edits[label] = QLineEdit(self)
            self.edits[label].setMaximumWidth(400)  # set a maximum width
            self.edits[label].textChanged.connect(self.update_csv_file)
            self.layouts[label] = QHBoxLayout()
            self.layouts[label].addWidget(self.labels[label])
            self.layouts[label].addWidget(self.edits[label])
            self.layouts[label].addStretch()

        self.labels['CSV File'] = QLabel(self.translator.translate('CSV File'), self)
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

    def on_start_button(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_button.setText(self.translator.translate('start'))
        else:
            self.cycle_count = 0  # initialize cycle counter
            self.starting_time = QDateTime.currentMSecsSinceEpoch() # initialize starting time
            self.time_data = []
            self.component_state = []
            self.start_cycle()
            
    def start_cycle(self):
        # Start a cycle
        self.activate_component()  # activate component
        self.component_state.append(1)  # record that the component is up

        # Record the start time of the cycle
        start_time = (QDateTime.currentMSecsSinceEpoch() - self.starting_time) / 1000.0
        self.time_data.append(start_time)

        self.sensor_check_start_time = QDateTime.currentMSecsSinceEpoch() # initialize sensor check start time
        self.sensor_check_timer.start(10)  # start checking the sensor every 10 ms
        self.start_button.setText(self.translator.translate('stop'))
        self.timer.start(15000)  # start a timer to stop the cycle if it takes more than 15 seconds


    def on_timer(self):
        # This method is called when the 15-second timer expires
        self.timer.stop()  # stop the timer
        self.sensor_check_timer.stop()  # stop checking the sensor
        self.start_button.setText(self.translator.translate('start'))
        self.edits['status'].setText('Error: Sensor not reached in 15 seconds')

    def check_sensor(self):
        # This method is called every 10 ms to check the sensor
        if self.is_sensor_reached():
            self.sensor_check_timer.stop()  # stop checking the sensor
            self.timer.stop()  # stop the 15-second timer

            # Set component state to down
            self.component_state.append(0)  # record that the component is down

            # Record the time the sensor was reached
            sensor_reached_time = (QDateTime.currentMSecsSinceEpoch() - self.starting_time) / 1000.0
            self.time_data.append(sensor_reached_time)

            self.cycle_count += 1  # increment cycle counter

            if self.cycle_count >= self.edits['cycle'].value():
                # If the requested number of cycles is reached, stop everything
                self.start_button.setText(self.translator.translate('start'))
                self.save_to_csv(self.time_data, self.component_state)  # save the data to CSV

            else:
                # If more cycles are needed, start another cycle
                self.start_cycle()

            # Update the graph
            self.ax.clear()
            self.ax.step(self.time_data, self.component_state)
            self.canvas.draw()

        else:
            # If the sensor is not reached yet, update the status
            self.edits['status'].setText('Waiting for sensor')



    def activate_component(self):
        # This is a placeholder for the function that activates a component
        print('Component activated')
        return True

    def deactivate_component(self):
        # This is a placeholder for the function that deactivates a component
        print('Component deactivated')


    def is_sensor_reached(self):
        # This is a placeholder for the function that checks if a sensor is reached
        # Here, it simulates a sensor that is randomly reached with a probability of 0.1
        # print('Checking sensor')
        sleep(0.01)
        return random.random() > 0.9

    def update_csv_file(self):
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

    def save_to_csv(self, time_data, component_state):
        filename = self.edits['CSV File'].text()
        path = "data/" + filename
        
        #create data folder if it doesn't exist
        if not os.path.exists("data"):
            os.makedirs("data")

        with open(path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Time', 'Component State'])
        with open(path, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            for i in range(len(time_data)):
                writer.writerow([time_data[i], component_state[i]])