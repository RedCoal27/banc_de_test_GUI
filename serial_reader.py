

from serial import Serial, SerialException
from serial.tools.list_ports import comports
from PyQt5.QtWidgets import QMessageBox

class SerialReader:
    def __init__(self, translator, current_language):
        self.ser = None
        self.translator = translator
        self.current_language = current_language
        self.set_com_port(self.get_available_com_ports()[0] if self.get_available_com_ports() else None)

    def get_available_com_ports(self):
        return [port.device for port in comports()]

    def set_com_port(self, port):
        if port is not None:
            if self.ser is not None and self.ser.port == port:
                return
            try:
                self.ser = Serial(port)
            except SerialException:
                print(self.translator.translate("serial_port_error", self.current_language, port=port))
        else:
            QMessageBox.warning(None, self.translator.translate("warning", self.current_language), self.translator.translate("no_com_port", self.current_language))

    def read(self):
        if self.ser is not None:
            try:
                if self.ser.in_waiting:
                    return self.ser.readline()
            except SerialException:
                QMessageBox.warning(None, self.translator.translate("Warning", self.current_language), self.translator.translate("serial_port_disconnected", self.current_language))
                self.ser = None
        return None

