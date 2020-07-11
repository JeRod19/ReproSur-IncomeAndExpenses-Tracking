# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 20:26:46 2020

@author: TOSHIBA
"""
import tkinter as tk
from tkintertable import TableCanvas, TableModel


def Insert_main_labels(lb_wt, lb_ht, x_offset, y_offset, main_wt, values, Main):
    lb_wt = 200
    lb_ht = 50
    lb_pos = round((((main_wt - 2*x_offset)/4) - lb_wt)/2)

    lb_ingress = tk.Label(Main, text="Ingresos", fg="green", bg = "skyblue")
    lb_ingress.place(height=25, width = lb_wt, x=x_offset + lb_pos + 275*0, y=y_offset-25)    
    ingress = tk.Label(Main, text=values[0], bg="green", font=("Arial", 18))
    ingress.place(height=lb_ht, width = lb_wt, x=x_offset + lb_pos + 275*0, y=y_offset)
    
    
    lb_equip = tk.Label(Main, text="Equipo", fg="blue", bg = "skyblue")
    lb_equip.place(height=25, width = lb_wt, x=x_offset + lb_pos + 275*1, y=y_offset-25)
    equip = tk.Label(Main, text=values[2], bg="blue", font=("Arial", 18))
    equip.place(height=lb_ht, width = lb_wt, x=x_offset + lb_pos + 275*1, y=y_offset)
    
    lb_egress = tk.Label(Main, text="Egresos", fg="red", bg = "skyblue")
    lb_egress.place(height=25, width = lb_wt, x=x_offset + lb_pos + 275*2, y=y_offset-25)
    egress = tk.Label(Main, text=values[1], bg="red", font=("Arial", 18))
    egress.place(height=lb_ht, width = lb_wt, x=x_offset + lb_pos + 275*2, y=y_offset)
    
    lb_decrease = tk.Label(Main, text="Depreciación", fg="orange", bg = "skyblue")
    lb_decrease.place(height=25, width = lb_wt, x=x_offset + lb_pos + 275*3, y=y_offset-25)
    decrease = tk.Label(Main, text=values[3], bg="orange", font=("Arial", 18))
    decrease.place(height=lb_ht, width = lb_wt, x=x_offset + lb_pos + 275*3, y=y_offset)
    
    lb_earns = tk.Label(Main, text="Ganancias", fg="darkgreen", bg = "skyblue")
    lb_earns.place(height=25, width = lb_wt, x=(1100/4)- 50, y=150 - 25)
    earns = tk.Label(Main, text=values[4], bg="darkgreen", font=("Arial", 18))
    earns.place(height=lb_ht, width = lb_wt, x=(1100/4)- 50, y=150)

    lb_value = tk.Label(Main, text="Valoración", fg="grey", bg = "skyblue")
    lb_value.place(height=25, width = lb_wt, x=(1100*3/4)- 50, y=150 - 25)
    value = tk.Label(Main, text=values[5], bg="grey", font=("Arial", 18))
    value.place(height=lb_ht, width = lb_wt, x=(1100*3/4)- 50, y=150)
    
    Values_labels = [ingress, egress, equip, decrease, earns, value]
    return Values_labels
    
def Insert_main_buttoms(Main, filter_main_collumns, ingress_window, record_egress):
    btn_filter_col = tk.Button(Main, text= "Editar", bg="blue", fg="white", command=filter_main_collumns)
    btn_filter_col.place(height=25, width = 100, x=50, y=250)  
  
    btn_ingress = tk.Button(Main, text= "Ingreso", bg="green", fg="black", command= ingress_window)
    btn_ingress.place(height=25, width = 100, x=150, y=250)  
    
    btn_filter_col = tk.Button(Main, text= "Egreso", bg="red", fg="black", command= record_egress )
    btn_filter_col.place(height=25, width = 100, x=250, y=250)
    
def CreateTable(Main, Data):
    
    tframe = tk.Frame(Main,
                      bg ="blue",
                      highlightcolor = "blue") 
    tframe.place(x = 50, y =275,
                 height = 275, width =1100)
    
    rec, col = Data.shape
    aux = dict()
    data = dict()
    
    for i in range(rec):
        for j in range(col):
            aux [Data.columns[j]] = Data.values[i,j]
        data['rec'+str(i+1)] = aux.copy()
    
    model = TableModel()    
    table = TableCanvas(tframe, cellbackgr='white', 
    			thefont=('Arial',12, ), cellwidth = 100 ,
                rowheight=25, rowheaderwidth=30,
    			rowselectedcolor='yellow', editable=False,
                model = model)
    table.createTableFrame()
    model = table.model
    model.importDict(data)

    table.show()
    return table, model

def UpdateTable (table, model, Data):
    
    rec, col = Data.shape
    aux = dict()
    data = dict()
    
    for i in range(rec):
        for j in range(col):
            aux [Data.columns[j]] = Data.values[i,j]
        data['rec'+str(i+1)] = aux.copy()
    
    model.importDict(data)
    table.redraw()
    
    return table
 
def UpdateLabels(Labels, values):
    for i in range(len(Labels)):
        Labels[i].configure(text = values[i])