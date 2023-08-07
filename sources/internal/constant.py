



MCP2_A = 1
MCP2_B = 2
MCP3_A = 3
MCP3_B = 4

class Cmd():
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

    class WL1():
        DO = 10
        Port = MCP2_A #input port
        Up = 64
        Down = 128

    class WL2():
        DO = 9
        Port = MCP2_A #input port
        Up = 16
        Down = 32

    class WL3():
        DO = 8
        Port = MCP2_A #input port
        Up = 4
        Down = 8

    class SV():
        DO = 7
        Port = MCP2_A #input port
        Up = 1
        Down = 2

    class RGAGate():
        DO = 6 #CVD
        Port = MCP2_B #input port
        Up = 4 #Open
        Down = 8 #Close

    class Interlock():
        Port = MCP3_A
        RoughingPumpOff = 2
        PumpPressureHigh = 8
        ChamberOpen = 1
        ChamberPressureHigh = 4


        


class PiraniConfig():
    gas_types = ["N2", "Ar", "He", "CO2", "H", "Ne", "Kr"]
    units_types = ["mBar", "Pascal", "Torr"]

        
