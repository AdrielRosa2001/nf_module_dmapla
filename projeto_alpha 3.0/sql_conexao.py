import pyodbc

class ServerDB():

    cursor = None
    sessao = False
    database_name = "SICNET_139726"
    #money_convert = lambda x: "R$ "+str(round(x, 2)).replace(".", ",")

    def __init__(self):
        driver = "{SQL Server}" #"{ODBC Driver 18 for SQL Server}" #"{SQL Server}"
        server = "WIN-G1DK700PUJ5\SQLEXPRESS" #"DESKTOP-BOE9DIN\SQLEXPRESS"
        port = "55215" #"55215"
        database = "SICNET_139726"
        user = "sicnet" #"sicnet"
        password = "Sic12345"
        string_conection = "DRIVER={SQL Server};"+f"SERVER={server},{port};DATABASE={database};UID={user};PWD={password};PORT={port}"
        conn = pyodbc.connect(string_conection)
        #conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-BOE9DIN\SQLEXPRESS,35980;DATABASE=SICNET_139726;UID=ADMIN;PWD=Ab04042112#;PORT=35980')
        print("Server DB connected")
        self.sessao = True
        self.cursor = conn.cursor()
    
    def time_refine(self, x):
        return str(x).split(".")[0]

    def validate_money_value(self, x): 
        if x != None:
            return (("R$ "+str(round(x, 2)).replace(".", ",")), float(x))     
        else:
            return ("R$ 0,00", 0)
    
    def testeConsultas(self, querry):
        if self.sessao == True:
            self.cursor.execute(querry)
            #dados = self.cursor.fetchall()
            dados = self.cursor.fetchall()
            return dados
    
    def consultaNotas(self, mes, ano):
        if self.sessao == True:
            self.cursor.execute(f"SELECT [pedido] FROM [SICNET_139726].[dbo].[TABEST3A] WHERE YEAR(data) = {ano} AND MONTH(data) = {mes} AND [lkreceb] IN (8, 5, 10, 13) AND [lkcliente] = 0 AND [nota] IS NULL;")
            #dados = self.cursor.fetchall()
            dados = self.cursor.fetchall()
            return dados
    
    def consultaNotasDinheiro(self, quanttity, mes, ano):
        if self.sessao == True:
            self.cursor.execute(f"SELECT TOP ({quanttity}) [pedido] FROM [SICNET_139726].[dbo].[TABEST3A] WHERE YEAR(data) = {ano} AND MONTH(data) = {mes} AND [lkreceb] IN (2, 9) AND [lkcliente] = 0 AND [nota] IS NULL;")
            #dados = self.cursor.fetchall()
            dados = self.cursor.fetchall()
            return dados
        
            






