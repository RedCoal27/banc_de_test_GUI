from internal.constant import PiraniConfig
import time

class RS485:
    def __init__(self,parent) -> None:
        """
        Constructeur de la classe RS485.

        Args:
            parent: Objet parent.
        """
        self.pirani = {}
        self.pirani["chamber_pressure"] = self.__Pirani__(parent, "chamber_pressure")
        self.pirani["pump_pressure"] = self.__Pirani__(parent, "pump_pressure")

    class __Pirani__:
        """
        Cette classe gère la communication avec un capteur Pirani via RS485.

        Methods:
            __init__(self, parent, key):
                Constructeur de la classe Pirani.

            command(self, cmd):
                Envoie une commande au capteur Pirani.

            wait_to_send_command(self, cmd):
                Attend que la liaison série soit libre avant d'envoyer une commande au capteur Pirani.

            update_address(self):
                Met à jour l'adresse du capteur Pirani.

            convert_to_exp_format(self, value):
                Convertit une valeur en notation exponentielle.

            update_config(self):
                Met à jour la configuration du capteur Pirani.

            read_pressure(self):
                Lit la pression à partir du capteur Pirani.

            read_SN(self):
                Lit le numéro de série du capteur Pirani.

            calibrate(self):
                Effectue une calibration du capteur Pirani.
        """
        Command = {
            "change_address": "!S750 {address}",
            "read_pressure" : "?V752",
            "change_unit" : "!S755 {unit}",
            "change_gas": "!S756 {gas_type}",
            "read_SN" : "?S790",
            "calibration_atm":"!S761 1;1",
            "setpoint_high":"!S754 0;{pressure}",
            "setpoint_low":"!S754 1;{pressure}"
        }

        def __init__(self,parent,key) -> None:
            """
                Constructeur de la classe Pirani.

            Args:
                parent: Objet parent.
                key: Clé pour accéder à la configuration du capteur Pirani.
            """
            self.parent = parent
            self.serial_reader = parent.serial_reader
            self.key = key
            self.address = self.parent.config[self.key]["address"]


        def command(self,cmd):#envois une commande
            """
                Envoie une commande au capteur Pirani.

            Args:
                cmd: Commande à envoyer.

            Returns:
                Résultat de la commande.
            """
            self.serial_reader.send_data(8,self.address, cmd + "\n")
            data = self.serial_reader.wait_and_read_data(until='\n')
            return data.decode().strip().split(';')

        def wait_to_send_command(self,cmd):
            """
                Attend que la liaison série soit libre avant d'envoyer une commande au capteur Pirani.

            Args:
                cmd: Commande à envoyer.

            Returns:
                Résultat de la commande.
            """
            while(self.serial_reader.busy == True):
                time.sleep(0.01)
            self.serial_reader.busy = True
            data = self.command(cmd)
            self.serial_reader.busy = False
            return data



        def update_address(self):
            """
                Met à jour l'adresse du capteur Pirani.
            """
            while(self.serial_reader.busy == True):
                time.sleep(0.01)
            self.serial_reader.busy = True

            self.address = self.parent.config[self.key]["address"]
            new_address = f"{0 if(self.address<10) else ''}{self.address}"
            command = self.Command["change_address"].format(address=new_address) + "\n"
            self.serial_reader.send_data(8, 99, command)
            data = self.serial_reader.wait_and_read_data(until='\n')
            self.serial_reader.busy = False

        def convert_to_exp_format(self,value):
            """
                Convertit une valeur en notation exponentielle.

            Args:
                value: Valeur à convertir.

            Returns:
                Valeur convertie en notation exponentielle.
            """
            value = "{:.1e}".format(value)
            return value
        

        def update_config(self):
            """
                Met à jour la configuration du capteur Pirani.
            """
            while(self.serial_reader.busy == True):
                time.sleep(0.01)
            self.serial_reader.busy = True
            config = self.parent.config[self.key]

            unit = PiraniConfig.units_types.index(config["pressure_unit"]) + 1
            gas_type = PiraniConfig.gas_types.index(config["gas_type"])


            self.command(self.Command["change_unit"].format(unit=unit))
            self.command(self.Command["change_gas"].format(gas_type=gas_type))

            self.command(self.Command["setpoint_high"].format(pressure=self.convert_to_exp_format(config["setpoint_high"])))
            self.command(self.Command["setpoint_low"].format(pressure=self.convert_to_exp_format(config["setpoint_low"])))

            self.serial_reader.busy = False


        def read_pressure(self):
            """
                Lit la pression à partir du capteur Pirani.

            Returns:
                Résultat de la lecture de la pression.
            """
            return self.command(self.Command["read_pressure"])
        
        def read_SN(self):
            """
                Lit le numéro de série du capteur Pirani.

            Returns:
                Numéro de série du capteur Pirani.
            """
            return self.wait_to_send_command(self.Command["read_SN"])[0]


        def calibrate(self):
            """
                Effectue une calibration du capteur Pirani.
            """
            self.wait_to_send_command(self.Command["calibration_atm"])[0]
