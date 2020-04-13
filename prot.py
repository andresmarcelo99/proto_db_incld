import pkg_resources.py2_warn
import tkinter
import PIL
import os
from PIL import ImageTk
from PIL import Image
from tkcalendar import *
from tkinter import filedialog
import cv2
import numpy as np
from tkinter import messagebox
import tkinter.font as TkFont
import tkinter as GUI
import array
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

# Load Yolo
net = cv2.dnn.readNet("C:\\Users\\Marcelo Andres\\Documents\\YOLO obj detection\\yolov3.weights","C:\\Users\\Marcelo Andres\\Documents\\YOLO obj detection\\yolov3.cfg")
classes = []
with open("C:\\Users\\Marcelo Andres\\Documents\\YOLO obj detection\\coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layers_name = net.getLayerNames()

output_layers = [layers_name[i[0]-1] for i in net.getUnconnectedOutLayers()]

colors = np.random.uniform(0,255, size = (len(classes),3))

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

def insertVariablesIntoTable(id, Emp_id, Tipo_Producto, Date_, Ubicacion, Codigo, Descripcion, Inventario_T, Inventario_R, Diferencia):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='Electronics',
                                             user='root',
                                             password='Marcelosans12')
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO Inventario (Id, Emp_id, Tipo_Producto, Date_, Ubicacion,
                                Codigo, Descripcion, Inventario_T, Inventario_R, Diferencia)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

        recordTuple = (id, Emp_id, Tipo_Producto, Date_, Ubicacion, Codigo, Descripcion, Inventario_T, Inventario_R, Diferencia)
        cursor.execute(mySql_insert_query, recordTuple)
        connection.commit()
        print("Record inserted successfully into Inv table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def get_next_index():

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='Electronics',
                                             user='root',
                                             password='Marcelosans12')

        sql_select_Query = "select * from Inventario"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        print("Total number of rows in Inventario is: ", cursor.rowcount)

        #print("\nPrinting each inventory record")
        for row in records:
            ##print("Id = ", row[0], )
            curr = row[0]
        curr += 1

    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")

    return curr

def update_data():

      global index
      global inv_real_info
      global diff
      global curr_key

      connection = mysql.connector.connect(host='localhost',
                                     database='Electronics',
                                     user='root',
                                     password='Marcelosans12')

      cursor = connection.cursor()

      sql = "UPDATE Inventario SET Inventario_R = {} WHERE Id = {}".format(inv_real_info[index], curr_key[index])
      sql_dif = "UPDATE Inventario SET Diferencia = {} WHERE Id = {}".format(diff[index], curr_key[index])

      cursor.execute(sql)
      cursor.execute(sql_dif)

      connection.commit()

      print(cursor.rowcount, "record(s) affected")


def save_info():

    global file
    global index
    global emp_info
    global date_info
    global prod_type_info
    global ubi_info
    global codigos_info
    global descrip_info
    global inv_info
    global size_of
    global current_date
    global curr_key
    global diff
    global inv_real_info

    diff.append(0)
    inv_real_info.append(0)
    curr_key.append(get_next_index())
    emp_info.append(cod_emp.get())
    date_info.append(current_date)
    prod_type_info.append(clicked_type.get())
    ubi_info.append(ubicaciones_var.get())
    codigos_info.append(codigos_var.get())
    descrip_info.append(descripcion_var.get())
    inv_info.append(inventario_var.get())

    file.write(emp_info[index])
    file.write("\n")
    file.write(str(date_info[index]))
    file.write("\n")
    file.write(prod_type_info[index])
    file.write("\n")
    file.write(ubi_info[index])
    file.write("\n")
    file.write(codigos_info[index])
    file.write("\n")
    file.write(descrip_info[index])
    file.write("\n")
    file.write(str(inv_info[index]))
    file.write("\n")

    insertVariablesIntoTable(curr_key[index], emp_info[index], prod_type_info[index], date_info[index],
    ubi_info[index], codigos_info[index], descrip_info[index], inv_info[index], 0, 0)

    print("success")
    index += 1
    size_of = index

def get_back():

    global label_ubi_curr
    global size_of
    global index
    global ubi_info
    global frame_ubi_main
    global codigos_info
    global descrip_info
    global inv_infos
    global inv_real_info
    global diff

    if index > 0:
        index = index - 1

    label_ubi_curr = tkinter.Label(frame_ubi_main, text = ubi_info[index], borderwidth = 1, relief = "solid", width = 13)
    label_ubi_curr.grid(row = 1, column = 0)
    label_cod_curr = tkinter.Label(frame_ubi_main, text = codigos_info[index] , borderwidth = 1 , relief = "solid", width = 13)
    label_cod_curr.grid(row = 1, column = 1)
    label_descrip_curr = tkinter.Label(frame_ubi_main, text = descrip_info[index], borderwidth = 1, relief = "solid", width = 13)
    label_descrip_curr.grid(row = 1, column = 2)
    label_inv_curr = tkinter.Label(frame_ubi_main, text = inv_info[index], borderwidth = 1, relief = "solid", width = 13)
    label_inv_curr.grid(row = 1, column = 3)
    prod_type_text = tkinter.Label(screen, text = "Producto: " + prod_type_info[index], width = 20)
    prod_type_text.place(x = 400, y = 80)
    label_invR_curr = tkinter.Label(frame_ubi_main, text = inv_real_info[index], borderwidth = 1, relief = "solid", width = 13)
    label_invR_curr.grid(row = 1, column = 4)
    label_dif_curr = tkinter.Label(frame_ubi_main, text = diff[index], borderwidth = 1, relief = "solid", width = 13)
    label_dif_curr.grid(row = 1, column = 5)


def get_front():

    global label_ubi_curr
    global size_of
    global index
    global ubi_info
    global frame_ubi_main
    global codigos_info
    global descrip_info
    global inv_info
    global diff
    global inv_real_info

    #label_ubi_curr.grid_forget()

    if index < (size_of-1):
        index = index + 1

    label_ubi_curr = tkinter.Label(frame_ubi_main, text = ubi_info[index], borderwidth = 1, relief = "solid", width = 13)
    label_ubi_curr.grid(row = 1, column = 0)
    label_cod_curr = tkinter.Label(frame_ubi_main, text = codigos_info[index] , borderwidth = 1 , relief = "solid", width = 13)
    label_cod_curr.grid(row = 1, column = 1)
    label_descrip_curr = tkinter.Label(frame_ubi_main, text = descrip_info[index], borderwidth = 1, relief = "solid", width = 13)
    label_descrip_curr.grid(row = 1, column = 2)
    label_inv_curr = tkinter.Label(frame_ubi_main, text = inv_info[index], borderwidth = 1, relief = "solid", width = 13)
    label_inv_curr.grid(row = 1, column = 3)
    prod_type_text = tkinter.Label(screen, text = "Producto: " + prod_type_info[index], width = 20 )
    prod_type_text.place(x = 400, y = 80)
    label_invR_curr = tkinter.Label(frame_ubi_main, text = inv_real_info[index], borderwidth = 1, relief = "solid", width = 13)
    label_invR_curr.grid(row = 1, column = 4)
    label_dif_curr = tkinter.Label(frame_ubi_main, text = diff[index], borderwidth = 1, relief = "solid", width = 13)
    label_dif_curr.grid(row = 1, column = 5)


def openFile():

    global panel
    global img_conver
    global qtyObjs
    global index
    global inv_info
    global diff
    global curr_key
    qtyObjs = 0
    type_update = False

    try:
        screen.filename = filedialog.askopenfilename(initialdir = "C:/Users/Marcelo Andres/Documents/py files/SID PROT1/inventario", title = "Select a file" )
        my_image = ImageTk.PhotoImage(Image.open(screen.filename))

    except:
        print("file was empty")
    else:
        if os.path.getsize(screen.filename) !=0:

            #object detection
            original_img = cv2.imread(screen.filename)
            height, width, channels = original_img.shape
            blob = cv2.dnn.blobFromImage(original_img, 0.00392,(416,416),(0,0,0), True,crop=False)

            net.setInput(blob)
            outs = net.forward(output_layers)

            class_ids = []
            confidences = []
            boxes = []

            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.55:
                        #obj detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        #rect coordinates
                        x = int(center_x - w/2)
                        y = int(center_y - h/2)

                        boxes.append([x,y,w,h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            font = cv2.FONT_HERSHEY_PLAIN
            indexes = cv2.dnn.NMSBoxes(boxes,confidences, 0.5,0.4)
            print(indexes)
            number_objects_detected = len(boxes)
            for i in range(len(boxes)):

                if i in indexes:
                    x,y,w,h = boxes[i]
                    label = str(classes[class_ids[i]])
                    color = colors[i]
                    cv2.rectangle(original_img,(x,y),(x+w,y+h),color,2)
                    cv2.putText(original_img,label,(x,y+30),font,1,color,2)
                    print(label)
                    if prod_type_info[index] == "Botellas":
                        if label == "bottle":
                            qtyObjs = qtyObjs + 1
                        #type_update = True
                    if prod_type_info[index] == "Electronica":
                        if label == "tvmonitor" or label == "laptop":
                            qtyObjs = qtyObjs + 1

            diff[index] = inv_info[index] - qtyObjs
            inv_real_info[index] = qtyObjs
            #update value in db
            if qtyObjs > 0:
                update_data()


            #output of real inventory since qtyObj is local to openFile
            label_invR_curr = tkinter.Label(frame_ubi_main, text = inv_real_info[index], borderwidth = 1, relief = "solid", width = 13)
            label_invR_curr.grid(row = 1, column = 4)
            label_dif_curr = tkinter.Label(frame_ubi_main, text = diff[index], borderwidth = 1, relief = "solid", width = 13)
            label_dif_curr.grid(row = 1, column = 5)


            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.putText(original_img,str(qtyObjs), (15,680),font,1,(0,0,255),2)

            #resize
            widthcv2 = 600
            lengthcv2 = 400
            dim = (widthcv2,lengthcv2)
            original_img = cv2.resize(original_img, dim, interpolation =  cv2.INTER_AREA)

            #convert for tkinter display
            img_conver = Image.fromarray(original_img)
            img_conver = ImageTk.PhotoImage(img_conver)

            panel = tkinter.Label(screen, image = img_conver)
            panel.image = img_conver
            panel.place(x = 700, y = 120)
            print(str(qtyObjs))
            print(str(inv_info[index]))
            print(str(diff))
            print("success")



def enterMain():
    global screen
    global file
    global index
    global emp_info
    global date_info
    global prod_type_info
    global ubi_info
    global codigos_info
    global descrip_info
    global inv_info
    global logo
    global current_date

    date = ""

    if change == 0 :
        index = 0

    screen = tkinter.Toplevel() # initialize
    app = FullScreenApp(screen)
    screen.title("SID Form") # name the window

    #setting frame grid for main screen
    global frame_ubi_main
    frame_ubi_main = tkinter.Frame(screen,width=400, height=270)
    frame_ubi_main.place(x=90,y=200)
    frame_ubi_main.config(background='gray')

    label_ubi_main = tkinter.Label(frame_ubi_main, text = "Ubicaciones", borderwidth = 1, relief = "solid")
    label_ubi_main.grid(row = 0, column = 0)
    label_ubi_curr = tkinter.Label(frame_ubi_main, text = ubi_info[index], borderwidth = 1, relief = "solid", width = 13)
    label_ubi_curr.grid(row = 1, column = 0)

    label_cod_main = tkinter.Label(frame_ubi_main, text = "Codigo", borderwidth = 1 , relief = "solid")
    label_cod_main.grid(row = 0, column = 1)
    label_cod_curr = tkinter.Label(frame_ubi_main, text = codigos_info[index] , borderwidth = 1 , relief = "solid", width = 13)
    label_cod_curr.grid(row = 1, column = 1)

    label_descrip_main = tkinter.Label(frame_ubi_main, text = "Descripcion", borderwidth = 1, relief = "solid")
    label_descrip_main.grid(row = 0, column = 2)
    label_descrip_curr = tkinter.Label(frame_ubi_main, text = descrip_info[index], borderwidth = 1, relief = "solid", width = 13)
    label_descrip_curr.grid(row = 1, column = 2)

    label_inv_main = tkinter.Label(frame_ubi_main, text = "Inventario Teorico", borderwidth = 1, relief = "solid")
    label_inv_main.grid(row = 0, column = 3)
    label_inv_curr = tkinter.Label(frame_ubi_main, text = inv_info[index], borderwidth = 1, relief = "solid", width = 13)
    label_inv_curr.grid(row = 1, column = 3)

    label_invR_main = tkinter.Label(frame_ubi_main, text = "Inventario Real", borderwidth = 1, relief = "solid")
    label_invR_main.grid(row = 0, column = 4)

    label_dif_main = tkinter.Label(frame_ubi_main, text = "Diferencia", borderwidth = 1, relief = "solid")
    label_dif_main.grid(row = 0, column = 5)


    #opening file
    file_btn = tkinter.Button(screen, text = "open file", command = openFile)
    file_btn.place(x=1000, y = 600)

    logo_label_main = tkinter.Label(screen, image = logo)
    logo_label_main.place(x = 1250, y = 10)

    cod_emp_text = tkinter.Label(screen, text = "Empleado: " + cod_emp.get())
    cod_emp_text.place(x = 40, y = 80)

    date_text = tkinter.Label(screen, text = "Fecha: " +  current_date)
    date_text.place(x = 220, y = 80)

    prod_type_text = tkinter.Label(screen, text = "Producto: " + prod_type_info[index], width = 20)
    prod_type_text.place(x = 400, y = 80)

    #atras button
    BackButton = tkinter.Button(screen, text = "Anterior",width = 10, command = get_back)
    BackButton.place(x = 80, y=600)

    #siguiente button
    NextButton = tkinter.Button(screen, text = "Siguiente", width =10, command = get_front)
    NextButton.place(x = 235 , y=600)

    EditButton = tkinter.Button(screen, text = "Editar", width = 10)
    EditButton.place(x = 400 , y=600)
    intro_scr.wm_state('iconic')

#heading = tkinter.Label(text = "SID ™", bg = "blue", width=57, height = 2)
#heading.pack()

#main screen function

index = 0
change = 0
size_of = 0
curr_key = []
emp_info = []
ubi_info = []
date_info = []
prod_type_info = []
codigos_info = []
descrip_info = []
inv_info = []
inv_real_info = []
diff = []
file = open("C:\\Users\\Marcelo Andres\\Documents\\py files\\SID PROT1\\user.txt","w")

now = datetime.now()

current_date =  str(now.year) + "/" +  str(now.month)  + "/" + str(now.day)

#introScreen
intro_scr = tkinter.Tk()
intro_scr.geometry("600x600")

logo = Image.open("C:/Users/Marcelo Andres/Documents/py files/SID PROT1/logo.jpeg")
logo = logo.resize((70,70),Image.ANTIALIAS)
logo = ImageTk.PhotoImage(logo)
logo_label = tkinter.Label(intro_scr, image = logo)
logo_label.place(x = 500, y = 10)

#employee entry label
cod_emp_text = tkinter.Label(intro_scr, text = "Codidgo Empleado: * ")
cod_emp_text.place(x = 100, y = 80)

#date label
date_text = tkinter.Label(intro_scr, text = "Fecha: * ")
date_text.place(x = 150, y = 150)

#current date label
date_curr = tkinter.Label(intro_scr, text = current_date, width ="16", height = "1")
date_curr.place(x = 220, y = 150)


#type of prod label
prod_type_text = tkinter.Label(intro_scr, text = "Tipo de producto *")
prod_type_text.place(x = 100, y = 220)

#select type button
clicked_type = tkinter.StringVar()
clicked_type.set("empty")

prod_type_btn = tkinter.OptionMenu(intro_scr, clicked_type, "Botellas", "Electronica", "Linea Blanca", "Otros")
prod_type_btn.place(x=250, y = 220)


#storage variables
cod_emp =  tkinter.StringVar()

#data input
cod_emp_entry  = tkinter.Entry(intro_scr, textvariable= cod_emp)
cod_emp_entry.place(x = 250, y = 80)

#register button
register = tkinter.Button(intro_scr, text = "Register", width ="6", height = "2", command =  lambda:[enterMain(), file.close()])
register.place(x = 530, y = 530)

#add button
add_ubi = tkinter.Button(intro_scr, text = "Añadir", width ="5", height = "1", command = save_info)
add_ubi.place(x = 430, y = 360)

#frame setup
frame_ubi = tkinter.Frame(intro_scr,width=400, height=270)
frame_ubi.place(x=100,y=300)
frame_ubi.config(background='gray')

ubicaciones_var = tkinter.StringVar()
label_ubi_title = tkinter.Label(frame_ubi, text = "Ubicaciones", borderwidth = 1, relief = "solid")
label_ubi_title.grid(row = 0, column = 0)
ubi_entry = tkinter.Entry(frame_ubi, width = 15, textvariable = ubicaciones_var)
ubi_entry.grid(row=1,column=0)

codigos_var = tkinter.StringVar()
label_cod_title = tkinter.Label(frame_ubi, text = "Codigo", borderwidth = 1 , relief = "solid", width = 9)
label_cod_title.grid(row = 0, column = 1)
cod_entry = tkinter.Entry(frame_ubi, width = 15, textvariable = codigos_var)
cod_entry.grid(row=1,column=1)

descripcion_var = tkinter.StringVar()
label_descrip_title = tkinter.Label(frame_ubi, text = "Descripcion", borderwidth = 1, relief = "solid")
label_descrip_title.grid(row = 0, column = 2)
descripcion_entry = tkinter.Entry(frame_ubi, width = 15, textvariable = descripcion_var)
descripcion_entry.grid(row=1,column=2)

inventario_var = tkinter.IntVar()
label_inv_title = tkinter.Label(frame_ubi, text = "Inventario", borderwidth = 1, relief = "solid", width = 9)
label_inv_title.grid(row = 0, column = 3)
inventario_entry = tkinter.Entry(frame_ubi, width = 15, textvariable = inventario_var)
inventario_entry.grid(row=1,column=3)




tkinter.mainloop() # keep window open
