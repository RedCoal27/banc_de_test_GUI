MCP2_A = 1
MCP2_B = 2
MCP3_A = 3
MCP3_B = 4

class Cmd:
    """
    Cette classe contient les constantes pour les commandes utilisées dans le système par l'arduino.
    """
    nupro_final = 3
    nupro_mfc1 = 1
    nupro_mfc2 = 2
    nupro_vent = 4

    iso_rga = 16
    iso_rga_pump = 17

    iso_turbo = 15

    iso_chamber = 14

    RoughingPump = 26
    TurboRGA = 27
    TurboCH = 28

    MFC1 = 2
    MFC2 = 3

    class wafer_lift1:
        """
        Constantes liées à la wafer lift 1.
        """
        DO = 10
        Port = MCP2_A  # Port d'entrée
        Up = 64
        Down = 128

    class wafer_lift2:
        """
        Constantes liées à la wafer lift 2.
        """
        DO = 9
        Port = MCP2_A  # Port d'entrée
        Up = 16
        Down = 32

    class wafer_lift3:
        """
        Constantes liées à la wafer lift 3.
        """
        DO = 8
        Port = MCP2_A  # Port d'entrée
        Up = 4
        Down = 8

    class slit_valve:
        """
        Constantes liées à la slit valve.
        """
        DO = 7
        Port = MCP2_A  # Port d'entrée
        Up = 1
        Down = 2

    class RGAGate:
        """
        Constantes liées à la RGAGate.
        """
        DO = 6  # CVD
        Port = MCP2_B  # Port d'entrée
        Up = 4  # Ouvert
        Down = 8  # Fermé

    class Interlock:
        """
        Constantes liées à l'Interlock.
        """
        Port = MCP3_A
        RoughingPumpOff = 2
        PumpPressureHigh = 8
        ChamberOpen = 1
        ChamberPressureHigh = 4

    class Generator1:
        """
        Constantes liées au Generator 1.
        """
        Enable = 29
        Interlock = 30
        AO = 4

    class Generator2:
        """
        Constantes liées au Generator 2.
        """
        Enable = 31
        Interlock = 32
        AO = 5

    class ThrottleValve:
        """
        Constante lié a la Throttle Valve
        """
        cmd = 9
        set_position = 1
        sensors = 3
        position = 2


class PiraniConfig:
    """
    Cette classe contient les configurations liées au Pirani.
    """
    gas_types = ["N2", "Ar", "He", "CO2", "H", "Ne", "Kr"]
    units_types = ["mBar", "Pascal", "Torr"]
