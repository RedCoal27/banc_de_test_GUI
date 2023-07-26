from internal.constant import PiraniConfig
import time

class RS485:
    def __init__(self,parent) -> None:
        self.pirani = {}
        self.pirani["chamber_pressure"] = self.__Pirani__(parent, "chamber_pressure")
        self.pirani["pump_pressure"] = self.__Pirani__(parent, "pump_pressure")

    class __Pirani__:
        Command = {
            "change_address": "!S750 {address}",
            "change_unit" : "!S755 {unit}",
            "change_gas": "!S756 {gas_type}",
            "read_pressure" : "?V790"
        }

        def __init__(self,parent,key) -> None:
            self.parent = parent
            self.serial_reader = parent.serial_reader
            self.key = key
            self.address = self.parent.config[self.key]["address"]


        def command(self,command):
            self.serial_reader.send_data(8,self.address, command + "\n")
            data = self.serial_reader.wait_and_read_data(until='\n')

            return data.decode().strip().split(';')

        def update_address(self):
            while(self.serial_reader.busy_read == True):
                time.sleep(0.01)
            self.serial_reader.busy_read = True

            self.address = self.parent.config[self.key]["address"]
            new_address = f"{0 if(self.address<10) else ''}{self.address}"
            command = self.Command["change_address"].format(address=new_address) + "\n"
            self.serial_reader.send_data(8, 99, command)
            data = self.serial_reader.wait_and_read_data(until='\n')
            print(data)
            self.serial_reader.busy_read = False

        def update_config(self):
            while(self.serial_reader.busy_read == True):
                time.sleep(0.01)
            self.serial_reader.busy_read = True
            config = self.parent.config[self.key]

            unit = PiraniConfig.units_types.index(config["pressure_unit"]) + 1
            gas_type = PiraniConfig.gas_types.index(config["gas_type"])

            self.command(self.Command["change_unit"].format(unit=unit))
            self.command(self.Command["change_gas"].format(gas_type=gas_type))
    
            self.serial_reader.busy_read = False


        def read_pressure(self):
            return self.command(self.Command["read_pressure"])
        
        def read_SN(self):
            return self.command(self.Command["read_SN"])



        




