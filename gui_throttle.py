#conçu par Maillet Alexandre 2022
# Importing Libraries
import serial
import serial.tools.list_ports
import time
from tkinter import *
from tkinter import filedialog
import numpy as np



arduino = serial.Serial('COM7', baudrate=115200, timeout=0.2)

filePath = ""
Position = -1
HasDoneHome = 0
inOperation = 0
Delta = 0

#selection de fichier
def select_file():
    global filePath
    filePath = filedialog.asksaveasfilename(title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")),defaultextension=".csv")
    #add extension if not present
    if not filePath.endswith('.csv'):
        filePath += '.csv'
    print(filePath)
    filePathEntry.config(state=NORMAL)
    filePathEntry.delete("1.0", "end")
    filePathEntry.insert(END, filePath)
    filePathEntry.config(state=DISABLED)
    callback2()


# test pour le nombre de step pour le bouton "go to"
def callback():
    global stepEntry
    try:
        var = int(stepEntry.get())
        if var >= 0 and var <= 800 and HasDoneHome == 1:
            Buttons[3].config(state=NORMAL)
        else:
            Buttons[3].config(state=DISABLED)
    except ValueError:
        Buttons[3].config(state=DISABLED)

#test pour le bouton start/stop
def callback2():
    global Step
    global Cycle
    try:
        var =int(Step.get())
        var2 = int(Cycle.get())
        if var >= 0 and var <= 800 and var2 > 0 and filePath != "":
            Buttons[4].config(state=NORMAL)
        else:
            Buttons[4].config(state=DISABLED)
    except ValueError:
        Buttons[4].config(state=DISABLED)


#déplacement relatif en step
def relative_move(step):
    arduino.reset_input_buffer()
    arduino.flushInput()
    arduino.write(f"{step}\n".encode('utf-8'))

    while arduino.in_waiting <= 0:
        time.sleep(0.001)

    data = arduino.read_until("\n")
    data = data.decode('utf-8')
    data = data.split("|")
    #transform each string in list to float
    data = [float(i) for i in data]
    print(data)

    global Position
    global TextPosition
    Position = Position + step

    if Position < 0:
        Position = 0
    if Position > 800:
        Position = 800
        

    TextPosition.config(state=NORMAL)
    TextPosition.delete("1.0", "end")
    if data[4] == 1 :  
        TextPosition.insert(END, "Open", "ALIGN")
    elif data[5] == 1 :
        TextPosition.insert(END, "Close", "ALIGN")
    else :
        TextPosition.insert(END, int(Position), "ALIGN")
    
    TextPosition.config(state=DISABLED)

    global mw
    mw.update_idletasks()
    return data


#Lance un homing
def Home():
    global Position
    data = relative_move(100)
    data = relative_move(-1000)

    Position = 0
    while data[5] == 1:
        data = relative_move(1)

    data = relative_move(-1)
    global Delta
    Delta = Position
    print(Position)

#    Position = 0
    global HasDoneHome
    global Buttons
    HasDoneHome = 1
    callback()
    Buttons[1].config(state=NORMAL)
    Buttons[2].config(state=NORMAL)


#lance les mesures
def start_mesure():
    global Position
    relative_move(-800)
    Position = 0
    global Cycle
    global Step
    global mw
    global Buttons
    global inOperation
    inOperation = 1

    for Button in Buttons:
        Button.config(state=DISABLED)
    Buttons[5].config(state=NORMAL)
    try:
        with open(filePath, 'w') as f:
            f.write(f"Cycle; Position; Courant Moteur 1;Courant Moteur 2;Courant Moteur 3;Courant Moteur 4\n")
            for i in range(1,int(Cycle.get())+1):
                for j in np.linspace(0,800,int(Step.get())):
                    if inOperation == 0:
                        break
                    data = relative_move(int(j)-Position)
                    f.write(f"{i};{round(j,0)};{data[0]};{data[1]};{data[2]};{data[3]};\n")
                    mw.update()
                    mw.update_idletasks
    except:
        print("Error while writing file")
    
    inOperation = 0
    mw.update()
    Buttons[0].config(state=NORMAL)
    callback()
    callback2()
    


#arrete les mesure
def stop_mesure():
    global inOperation
    inOperation = 0
    global Buttons
    Buttons[5].config(state=DISABLED)



#main function
def main():
    arduino.flushInput()
    arduino.flushOutput()
    time.sleep(0.4)

    global mw
    mw = Tk()
    mw.title("Throttle Valve Controller")
    mw.geometry("390x220")
    mw.resizable(0, 0)


    mw.grid_columnconfigure(0, minsize=10)
    mw.grid_columnconfigure(2, minsize=20)
    mw.grid_columnconfigure(3, minsize=20)
    mw.grid_columnconfigure(4, minsize=20)
    mw.grid_columnconfigure(5, minsize=20)
    mw.grid_columnconfigure(6, minsize=10)

    mw.grid_rowconfigure(0, minsize=20)
    mw.grid_rowconfigure(2, minsize=20)
    mw.grid_rowconfigure(4, minsize=20)
    mw.grid_rowconfigure(6, minsize=20)
    mw.grid_rowconfigure(8, minsize=10)
    

    global Buttons
    Buttons = []

    #Home Button
    Buttons.append(Button(mw, text="Home", command=lambda: Home(),width=4))
    Buttons[0].grid(row=1, column=1,columnspan=1)

    #position display
    Label(mw, text="Position: ",height=1,width=7).grid(row=1, column=2,columnspan=2, sticky=N)
    global TextPosition
    TextPosition = Text(mw,width=7,height=1)
    TextPosition.tag_configure("ALIGN", justify="right")
    TextPosition.insert(END, "?","ALIGN")
    TextPosition.config(state=DISABLED)
    TextPosition.grid(row=1, column=3,columnspan=2,sticky=E)



    #Open Button
    Buttons.append(Button(mw, text="Open", command=lambda: relative_move(800),width=5))
    Buttons[1].grid(row=3, column=1,columnspan=1)
    Buttons[1].config(state=DISABLED)

    #Close Button
    Buttons.append(Button(mw, text="Close", command=lambda: relative_move(-800),width=5))
    Buttons[2].grid(row=3, column=2,columnspan=1)
    Buttons[2].config(state=DISABLED)
    
    #Go to step Button
    Buttons.append(Button(mw, text="Go to step", command=lambda: relative_move(int(stepEntry.get())-Position),width=10))
    Buttons[3].grid(row=3, column=3,columnspan=3,sticky=N)
    Buttons[3].config(state=DISABLED)
    

    #Go to step Entry (goto)
    global stepEntry
    stepEntry = StringVar()
    stepEntry.trace("w", lambda *args: callback())
    Entry(mw, textvariable=stepEntry, width=8,justify=RIGHT).grid(row=3, column=6,columnspan=1,sticky=W)


    #Cycle textbox
    Label(mw, text="Nb Cycle: ",width=8).grid(row=5, column=1,columnspan=1, sticky=E)
    global Cycle
    Cycle = StringVar()
    Cycle.trace("w", lambda *args: callback2())
    Entry(mw, textvariable=Cycle, width=8,justify=RIGHT).grid(row=5, column=2,columnspan=1,sticky=W)
    
    #Step textbox (cycle)

    Label(mw, text="Mesure/Cycle:",width=10,justify=RIGHT).grid(row=5, column=3,columnspan=2, sticky=E)
    global Step
    Step = StringVar()
    Step.trace("w", lambda *args: callback2())
    Entry(mw, textvariable=Step, width=8,justify=RIGHT).grid(row=5, column=5,columnspan=2,sticky=W)


    #Start button
    Buttons.append(Button(mw, text="Run", command=lambda: start_mesure(),width=4))
    Buttons[4].grid(row=5, column=6,columnspan=1,sticky=E)
    Buttons[4].config(state=DISABLED)

    #Stop button
    Buttons.append(Button(mw, text="Stop", command=lambda: stop_mesure(),width=4))
    Buttons[5].grid(row=5, column=7,columnspan=1)
    Buttons[5].config(state=DISABLED)



    #File selection
    global filePathEntry
    filePathEntry = Text(mw,width=40,height=1)
    filePathEntry.tag_configure("ALIGN", justify="right")
    filePathEntry.config(state=DISABLED)
    filePathEntry.grid(row=7, column=1,columnspan=6,sticky=E)
    Button(mw, text="...", command=lambda: select_file(),width=4).grid(row=7, column=7,columnspan=1,sticky=W)

    mw.mainloop()


if __name__ == '__main__':
    main()