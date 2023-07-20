from serial import Serial, SerialException
from serial.tools.list_ports import comports
from PyQt5.QtWidgets import QMessageBox

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
                self.ser = Serial(port=port, baudrate=9600, timeout=0.2)
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

    def wait_and_read_data(self, num_values=1):
        """
        Waits for data to be available on the serial port and reads it.

        Args:
            num_values (int): The number of bytes to read from the serial port.

        Returns:
            bytes: The data read from the serial port, or None if there was an error.
        """
        if self.ser is not None:
            try:
                data = self.ser.read(num_values)
                self.ser.reset_input_buffer()
                return data
            except SerialException:
                Logger.warning(f"Error while reading data from serial port {self.ser.port}.")
                QMessageBox.warning(None, self.translator.translate("warning"), self.translator.translate("serial_port_disconnected", port=self.ser.port))
                self.ser = None
        return None

    def write_data(self, action, state):
        self.send_data(0, action*2 + state)