from serial import Serial, SerialException
from serial.tools.list_ports import comports
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, QObject, QTimer

from internal.logger import Logger
from internal.constant import *
from internal.rs485 import RS485

import struct
import time

class SerialReader(QObject):
    error_occurred = pyqtSignal(str) 

    def __init__(self, parent):
        """
        Constructeur de la classe SerialReader.

        Args:
            parent: Objet parent.
        """
        super().__init__()
        self.ser = None
        self.translator = parent.translator
        self.error_occurred.connect(parent.show_error_message)

        self.busy = False 
        self.set_com_port(self.get_available_com_ports()[0] if self.get_available_com_ports() else None)


    def get_available_com_ports(self):
        """
        Obtient la liste des ports COM disponibles.

        Returns:
            List[str]: Liste des ports COM disponibles.
        """
        return [port.device for port in comports()]

    def set_com_port(self, port):
        """
        Définit le port COM à utiliser.

        Args:
            port (str): Port COM à utiliser.
        """
        if port is not None:
            if self.ser is not None and self.ser.port == port:
                return
            try:
                self.ser = Serial(port=port, baudrate=115200, timeout=0.3)
            except SerialException:
                Logger.error(f"Error while connecting to serial port {port}.")
        else:
            Logger.warning("No COM port selected.")
            QMessageBox.warning(None, self.translator.translate("warning"), self.translator.translate("no_com_port"))



    def float_to_bytes(self, f):
        """
        Convertit un nombre flottant en bytes au format little-endian.

        Args:
            f (float): Nombre flottant à convertir.

        Returns:
            bytes: Valeur convertie en bytes.
        """
        # Convertir le float en bytes en little-endian
        return struct.pack('<f', f)
    
    def send_data(self, type, data, other_data=[]):
        """
        Envoie des données via le port série.

        Args:
            type (int): Type de données à envoyer.
            data: Données à envoyer.
            other_data (list): Autres données à envoyer.
        """
        if self.ser is not None:
            try:
                self.ser.write(bytes([type]))
                if isinstance(data, float):
                    self.ser.write(self.float_to_bytes(data))
                else:
                    self.ser.write(bytes([data]))
                for d in other_data:
                    self.ser.write(bytes(d, 'utf-8'))
            except SerialException:
                Logger.warning(f"Error while sending data to serial port {self.ser.port}.")
                self.error_occurred.emit(self.translator.translate("serial_port_disconnected", port=self.ser.port))
                self.ser = None



    def wait_and_read_data(self, num_values=1, until:bytes="".encode()):
        """
        Attend que des données soient disponibles sur le port série et les lit.

        Args:
            num_values (int): Nombre d'octets à lire depuis le port série.
            until (bytes): Données jusqu'auxquelles lire.

        Returns:
            bytes: Données lues depuis le port série, ou None en cas d'erreur.
        """
        if self.ser is not None:
            try:
                if until == b"":
                    data = self.ser.read(num_values)
                else:
                    data = self.ser.read_until(until)
                self.ser.reset_input_buffer()
                return data
            except SerialException:
                Logger.warning(f"Error while reading data from serial port {self.ser.port}.")
                self.error_occurred.emit(self.translator.translate("serial_port_disconnected", port=self.ser.port))
                self.ser = None
        return None

    def write_data(self, action, state):
        """
        Écrit des données via le port série.

        Args:
            action (int): Action à écrire.
            state (int): État à écrire.
        """
        self.send_data(0, action*2 + state)





class SerialReaderThread(QThread):
    """
    Constructeur de la classe SerialReaderThread.

    Args:
        gui: Interface utilisateur associée.
    """
    def __init__(self, gui):
        super().__init__()
        self.parent = gui
        self.serial_reader = gui.serial_reader
        self.RS485 = gui.RS485
        self.custom_widgets = gui.custom_widgets


    def run(self):
        """
        Démarre le thread de lecture série.
        """
        while True:
            if self.serial_reader.busy == False and self.serial_reader.ser is not None:
                try:
                    #read all DI
                    self.serial_reader.busy = True # tell to serial_reader that it will be busy for some time
                    self.serial_reader.send_data(1,0)
                    data = self.serial_reader.wait_and_read_data(4)
                    # print(data)
                    if data is not None and len(data) == 4:
                        self.custom_widgets["wafer_lift2"].update_DI(data[0] & Cmd.wafer_lift2.Up, data[0] & Cmd.wafer_lift2.Down)
                        self.custom_widgets["wafer_lift3"].update_DI(data[0] & Cmd.wafer_lift3.Up, data[0] & Cmd.wafer_lift3.Down)
                        self.custom_widgets["slit_valve"].update_DI(data[0] & Cmd.slit_valve.Up, data[0] & Cmd.slit_valve.Down)
                        self.custom_widgets["wafer_lift1"].update_DI(data[0] & Cmd.wafer_lift1.Up, data[0] & Cmd.wafer_lift1.Down)
                        
                        self.custom_widgets["roughing_pump"].update_DI(data[2] & 2)
                        self.custom_widgets["turbo_pump_rga"].update_DI(data[1] & 64)
                        self.custom_widgets["turbo_pump_ch"].update_DI(data[1] & 32)

                        self.custom_widgets["turbo_pump_gate"].update_sensors(data[1] & Cmd.RGAGate.Up, data[1] & Cmd.RGAGate.Down)

                        
                        self.custom_widgets["interlock"].update_interlock([data[2] & Cmd.Interlock.RoughingPumpOff,
                                                                            data[2] & Cmd.Interlock.PumpPressureHigh,
                                                                            data[2] & Cmd.Interlock.ChamberOpen,
                                                                            data[2] & Cmd.Interlock.ChamberPressureHigh
                                                                            ])
                        QTimer.singleShot(0, self.parent.update_AI)

                    # read analog inputs 1 (MFC1, MFC2, baratron1, baratron2)
                    self.serial_reader.send_data(6,4)
                    data = None
                    data = self.serial_reader.wait_and_read_data(until='\n'.encode())
                    if data is not None and len(data) > 0:
                        data = data.decode().strip().split(' ')
                        self.custom_widgets["MFC1"].update_AI(data[0])
                        self.custom_widgets["MFC2"].update_AI(data[1])
                        self.custom_widgets["baratron1"].update_AI(data[2])
                        self.custom_widgets["baratron2"].update_AI(data[3])
                        
                    #read analog inputs 2 (generator1 source power, generator1 reflected power, generator2 source power, generator2 reflected power)
                    self.serial_reader.send_data(6,5)
                    data = None
                    data = self.serial_reader.wait_and_read_data(until='\n'.encode())
                    if data is not None and len(data) > 0:
                        data = data.decode().strip().split(' ')
                        self.custom_widgets["generator1"].update_AI(data[0:2])
                        self.custom_widgets["generator2"].update_AI(data[2:4])
                        
                    # read RS485 sensors
                    for key in ["chamber_pressure","pump_pressure"]:
                        data = None
                        data = self.RS485.pirani[key].read_pressure()
                        # print(data)
                        if len(data)==2 or data[0]=='error':
                            self.custom_widgets[key].update_pressure(data)

                except Exception as e:
                    # print("Serial Reader:",e)
                    pass

                self.serial_reader.busy = False # free the serial reader
                self.msleep(1000) # Sleep for 1 second
            else:
                # print("busy")
                self.msleep(50)


