

from serial import Serial, SerialException
from serial.tools.list_ports import comports
from PyQt5.QtWidgets import QMessageBox

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
                self.ser = Serial(port)
            except SerialException:
                print(self.translator.translate("serial_port_error", port=port))
        else:
            QMessageBox.warning(None, self.translator.translate("warning"), self.translator.translate("no_com_port"))

    def read(self):
        if self.ser is not None:
            try:
                if self.ser.in_waiting:
                    return self.ser.readline()
            except SerialException:
                QMessageBox.warning(None, self.translator.translate("Warning"), self.translator.translate("serial_port_disconnected"))
                self.ser = None
        return None

