# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 21:33:14 2020

@author: TOSHIBA
"""

import pyodbc
import pandas as pd

def num2MX(value):
    for j in range(len(value)):
        aux = ""
        coma = 0
        for i in range(len(value[j])-1, -1, -1):
            if coma == 3:
               aux = "," + aux
               coma = 0
            aux = value[j][i] + aux 
            coma =coma+1
        value[j] = "$" + aux
    return value
    
def connect_db():
    
    # conn = pyodbc.connect('Driver={SQL Server};'
    #                   'Server=LAP-ALFONSO\SQLEXPRESS;'
    #                   'Database=Transactions;'
    #                   'Trusted_Connection=yes;')    # LAP-MORA 
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-K3FSM8U\SQLEXPRESS;'
                      'Database=Transactions;'
                      'Trusted_Connection=yes;')    # LAP-RODRIGO
    try:
        cursor = conn.cursor()
        return conn, cursor
    except:
        print ("Unable to connect")

def upload_ingress(data, conn, cursor):
    key = int(pd.read_sql("SELECT MAX(#) FROM Transactions.dbo.Transactions;", conn)[""]) + 1
    Fecha = data[0]
    Fecha = Fecha[6:10]+"-"+Fecha[3:5]+"-"+Fecha[0:2]
    Concepto = data[1]
    Monto = data[2]
    Responsable = data[3]
    Cliente = data[4]
    Sueldo = data[5]
    Comentario = data[6]
    
    insertQuery = "INSERT INTO Transactions.dbo.Transactions " \
        "VALUES (" + str(key) + ",'" + Fecha + "','" + Concepto + "',"+ Monto + ",'"+ Responsable\
        +"','"+ Cliente + "','','','" + Comentario + "','Ingreso');"
    cursor.execute(insertQuery)
    conn.commit()
    
    if Responsable != "Alfonso":
        insertQuery = "INSERT INTO Transactions.dbo.Transactions " \
            "VALUES (" + str(key+1) + ",'" + Fecha + "','Sueldo',-" + Sueldo + ",'" + Responsable\
            +"', '', '', '','" + Concepto + "-" + Cliente + "','Egreso');"
        cursor.execute(insertQuery)
        conn.commit()
    elif Sueldo != "" and Responsable == "Alfonso":
        insertQuery = "INSERT INTO Transactions.dbo.Transactions " \
            "VALUES (" + str(key+1) + ",'" + Fecha + "','Sueldo',-" + Sueldo + ",'" + Comentario\
            +"', '', '', '','" + Concepto + "-" + Cliente + "','Egreso');"
        cursor.execute(insertQuery)
        conn.commit()

def upload_egress(data, conn, cursor):
    key = int(pd.read_sql("SELECT MAX(#) FROM Transactions.dbo.Transactions;", conn)[""]) + 1
    Fecha = data[0]
    Fecha = "'"+Fecha[6:10]+"-"+Fecha[3:5]+"-"+Fecha[0:2]+"'"
    Concepto ="'"+data[1]+"'"
    Monto = data[2]
    Responsable ="'"+data[3]+"'"
    Km = "'"+data[4]+"'"
    Rate = "'"+data[5]+"'"
    Comment = "'"+data[6]+"'"
    
    
    insertQuery = "INSERT INTO Transactions.dbo.Transactions " \
        "VALUES (" + str(key) + "," + Fecha + "," + Concepto + ",-"+ Monto + ","+ Responsable\
        +",'',"+ Rate + ","+ Km + "," + Comment +  ",'Egreso');"
    cursor.execute(insertQuery)
    conn.commit()
    
    if Concepto == "'Equipo'":
        insertQuery = "INSERT INTO Transactions.dbo.Transactions " \
            "VALUES (" + str(key+1) + "," + Fecha + "," + Comment + ","+ Monto + ","+ Responsable\
            +",'',"+ Rate + ",'','','Equipo');"
        cursor.execute(insertQuery)
        conn.commit()

def GetValues(conn):
    value = list()
    value.append(str(int(pd.read_sql("SELECT SUM(Monto) FROM Transactions.dbo.Transactions WHERE Tipo = 'Ingreso';", conn)[""])))
    value.append(str(int(pd.read_sql("SELECT SUM(Monto) FROM Transactions.dbo.Transactions WHERE Tipo = 'Egreso';", conn)[""])))
    value.append(str(int(pd.read_sql("SELECT SUM(Monto) FROM Transactions.dbo.Transactions WHERE Tipo = 'Equipo';", conn)[""])))
    value.append(str(0))
    value.append(str( int(value[0]) + int(value[1])))
    value.append(str( int(value[4]) + int(value[2]) + int(value[3])))
    return num2MX(value)

def update_record(data, conn, cursor):
    data[1] = data[1][5:11]+"-"+data[1][4:6]+"-"+data[1][1:3]
    updateQuery = "UPDATE Transactions.dbo.Transactions\n" \
        "SET Fecha =" + data[1] + ", " + \
            "\nConcepto =" + data[2] + ", " + \
            "\nMonto =" + data[3] + ", " + \
            "\nResponsable =" + data[4] + ", " + \
            "\nCliente =" + data[5] + ", " + \
            "\nProrrateo =" + data[6] + ", " + \
            "\nKm =" + data[7] + ", " + \
            "\nComentario =" + data[8] + ", " + \
            "\nTipo =" + data[9] + \
        "\nWHERE # =" + data[0] + ";"
    cursor.execute(updateQuery)
    conn.commit()
    
    pass
    
