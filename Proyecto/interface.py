import sys
from tkinter import *
from tkinter import messagebox
from hammingcode import *
from logica import *
from settings import *


##Funciones
def close(event):
    # root.withdraw() # if you want to bring it back
    sys.exit()  # if you want to exit the entire thing


# Funcion para detectar enter en el entry.
def onEnter(event=None):
    mostrar_conversiones()
    mostrar_codigo_nrzi(nzriCanvas)


# Funcion para detectar click en el toggle button y para cambiar paridad.
def switch(event):
    global parity
    if parity == 'impar':
        switchLabel.config(image=switchbtn0)
        dirTxt.set('Par')
        parity = 'par'
        print("PAR")
        entrysList[17].delete(0, END)
        entrysList[17].insert(0, '0')
        entrysList[17].config(bg=parColor)

    else:
        switchLabel.config(image=switchbtn1)
        dirTxt.set('Impar')
        parity = 'impar'
        print("IMPAR")
        entrysList[17].delete(0, END)
        entrysList[17].insert(0, '1')
        entrysList[17].config(bg=imparColor)


def mostrar_codigo_nrzi(canvas):
    num = numberEntry.get()
    if is_binary(num) == 0:
        return
    canvas.delete("all")

    codigo = obtener_codigo_nrzi(num, "bajo")

    x = 1
    y = 105
    sumx = 30
    resty = 85
    partition = (10, 120)

    last = 'bajo'
    for b in codigo:
        # print(b)
        if b == 'alto':  # ¯|
            if last != b:
                canvas.create_line(x, y - resty, x + sumx, y - resty, fill='black', width=2)
                canvas.create_line(x, y, x, y - resty, fill="black", width=2)
            else:
                canvas.create_line(x, y - resty, x + sumx, y - resty, fill="black", width=2)
                canvas.create_line(x, partition[0], x, partition[1], fill='red', width=2, dash=(5, 5))
            last = 'alto'

        else:  # ㇄
            if last != b:  # si es bajo
                canvas.create_line(x, y, x + sumx, y, fill=white, width=3)
                canvas.create_line(x, y, x, y - resty, fill=white, width=3)
            else:
                canvas.create_line(x, y, x + sumx, y, fill=white, width=3)
                canvas.create_line(x, partition[0], x, partition[1], fill='red', width=2, dash=(5, 5))
            last = 'bajo'
        x += sumx
    canvas.config(width=x + 1)
    canvas.create_line(0, canvas.winfo_height() / 2, x + 1, canvas.winfo_height() / 2, fill="black", width=3)


def mostrar_conversiones():
    cnvVar.set(convertir_binario_h_o_d(numberEntry.get()))


# Tabla 1.
def createTable1(columnsNames, rowsNames, canvas):
    # Headers
    for c in range(len(columnsNames)):
        cell = Label(canvas, font=(font, 11, 'bold'), text=columnsNames[c], width=3, relief="flat", bg=white,
                     justify='center')
        cell.grid(row=0, column=c, sticky=NSEW, padx=(1, 0), pady=(1, 1))
        if c == 0:
            cell.config(bg=bodyColor)
            cell.grid(pady=(0, 1), padx=(0, 0))

    # Descriptions
    for r in range(len(rowsNames)):
        cell = Label(canvas, font=(font, 11, 'bold'), text=rowsNames[r], width=27, relief="flat", bg=white,
                     justify='center')
        cell.grid(row=r + 1, column=0, sticky=NSEW, padx=(1, 0), pady=(0, 1))
        if r == 0 or r == (len(rowsNames) - 1):
            cell.config(bg=tablesColor)

    # Data
    # Row1
    for c in range(len(columnsNames) - 1):
        cell = Label(canvas, font=(font, 11), width=3, relief="flat", bg=splitLineColor, justify='center')
        cell.grid(row=1, column=c + 1, sticky=NSEW, padx=(1, 0), pady=(0, 1))
        row1Table1.append(cell)

    # Row7
    for c in range(len(columnsNames) - 1):
        cell = Label(canvas, font=(font, 11), width=3, relief="flat", bg=tablesColor, justify='center')
        cell.grid(row=len(rowsNames), column=c + 1, sticky=NSEW, padx=(1, 0), pady=(0, 1))
        row7Table1.append(cell)
        if c in (0, 1, 3, 7, 15):
            cell.config(font=(font, 11, 'bold'))

    # Row2al5 - Matrix data
    for r in range(2, len(rowsNames)):  # del 2 al 6
        cols = []
        for c in range(len(columnsNames) - 1):
            cell = Label(canvas, font=(font, 11), width=3, relief="flat", bg=white, justify='center')
            cell.grid(row=r, column=c + 1, sticky=NSEW, padx=(1, 0), pady=(0, 1))
            if c in (0, 1, 3, 7, 15):
                cell.config(font=(font, 11, 'bold'))
            cols.append(cell)
        matrizData1.append(cols)
    # print(len(matrizData1))
    # print(len(matrizData1[0]))


# Fill table1
def fillTable1():
    onEnter()

    num_without_parity = numberEntry.get()  # Obtener el número.
    # print("Entrada : ", num_without_parity)

    matrix = obtener_matriz_tabla_1(num_without_parity, parity)  # Obtener matriz.
    if not matrix:
        messagebox.showerror("Error!", "El número ingresado debe ser de 12 bits.")
        return

    num_with_parity = str(palabra_con_paridad(matrix))  # Resultado con paridad.

    # Llenar filas 1 y 7 y matriz
    fillListWith(num_without_parity, row1Table1, (0, 1, 3, 7, 15))
    fillListWith(num_with_parity, row7Table1)
    fillMatrixWith(matrix, matrizData1)

    # Acomodar entry en tabla 2.
    setTable2Number(num_with_parity)
    clearTable2()
    verifyLabel.config(text=verifyTxt)


# Funcion para meter datos dentro de una lista. AMBOS del mismo tamaño.
def fillListWith(data, lst, atIndex=None, index=0):
    if atIndex is None:
        for e in range(len(lst)):
            lst[e].config(text=data[e])
    else:
        for i in range(len(lst)):
            if not i in atIndex:
                lst[i].config(text=data[index])
                index += 1


def fillMatrixWith(data, matrix):
    for r in range(len(matrix)):  # 0 al 4 -> necesito ir del 1 al 5
        for c in range(len(matrix[0])):
            matrizData1[r][c].config(text=data[r][c])


# Tabla 2.
def createTable2(columnsNames, rowsNames, canvas):
    # Headers
    for c in range(len(columnsNames)):
        cell = Label(canvas, font=(font, 11, 'bold'), text=columnsNames[c], width=3, relief="flat", bg=white,
                     justify='center')
        cell.grid(row=0, column=c, sticky=NSEW, padx=(0, 1), pady=(1, 1))
        if c == 0:
            cell.config(bg=bodyColor)
            cell.grid(pady=(0, 1))
        elif c == (len(columnsNames) - 2):
            cell.config(width=16)
        elif c == (len(columnsNames) - 1):
            cell.config(width=17)

    # Descriptions
    for r in range(len(rowsNames)):
        cell = Label(canvas, font=(font, 11, 'bold'), text=rowsNames[r], width=15, relief="flat", bg=white,
                     justify='center')
        cell.grid(row=r + 1, column=0, sticky=NSEW, padx=(1, 0), pady=(0, 1))
        if r == 0:
            cell.config(bg=tablesColor)

    # Data
    for r in range(len(rowsNames)):
        cols = []
        for c in range(len(columnsNames) - 1):
            if r == 0 and c != (len(columnsNames) - 2):
                cell = Entry(canvas, font=(font, 11), width=3, relief="flat", bg=white, justify='center')
                cell.grid(row=r + 1, column=c + 1, sticky=NSEW, padx=(1, 0), pady=(0, 1))
                cell.config(bg=splitLineColor)
                if c == 17:
                    cell.insert(0, '0')  # valor quemado de 1.
                    cell.config(bg=parColor)
                entrysList.append(cell)
            else:
                cell = Label(canvas, font=(font, 11), width=3, relief="flat", bg=white, justify='center')
                cell.grid(row=r + 1, column=c + 1, sticky=NSEW, padx=(1, 0), pady=(0, 1))
                if c in (0, 1, 3, 7, 15):
                    cell.config(font=(font, 11, 'bold'))
                elif r == 0:
                    cell.config(bg=tablesColor)
                cols.append(cell)
        if r != 0:
            matrizData2.append(cols)


def setTable2Number(num):
    index = 0
    # entrada=''
    for e in range(len(entrysList) - 1):
        data = num[index]
        entrysList[e].delete(0, END)
        entrysList[e].insert(0, data)
        # entrada+=data
        index += 1

    # print ("Salida  :  ", entrada)


def clearTable2():
    for r in range(len(description2) - 1):  # del 0 al 4
        for c in range(len(headers2) - 1):  # del 0 al 18
            matrizData2[r][c].config(text='')


def getErrorNumTable2():
    data = ""
    for e in entrysList:
        data += e.get()

    if len(data) == 0:
        return
    # print(data)
    # print(data[:-1])
    tupleEntry = ()
    if len(data) == 18:
        if data[-1] == '1':
            tupleEntry = (data[:-1], "impar")
        elif data[-1] == '0':
            tupleEntry = (data[:-1], "par")
        else:
            messagebox.showerror("Error!", "Solo puede ingresar 1 o 0.")
            return
    else:
        messagebox.showerror("Error!", "Ingrese un valor de prueba para la paridad.")
        return
    # print(tupleEntry[0], tupleEntry[1])
    return tupleEntry


def fillTable2():
    entryValues = getErrorNumTable2()  # Obtener el número.
    # entryValues = ('11001100101010101', "par")
    if entryValues is None:
        return
    print("SALIDA  : ", entryValues[0])
    print("TEST    : ", '11001101111111100')
    # print("PRUEBA  : ", entryValues[1])

    num = entryValues[0]
    paridad = entryValues[1]
    pair = verificar_errores_tabla_2(num, paridad)  # Esta funcion devuelve un par ordenado (matriz, pos bit error)
    matrix = pair[0]  # Almacena la matriz final
    error = pair[1]  # Almacena la posicion donde está el error
    bitsList = pair[2]  # Lista en orden de los bits comparacion, elemento 0: bit comprobacion para bit de paridad 1

    # print("Matrix : ", matrix)
    # print("Error : ", error)
    print("Bits : ", str(bitsList))

    # Rellena datos
    for r in range(len(description2) - 1):  # del 0 al 4
        for c in range(len(headers2) - 3):  # del 0 al 17
            matrizData2[r][c].config(text=matrix[r][c])

    # Rellena bits
    index = 0
    for r in range(len(description2) - 1):
        bit = bitsList[index]
        matrizData2[r][len(headers2) - 2].config(text=bit)

        if paridad == 'par':
            matrizData2[r][len(headers2) - 3].config(text='Error') if (bit == '1') else matrizData2[r][
                len(headers2) - 3].config(text='Correct')

        elif paridad == 'impar':
            if bit == '0':
                matrizData2[r][len(headers2) - 2].config(text='1')
            else:
                matrizData2[r][len(headers2) - 2].config(text='0')

            matrizData2[r][len(headers2) - 3].config(text='Correcto') if (bit == '1') else matrizData2[r][
                len(headers2) - 3].config(text='Error')
        index += 1
    verifyLabel.config(text='No hay error.') if (error == '0') else verifyLabel.config(text=verifyTxt + str(error))


# Window
root = Tk()
root.title("Proyecto 1 - Diseño Lógico")
root.overrideredirect(False)
root.resizable(False, False)
root.configure(background='black')
root.bind('<Escape>', close)

# Header Canvas
headerCanvas = Canvas(root, bg=headerColor, highlightthickness=0)

# Body Canvas
bodyCanvas = Canvas(root, bg=bodyColor, highlightthickness=0)

# Label de instruccion.
headerLabel = Label(headerCanvas, text=label1, bg=headerColor, fg=white, font=(font, 16))

# Entry del numero.
numberEntry = Entry(headerCanvas, width=20, font=(font, 14), relief="flat")
numberEntry.insert(0, '011011111110')
numberEntry.bind("<Return>", onEnter)

# Button para llamar a Hamming
hammingImg = PhotoImage(file="resources/hamming.png")
hammingButton = Button(headerCanvas, image=hammingImg, command=fillTable1, bg=headerColor, activebackground=headerColor,
                       relief='flat', borderwidth=0)
# Button para llamar verificar
errorImg = PhotoImage(file="resources/error.png")
errorButton = Button(headerCanvas, image=errorImg, command=fillTable2, bg=headerColor, activebackground=headerColor,
                     relief='flat', borderwidth=0)

# Toggle Button
switchbtn0 = PhotoImage(file="resources/toggle_on.png")
switchbtn1 = PhotoImage(file="resources/toggle_off.png")
switchLabel = Label(headerCanvas, image=switchbtn0, width=70, height=50, bg=headerColor)
switchLabel.bind("<Button-1>", switch)

# Toggle Label
dirTxt = StringVar()
global parity
dirTxt.set("Par" if parity == "par" else "Impar")
toggleText = Label(headerCanvas, textvariable=dirTxt, justify=CENTER, anchor='center',
                   bg=headerColor, fg=white, font=(font, 10), width=8)

# Frame Base
groundFrame = Frame(bodyCanvas, bg=groundFrameColor, width=500, height=150)

# Conversion Widgets
cnvVar = StringVar("")
cnvLabel = Label(groundFrame, textvariable=cnvVar, justify=LEFT, anchor="nw",
                 bg=groundFrameColor, fg=white, font=(font, 13), height=5, width=-50)

# Conversion Widgets
nzriCanvas = Canvas(groundFrame, bg=tablesColor, height=125)

# tables
l1 = Label(bodyCanvas, text="Tabla 1. Cálculo de los bits de paridad en el código Hamming.", bg=bodyColor,
           font=(font, 13))
l2 = Label(bodyCanvas, text="Tabla 2. Comprobación de los bits de paridad.", bg=bodyColor, font=(font, 13))

c1 = Frame(bodyCanvas, bg=tablesColor, width=600, height=250)
c2 = Frame(bodyCanvas, bg=tablesColor, width=600, height=250)
verifyLabel = Label(c2, text=verifyTxt, bg=tablesColor, fg='black', font=(font, 11))

# Create table
createTable1(headers1, description1, c1)
createTable2(headers2, description2, c2)

# Shoving on screen.
headerCanvas.grid(row=0, column=0, sticky='NSEW', columnspan=5, rowspan=2)
bodyCanvas.grid(row=2, column=0, sticky='NSEW', columnspan=5, rowspan=5)

headerLabel.grid(row=0, column=0, columnspan=1, ipadx=10, sticky='EW')
numberEntry.grid(row=0, column=1, columnspan=1, padx=5, pady=25)

hammingButton.grid(row=0, column=3, sticky='NSEW', padx=(20, 5), pady=5)
errorButton.grid(row=0, column=4, sticky='NSEW', padx=(5, 280), pady=5)

switchLabel.grid(row=0, column=5, pady=(0, 2), sticky='SW')
toggleText.grid(row=0, column=5, pady=(7, 0), sticky='NW')

groundFrame.grid(row=2, column=0, rowspan=2, columnspan=6, padx=5, pady=5, sticky='NSEW')
cnvLabel.grid(row=0, column=2, columnspan=2, rowspan=2, padx=5, pady=10, sticky='NSEW')
nzriCanvas.grid(row=0, column=0, columnspan=2, rowspan=2, padx=10, pady=10, sticky='NSEW')

l1.grid(row=4, column=0, columnspan=6, padx=10, pady=(5, 0), ipady=5)
l2.grid(row=8, column=0, columnspan=6, padx=10, pady=(0, 0), ipady=5)
c1.grid(row=5, column=0, rowspan=3, columnspan=6, padx=(15, 15), pady=(0, 15), sticky='N')
c2.grid(row=9, column=0, rowspan=3, columnspan=6, padx=(15, 15), pady=(0, 15), sticky='N')
verifyLabel.grid(row=7, column=0, columnspan=19, padx=5, sticky='W')

root.mainloop()
