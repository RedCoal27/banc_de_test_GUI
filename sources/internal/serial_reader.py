from serial import Serial, SerialException
from serial.tools.list_ports import comports
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread,pyqtSignal,QObject

from internal.logger import Logger
from internal.constant import *

import struct
import time

class SerialReader(QObject):
    error_occurred = pyqtSignal(str, str,  str) 

    def __init__(self, translator):
        super().__init__()
        self.ser = None
        self.translator = translator
        self.busy_write = False
        self.busy_read = False
        self.set_com_port(self.get_available_com_ports()[0] if self.get_available_com_ports() else None)



    def get_available_com_ports(self):
        return [port.device for port in comports()]

    def set_com_port(self, port):
        if port is not None:
            if self.ser is not None and self.ser.port == port:
                return
            try:
                self.ser = Serial(port=port, baudrate=115200, timeout=0.5)
            except SerialException:
                Logger.error(f"Error while connecting to serial port {port}.")
        else:
            Logger.warning("No COM port selected.")
            self.error_occurred.emit("warning", "serial_port_disconnected", port)

    def float_to_bytes(self, f):
        # Convertir le float en bytes en little-endian
        return struct.pack('<f', f)
    
    def send_data(self, type, data):
        if self.ser is not None:
            try:
                self.ser.write(bytes([type]))
                if isinstance(data, float):
                    self.ser.write(self.float_to_bytes(data))
                else:
                    self.ser.write(bytes([data]))
            except SerialException:
                Logger.warning(f"Error while sending data to serial port {self.ser.port}.")
                self.error_occurred.emit("warning", "serial_port_disconnected", self.ser.port)
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
                self.error_occurred.emit("warning", "serial_port_disconnected", self.ser.port)
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
            if self.serial_reader.busy_read == False:
                self.serial_reader.busy_read = True # tell to serial_reader that it will be busy for some time
                self.serial_reader.send_data(1,0)
                data = self.serial_reader.wait_and_read_data(4)
                if data is not None and len(data) == 4:
                    self.custom_widgets["WL2"].update_DI(data[0] & Cmd.WL2.Up, data[0] & Cmd.WL2.Down)
                    self.custom_widgets["WL3"].update_DI(data[0] & Cmd.WL3.Up, data[0] & Cmd.WL3.Down)
                    self.custom_widgets["SV"].update_DI(data[0] & Cmd.SV.Up, data[0] & Cmd.SV.Down)
                    self.custom_widgets["WL1"].update_DI(data[0] & Cmd.WL1.Up, data[0] & Cmd.WL1.Down)


                    self.custom_widgets["roughing_pump"].update_DI(data[1] & 128)
                    self.custom_widgets["turbo_pump_rga"].update_DI(data[1] & 64)
                    self.custom_widgets["turbo_pump_ch"].update_DI(data[1] & 32)
                self.serial_reader.send_data(6,4)
                data = self.serial_reader.wait_and_read_data(until='\n'.encode())
                print(data)
                if data is not None and len(data) == 4:
                    self.custom_widgets["MFC1"].update_AI(data[0])
                    self.custom_widgets["MFC2"].update_AI(data[1])
                    self.custom_widgets["baratron1"].update_AI(data[2])
                    self.custom_widgets["baratron2"].update_AI(data[3])
                self.serial_reader.busy_read = False # free the serial reader
                self.msleep(1000) # Sleep for 1 second
            else:
                # print("busy_read")
                self.msleep(50)