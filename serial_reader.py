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


    def send_data(self, type, action):
        if self.ser is not None:
            try:
                self.ser.write(bytes([type]))
                self.ser.write(bytes([action]))
            except SerialException:
                QMessageBox.warning(None, self.translator.translate("warning"), self.translator.translate("serial_port_disconnected", port=self.ser.port))
                self.ser = None

    def wait_and_read_data(self, num_values=1):
        if self.ser is not None:
            try:
                data = []
                while len(data) < num_values:
                    if self.ser.in_waiting:
                        data.append(self.ser.readline())
                return data
            except SerialException:
                QMessageBox.warning(None, self.translator.translate("warning"), self.translator.translate("serial_port_disconnected", port=self.ser.port))
                self.ser = None
        return None
