from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QSpinBox
from PyQt5.QtCore import QTimer, QDate, Qt, QTime,QDateTime
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT
from matplotlib.figure import Figure
import csv
import os
import random
from time import sleep

from internal.logger import Logger

class GraphWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

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
        self.resize(800, 600)


    def create_top_widgets(self):
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
        self.start_button = QPushButton(self.parent.translator.translate('start'), self)
        self.start_button.clicked.connect(self.on_start_button)
        self.start_button.setEnabled(False)  # initially disabled until a CSV file name is defined

    def create_max_min_widgets(self):
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
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax1 = self.figure.add_subplot(211)  # the first subplot for the ascent times
        self.ax1.set_title(self.parent.translator.translate('ascent_time'))
        self.ax2 = self.figure.add_subplot(212)  # the second subplot for the descent times
        self.ax2.set_title(self.parent.translator.translate('descent_time'))
        self.figure.subplots_adjust(hspace=0.5)  # adjust vertical spacing between subplots
        self.toolbar = NavigationToolbar2QT(self.canvas, self)


        self.layouts['graph'] = QVBoxLayout()
        self.layouts['graph'].addWidget(self.toolbar)
        self.layouts['graph'].addWidget(self.canvas)
        
        self.layouts['values'] = QVBoxLayout()
        self.layouts['values'].addStretch(2)  # add stretch before the labels

        # Create min_val, max_val, and avg_val labels for both graphs
        for label in ['min_val_ascent', 'max_val_ascent', 'avg_val_ascent','last_val_ascent']:
            self.labels[label] = QLabel(self.parent.translator.translate(label, value = 0), self)
            self.labels[label].setFixedWidth(200)  # set a fixed width for the label
            self.layouts['values'].addWidget(self.labels[label])
        self.layouts['values'].addStretch(2)  # add stretch before the labels

        for label in ['min_val_descent', 'max_val_descent', 'avg_val_descent','last_val_descent']:
            self.labels[label] = QLabel(self.parent.translator.translate(label, value = 0), self)
            self.labels[label].setFixedWidth(200)  # set a fixed width for the label
            self.layouts['values'].addWidget(self.labels[label])
        self.layouts['values'].addStretch(1)  # add stretch after the labels
        



        self.values_widget = QWidget()  # create a new widget for the values
        self.values_widget.setLayout(self.layouts['values'])  # set the layout of the widget
        self.values_widget.setFixedWidth(self.values_widget.sizeHint().width())  # set the widget to its preferred width


    def create_pn_sn_widgets(self):
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
        self.edits['PN'].setEnabled(state)
        self.edits['SN'].setEnabled(state)
        self.edits['cycle'].setEnabled(state)
        self.edits['max'].setEnabled(state)
        self.edits['min'].setEnabled(state)

    def on_start_button(self):
        if self.is_running:
            Logger.info("Stopping the cycles")
            self.stop_cycle()
            self.edits['status'].setText('stopped')  # update status to show that the cycles are stopped
            self.change_widget_state(True)
            
        else:
            Logger.info(f"Starting the cycles with {self.edits['cycle'].value()} cycles, filename: {self.edits['CSV File'].text()}")
            self.cycle_count = 1  # initialize cycle counter
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
        self.activate_component()
        if not self.is_sensor_reached():  # wait that the component is down
            if self.is_running:  # check if the cycles are running
                QTimer.singleShot(100, self.pre_start_cycle)
        else:
            QTimer.singleShot(100, self.start_cycle)

    def stop_cycle(self):
        if self.timer.isActive():
            self.timer.stop()
        if self.sensor_check_timer.isActive():
            self.sensor_check_timer.stop()
        self.start_button.setText(self.parent.translator.translate('start'))
        self.is_running = False


    def start_cycle(self):
        # Start a cycle
        self.deactivate_component()  # activate component
        self.component_state.append(0)
        # Record the start time of the cycle
        start_time = QDateTime.currentMSecsSinceEpoch()/1000
        self.time_data.append(start_time)

        self.sensor_check_start_time = start_time # initialize sensor check start time
        self.sensor_check_timer.start(25)  # start checking the sensor every 25 ms
        self.timer.start(15000)  # start a timer to stop the cycle if it takes more than 15 seconds


    def on_timer(self):
        # This method is called when the 15-second timer expires
        self.timer.stop()  # stop the timer
        self.sensor_check_timer.stop()  # stop checking the sensor
        self.start_button.setText(self.parent.translator.translate('start'))
        self.edits['status'].setText('error')  # update status to show that the sensor was not reached

    def check_sensor(self):
        # This method is called every 25 ms to check the sensor
        if self.is_sensor_reached():
            self.sensor_check_timer.stop()  # stop checking the sensor
            self.timer.stop()  # stop the 15-second timer

            # Record the time the sensor was reached
            sensor_reached_time = QDateTime.currentMSecsSinceEpoch()/1000
            self.time_data.append(sensor_reached_time)  # record the time in seconds

            # Calculate cycle duration
            cycle_duration = sensor_reached_time - self.time_data[-2]
            self.cycle_durations.append(cycle_duration)

            # Add corresponding component state
            if self.component_state[-1] == 1:  # if the component is up
                self.component_state.append(0)
                self.deactivate_component()
                self.sensor_check_timer.start(25)

            else:  # if the component is down
                self.component_state.append(1)
                self.activate_component()
                self.cycle_count += 1  # increment cycle counter only after a complete ascent and descent

            if self.cycle_count > self.edits['cycle'].value():
                # If the requested number of cycles is reached, stop everything
                self.start_button.setText(self.parent.translator.translate('start'))
                self.save_to_csv(self.cycle_durations)
                self.deactivate_component()  # deactivate component
                self.change_widget_state(True)
                self.edits['status'].setText('finished')  # update status to show that the cycles are finished
                Logger.info("Cycles finished and saved to CSV file")
            else:
                # If more cycles are needed, start another cycle
                self.sensor_check_timer.start(25)  # start checking the sensor every 25 ms
                self.timer.start(15000)  # start a timer to stop the cycle if it takes more than 15 seconds

            # Update the graphs
            self.ax1.clear()
            self.ax2.clear()
            self.ax1.set_title(self.parent.translator.translate('ascent_time'))  # reset title after clearing
            self.ax2.set_title(self.parent.translator.translate('descent_time'))  # reset title after clearing
            self.ax1.step([i for i in range(len(self.cycle_durations[::2])+1)], [0]+[duration for duration in self.cycle_durations[::2]])  # plot ascent times in seconds
            self.ax1.axhline(y=self.edits['max'].value(), color='r', linestyle='--')
            self.ax1.axhline(y=self.edits['min'].value(), color='r', linestyle='--')
            self.ax2.step([i for i in range(len(self.cycle_durations[1::2])+1)], [0]+[duration for duration in self.cycle_durations[1::2]])  # plot descent times in seconds
            self.ax2.axhline(y=self.edits['max'].value(), color='r', linestyle='--')
            self.ax2.axhline(y=self.edits['min'].value(), color='r', linestyle='--')

            if self.cycle_durations[::2]:  # check if the list of ascent durations is not empty
                self.labels['min_val_ascent'].setText(self.parent.translator.translate('min_val_ascent', value=f'{min(self.cycle_durations[::2]):.2f}'))
                self.labels['max_val_ascent'].setText(self.parent.translator.translate('max_val_ascent', value=f'{max(self.cycle_durations[::2]):.2f}'))
                self.labels['avg_val_ascent'].setText(self.parent.translator.translate('avg_val_ascent', value=f'{sum(self.cycle_durations[::2]) / len(self.cycle_durations[::2]):.2f}'))
                self.labels['last_val_ascent'].setText(self.parent.translator.translate('last_val_ascent', value=f'{self.cycle_durations[::2][-1]:.2f}'))
            if self.cycle_durations[1::2]:  # check if the list of descent durations is not empty
                self.labels['min_val_descent'].setText(self.parent.translator.translate('min_val_descent', value=f'{min(self.cycle_durations[1::2]):.2f}'))
                self.labels['max_val_descent'].setText(self.parent.translator.translate('max_val_descent', value=f'{max(self.cycle_durations[1::2]):.2f}'))
                self.labels['avg_val_descent'].setText(self.parent.translator.translate('avg_val_descent', value=f'{sum(self.cycle_durations[1::2]) / len(self.cycle_durations[1::2]):.2f}'))
                self.labels['last_val_descent'].setText(self.parent.translator.translate('last_val_descent', value=f'{self.cycle_durations[1::2][-1]:.2f}'))
            
            self.canvas.draw()

        else:
            # If the sensor is not reached yet, update the status
            self.edits['status'].setText(f'{self.cycle_count}')



    def activate_component(self): #set to up
        self.parent.update_DO(True)

    def deactivate_component(self): #set to down
        self.parent.update_DO(False)


    def is_sensor_reached(self):
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
        filename = self.edits['CSV File'].text()
        path = "data/" + filename

        #create data folder if it doesn't exist
        if not os.path.exists("data"):
            os.makedirs("data")

        with open(path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Cycle Number', 'Ascent Time', 'Descent Time'])
            ascent_times = cycle_durations[::2]
            descent_times = cycle_durations[1::2]
            for i in range(len(ascent_times)):
                writer.writerow([i + 1, round(ascent_times[i],3), round(descent_times[i],3)])

    def closeEvent(self, event):
        self.stop_cycle()
        event.accept()
