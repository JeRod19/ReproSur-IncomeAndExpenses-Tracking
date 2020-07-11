
# -*- coding: utf-8 -*-

import tkinter as tk
from tkintertable import TableCanvas, TableModel
import Module1 as M1 # Contain fuctions to create Tkinter widgets use on the program
import Module2 as M2 # Contain functions to interact with the IBM Cloud Database
import pandas as pd
import numpy as np
from datetime import date
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2Tk
from matplotlib.figure import Figure



class deleteButton():
    def __init__(self, Main):
        btn_delete = tk.Button(Main, text= "Borrar", bg="black", fg="white",
                               command = self.Comfirm_wd)
        btn_delete.place(height=25, width = 100, x=350, y=250)
        
    def Comfirm_wd(self):
        self.window = tk.Toplevel(Main)
        self.window.configure(background = 'gray30')
        self.window.title("Borrar Registro")
        self.window.geometry('300x110')
        
        rclicked = MainTable.currentrow
        Rec = MainTableModel.getRecordAtRow(rclicked)
        Rec = str(list(Rec.values()))
        self.key = MainTableModel.getValueAt(rclicked, 0)
        
        Lb = tk.Label(self.window, bg = 'gray30', fg = 'white',
                          font=("Arial", 10), text = "Desea borrar:\n" \
                              + Rec[0:int(len(Rec)/2)] + "\n" \
                              + Rec[int(len(Rec)/2):] )
        Lb.place(x= 30, y = 10)
        Record = tk.Button(self.window, text= "Borrar", bg="white", fg="black",
                               font=("Arial", 12), 
                               command = self.delete_rows)
        Record.place(height=30, width = 50, x=115, y=70)
        
    def delete_rows(self):
        cursor.execute("delete from Transactions.dbo.Transactions where # =" + str(self.key))
        conn.commit()
        Ex = pd.read_sql(Read_records_query, conn)
        Ex['Fecha'] = pd.to_datetime(Ex['Fecha']).dt.strftime('%d/%m/%Y')
        extrarow = list(pd.read_sql("SELECT COUNT(*) FROM Transactions.dbo.Transactions;", conn)[""])
        M1.UpdateTable(MainTable, MainTableModel, Ex)
        values = M2.GetValues(conn)
        M1.UpdateLabels(Values_labels, values)
        MainTableModel.deleteRows(extrarow)
        MainTable.redraw()
        self.window.destroy()
        
class SalariesCalculator():
    def __init__(self, Salaries):
        date_var1 = tk.StringVar()
        date_var2 = tk.StringVar()
        self.Worker = "Francisco"
        self.window = Salaries
        Date =str( date.today().strftime("%d/%m/%Y") )
        if Date[0:2] <= '15':
            D1 = "01"+Date[2:]
            D2 = "15"+Date[2:]
        else:
            D1 = "16"+Date[2:]
            D2 = Date
        X = 50
        Y = 50
        
        Lb = tk.Label(self.window,bg = 'skyblue',
                          font=("Arial", 12), text = "De:")
        Lb.place(x= X + 80, y = Y)
        self.Date1 = tk.Entry(self.window, bg = 'white', font=("Arial", 12), textvariable = date_var1)
        date_var1.set(D1)
        self.Date1.place(x = X + 80, y = Y + 30)
        
        Lb = tk.Label(self.window,bg = 'skyblue',
                          font=("Arial", 12), text = "Hasta:")
        Lb.place(x= X + 80, y = Y + 60)
        self.Date2 = tk.Entry(self.window, bg = 'white', font=("Arial", 12), textvariable = date_var2)
        date_var2.set(D2)
        self.Date2.place(x = X + 80, y = Y + 90)      
        
        Lb = tk.Label(self.window,bg = 'skyblue',
                          font=("Arial", 12), text = "Concepto:")
        Lb.place(x= X + 335, y = Y)
        self.Worker_list = tk.Listbox(self.window,
                      bg = 'white', fg = 'black', height = 3,
                      selectmode = 'SINGLE',
                      width = 25, font=("Arial", 12))
        Workers = ['Francisco', 'Guadalupe', 'Diego']
        for item in Workers:
            self.Worker_list.insert(tk.END, item)    
        self.Worker_list.place(x = X + 335, y = Y + 30)
        self.Worker_list.bind("<ButtonRelease-1>", self.update_table)
        
        ###### Tabla de Salarios ######
        Lb = tk.Label(self.window,bg = 'skyblue',
                          font=("Arial", 12), text = "Salarios:")
        Lb.place(x= X + 663, y = Y)
        Fecha = self.Date1.get()
        Fecha1 = Fecha[6:10]+"-"+Fecha[3:5]+"-"+Fecha[0:2]
        Fecha = self.Date2.get()
        Fecha2 = Fecha[6:10]+"-"+Fecha[3:5]+"-"+Fecha[0:2]
        try:
            SelectQuery = "SELECT Responsable, SUM(Monto) AS Salario FROM Transactions.dbo.Transactions \
                where Concepto = 'Sueldo' and Fecha between '"+ Fecha1 \
                    + "' and '" + Fecha2 + "' GROUP BY Responsable;"
            Data = pd.read_sql(SelectQuery, conn)
        except:
            df ={'Responsable':['Francisco', 'Guadalupe', 'Diego'],'Salario':['','','']}
            Data = pd.DataFrame(df)
        
        tframe_sal = tk.Frame(self.window,
                      bg ="blue",
                      highlightcolor = "blue") 
        tframe_sal.place(x = X + 663, y = Y + 30,
                     height = 130, width = 318)
        rec, col = Data.shape
        aux = dict()
        data = dict()     
        for i in range(rec):
            for j in range(col):
                aux [Data.columns[j]] = Data.values[i,j]
            data['rec'+str(i+1)] = aux.copy()
    
        self.model_sal = TableModel()    
        self.table_sal = TableCanvas(tframe_sal, cellbackgr='white', 
        			thefont=('Arial',12, ), cellwidth = 140 ,
                    rowheight=25, rowheaderwidth=30,
        			rowselectedcolor='yellow', editable=False,
                    model = self.model_sal)
        self.table_sal.createTableFrame()
        self.model_sal = self.table_sal.model
        self.model_sal.importDict(data)
        self.table_sal.show()
        
        ###### Tabla de Actividades ######
        try:
            SelectQuery = "SELECT #, Fecha, Concepto, Monto, Responsable, Comentario FROM Transactions.dbo.Transactions \
                where Concepto = 'Sueldo' and Responsable = '" + self.Worker + "' and Fecha between '"+ Fecha1 \
                    + "' and '" + Fecha2 + "';"
            Data = pd.read_sql(SelectQuery, conn)
        except:
            df ={'#':[''],'Fecha':[''],'Concepto':[''],'Monto':[''],'Responsable':[''],'Comentario':[''] }
            Data = pd.DataFrame(df)
        
        tframe_act = tk.Frame(self.window,
                      bg ="blue",
                      highlightcolor = "blue") 
        tframe_act.place(x = X + 80, y = Y + 135,
                     height = 350, width = 900)
        rec, col = Data.shape
        aux = dict()
        data = dict()     
        for i in range(rec):
            for j in range(col):
                aux [Data.columns[j]] = Data.values[i,j]
            data['rec'+str(i+1)] = aux.copy()
    
        self.model_act = TableModel()    
        self.table_act = TableCanvas(tframe_act, cellbackgr='white', 
        			thefont=('Arial',12, ), cellwidth = 140 ,
                    rowheight=25, rowheaderwidth=30,
        			rowselectedcolor='yellow', editable=False,
                    model = self.model_act)
        self.table_act.createTableFrame()
        self.model_act = self.table_act.model
        self.model_act.importDict(data)
        self.table_act.show()
        
    def update_table(self, event):
        widget = event.widget
        selection=widget.curselection()
        self.Worker = widget.get(selection[0])
        Fecha = self.Date1.get()
        Fecha1 = Fecha[6:10]+"-"+Fecha[3:5]+"-"+Fecha[0:2]
        Fecha = self.Date2.get()
        Fecha2 = Fecha[6:10]+"-"+Fecha[3:5]+"-"+Fecha[0:2]
        
        try:
            SelectQuery = "SELECT #, Fecha, Concepto, Monto, Responsable, Comentario FROM Transactions.dbo.Transactions \
                where Concepto = 'Sueldo' and Responsable = '" + self.Worker + "' and Fecha between '"+ Fecha1 \
                    + "' and '" + Fecha2 + "';"
            Data = pd.read_sql(SelectQuery, conn)
        except:
            df ={'#':[''],'Fecha':[''],'Concepto':[''],'Monto':[''],'Responsable':[''],'Comentario':[''] }
            Data = pd.DataFrame(df)
        rec, col = Data.shape
        aux = dict()
        data = dict()
        
        for i in range(rec):
            for j in range(col):
                aux [Data.columns[j]] = Data.values[i,j]
            data['rec'+str(i+1)] = aux.copy()
        self.model_act.deleteRows(range(0,self.model_act.getRowCount()))
        self.model_act.importDict(data)
        self.table_act.redraw()
        
        try:
            SelectQuery = "SELECT Responsable, SUM(Monto) AS Salario FROM Transactions.dbo.Transactions \
                where Concepto = 'Sueldo' and Fecha between '"+ Fecha1 \
                    + "' and '" + Fecha2 + "' GROUP BY Responsable;"
            Data = pd.read_sql(SelectQuery, conn)
        except:
            df ={'Responsable':['Francisco', 'Guadalupe', 'Diego'],'Salario':['','','']}
            Data = pd.DataFrame(df)
        rec, col = Data.shape
        aux = dict()
        data = dict()
        
        for i in range(rec):
            for j in range(col):
                aux [Data.columns[j]] = Data.values[i,j]
            data['rec'+str(i+1)] = aux.copy()
        self.model_sal.deleteRows(range(0,self.model_sal.getRowCount()))
        self.model_sal.importDict(data)
        self.table_sal.redraw()
        
class GraphsGenerator():
    
    def __init__(self, Graphs):
        #Crea 4 framespara las graficas, 4 selectores de opciones
        height = 287
        width = 600
        Graphs_list = ["Ganancias x Mes", "Egresos x Mes", "Ingresos x Empleado", "Ingresos x Concepto", "Egresos x Concepto"]
        Date = tk.StringVar()
        
        self.Window = Graphs
        
        self.Frame_1= tk.Frame(self.Window,
                               bg ="skyblue",
                               highlightcolor = "skyblue") 
        self.Frame_1.place(x = 0, y =0,
                 height = height, width =width)
        
        self.Frame_2= tk.Frame(self.Window,
                               bg ="red",
                               highlightcolor = "red") 
        self.Frame_2.place(x = width, y =0,
                 height = height, width =width)
        
        self.Frame_3= tk.Frame(self.Window,
                               bg ="green",
                               highlightcolor = "green") 
        self.Frame_3.place(x = 0, y = height,
                 height = height, width =width)
        
        self.Frame_4= tk.Frame(self.Window,
                               bg ="yellow",
                               highlightcolor = "yellow") 
        self.Frame_4.place(x = width, y = height,
                 height = height, width =width)
        
        self.Combo_1 = tk.ttk.Combobox(self.Window, state = "readonly")
        self.Combo_1.place(height = 25, width = 150, x = width - 155, y = height - 30)
        self.Combo_1["values"] = Graphs_list
        
        self.Combo_2 = tk.ttk.Combobox(self.Window, state = "readonly")
        self.Combo_2.place(height = 25, width = 150, x = width + 5, y = height - 30)
        self.Combo_2["values"] = Graphs_list
        
        self.Combo_3 = tk.ttk.Combobox(self.Window, state = "readonly")
        self.Combo_3.place(height = 25, width = 150, x = width - 155, y = height + 5)
        self.Combo_3["values"] = Graphs_list
        
        self.Combo_4 = tk.ttk.Combobox(self.Window, state = "readonly")
        self.Combo_4.place(height = 25, width = 150, x = width + 5, y = height + 5)
        self.Combo_4["values"] = Graphs_list
        
        Lb = tk.Label(self.Frame_1, bg = 'skyblue',
                          font=("Arial", 12), text = "Fecha:")
        Lb.place(x = 450, y = 90)
        self.Date_1 = tk.Entry(self.Frame_1, bg = 'white', font=("Arial", 12), textvariable = Date)
        Date.set(str( date.today().strftime("%m/%Y") ))
        self.Date_1.place(x = 450, y = 130, width = 100)
        
        self.Ganancias_Mes(self.Frame_1, self.Date_1.get() )
        
    def Ganancias_Mes(self, Frame, Date):
        Year = Date[3:]
        SelectQuery = "SELECT MONTH(Fecha) as 'Month', SUM(Monto) as 'Earns' FROM Transactions.dbo.Transactions WHERE YEAR(Fecha) = " + Year + " GROUP BY MONTH(Fecha)"
        Data = pd.read_sql(SelectQuery, conn)
        Y = np.zeros(12)
        Y[Data['Month'] - 1] = Data['Earns'] /1000
        
        fig = Figure(figsize = (5,5), dpi = 100)
        ax0 = fig.add_axes( (0.15, .15, .8, .8), frameon=True)
        
        X = np.arange(1, 13, 1)
        Lab = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        ax0.barh(y =X[::-1], width = Y, tick_label = Lab, height = .95, color = 'c' ) 
        ax0.set_ylabel( 'Año: ' + Year )
        ax0.set_xlabel( 'Ganancias en Miles de Pesos' )
        for index, value in enumerate(Y[::-1]):
            ax0.text( 5, index + .72, str(value))
        
        canvas = FigureCanvasTkAgg(fig, master = Frame)
        canvas.draw()
        canvas.get_tk_widget().place(height = 287, width = 445, x = 0, y = 0)
        
        
        
        

#Define the callback functions for the buttons on the main page
def Edit_record():    
    class Edit_win():
        
        def __init__(self, Main):
            
            rclicked = MainTable.currentrow
            Rec = MainTableModel.getRecordAtRow(rclicked)
            
            self.Key = Rec['#']
            date_var = tk.StringVar()
            concept_var = tk.StringVar()
            mount_var = tk.StringVar()
            responsible_var = tk.StringVar()
            client_var = tk.StringVar()
            rate_var = tk.StringVar()
            km_var = tk.StringVar()
            comment_var = tk.StringVar()
            self.Type = Rec['Tipo']
                        
            self.window = tk.Toplevel(Main)
            self.window.configure(background = 'skyblue')
            self.window.title("Editar Registro")
            self.window.geometry('500x350')
           
            Lb = tk.Label(self.window,bg = 'skyblue',
                          font=("Arial", 12), text = "Concepto:")
            Lb.place(x= 50, y = 25, width = 100)
            self.Concept = tk.Entry(self.window, bg = 'white', font=("Arial", 12),
                            textvariable = concept_var, width = 25)
            concept_var.set(Rec['Concepto'])
            self.Concept.place(x = 200, y = 25)
            
            Lb = tk.Label(self.window,bg = 'skyblue',
                          font=("Arial", 12), text = "Fecha:")
            Lb.place(x= 50, y = 55, width = 100)
            self.Date = tk.Entry(self.window, bg = 'white', font=("Arial", 12),
                            textvariable = date_var, width = 25)
            date_var.set(Rec['Fecha'])
            self.Date.place(x = 200, y = 55)
                        
            Lb = tk.Label(self.window,bg = 'skyblue',
                          font=("Arial", 12), text = "Monto:")
            Lb.place(x= 50, y = 85, width = 100)
            self.Mount = tk.Entry(self.window, bg = 'white', font=("Arial", 12),
                            textvariable = mount_var, width = 25)
            mount_var.set(Rec['Monto'])
            self.Mount.place(x = 200, y = 85)
            
            Lb = tk.Label(self.window,bg = 'skyblue',
                          font=("Arial", 12), text = "Responsable:")
            Lb.place(x= 50, y = 115, width = 100)
            self.Responsible = tk.Entry(self.window, bg = 'white', font=("Arial", 12),
                            textvariable = responsible_var, width = 25)
            responsible_var.set(Rec['Responsable'])
            self.Responsible.place(x = 200, y = 115)
            
            Lb = tk.Label(self.window,bg = 'skyblue',
                          font=("Arial", 12), text = "Cliente:")
            Lb.place(x= 50, y = 145, width = 100)
            self.Client = tk.Entry(self.window, bg = 'white', font=("Arial", 12),
                            textvariable = client_var, width = 25)
            client_var.set(Rec['Cliente'])
            self.Client.place(x = 200, y = 145)
            
            Lb = tk.Label(self.window,bg = 'skyblue',
                          font=("Arial", 12), text = "Prorrateo:")
            Lb.place(x= 50, y = 175, width = 100)
            self.Rate = tk.Entry(self.window, bg = 'white', font=("Arial", 12),
                            textvariable = rate_var, width = 25)
            rate_var.set(Rec['Prorrateo'])
            self.Rate.place(x = 200, y = 175)
            
            Lb = tk.Label(self.window,bg = 'skyblue',
                          font=("Arial", 12), text = "Km:")
            Lb.place(x= 50, y = 205, width = 100)
            self.Km = tk.Entry(self.window, bg = 'white', font=("Arial", 12),
                            textvariable = km_var, width = 25)
            km_var.set(Rec['Km'])
            self.Km.place(x = 200, y = 205)
            
            Lb = tk.Label(self.window,bg = 'skyblue',
                          font=("Arial", 12), text = "Comentario:")
            Lb.place(x= 50, y = 235, width = 100)
            self.Comment = tk.Entry(self.window, bg = 'white', font=("Arial", 12),
                            textvariable = comment_var, width = 25)
            comment_var.set(Rec['Comentario'])
            self.Comment.place(x = 200, y = 235)
     
            Record = tk.Button(self.window, text= "Registrar", bg="white", fg="black",
                                font=("Arial", 14), 
                                command = self.record_egress)
            Record.place(height=50, width = 100, x=200, y=275)
            
        def record_egress(self):
            Data =[str(self.Key),
                   "'" + self.Date.get() + "'",
                   "'" + self.Concept.get() + "'",
                   str(self.Mount.get()),
                   "'" + self.Responsible.get()[:12] + "'",
                   "'" + self.Client.get() + "'",
                   "'" + self.Km.get() + "'",
                   "'" + self.Rate.get() + "'",
                   "'" + self.Comment.get() + "'",
                   "'" + self.Type + "'"]
            
            try:
                M2.update_record(Data, conn, cursor)
                tk.messagebox.showinfo(title="Exito", message="Operación Registrada")
                Ex = pd.read_sql(Read_records_query, conn)
                Ex['Fecha'] = pd.to_datetime(Ex['Fecha']).dt.strftime('%d/%m/%Y')
                values = M2.GetValues(conn)
                M1.UpdateLabels(Values_labels, values)
                M1.UpdateTable(MainTable, MainTableModel, Ex)
            except:
                tk.messagebox.showinfo(title="Error", message="Error en registrar")
                                
    Edit_window = Edit_win(Main)
def create_ingress_window():
    
    class In_win():
        
        def __init__(self, Main):
            date_var = tk.StringVar()
            self.Select_Worker = None
            self.Select_Concept = None
            
            self.window = tk.Toplevel(Main)
            self.window.configure(background = 'lightgreen')
            self.window.title("Registrar Ingreso")
            self.window.geometry('450x500')
           
            Lb = tk.Label(self.window,bg = 'lightgreen',
                          font=("Arial", 12),
                          text = "Concepto:"+6*"\n"+"Fecha:\n\nMonto:\n\n"
                          +"Responsable: \n\n\n\n\n Cliente:\n\n Salario del\n responsable:\n\n Comentario\n(Ayudante):")
            Lb.place(x= 45, y = 30)
            
            self.Concept = tk.Listbox(self.window,
                          bg = 'white', fg = 'black', height = 5,
                          selectmode = 'SINGLE',
                          width = 25, font=("Arial", 12))
            Concepts = ['Dx ECO', 'IATF', 'Fertilidad', 'Conge. Semen', 'Transf. de Embriones']
            for item in Concepts:
                self.Concept.insert(tk.END, item)         
            self.Concept.place(x = 150, y = 30)
            self.Concept.bind("<ButtonRelease-1>", self.save_concept)
            
            self.Date = tk.Entry(self.window, bg = 'white', font=("Arial", 12),
                            textvariable = date_var)
            date_var.set(str( date.today().strftime("%d/%m/%Y") ) )
            self.Date.place(x = 150, y = 143)
            
            self.Mount = tk.Entry(self.window, bg = 'white', font=("Arial", 12))
            self.Mount.place (x = 150, y = 175, height = 25, width = 100)
            
            self.Worker = tk.Listbox(self.window,
                      bg = 'white', fg = 'black', height = 4,
                      selectmode = 'SINGLE',
                      width = 25, font=("Arial", 12))
            Workers = ['Alfonso', 'Francisco', 'Guadalupe', 'Diego']
            for item in Workers:
                self.Worker.insert(tk.END, item)    
            self.Worker.place(x = 150, y = 210)
            self.Worker.bind("<ButtonRelease-1>", self.save_worker)
            
            self.Client = tk.Entry(self.window, bg = 'white', font=("Arial", 12))
            self.Client.place (x = 150, y = 300, height = 25, width = 250)
            
            self.Salary = tk.Entry(self.window, bg = 'white', font=("Arial", 12))
            self.Salary.place (x = 150, y = 350, height = 25, width = 100)
            
            self.Comment = tk.Entry(self.window, bg = 'white', font=("Arial", 12))
            self.Comment.place (x = 150, y = 397, height = 25, width = 250)
            
            Record = tk.Button(self.window, text= "Registrar", bg="white", fg="black",
                               font=("Arial", 14), 
                               command = self.record_ingress)
            Record.place(height=50, width = 100, x=180, y=435)
        
        def save_concept(self, event):
            widget = event.widget
            selection=widget.curselection()
            self.Select_Concept = widget.get(selection[0])

        def save_worker(self, event):
            widget = event.widget
            selection=widget.curselection()
            self.Select_Worker = widget.get(selection[0])
            
        def record_ingress(self):
            Data =[self.Date.get(),
                   self.Select_Concept,
                   self.Mount.get(),
                   self.Select_Worker,
                   self.Client.get(),
                   self.Salary.get(),
                   self.Comment.get()]
            
            if self.Select_Concept == None:
                tk.messagebox.showerror(message = "Falta Concepto")
            elif self.Select_Worker ==None:
                tk.messagebox.showerror(message = "Falta Responsable")
            elif Data[2] == None:
                tk.messagebox.showerror(message = "Falta Monto")
            elif self.Select_Worker == 'Alfonso' and  Data[5] > '' and Data[6] == '':
                tk.messagebox.showerror(message = "Falta Responsable en comentario")
            else:
                try:
                    M2.upload_ingress(Data, conn, cursor)
                    self.Select_Concept = None
                    self.Select_Worker = None
                    self.Mount.delete(0,tk.END)
                    self.Client.delete(0,tk.END)
                    self.Salary.delete(0,tk.END)
                    self.Comment.delete(0,tk.END)
                    tk.messagebox.showinfo(title="Exito", 
                                           message="Operación Registrada")
                    Ex = pd.read_sql(Read_records_query, conn)
                    Ex['Fecha'] = pd.to_datetime(Ex['Fecha']).dt.strftime('%d/%m/%Y')
                    values = M2.GetValues(conn)
                    M1.UpdateLabels(Values_labels, values)
                    M1.UpdateTable(MainTable, MainTableModel, Ex)
                except:
                    tk.messagebox.showinfo(title="Error", 
                                           message="Error en registrar")
                
                
    Ingress_window = In_win(Main) 
def create_egress_window():
    
    class Eg_win():
        
        def __init__(self, Main):
            date_var = tk.StringVar()
            self.Select_Worker = None
            self.Select_Concept = None
            
            self.window = tk.Toplevel(Main)
            self.window.configure(background = 'lightcoral')
            self.window.title("Registrar Egreso")
            self.window.geometry('450x560')
           
            Lb = tk.Label(self.window,bg = 'lightcoral',
                          font=("Arial", 12), text = "Concepto:")
            Lb.place(x= 45, y = 25)
            self.Concept = tk.Listbox(self.window,
                          bg = 'white', fg = 'black', height = 10,
                          selectmode = 'SINGLE',
                          width = 25, font=("Arial", 12))
            Concepts = ['Gasolina', 'Viaticos', 'Serv. y Refac.', 'Consumibles', 'Equipo', 'Impuestos', 'Capacitaciones', 'Seguros', 'Sueldo', 'Otros']
            for item in Concepts:
                self.Concept.insert(tk.END, item)         
            self.Concept.place(x = 150, y = 25)
            self.Concept.bind("<ButtonRelease-1>", self.save_concept)
            
            y=235
            self.Date = tk.Entry(self.window, bg = 'white', font=("Arial", 12),
                            textvariable = date_var)
            date_var.set(str( date.today().strftime("%d/%m/%Y") ) )
            self.Date.place(x = 150, y = y)
            Lb = tk.Label(self.window,bg = 'lightcoral',
                          font=("Arial", 12), text = "Fecha:")
            Lb.place(x= 45, y = y)
            
            y=265
            self.Mount = tk.Entry(self.window, bg = 'white', font=("Arial", 12))
            self.Mount.place (x = 150, y = y, height = 25, width = 100)
            Lb = tk.Label(self.window,bg = 'lightcoral',
                          font=("Arial", 12), text = "Monto:")
            Lb.place(x= 45, y = y)
            
            y=300
            self.Worker = tk.Listbox(self.window,
                      bg = 'white', fg = 'black', height = 4,
                      selectmode = 'SINGLE',
                      width = 25, font=("Arial", 12))
            Workers = ['Alfonso', 'Francisco', 'Guadalupe', 'Diego']
            for item in Workers:
                self.Worker.insert(tk.END, item)    
            self.Worker.place(x = 150, y = y)
            self.Worker.bind("<ButtonRelease-1>", self.save_worker)
            Lb = tk.Label(self.window,bg = 'lightcoral',
                          font=("Arial", 12), text = "Responsable:")
            Lb.place(x= 45, y = y)
            
            y=390
            self.Km = tk.Entry(self.window, bg = 'white', font=("Arial", 12))
            self.Km.place (x = 150, y = y, height = 25, width = 250)
            Lb = tk.Label(self.window,bg = 'lightcoral',
                          font=("Arial", 12), text = "Km:")
            Lb.place(x= 45, y = y)
            
            y=425
            self.Rate = tk.Entry(self.window, bg = 'white', font=("Arial", 12))
            self.Rate.place (x = 150, y = y, height = 25, width = 100)
            Lb = tk.Label(self.window,bg = 'lightcoral',
                          font=("Arial", 12), text = "Prorrateo:")
            Lb.place(x= 45, y = y)
            
            y=460
            self.Comment = tk.Entry(self.window, bg = 'white', font=("Arial", 12))
            self.Comment.place (x = 150, y = y, height = 25, width = 250)
            Lb = tk.Label(self.window,bg = 'lightcoral',
                          font=("Arial", 12), text = "Comentario:")
            Lb.place(x= 45, y = y)
            
            y=500
            Record = tk.Button(self.window, text= "Registrar", bg="white", fg="black",
                                font=("Arial", 14), 
                                command = self.record_egress)
            Record.place(height=50, width = 100, x=175, y=y)
        
        def save_concept(self, event):
            widget = event.widget
            selection=widget.curselection()
            self.Select_Concept = widget.get(selection[0])

        def save_worker(self, event):
            widget = event.widget
            selection=widget.curselection()
            self.Select_Worker = widget.get(selection[0])
            
        def record_egress(self):
            Data =[self.Date.get(),
                   self.Select_Concept,
                   self.Mount.get(),
                   self.Select_Worker,
                   self.Km.get(),
                   self.Rate.get(),
                   self.Comment.get()]
            if self.Select_Concept == None:
                tk.messagebox.showerror(message = "Falta Concepto")
            elif self.Select_Worker ==None:
                tk.messagebox.showerror(message = "Falta Responsable")
            elif Data[2] == None:
                tk.messagebox.showerror(message = "Falta Monto")
            else:
                try:
                    M2.upload_egress(Data, conn, cursor)
                    self.Select_Concept = None
                    self.Select_Worker = None
                    self.Mount.delete(0,tk.END)
                    self.Km.delete(0,tk.END)
                    self.Rate.delete(0,tk.END)
                    self.Comment.delete(0,tk.END)
                    tk.messagebox.showinfo(title="Exito", message="Operación Registrada")
                    Ex = pd.read_sql(Read_records_query, conn)
                    Ex['Fecha'] = pd.to_datetime(Ex['Fecha']).dt.strftime('%d/%m/%Y')
                    values = M2.GetValues(conn)
                    M1.UpdateLabels(Values_labels, values)
                    M1.UpdateTable(MainTable, MainTableModel, Ex)
                    self.window.lift
                except:
                    tk.messagebox.showinfo(title="Error", message="Error en registrar")
                    self.window.deiconify
                    
                                
    Egress_window = Eg_win(Main)

conn, cursor = M2.connect_db()
Read_records_query = "Select * From Transactions.dbo.Transactions order by Fecha desc, # desc;"

#Create the Tkinter "Root" object which work as  main page for the app
Root = tk.Tk()
Root.title("Registro de cuentas")
Root.geometry('1200x600') 

#Create the notebook where sheets will be contain
nb = tk.ttk.Notebook(Root)
nb.pack(fill = "both", expand = "yes")

#Create and add the sheets
Main = tk.Frame(nb, background="skyblue")
Salaries = tk.Frame(nb, background = "skyblue")
Graphs = tk.Frame(nb, background = "skyblue")

nb.add(Main, text = "Registros")
nb.add(Salaries, text = "Salarios")
nb.add(Graphs, text = "Graficas")

#Use Module1 functions to create all the widgets on the main page
values = M2.GetValues(conn)
Values_labels = M1.Insert_main_labels(lb_wt=200, lb_ht=50, 
                      x_offset = 50, y_offset = 50, 
                      main_wt = 1200,values = values, Main = Main)
M1.Insert_main_buttoms(Main, 
                       Edit_record, 
                       create_ingress_window, 
                       create_egress_window)
btn_delete = deleteButton(Main)

Ex = pd.read_sql(Read_records_query, conn)
Ex['Fecha'] = pd.to_datetime(Ex['Fecha']).dt.strftime('%d/%m/%Y')
MainTable, MainTableModel = M1.CreateTable(Main, Ex)

#Use SalariesCalculator class to create second window
SalaryTable = SalariesCalculator(Salaries)

#Use GraphsGenerator class to create second window
GraphsPage = GraphsGenerator(Graphs)


Main.mainloop()
