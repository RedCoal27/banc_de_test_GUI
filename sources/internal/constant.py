MCP2_A = 1
MCP2_B = 2
MCP3_A = 3
MCP3_B = 4

class Cmd():
    nupro_final = 3
    nupro_mfc1 = 1
    nupro_mfc2 = 2
    nupro_vent = 4

    turbo_pump_rga_gate = 16
    turbo_pump_rga_gate_p = 17

    turbo_pump_ch_gate = 5 
    turbo_pump_ch_gate_p = 15

    iso_chamber = 14

    RoughingPump = 26
    TurboRGA = 27
    TurboCH = 28

    MFC1 = 2
    MFC2 = 3

    class WL1():
        DO = 10
        Port = MCP2_A
        Up = 64
        Down = 128

    class WL2():
        DO = 9
        Port = MCP2_A
        Up = 16
        Down = 32

    class WL3():
        DO = 8
        Port = MCP2_A
        Up = 4
        Down = 8

    class SV():
        DO = 7
        Port = MCP2_A
        Up = 1
        Down = 2
    
        


        
