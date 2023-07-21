from serial import Serial, SerialException
from serial.tools.list_ports import comports
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread

from internal.logger import Logger

import time

class SerialReader:
    def __init__(self, translator):
        self.ser = None
        self.translator = translator
        self.set_com_port(self.get_available_com_ports()[0] if self.get_available_com_ports() else None)

    def get_available_com_ports(self):
        return [port.device for port in comports()]

    def set_com_port(self, port):
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



    def send_data(self, type, data):
        if self.ser is not None:
            try:
                self.ser.write(bytes([type]))
                self.ser.write(bytes([data]))
            except SerialException:
                Logger.warning(f"Error while sending data to serial port {self.ser.port}.")
                QMessageBox.warning(None, self.translator.translate("warning"), self.translator.translate("serial_port_disconnected", port=self.ser.port))
                self.ser = None

    def wait_and_read_data(self, num_values=1, until:bytes="".encode()):
        """
        Waits for data to be available on the serial port and reads it.

        Args:
            num_values (int): The number of bytes to read from the serial port.

        Returns:
            bytes: The data read from the serial port, or None if there was an error.
        """
        if self.ser is not None:
            try:
                if until == "":
                    data = self.ser.read(num_values)
                else:
                    data = self.ser.read_until(until)
                self.ser.reset_input_buffer()
                return data
            except SerialException:
                Logger.warning(f"Error while reading data from serial port {self.ser.port}.")
                QMessageBox.warning(None, self.translator.translate("warning"), self.translator.translate("serial_port_disconnected", port=self.ser.port))
                self.ser = None
        return None

    def write_data(self, action, state):
        self.send_data(0, action*2 + state)





class SerialReaderThread(QThread):
    def __init__(self, serial_reader, custom_widgets):
        super().__init__()
        self.serial_reader = serial_reader
        self.custom_widgets = custom_widgets

    def run(self):
        while True:
            self.serial_reader.send_data(1,0)
            data = self.serial_reader.wait_and_read_data(4)
            if data is not None and len(data) == 4:
                self.custom_widgets["WL2"].update_DI(data[0] & 16, data[0] & 32)
                self.custom_widgets["WL3"].update_DI(data[0] & 4, data[0] & 8)
                self.custom_widgets["SV"].update_DI(data[0] & 1, data[0] & 2)
                self.custom_widgets["WL1"].update_DI(data[0] & 64, data[0] & 128)

            self.serial_reader.send_data(6,4)
            data = self.serial_reader.wait_and_read_data(until='\n'.encode())
            if data is not None and len(data) > 0:
                data = data.decode().strip().split(' ')
                self.custom_widgets["MFC1"].update_AI(data[0])
                self.custom_widgets["MFC2"].update_AI(data[1])
                self.custom_widgets["baratron1"].update_AI(data[2])
                self.custom_widgets["baratron2"].update_AI(data[3])
            self.msleep(1000) # Sleep for 1 second
