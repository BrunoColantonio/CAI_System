import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
from tkinter.font import Font
import sqlite3
from fpdf import FPDF
from datetime import datetime
import os

def capitalize_string(string):
    string_aux = string
    string_aux = string_aux.lower()
    string_aux = string_aux.split(" ")
    string = ""
    for i in string_aux:
        string += i.capitalize() + " "
    string = string[:-1]
    
    return string

def is_valid_date(number):
    number = str(number)
    size = len(number)
    if(size < 8):
        return False
    else:
        return True

def format_date(date):
    day = int(date[:2])
    month = int(date[2:4])
    year = int(date[4:])

    formatted_date = datetime(day = day,
                            month = month,
                            year = year)

    return (formatted_date.strftime('%d/%m/%Y')) 

def validate_art(art):
    ## validate ART name
    conn = sqlite3.connect('..\database\cai_database.db')
    art = art.upper()
    if(art == '-'):
        art = 'PARTICULAR'
    query = f"SELECT Id FROM Art WHERE Nombre = '{art}' "
    cursor = conn.execute(query)
    data = cursor.fetchone()
            
    if(data == None):
        return False, art
    else:
        return True, data[0]
    
def dni_is_valid(dni):
    conn = sqlite3.connect('..\database\cai_database.db')
    query = f"SELECT Dni FROM Paciente WHERE Dni = {dni} "
    cursor = conn.execute(query)
    data = cursor.fetchone()
    
    #already exists one person with that dni
    if(data != None):
        return False
    else:
        return True

def get_pacient(obj, query_arg):
        conn = sqlite3.connect('..\database\cai_database.db')
        
        if(query_arg =='dni'):
            dni = int(obj.entry_dni_var.get())
            query = f'''SELECT P.Dni, P.Nombre, P.Apellido, A.Nombre, P.Siniestro,
                    P.Puesto_Trabajo, P.Fecha_Accidente, P.Telefono, P.Dr_derivante,
                    P.Fecha_Inicio, P.Empresa, P.Domicilio, P.Edad
                    FROM Paciente P
                    INNER JOIN Art A on P.Art = A.Id
                    WHERE P.Dni = {dni} '''
                    
        else:
            name = capitalize_string(obj.entry_name_var.get())
            
            surname = capitalize_string(obj.entry_surname_var.get())
            
            query = f'''SELECT P.Dni, P.Nombre, P.Apellido, A.Nombre, P.Siniestro, 
                    P.Puesto_Trabajo, P.Fecha_Accidente, P.Telefono, P.Dr_derivante,
                    P.Fecha_Inicio, P.Empresa, P.Domicilio, P.Edad
                    FROM Paciente P
                    INNER JOIN Art A on P.Art = A.Id
                    WHERE P.Nombre = '{name}' AND P.Apellido = '{surname}' '''
            
        cursor = conn.execute(query)
        data = cursor.fetchone()
        if(data == None and query_arg == 'dni'):
            messagebox.showerror(title = 'Error: Dni no valido', message = f'No existe el paciente con dni: {dni}')
        elif(data == None and query_arg == 'fullname'):
            messagebox.showerror(title = 'Error: Nombre no valido', message = f'No existe el paciente con nombre: {surname}, {name}')
        else:
            # parse data
            obj.dni_text_var.set(data[0])
            obj.name_text_var.set(data[1])
            obj.surname_text_var.set(data[2])
            obj.art_text_var.set(data[3])
            obj.siniester_text_var.set(data[4])
            obj.job_text_var.set(data[5])
            obj.accident_date_text_var.set(data[6])
            obj.phone_text_var.set(data[7])
            obj.dr_text_var.set(data[8])
            obj.start_date_text_var.set(data[9])
            obj.company_text_var.set(data[10])
            obj.address_text_var.set(data[11])
            obj.age_text_var.set(data[12])
            
        
        conn.close()

def get_pacient_event(obj, event, query_arg):
    conn = sqlite3.connect('..\database\cai_database.db')
        
    if(query_arg =='dni'):
        dni = int(obj.entry_dni_var.get())
        query = f'''SELECT P.Dni, P.Nombre, P.Apellido, A.Nombre, P.Siniestro,
                P.Puesto_Trabajo, P.Fecha_Accidente, P.Telefono, P.Dr_derivante,
                P.Fecha_Inicio, P.Empresa, P.Domicilio, P.Edad
                FROM Paciente P
                INNER JOIN Art A on P.Art = A.Id
                WHERE P.Dni = {dni} '''
                    
    else:
        name = capitalize_string(obj.entry_name_var.get())
            
        surname = capitalize_string(obj.entry_surname_var.get())
            
        query = f'''SELECT P.Dni, P.Nombre, P.Apellido, A.Nombre, P.Siniestro, 
                P.Puesto_Trabajo, P.Fecha_Accidente, P.Telefono, P.Dr_derivante,
                P.Fecha_Inicio, P.Empresa, P.Domicilio, P.Edad
                FROM Paciente P
                INNER JOIN Art A on P.Art = A.Id
                WHERE P.Nombre = '{name}' AND P.Apellido = '{surname}' '''
            
    cursor = conn.execute(query)
    data = cursor.fetchone()
    if(data == None and query_arg == 'dni'):
        messagebox.showerror(title = 'Error: Dni no valido', message = f'No existe el paciente con dni: {dni}')
    elif(data == None and query_arg == 'fullname'):
        messagebox.showerror(title = 'Error: Nombre no valido', message = f'No existe el paciente con nombre: {surname}, {name}')
    else:
        # parse data
        obj.dni_text_var.set(data[0])
        obj.name_text_var.set(data[1])
        obj.surname_text_var.set(data[2])
        obj.art_text_var.set(data[3])
        obj.siniester_text_var.set(data[4])
        obj.job_text_var.set(data[5])
        obj.accident_date_text_var.set(data[6])
        obj.phone_text_var.set(data[7])
        obj.dr_text_var.set(data[8])
        obj.start_date_text_var.set(data[9])
        obj.company_text_var.set(data[10])
        obj.address_text_var.set(data[11])
        obj.age_text_var.set(data[12])
            
        
    conn.close()

def get_fields(obj):
    
    accident_date = obj.accident_date_text_var.get()
    if(is_valid_date(accident_date)):
        accident_date = format_date(accident_date)
        
        dni = obj.dni_text_var.get()
            
        name = capitalize_string(obj.name_text_var.get())
                
        surname = capitalize_string(obj.surname_text_var.get())
            
        age = obj.age_text_var.get()
            
        phone = obj.phone_text_var.get()
            
        address = capitalize_string(obj.address_text_var.get())
            
        company = capitalize_string(obj.company_text_var.get())
            
        job = capitalize_string(obj.job_text_var.get())
            
        art = obj.art_text_var.get()
            
        siniester = obj.siniester_text_var.get()
            
        dr = capitalize_string(obj.dr_text_var.get())
        
        return dni,name,surname,age,phone,address,company,job,art,siniester,accident_date,dr
    
    else:
        messagebox.showerror(title = 'Error: Fecha no valida', message = 'Ingresar fecha en formato DDMMAAAA')
        return [""]
     
def clear_fields(obj):
        obj.entry_dni_var.set('')
        obj.entry_name_var.set('')
        obj.entry_surname_var.set('')
        obj.dni_text_var.set('')
        obj.name_text_var.set('')
        obj.surname_text_var.set('')
        obj.art_text_var.set('')
        obj.phone_text_var.set('')
        obj.address_text_var.set('')
        obj.company_text_var.set('')
        obj.job_text_var.set('')
        obj.siniester_text_var.set('')
        obj.accident_date_text_var.set('')
        obj.dr_text_var.set('')
        obj.start_date_text_var.set('')
        obj.age_text_var.set('')

class App(ctk.CTk):
    def __init__(self):
        # main setup
        super().__init__()
        self.title('Fichas pacientes')
        self.iconbitmap('..\images\cai_logo.ico')
        self.state('zoomed')
        ctk.set_appearance_mode("light")
        
        #widgets
        self.main = Main(self)
        
        # layout
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        
class Main(ctk.CTkTabview):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row = 0, column = 0, sticky = 'nsew')
        
        self.configure(text_color = 'black', segmented_button_selected_hover_color = "#196ef7")
        # tabs
        self.add('ASISTENCIA')
        self.add('ALTA PACIENTE')
        self.add('ALTA ART')
        self.add('BAJA')
        self.add('MODIFICAR')
        self.add('HISTORIA CLINICA')
        
        # widgets
        GenerarFichaFrame(self.tab('ASISTENCIA'))
        AltaPacienteFrame(self.tab('ALTA PACIENTE'))
        BajaPacienteFrame(self.tab('BAJA'))
        ModificarPacienteFrame(self.tab('MODIFICAR'))
        AltaARTFrame(self.tab('ALTA ART'))
        HistoriaClinica(self.tab('HISTORIA CLINICA'))
        
class GenerarFichaFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.create_widgets()
        self.create_layout()
        self.pack(expand = True, fill = 'both')
         
    def create_widgets(self):        
        self.header_label = ctk.CTkLabel(self, text = 'Generar ficha asistencia paciente', font = ("Calibri",30), compound = 'center')
        
        ## DNI entry ##
        self.enter_dni_label = ctk.CTkLabel(self, text = 'D.N.I:', font = ("Calibri",18), compound = 'center')
        self.entry_dni_var = ctk.StringVar()
        self.entry_dni = ctk.CTkEntry(self, textvariable = self.entry_dni_var,border_color='black')
        self.entry_dni.bind('<Return>', lambda event, query_arg='dni': get_pacient_event(self,event,query_arg))
        self.submit_dni_button = ctk.CTkButton(self, text = 'Enviar', command = lambda : get_pacient(self,'dni'),
                                               font = ("Calibri",15), fg_color="#4287f5",hover_color = "#196ef7",
                                               border_width=2.8,border_color="black",text_color='black')
        
        ## Name entry ##
        self.enter_name_label = ctk.CTkLabel(self, text = 'NOMBRE:', font = ("Calibri",18), compound = 'center')
        self.enter_surname_label = ctk.CTkLabel(self, text = 'APELLIDO:', font = ("Calibri",18), compound = 'center')
        self.entry_name_var = ctk.StringVar()
        self.entry_name = ctk.CTkEntry(self, textvariable = self.entry_name_var,border_color='black')
        self.entry_surname_var = ctk.StringVar()
        self.entry_surname = ctk.CTkEntry(self, textvariable = self.entry_surname_var,border_color='black')
        self.entry_surname.bind('<Return>', lambda event, query_arg = 'fullname': get_pacient_event(self,event,query_arg))
        self.submit_fullname_button = ctk.CTkButton(self, text = 'Enviar', command = lambda : get_pacient(self,'fullname'),
                                                    font = ("Calibri",15), fg_color="#4287f5",hover_color = "#196ef7",
                                                    border_width=2.8,border_color="black",text_color='black')
        
        ## Data Results ## 
        self.header_data_label = ctk.CTkLabel(self, text = 'Datos del paciente:', font = ("Calibri",30), compound = 'center')
        
        self.dni_label = ctk.CTkLabel(self, text = 'D.N.I:', font = ("Calibri",18), compound = 'center')
        self.dni_text_var = ctk.StringVar()
        self.entry_data_dni = ctk.CTkLabel(self, textvariable = self.dni_text_var)
        
        self.name_label = ctk.CTkLabel(self, text = 'NOMBRE:', font = ("Calibri",18), compound = 'center')
        self.name_text_var = ctk.StringVar()
        self.entry_data_name = ctk.CTkLabel(self, textvariable = self.name_text_var)
        
        self.surname_label = ctk.CTkLabel(self, text = 'APELLIDO:', font = ("Calibri",18), compound = 'center')
        self.surname_text_var = ctk.StringVar()
        self.entry_data_surname = ctk.CTkLabel(self, textvariable = self.surname_text_var)
        
        self.age_label = ctk.CTkLabel(self, text = 'EDAD:', font = ("Calibri",18), compound = 'center')
        self.age_text_var = ctk.StringVar()
        self.entry_data_age = ctk.CTkLabel(self, textvariable = self.age_text_var)
        
        self.phone_label = ctk.CTkLabel(self, text = 'TELEFONO:', font = ("Calibri",18), compound = 'center')
        self.phone_text_var = ctk.StringVar()
        self.entry_phone = ctk.CTkLabel(self, textvariable = self.phone_text_var)
        
        self.address_label = ctk.CTkLabel(self, text = 'DOMICILIO:', font = ("Calibri",18), compound = 'center')
        self.address_text_var = ctk.StringVar()
        self.entry_address = ctk.CTkLabel(self, textvariable = self.address_text_var)
        
        self.company_label = ctk.CTkLabel(self, text = 'EMPRESA:', font = ("Calibri",18), compound = 'center')
        self.company_text_var = ctk.StringVar()
        self.entry_company = ctk.CTkLabel(self, textvariable = self.company_text_var)
        
        self.job_label = ctk.CTkLabel(self, text = 'PUESTO DE TRABAJO:', font = ("Calibri",18), compound = 'center')
        self.job_text_var = ctk.StringVar()
        self.entry_job = ctk.CTkLabel(self, textvariable = self.job_text_var)
        
        self.art_label = ctk.CTkLabel(self, text = 'A.R.T:', font = ("Calibri",18), compound = 'center')
        self.art_text_var = ctk.StringVar()
        self.entry_art = ctk.CTkLabel(self, textvariable = self.art_text_var)
        
        self.siniester_label = ctk.CTkLabel(self, text = 'N° SINIESTRO:', font = ("Calibri",18), compound = 'center')
        self.siniester_text_var = ctk.StringVar()
        self.entry_siniester = ctk.CTkLabel(self, textvariable = self.siniester_text_var)
        
        self.accident_date_label = ctk.CTkLabel(self, text = 'FECHA DE ACCIDENTE:', font = ("Calibri",18), compound = 'center')
        self.accident_date_text_var = ctk.StringVar()
        self.entry_accident_date = ctk.CTkLabel(self, textvariable = self.accident_date_text_var)
        
        self.dr_label = ctk.CTkLabel(self, text = 'DR DERIVANTE:', font = ("Calibri",18), compound = 'center')
        self.dr_text_var = ctk.StringVar()
        self.entry_dr = ctk.CTkLabel(self, textvariable = self.dr_text_var)
        
        self.start_date_label = ctk.CTkLabel(self, text = 'FECHA DE INICIO', font = ("Calibri",18), compound = 'center')
        self.start_date_text_var = ctk.StringVar()
        self.entry_start_date = ctk.CTkLabel(self, textvariable = self.start_date_text_var)
        
        self.generate_button = ctk.CTkButton(self, text = 'Generar ficha asistencia', command = lambda : GenerarFichaFrame.generatePdf(self),
                                            font = ("Calibri",15), fg_color="#4287f5",hover_color = "#196ef7",
                                            border_width=2.8,border_color="black",text_color='black')
          
    def create_layout(self):
        self.columnconfigure((0,1,2,3), weight = 1)
        self.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight = 1)
        
        ## HEADER ##
        self.header_label.grid(row = 0, column = 0, columnspan = 4)
        
        ## ENTRY ##
        self.enter_dni_label.grid(row = 1, column = 0, rowspan = 2)
        self.entry_dni.grid(row = 1, column = 1, rowspan = 2)
        
        self.enter_name_label.grid(row = 1, column = 2)
        self.entry_name.grid(row = 1, column = 3)
        
        self.enter_surname_label.grid(row = 2, column = 2)
        self.entry_surname.grid(row = 2, column = 3)
        
        self.submit_dni_button.grid(row = 3, column = 0, columnspan = 2)
        self.submit_fullname_button.grid(row = 3, column = 2, columnspan = 2)
        
        ## DATA ##
        self.header_data_label.grid(row = 4, column = 0, columnspan = 4, pady = 18)
        
        self.dni_label.grid(row = 5, column = 0)
        self.entry_data_dni.grid(row = 5, column = 1)
        
        self.name_label.grid(row = 5, column = 2)
        self.entry_data_name.grid(row = 5, column = 3)
        
        self.surname_label.grid(row = 6, column = 0)
        self.entry_data_surname.grid(row = 6, column = 1)
        
        self.age_label.grid(row = 6, column = 2)
        self.entry_data_age.grid(row = 6, column = 3)
        
        self.phone_label.grid(row = 7, column = 0)
        self.entry_phone.grid(row = 7, column = 1)
        
        self.address_label.grid(row = 7, column = 2)
        self.entry_address.grid(row = 7, column = 3)
        
        self.company_label.grid(row = 8, column = 0)
        self.entry_company.grid(row = 8, column = 1)
        
        self.job_label.grid(row = 8, column = 2)
        self.entry_job.grid(row = 8, column = 3)
        
        self.art_label.grid(row = 9, column = 0)
        self.entry_art.grid(row = 9, column = 1)
        
        self.siniester_label.grid(row = 9, column = 2)
        self.entry_siniester.grid(row = 9, column = 3)
        
        self.accident_date_label.grid(row = 10, column = 0)
        self.entry_accident_date.grid(row = 10, column = 1)
        
        self.dr_label.grid(row = 10, column = 2)
        self.entry_dr.grid(row = 10, column = 3)
        
        self.generate_button.grid(row = 11, column = 0, columnspan = 4, pady = 18)
    
    def generatePdf(self):
        answer = messagebox.askquestion(title = 'Confirmación', message = '¿Seguro que desea continuar?')
        if answer == "yes":
            output_pdf = '..\\files\planilla_asistencia.pdf'
            dni = self.dni_text_var.get()
            name = self.name_text_var.get()
            surname = self.surname_text_var.get()
            art = self.art_text_var.get()
            
            #-------------------- pdf creation ------------------------- #
            
            # if art = galeno, create especific galeno's pdf
            if(art == 'GALENO'):
                siniester = self.siniester_text_var.get()
                job = self.job_text_var.get()
                accident_date = self.accident_date_text_var.get()
                start_date = self.start_date_text_var.get()
                
                pdf = FPDF('P','mm','A4')
                pdf.add_page()
                pdf.set_font('helvetica','',10)
                pdf.set_margins(left=8,top=18,right=0)
            
                pdf.cell(0,7.6,"N° Caso/siniestro: " + siniester, new_x="LMARGIN", new_y="NEXT")
                pdf.cell(92,7.6,"Apellido y nombre: " + surname + ", " + name)
                pdf.cell(92,7.6,"CUIL/DNI: " + dni, new_x="LMARGIN", new_y="NEXT")
                pdf.cell(0,7.6,"Puesto de trabajo: " + job, new_x="LMARGIN", new_y="NEXT")
                pdf.cell(53,7.6,"Fecha de accidente: 12/12/2001")
                pdf.cell(90,7.6,"Lugar del accidente (laboral/In itinere,etc.) ....................")
                pdf.cell(55,7.6,"Traslado: R/TP /Ambulancia", new_x="LMARGIN", new_y="NEXT")
                pdf.cell(110,7.6,"Mecanismo del accidente: ................................................................")
                pdf.cell(88,7.6,"Fecha de ingreso a centro medico: ..........................", new_x="LMARGIN", new_y="NEXT")
                pdf.cell(62,7.6,"Fecha Qx (cirugía: ........../....../...........")
                pdf.cell(65,7.6,"Fecha de indicación: ........../....../...........")
                pdf.cell(65,7.6,"Cantidad de sesiones: ..........................", new_x="LMARGIN", new_y="NEXT")
                
                pdf.output(output_pdf)
            else:
                pdf = FPDF('P','mm','Legal')
                pdf.add_page()
                pdf.set_font('helvetica','',18)
                pdf.set_margins(left=3,top=45,right=15)
            
                #pdf.cell(0,16,"Nombre y apellido: " + surname +" " + name, new_x="LMARGIN", new_y="NEXT")
                pdf.cell(60,16,"Nombre y apellido: ")
                pdf.set_font('helvetica','B',25)
                pdf.cell(0,16,surname +" " + name, new_x="LMARGIN", new_y="NEXT")
                
                pdf.set_font('helvetica','',18)
                pdf.cell(130,16,"D.N.I: " + dni)
                pdf.cell(20,16,"A.R.T: ")
                pdf.set_font('helvetica','B',25)
                pdf.cell(0,16,art, new_x="LMARGIN", new_y="NEXT")
                
                
                #pdf.cell(150,16,"A.R.T: " + art, new_x="LMARGIN", new_y="NEXT")
                pdf.set_font('helvetica','',18)
                pdf.cell(0,16,"TURNO: ........................",new_x="LMARGIN",new_y="NEXT")
                
                pdf.output(output_pdf)
            
            
            # print generated pdf
            os.startfile(output_pdf, 'print')
            clear_fields(self)
               
class AltaPacienteFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)  
        self.create_widgets()
        self.create_layout()
        self.pack(expand = True, fill = 'both')
       
    def create_widgets(self):
        self.header_label = ctk.CTkLabel(self, text = 'Dar de alta paciente:', font = ("Calibri",30), compound = 'center')
        
        self.dni_label = ctk.CTkLabel(self, text = 'D.N.I:', font = ("Calibri",18), compound = 'center')
        self.dni_text_var = ctk.StringVar()
        self.entry_data_dni = ctk.CTkEntry(self, textvariable = self.dni_text_var,border_color='black')
        
        self.name_label = ctk.CTkLabel(self, text = 'NOMBRE:', font = ("Calibri",18), compound = 'center')
        self.name_text_var = ctk.StringVar()
        self.entry_data_name = ctk.CTkEntry(self, textvariable = self.name_text_var,border_color='black')
        
        self.surname_label = ctk.CTkLabel(self, text = 'APELLIDO:', font = ("Calibri",18), compound = 'center')
        self.surname_text_var = ctk.StringVar()
        self.entry_data_surname = ctk.CTkEntry(self, textvariable = self.surname_text_var,border_color='black')
        
        self.age_label = ctk.CTkLabel(self, text = 'EDAD:', font = ("Calibri",18), compound = 'center')
        self.age_text_var = ctk.StringVar()
        self.entry_data_age = ctk.CTkEntry(self, textvariable = self.age_text_var,border_color='black')
        
        self.phone_label = ctk.CTkLabel(self, text = 'TELEFONO:', font = ("Calibri",18), compound = 'center')
        self.phone_text_var = ctk.StringVar()
        self.entry_data_phone = ctk.CTkEntry(self, textvariable = self.phone_text_var,border_color='black')
        
        self.address_label = ctk.CTkLabel(self, text = 'DOMICILIO:', font = ("Calibri",18), compound = 'center')
        self.address_text_var = ctk.StringVar()
        self.entry_data_address = ctk.CTkEntry(self, textvariable = self.address_text_var,border_color='black')
        
        self.company_label = ctk.CTkLabel(self, text = 'EMPRESA:', font = ("Calibri",18), compound = 'center')
        self.company_text_var = ctk.StringVar()
        self.entry_data_company = ctk.CTkEntry(self, textvariable = self.company_text_var,border_color='black')
        
        self.job_label = ctk.CTkLabel(self, text = 'PUESTO DE TRABAJO:', font = ("Calibri",18), compound = 'center')
        self.job_text_var = ctk.StringVar()
        self.entry_data_job = ctk.CTkEntry(self, textvariable = self.job_text_var,border_color='black')
        
        self.art_label = ctk.CTkLabel(self, text = 'A.R.T:', font = ("Calibri",18), compound = 'center')
        self.art_text_var = ctk.StringVar()
        self.entry_data_art = ctk.CTkEntry(self, textvariable = self.art_text_var,border_color='black')
        
        self.siniester_label = ctk.CTkLabel(self, text = 'N° SINIESTRO:', font = ("Calibri",18), compound = 'center')
        self.siniester_text_var = ctk.StringVar()
        self.entry_data_siniester = ctk.CTkEntry(self, textvariable = self.siniester_text_var,border_color='black')
        
        self.accident_date_label = ctk.CTkLabel(self, text = 'FECHA ACCIDENTE:', font = ("Calibri",18), compound = 'center')
        self.accident_date_text_var = ctk.StringVar()
        self.entry_data_accident_date = ctk.CTkEntry(self, textvariable = self.accident_date_text_var,border_color='black')
        
        self.dr_label = ctk.CTkLabel(self, text = 'DR DERIVANTE:', font = ("Calibri",18), compound = 'center')
        self.dr_text_var = ctk.StringVar()
        self.entry_data_dr = ctk.CTkEntry(self, textvariable = self.dr_text_var,border_color='black')
        self.entry_data_dr.bind('<Return>', lambda event: AltaPacienteFrame.create_pacient_event(self,event))
        
        self.start_date_label = ctk.CTkLabel(self, text = 'FECHA DE INICIO:', font = ("Calibri",18), compound = 'center')
        self.start_date_text_var = ctk.StringVar()
        self.entry_data_start_date = ctk.CTkEntry(self, textvariable = self.start_date_text_var,border_color='black')
        
        self.submit_button = ctk.CTkButton(self, text = 'Enviar', command = lambda : AltaPacienteFrame.create_pacient(self),
                                            font = ("Calibri",15), fg_color="#4287f5",hover_color = "#196ef7",
                                            border_width=2.8,border_color="black",text_color='black')
        
    def create_layout(self):
        self.columnconfigure((0,1,2,3), weight = 1)
        self.rowconfigure((0,1,2,3,4,5,6,7), weight = 1)
        
        self.header_label.grid(row = 0, column = 0, columnspan = 4)
        
        self.dni_label.grid(row = 1, column = 0)
        self.entry_data_dni.grid(row = 1, column = 1)
        
        self.name_label.grid(row = 1, column = 2)
        self.entry_data_name.grid(row = 1, column = 3)
        
        self.surname_label.grid(row = 2, column = 0)
        self.entry_data_surname.grid(row = 2, column = 1)
        
        self.age_label.grid(row = 2, column = 2)
        self.entry_data_age.grid(row = 2, column = 3)
        
        self.phone_label.grid(row = 3, column = 0)
        self.entry_data_phone.grid(row = 3, column = 1)
        
        self.address_label.grid(row = 3, column = 2)
        self.entry_data_address.grid(row = 3, column = 3)
        
        self.company_label.grid(row = 4, column = 0)
        self.entry_data_company.grid(row = 4, column = 1)
        
        self.job_label.grid(row = 4, column = 2)
        self.entry_data_job.grid(row = 4, column = 3)
        
        self.art_label.grid(row = 5, column = 0)
        self.entry_data_art.grid(row = 5, column = 1)
        
        self.siniester_label.grid(row = 5, column = 2)
        self.entry_data_siniester.grid(row = 5, column = 3)
        
        self.accident_date_label.grid(row = 6, column = 0)
        self.entry_data_accident_date.grid(row = 6, column = 1)
        
        self.dr_label.grid(row = 6, column = 2)
        self.entry_data_dr.grid(row = 6, column = 3)
        
        self.submit_button.grid(row = 7, column = 0, columnspan = 4)
        
    def clear_fields(self):
        self.dni_text_var.set('')
        self.name_text_var.set('')
        self.surname_text_var.set('')
        self.art_text_var.set('')
        self.age_text_var.set('')
        self.phone_text_var.set('')
        self.address_text_var.set('')
        self.company_text_var.set('')
        self.job_text_var.set('')
        self.siniester_text_var.set('')
        self.accident_date_text_var.set('')
        self.dr_text_var.set('')
    
    def create_pacient(self):
        conn = sqlite3.connect('..\database\cai_database.db')
        dni,name,surname,age,phone,address,company,job,art,siniester,accident_date,dr = get_fields(self)
        
        current_date = datetime.now()
        current_date = current_date.strftime('%d/%m/%Y')
        start_date = current_date
        
        if(dni == '' or name == '' or surname == '' or art == ''):
            messagebox.showerror(title = 'Error: Datos no validos', message = 'El DNI, NOMBRE, APELLIDO y ART no pueden estar en blanco')
        else:
            dni = int(dni)

            ## validate ART name
            is_valid, art_id = validate_art(art)
            
            if (not is_valid):
                messagebox.showerror(title = 'Error: ART invalida', message = f'La ART: {art} no existe')
            else:
                #validate dni
                if(not dni_is_valid(dni)):
                    messagebox.showerror(title = 'Error: Dni no valido', message = f'Ya existe el paciente con dni: {dni}')
                else:
                    query = f'''INSERT INTO Paciente 
                                (Dni,Nombre,Apellido,Edad,Art,Siniestro,Puesto_Trabajo,Fecha_Accidente,Telefono,Dr_derivante,Fecha_Inicio,Empresa,Domicilio) 
                                VALUES ({dni},'{name}','{surname}','{age}',{art_id},'{siniester}','{job}','{accident_date}',{phone},'{dr}','{start_date}','{company}','{address}')'''
                    try:
                        cursor = conn.execute(query)
                        conn.commit()
                    except sqlite3.Error as err:
                        messagebox.showerror(title = 'Error', message = 'Algo ha salido mal :(')
                    else:
                        messagebox.showinfo(title = 'Operacion satisfactoria!', message = f'Se ha dado de alta al paciente {surname}, {name}')
                        self.clear_fields()
                    finally:
                        conn.close()
                    
    def create_pacient_event(self, event):
        conn = sqlite3.connect('..\database\cai_database.db')
        dni,name,surname,age,phone,address,company,job,art,siniester,accident_date,dr = get_fields(self)
        
        current_date = datetime.now()
        current_date = current_date.strftime('%d/%m/%Y')
        start_date = current_date
        
        if(dni == '' or name == '' or surname == '' or art == ''):
            messagebox.showerror(title = 'Error: Datos no validos', message = 'El DNI, NOMBRE, APELLIDO y ART no pueden estar en blanco')
        else:
            dni = int(dni)

            ## validate ART name
            is_valid, art_id = validate_art(art)
            
            if (not is_valid):
                messagebox.showerror(title = 'Error: ART invalida', message = f'La ART: {art} no existe')
            else:
                #validate dni
                if(not dni_is_valid(dni)):
                    messagebox.showerror(title = 'Error: Dni no valido', message = f'Ya existe el paciente con dni: {dni}')
                else:
                    query = f'''INSERT INTO Paciente 
                                (Dni,Nombre,Apellido,Edad,Art,Siniestro,Puesto_Trabajo,Fecha_Accidente,Telefono,Dr_derivante,Fecha_Inicio,Empresa,Domicilio) 
                                VALUES ({dni},'{name}','{surname}','{age}',{art_id},'{siniester}','{job}','{accident_date}',{phone},'{dr}','{start_date}','{company}','{address}')'''
                    try:
                        cursor = conn.execute(query)
                        conn.commit()
                    except sqlite3.Error as err:
                        messagebox.showerror(title = 'Error', message = 'Algo ha salido mal :(')
                    else:
                        messagebox.showinfo(title = 'Operacion satisfactoria!', message = f'Se ha dado de alta al paciente {surname}, {name}')
                        self.clear_fields()
                    finally:
                        conn.close()

class AltaARTFrame(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.create_widgets()
        self.create_layout()
        self.pack(expand = True, fill = 'both')

    def create_widgets(self):
        self.header_label = ctk.CTkLabel(self, text = 'Dar de alta ART', font = ("Calibri",30), compound = 'center')
        self.name_label = ctk.CTkLabel(self, text = 'A.R.T:', font = ("Calibri",18), compound = 'center')
        self.entry_name_var = ctk.StringVar()
        self.entry_name = ctk.CTkEntry(self, textvariable = self.entry_name_var,border_color='black')
        self.entry_name.bind('<Return>', lambda event: AltaARTFrame.create_art_event(self,event))
        self.submit_button = ctk.CTkButton(self, text = 'Dar de alta', command = lambda : AltaARTFrame.create_art(self),
                                            font = ("Calibri",15), fg_color="#4287f5",hover_color = "#196ef7",
                                            border_width=2.8,border_color="black",text_color='black')
        
    def create_layout(self):
        self.columnconfigure((0,1), weight = 1)
        self.rowconfigure((0,1,2), weight = 3)
        
        self.header_label.grid(row = 0, column = 0, columnspan = 2)
        self.name_label.grid(row = 1, column = 0)
        self.entry_name.grid(row = 1, column = 1)
        self.submit_button.grid(row = 2, column = 0, columnspan = 2)
        
    def clear_fields(self):
        self.entry_name_var.set('')
    
    def create_art(self):
        conn = sqlite3.connect('..\database\cai_database.db')
        name_art = self.entry_name_var.get()
        
        ## validate entry
        if(name_art == ''):
            messagebox.showerror(title = 'Error: Campos en blanco', message = f'Debe completar todos los campos')
            
        else:
            name_art = name_art.upper()
            query = f"SELECT Nombre FROM Art"
            cursor = conn.execute(query)
            data = cursor.fetchall()
            
            if(data == None):
                messagebox.showerror(title = 'Error', message = f'Algo ha salido mal :(')
            else:
                already_exists = False
                for art in data:
                    if(name_art == art[0]):
                        already_exists = True
                        break
                
                if(already_exists == True):
                    messagebox.showerror(title = 'Error', message = f'Ya existe la ART con nombre: {name_art}')
                else:
                    query = f"INSERT INTO Art (Nombre) VALUES ('{name_art}')"
                    try:
                        cursor = conn.execute(query)
                        conn.commit()
                    except sqlite3.Error as err:
                        messagebox.showerror(title = 'Error', message = f'Algo ha salido mal :(')
                    else:
                        messagebox.showinfo(title = 'Operacion satisfactoria!', message = f'Se ha dado de alta la ART {name_art}')
                    finally:
                        conn.close()
                        
            self.clear_fields()
                        
    def create_art_event(self,event):
        conn = sqlite3.connect('..\database\cai_database.db')
        name_art = self.entry_name_var.get()
        
        ## validate entry
        if(name_art == ''):
            messagebox.showerror(title = 'Error: Campos en blanco', message = f'Debe completar todos los campos')
            
        else:
            name_art = name_art.upper()
            query = f"SELECT Nombre FROM Art"
            cursor = conn.execute(query)
            data = cursor.fetchall()
            
            if(data == None):
                messagebox.showerror(title = 'Error', message = f'Algo ha salido mal :(')
            else:
                already_exists = False
                for art in data:
                    if(name_art == art[0]):
                        already_exists = True
                        break
                
                if(already_exists == True):
                    messagebox.showerror(title = 'Error', message = f'Ya existe la ART con nombre: {name_art}')
                else:
                    query = f"INSERT INTO Art (Nombre) VALUES ('{name_art}')"
                    try:
                        cursor = conn.execute(query)
                        conn.commit()
                    except sqlite3.Error as err:
                        messagebox.showerror(title = 'Error', message = f'Algo ha salido mal :(')
                    else:
                        messagebox.showinfo(title = 'Operacion satisfactoria!', message = f'Se ha dado de alta la ART {name_art}')
                    finally:
                        conn.close()
                        
        self.clear_fields()
    
class BajaPacienteFrame(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.create_widgets()
        self.create_layout()
        self.pack(expand = True, fill = 'both')
    
    def create_widgets(self):
        self.header_label = ctk.CTkLabel(self, text = 'Modificar datos paciente', font = ("Calibri",30), compound = 'center')
        
        ## DNI entry ##
        self.enter_dni_label = ctk.CTkLabel(self, text = 'D.N.I:', font = ("Calibri",18), compound = 'center')
        self.entry_dni_var = ctk.StringVar()
        self.entry_dni = ctk.CTkEntry(self, textvariable = self.entry_dni_var,border_color='black')
        self.entry_dni.bind('<Return>', lambda event, query_arg='dni': get_pacient_event(self,event,query_arg))
        self.submit_dni_button = ctk.CTkButton(self, text = 'Enviar', command = lambda : get_pacient(self,'dni'),
                                               font = ("Calibri",15), fg_color="#4287f5",hover_color = "#196ef7",
                                               border_width=2.8,border_color="black",text_color='black')
        
        ## Name entry ##
        self.enter_name_label = ctk.CTkLabel(self, text = 'NOMBRE:', font = ("Calibri",18), compound = 'center')
        self.enter_surname_label = ctk.CTkLabel(self, text = 'APELLIDO:', font = ("Calibri",18), compound = 'center')
        self.entry_name_var = ctk.StringVar()
        self.entry_name = ctk.CTkEntry(self, textvariable = self.entry_name_var,border_color='black')
        self.entry_surname_var = ctk.StringVar()
        self.entry_surname = ctk.CTkEntry(self, textvariable = self.entry_surname_var,border_color='black')
        self.entry_surname.bind('<Return>', lambda event, query_arg = 'fullname': get_pacient_event(self,event,query_arg))
        self.submit_fullname_button = ctk.CTkButton(self, text = 'Enviar', command = lambda : get_pacient(self,'fullname'),
                                                    font = ("Calibri",15), fg_color="#4287f5",hover_color = "#196ef7",
                                                    border_width=2.8,border_color="black",text_color='black')
        
        ## Data Results ## 
        self.header_data_label = ctk.CTkLabel(self, text = 'Datos del paciente:', font = ("Calibri",30), compound = 'center')
        
        self.dni_label = ctk.CTkLabel(self, text = 'D.N.I:', font = ("Calibri",18), compound = 'center')
        self.dni_text_var = ctk.StringVar()
        self.entry_data_dni = ctk.CTkLabel(self, textvariable = self.dni_text_var)
        
        self.name_label = ctk.CTkLabel(self, text = 'NOMBRE:', font = ("Calibri",18), compound = 'center')
        self.name_text_var = ctk.StringVar()
        self.entry_data_name = ctk.CTkLabel(self, textvariable = self.name_text_var)
        
        self.surname_label = ctk.CTkLabel(self, text = 'APELLIDO:', font = ("Calibri",18), compound = 'center')
        self.surname_text_var = ctk.StringVar()
        self.entry_data_surname = ctk.CTkLabel(self, textvariable = self.surname_text_var)
        
        self.age_label = ctk.CTkLabel(self, text = 'EDAD:', font = ("Calibri",18), compound = 'center')
        self.age_text_var = ctk.StringVar()
        self.entry_data_age = ctk.CTkLabel(self, textvariable = self.age_text_var)
        
        self.phone_label = ctk.CTkLabel(self, text = 'TELEFONO:', font = ("Calibri",18), compound = 'center')
        self.phone_text_var = ctk.StringVar()
        self.entry_phone = ctk.CTkLabel(self, textvariable = self.phone_text_var)
        
        self.address_label = ctk.CTkLabel(self, text = 'DIRECCION:', font = ("Calibri",18), compound = 'center')
        self.address_text_var = ctk.StringVar()
        self.entry_address = ctk.CTkLabel(self, textvariable = self.address_text_var)
        
        self.company_label = ctk.CTkLabel(self, text = 'EMPRESA:', font = ("Calibri",18), compound = 'center')
        self.company_text_var = ctk.StringVar()
        self.entry_company = ctk.CTkLabel(self, textvariable = self.company_text_var)
        
        self.job_label = ctk.CTkLabel(self, text = 'PUESTO DE TRABAJO:', font = ("Calibri",18), compound = 'center')
        self.job_text_var = ctk.StringVar()
        self.entry_job = ctk.CTkLabel(self, textvariable = self.job_text_var)
        
        self.art_label = ctk.CTkLabel(self, text = 'A.R.T:', font = ("Calibri",18), compound = 'center')
        self.art_text_var = ctk.StringVar()
        self.entry_art = ctk.CTkLabel(self, textvariable = self.art_text_var)
        
        self.siniester_label = ctk.CTkLabel(self, text = 'N° SINIESTRO:', font = ("Calibri",18), compound = 'center')
        self.siniester_text_var = ctk.StringVar()
        self.entry_siniester = ctk.CTkLabel(self, textvariable = self.siniester_text_var)
        
        self.accident_date_label = ctk.CTkLabel(self, text = 'FECHA DE ACCIDENTE:', font = ("Calibri",18), compound = 'center')
        self.accident_date_text_var = ctk.StringVar()
        self.entry_accident_date = ctk.CTkLabel(self, textvariable = self.accident_date_text_var)
        
        self.dr_label = ctk.CTkLabel(self, text = 'DR DERIVANTE:', font = ("Calibri",18), compound = 'center')
        self.dr_text_var = ctk.StringVar()
        self.entry_dr = ctk.CTkLabel(self, textvariable = self.dr_text_var)
        
        self.start_date_label = ctk.CTkLabel(self, text = 'FECHA DE INICIO:', font = ("Calibri",18), compound = 'center')
        self.start_date_text_var = ctk.StringVar()
        self.entry_start_date = ctk.CTkLabel(self, textvariable = self.start_date_text_var)
        
        self.delete_button = ctk.CTkButton(self, text = 'Borrar', command = lambda : BajaPacienteFrame.delete_pacient(self),
                                            font = ("Calibri",15), fg_color="#4287f5",hover_color = "#196ef7",
                                            border_width=2.8,border_color="black",text_color='black')
        
    def create_layout(self):
        self.columnconfigure((0,1,2,3), weight = 1)
        self.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight = 1)
        
        ## HEADER ##
        self.header_label.grid(row = 0, column = 0, columnspan = 4)
        
        ## ENTRY ##
        self.enter_dni_label.grid(row = 1, column = 0, rowspan = 2)
        self.entry_dni.grid(row = 1, column = 1, rowspan = 2)
        
        self.enter_name_label.grid(row = 1, column = 2)
        self.entry_name.grid(row = 1, column = 3)
        
        self.enter_surname_label.grid(row = 2, column = 2)
        self.entry_surname.grid(row = 2, column = 3)
        
        self.submit_dni_button.grid(row = 3, column = 0, columnspan = 2)
        self.submit_fullname_button.grid(row = 3, column = 2, columnspan = 2)
        
        ## DATA ##
        self.header_data_label.grid(row = 4, column = 0, columnspan = 4, pady = 18)
        
        self.dni_label.grid(row = 5, column = 0)
        self.entry_data_dni.grid(row = 5, column = 1)
        
        self.name_label.grid(row = 5, column = 2)
        self.entry_data_name.grid(row = 5, column = 3)
        
        self.surname_label.grid(row = 6, column = 0)
        self.entry_data_surname.grid(row = 6, column = 1)
        
        self.age_label.grid(row = 6, column = 2)
        self.entry_data_age.grid(row = 6, column = 3)
        
        self.phone_label.grid(row = 7, column = 0)
        self.entry_phone.grid(row = 7, column = 1)
        
        self.address_label.grid(row = 7, column = 2)
        self.entry_address.grid(row = 7, column = 3)
        
        self.company_label.grid(row = 8, column = 0)
        self.entry_company.grid(row = 8, column = 1)
        
        self.job_label.grid(row = 8, column = 2)
        self.entry_job.grid(row = 8, column = 3)
        
        self.art_label.grid(row = 9, column = 0)
        self.entry_art.grid(row = 9, column = 1)
        
        self.siniester_label.grid(row = 9, column = 2)
        self.entry_siniester.grid(row = 9, column = 3)
        
        self.accident_date_label.grid(row = 10, column = 0)
        self.entry_accident_date.grid(row = 10, column = 1)
        
        self.dr_label.grid(row = 10, column = 2)
        self.entry_dr.grid(row = 10, column = 3)
        
        self.delete_button.grid(row = 11, column = 0, columnspan = 4, pady = 18)
    
    def delete_pacient(self):
        dni = int(self.dni_text_var.get())
        name = self.name_text_var.get()
        surname = self.surname_text_var.get()
        
        answer = messagebox.askquestion(title = 'Confirmación', message = f'¿Seguro que desea dar de baja al paciente {surname}, {name}?')
        
        if answer == "yes":
            conn = sqlite3.connect('..\database\cai_database.db')    
            query = f"SELECT * FROM Paciente WHERE dni = {dni}"
            cursor = conn.execute(query)
            data = cursor.fetchone()
            if (data == None):
                messagebox.showerror(title = 'Error: Dni no valido', message = f'No existe el paciente: {surname}, {name}')
            else:
                query = f"DELETE FROM Paciente WHERE dni = {dni}"
                        
                try:
                    cursor = conn.execute(query)
                    conn.commit()
                except sqlite3.Error as err:
                    messagebox.showerror(title = 'Error', message = f'Algo ha salido mal :(')
                else:
                    messagebox.showinfo(title = 'Operacion satisfactoria!', message = f'Se ha dado de baja al paciente {surname}, {name}')
                finally:
                    conn.close()
                    
        clear_fields(self)
               
class ModificarPacienteFrame(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.create_widgets()
        self.create_layout()
        self.pack(expand = True, fill = 'both')

    def create_widgets(self):
        self.header_label = ctk.CTkLabel(self, text = 'Modificar datos paciente', font = ("Calibri",30), compound = 'center')
        
        ## DNI entry ##
        self.enter_dni_label = ctk.CTkLabel(self, text = 'D.N.I:', font = ("Calibri",18), compound = 'center')
        self.entry_dni_var = ctk.StringVar()
        self.entry_dni = ctk.CTkEntry(self, textvariable = self.entry_dni_var,border_color='black')
        self.entry_dni.bind('<Return>', lambda event, query_arg='dni': get_pacient_event(self,event,query_arg))
        self.submit_dni_button = ctk.CTkButton(self, text = 'Enviar', command = lambda : get_pacient(self,'dni'),
                                               font = ("Calibri",15), fg_color="#4287f5",hover_color = "#196ef7",
                                               border_width=2.8,border_color="black",text_color='black')
        
        ## Name entry ##
        self.enter_name_label = ctk.CTkLabel(self, text = 'NOMBRE:', font = ("Calibri",18), compound = 'center')
        self.enter_surname_label = ctk.CTkLabel(self, text = 'APELLIDO:', font = ("Calibri",18), compound = 'center')
        self.entry_name_var = ctk.StringVar()
        self.entry_name = ctk.CTkEntry(self, textvariable = self.entry_name_var,border_color='black')
        self.entry_surname_var = ctk.StringVar()
        self.entry_surname = ctk.CTkEntry(self, textvariable = self.entry_surname_var,border_color='black')
        self.entry_surname.bind('<Return>', lambda event, query_arg = 'fullname': get_pacient_event(self,event,query_arg))
        self.submit_fullname_button = ctk.CTkButton(self, text = 'Enviar', command = lambda : get_pacient(self,'fullname'),
                                                    font = ("Calibri",15), fg_color="#4287f5",hover_color = "#196ef7",
                                                    border_width=2.8,border_color="black",text_color='black')
        
        ## Data Results ## 
        self.header_data_label = ctk.CTkLabel(self, text = 'Datos del paciente:', font = ("Calibri",30), compound = 'center')
        
        self.dni_label = ctk.CTkLabel(self, text = 'D.N.I:', font = ("Calibri",18), compound = 'center')
        self.dni_text_var = ctk.StringVar()
        self.entry_data_dni = ctk.CTkEntry(self, textvariable = self.dni_text_var,border_color='black')
        
        self.name_label = ctk.CTkLabel(self, text = 'NOMBRE:', font = ("Calibri",18), compound = 'center')
        self.name_text_var = ctk.StringVar()
        self.entry_data_name = ctk.CTkEntry(self, textvariable = self.name_text_var,border_color='black')
        
        self.surname_label = ctk.CTkLabel(self, text = 'APELLIDO:', font = ("Calibri",18), compound = 'center')
        self.surname_text_var = ctk.StringVar()
        self.entry_data_surname = ctk.CTkEntry(self, textvariable = self.surname_text_var,border_color='black')
        
        self.age_label = ctk.CTkLabel(self, text = 'EDAD:', font = ("Calibri",18), compound = 'center')
        self.age_text_var = ctk.StringVar()
        self.entry_data_age = ctk.CTkEntry(self, textvariable = self.age_text_var,border_color='black')
        
        self.phone_label = ctk.CTkLabel(self, text = 'TELEFONO:', font = ("Calibri",18), compound = 'center')
        self.phone_text_var = ctk.StringVar()
        self.entry_data_phone = ctk.CTkEntry(self, textvariable = self.phone_text_var,border_color='black')
        
        self.address_label = ctk.CTkLabel(self, text = 'DOMICILIO:', font = ("Calibri",18), compound = 'center')
        self.address_text_var = ctk.StringVar()
        self.entry_data_address = ctk.CTkEntry(self, textvariable = self.address_text_var,border_color='black')
        
        self.company_label = ctk.CTkLabel(self, text = 'EMPRESA:', font = ("Calibri",18), compound = 'center')
        self.company_text_var = ctk.StringVar()
        self.entry_data_company = ctk.CTkEntry(self, textvariable = self.company_text_var,border_color='black')
        
        self.job_label = ctk.CTkLabel(self, text = 'PUESTO DE TRABAJO:', font = ("Calibri",18), compound = 'center')
        self.job_text_var = ctk.StringVar()
        self.entry_data_job = ctk.CTkEntry(self, textvariable = self.job_text_var,border_color='black')
        
        self.art_label = ctk.CTkLabel(self, text = 'A.R.T:', font = ("Calibri",18), compound = 'center')
        self.art_text_var = ctk.StringVar()
        self.entry_data_art = ctk.CTkEntry(self, textvariable = self.art_text_var,border_color='black')
        
        self.siniester_label = ctk.CTkLabel(self, text = 'N° SINIESTRO:', font = ("Calibri",18), compound = 'center')
        self.siniester_text_var = ctk.StringVar()
        self.entry_data_siniester = ctk.CTkEntry(self, textvariable = self.siniester_text_var,border_color='black')
        
        self.accident_date_label = ctk.CTkLabel(self, text = 'FECHA ACCIDENTE:', font = ("Calibri",18), compound = 'center')
        self.accident_date_text_var = ctk.StringVar()
        self.entry_data_accident_date = ctk.CTkEntry(self, textvariable = self.accident_date_text_var,border_color='black')
        
        self.dr_label = ctk.CTkLabel(self, text = 'DR DERIVANTE:', font = ("Calibri",18), compound = 'center')
        self.dr_text_var = ctk.StringVar()
        self.entry_data_dr = ctk.CTkEntry(self, textvariable = self.dr_text_var,border_color='black')
        self.entry_data_dr.bind('<Return>', lambda event: AltaPacienteFrame.create_pacient_event(self,event))
        
        self.start_date_label = ctk.CTkLabel(self, text = 'FECHA DE INICIO:', font = ("Calibri",18), compound = 'center')
        self.start_date_text_var = ctk.StringVar()
        self.entry_data_start_date = ctk.CTkEntry(self, textvariable = self.start_date_text_var,border_color='black')
        
        self.update_button = ctk.CTkButton(self, text = 'Actualizar datos', command = lambda : ModificarPacienteFrame.update_pacient(self),
                                            font = ("Calibri",15), fg_color="#4287f5",hover_color = "#196ef7",
                                            border_width=2.8,border_color="black",text_color='black')
        self.clear_button = ctk.CTkButton(self, text = 'Limpiar', command = lambda : clear_fields(self),
                                            font = ("Calibri",15), fg_color="#c7c4bd",hover_color = "#a19e97",
                                            border_width=2.8,border_color="black",text_color='black')

    def create_layout(self):
        self.columnconfigure((0,1,2,3), weight = 1)
        self.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13), weight = 1)
        
        ## HEADER ##
        self.header_label.grid(row = 0, column = 0, columnspan = 4)
        
        ## ENTRY ##
        self.enter_dni_label.grid(row = 1, column = 0, rowspan = 2)
        self.entry_dni.grid(row = 1, column = 1, rowspan = 2)
        
        self.enter_name_label.grid(row = 1, column = 2)
        self.entry_name.grid(row = 1, column = 3)
        
        self.enter_surname_label.grid(row = 2, column = 2)
        self.entry_surname.grid(row = 2, column = 3)
        
        self.submit_dni_button.grid(row = 3, column = 0, columnspan = 2)
        self.submit_fullname_button.grid(row = 3, column = 2, columnspan = 2)
        
        ## DATA ##
        self.header_data_label.grid(row = 4, column = 0, columnspan = 4, pady = 18)
        
        self.dni_label.grid(row = 5, column = 0)
        self.entry_data_dni.grid(row = 5, column = 1)
        
        self.name_label.grid(row = 5, column = 2)
        self.entry_data_name.grid(row = 5, column = 3)
        
        self.surname_label.grid(row = 6, column = 0)
        self.entry_data_surname.grid(row = 6, column = 1)
        
        self.age_label.grid(row = 6, column = 2)
        self.entry_data_age.grid(row = 6, column = 3)
        
        self.phone_label.grid(row = 7, column = 0)
        self.entry_data_phone.grid(row = 7, column = 1)
        
        self.address_label.grid(row = 7, column = 2)
        self.entry_data_address.grid(row = 7, column = 3)
        
        self.company_label.grid(row = 8, column = 0)
        self.entry_data_company.grid(row = 8, column = 1)
        
        self.job_label.grid(row = 8, column = 2)
        self.entry_data_job.grid(row = 8, column = 3)
        
        self.art_label.grid(row = 9, column = 0)
        self.entry_data_art.grid(row = 9, column = 1)
        
        self.siniester_label.grid(row = 9, column = 2)
        self.entry_data_siniester.grid(row = 9, column = 3)
        
        self.accident_date_label.grid(row = 10, column = 0)
        self.entry_data_accident_date.grid(row = 10, column = 1)
        
        self.dr_label.grid(row = 10, column = 2)
        self.entry_data_dr.grid(row = 10, column = 3)
        
        self.start_date_label.grid(row = 11, column = 0)
        self.entry_data_start_date.grid(row = 11, column = 1)
        
        self.update_button.grid(row = 12, column = 0, columnspan = 4, pady = 18)
        self.clear_button.grid(row = 13, column = 3,pady = 18)
              
    def update_pacient(self):
        conn = sqlite3.connect('..\database\cai_database.db')
        
        parsed_date = self.accident_date_text_var.get()
        parsed_date = parsed_date.replace('/',"")
        self.accident_date_text_var.set(parsed_date)
        
        dni,name,surname,age,phone,address,company,job,art,siniester,accident_date,dr = get_fields(self)
        
        parsed_date = self.start_date_text_var.get()
        parsed_date = parsed_date.replace('/',"")
        self.start_date_text_var.set(parsed_date)
        
        start_date = self.start_date_text_var.get()
        
        #validate dates
        if(not is_valid_date(start_date)):
            messagebox.showerror(title = 'Error: Fecha no valida', message = 'Ingresar fecha en formato DDMMAAAA')
        
        else:
            start_date = format_date(start_date)
            ## validate ART name
            is_valid, art_id = validate_art(art)
        
            if (not is_valid):
                messagebox.showerror(title = 'Error: ART invalida', message = f'La ART: {art} no existe')
            else:
                query = f'SELECT * FROM Paciente WHERE dni = {dni}'
                cursor = conn.execute(query)
                data = cursor.fetchone()
                
                # Si data == None es porque lo que se modifico fue el dni
                if(data == None):
                    query = f'''SELECT * FROM Paciente WHERE Nombre = '{name}' AND Apellido = '{surname}' '''
                    cursor = conn.execute(query)
                    data = cursor.fetchone()
                    
                    if(data == None):
                        messagebox.showerror(title = 'Error', message = f'Algo ha salido mal :(')
                    else:
                        query = f'''UPDATE Paciente 
                                    SET Dni = {dni}, Nombre = '{name}', Apellido = '{surname}', Art = {art_id},
                                    Siniestro = '{siniester}', Puesto_Trabajo = '{job}', Fecha_Accidente = '{accident_date}',
                                    Telefono = {phone}, Dr_derivante = '{dr}', Fecha_Inicio = '{start_date}', 
                                    Empresa = '{company}', Domicilio = '{address}', Edad = '{age}'
                                    WHERE Nombre = '{name}' AND Apellido = '{surname}' '''
                        
                        try:
                            conn.execute(query)
                            conn.commit()
                        except sqlite3.Error as err:
                            messagebox.showerror(title = 'Error', message = f'Algo ha salido mal :(')
                        else:
                            messagebox.showinfo(title = 'Operacion satisfactoria!', message = f'Se han modificado los datos del paciente {surname}, {name}')
                        finally:
                            conn.close()
                    
                    
                else:
                    query = f'''UPDATE Paciente 
                                SET Dni = {dni}, Nombre = '{name}', Apellido = '{surname}', Art = {art_id},
                                Siniestro = '{siniester}', Puesto_Trabajo = '{job}', Fecha_Accidente = '{accident_date}',
                                Telefono = {phone}, Dr_derivante = '{dr}', Fecha_Inicio = '{start_date}', 
                                Empresa = '{company}', Domicilio = '{address}', Edad = '{age}'
                                WHERE Dni = {dni}'''
                    try:
                        conn.execute(query)
                        conn.commit()
                    except sqlite3.Error as err:
                        messagebox.showerror(title = 'Error', message = f'Algo ha salido mal :(')
                    else:
                        messagebox.showinfo(title = 'Operacion satisfactoria!', message = f'Se han modificado los datos del paciente {surname}, {name}')
                    finally:
                        conn.close()
                        
        clear_fields(self)
        
    def update_pacient_event(self,event):
        conn = sqlite3.connect('..\database\cai_database.db')
        
        parsed_date = self.accident_date_text_var.get()
        parsed_date = parsed_date.replace('/',"")
        self.accident_date_text_var.set(parsed_date)
        
        dni,name,surname,age,phone,address,company,job,art,siniester,accident_date,dr = get_fields(self)
        
        parsed_date = self.start_date_text_var.get()
        parsed_date = parsed_date.replace('/',"")
        self.start_date_text_var.set(parsed_date)
        
        start_date = self.start_date_text_var.get()
        
        #validate dates
        if(not is_valid_date(start_date)):
            messagebox.showerror(title = 'Error: Fecha no valida', message = 'Ingresar fecha en formato DDMMAAAA')
        
        else:
            start_date = format_date(start_date)
            ## validate ART name
            is_valid, art_id = validate_art(art)
        
            if (not is_valid):
                messagebox.showerror(title = 'Error: ART invalida', message = f'La ART: {art} no existe')
            else:
                query = f'SELECT * FROM Paciente WHERE dni = {dni}'
                cursor = conn.execute(query)
                data = cursor.fetchone()
                
                # Si data == None es porque lo que se modifico fue el dni
                if(data == None):
                    query = f'''SELECT * FROM Paciente WHERE Nombre = '{name}' AND Apellido = '{surname}' '''
                    cursor = conn.execute(query)
                    data = cursor.fetchone()
                    
                    if(data == None):
                        messagebox.showerror(title = 'Error', message = f'Algo ha salido mal :(')
                    else:
                        query = f'''UPDATE Paciente 
                                    SET Dni = {dni}, Nombre = '{name}', Apellido = '{surname}', Art = {art_id},
                                    Siniestro = '{siniester}', Puesto_Trabajo = '{job}', Fecha_Accidente = '{accident_date}',
                                    Telefono = {phone}, Dr_derivante = '{dr}', Fecha_Inicio = '{start_date}', 
                                    Empresa = '{company}', Domicilio = '{address}', Edad = '{age}'
                                    WHERE Nombre = '{name}' AND Apellido = '{surname}' '''
                        
                        try:
                            conn.execute(query)
                            conn.commit()
                        except sqlite3.Error as err:
                            messagebox.showerror(title = 'Error', message = f'Algo ha salido mal :(')
                        else:
                            messagebox.showinfo(title = 'Operacion satisfactoria!', message = f'Se han modificado los datos del paciente {surname}, {name}')
                        finally:
                            conn.close()
                    
                    
                else:
                    query = f'''UPDATE Paciente 
                                SET Dni = {dni}, Nombre = '{name}', Apellido = '{surname}', Art = {art_id},
                                Siniestro = '{siniester}', Puesto_Trabajo = '{job}', Fecha_Accidente = '{accident_date}',
                                Telefono = {phone}, Dr_derivante = '{dr}', Fecha_Inicio = '{start_date}', 
                                Empresa = '{company}', Domicilio = '{address}', Edad = '{age}'
                                WHERE Dni = {dni}'''
                    try:
                        conn.execute(query)
                        conn.commit()
                    except sqlite3.Error as err:
                        messagebox.showerror(title = 'Error', message = f'Algo ha salido mal :(')
                    else:
                        messagebox.showinfo(title = 'Operacion satisfactoria!', message = f'Se han modificado los datos del paciente {surname}, {name}')
                    finally:
                        conn.close()
                        
        clear_fields(self)

class HistoriaClinica(ctk.CTkFrame):  
    def __init__(self, parent):
        super().__init__(parent)
        
        self.create_widgets()
        self.create_layout()
        self.pack(expand = True, fill = 'both')
         
    def create_widgets(self):        
        self.header_label = ctk.CTkLabel(self, text = 'Generar historia clínica', font = ("Calibri",30), compound = 'center')
        
        ## DNI entry ##
        self.enter_dni_label = ctk.CTkLabel(self, text = 'D.N.I:', font = ("Calibri",18), compound = 'center')
        self.entry_dni_var = ctk.StringVar()
        self.entry_dni = ctk.CTkEntry(self, textvariable = self.entry_dni_var,border_color='black')
        self.entry_dni.bind('<Return>', lambda event, query_arg='dni': get_pacient_event(self,event,query_arg))
        self.submit_dni_button = ctk.CTkButton(self, text = 'Enviar', command = lambda : get_pacient(self,'dni'),
                                               font = ("Calibri",15), fg_color="#4287f5",hover_color = "#196ef7",
                                               border_width=2.8,border_color="black",text_color='black')
        
        ## Name entry ##
        self.enter_name_label = ctk.CTkLabel(self, text = 'NOMBRE:', font = ("Calibri",18), compound = 'center')
        self.enter_surname_label = ctk.CTkLabel(self, text = 'APELLIDO:', font = ("Calibri",18), compound = 'center')
        self.entry_name_var = ctk.StringVar()
        self.entry_name = ctk.CTkEntry(self, textvariable = self.entry_name_var,border_color='black')
        self.entry_surname_var = ctk.StringVar()
        self.entry_surname = ctk.CTkEntry(self, textvariable = self.entry_surname_var,border_color='black')
        self.entry_surname.bind('<Return>', lambda event, query_arg = 'fullname': get_pacient_event(self,event,query_arg))
        self.submit_fullname_button = ctk.CTkButton(self, text = 'Enviar', command = lambda : get_pacient(self,'fullname'),
                                                    font = ("Calibri",15), fg_color="#4287f5",hover_color = "#196ef7",
                                                    border_width=2.8,border_color="black",text_color='black')
        
        ## Data Results ## 
        self.header_data_label = ctk.CTkLabel(self, text = 'Datos del paciente:', font = ("Calibri",30), compound = 'center')
        
        self.dni_label = ctk.CTkLabel(self, text = 'D.N.I:', font = ("Calibri",18), compound = 'center')
        self.dni_text_var = ctk.StringVar()
        self.entry_data_dni = ctk.CTkLabel(self, textvariable = self.dni_text_var)
        
        self.name_label = ctk.CTkLabel(self, text = 'NOMBRE:', font = ("Calibri",18), compound = 'center')
        self.name_text_var = ctk.StringVar()
        self.entry_data_name = ctk.CTkLabel(self, textvariable = self.name_text_var)
        
        self.surname_label = ctk.CTkLabel(self, text = 'APELLIDO:', font = ("Calibri",18), compound = 'center')
        self.surname_text_var = ctk.StringVar()
        self.entry_data_surname = ctk.CTkLabel(self, textvariable = self.surname_text_var)
        
        self.age_label = ctk.CTkLabel(self, text = 'EDAD:', font = ("Calibri",18), compound = 'center')
        self.age_text_var = ctk.StringVar()
        self.entry_data_age = ctk.CTkLabel(self, textvariable = self.age_text_var)
        
        self.phone_label = ctk.CTkLabel(self, text = 'TELEFONO:', font = ("Calibri",18), compound = 'center')
        self.phone_text_var = ctk.StringVar()
        self.entry_phone = ctk.CTkLabel(self, textvariable = self.phone_text_var)
        
        self.address_label = ctk.CTkLabel(self, text = 'DOMICILIO:', font = ("Calibri",18), compound = 'center')
        self.address_text_var = ctk.StringVar()
        self.entry_address = ctk.CTkLabel(self, textvariable = self.address_text_var)
        
        self.company_label = ctk.CTkLabel(self, text = 'EMPRESA:', font = ("Calibri",18), compound = 'center')
        self.company_text_var = ctk.StringVar()
        self.entry_company = ctk.CTkLabel(self, textvariable = self.company_text_var)
        
        self.job_label = ctk.CTkLabel(self, text = 'PUESTO DE TRABAJO:', font = ("Calibri",18), compound = 'center')
        self.job_text_var = ctk.StringVar()
        self.entry_job = ctk.CTkLabel(self, textvariable = self.job_text_var)
        
        self.art_label = ctk.CTkLabel(self, text = 'A.R.T:', font = ("Calibri",18), compound = 'center')
        self.art_text_var = ctk.StringVar()
        self.entry_art = ctk.CTkLabel(self, textvariable = self.art_text_var)
        
        self.siniester_label = ctk.CTkLabel(self, text = 'N° SINIESTRO:', font = ("Calibri",18), compound = 'center')
        self.siniester_text_var = ctk.StringVar()
        self.entry_siniester = ctk.CTkLabel(self, textvariable = self.siniester_text_var)
        
        self.accident_date_label = ctk.CTkLabel(self, text = 'FECHA DE ACCIDENTE:', font = ("Calibri",18), compound = 'center')
        self.accident_date_text_var = ctk.StringVar()
        self.entry_accident_date = ctk.CTkLabel(self, textvariable = self.accident_date_text_var)
        
        self.dr_label = ctk.CTkLabel(self, text = 'DR DERIVANTE:', font = ("Calibri",18), compound = 'center')
        self.dr_text_var = ctk.StringVar()
        self.entry_dr = ctk.CTkLabel(self, textvariable = self.dr_text_var)
        
        self.start_date_label = ctk.CTkLabel(self, text = 'FECHA DE INICIO', font = ("Calibri",18), compound = 'center')
        self.start_date_text_var = ctk.StringVar()
        self.entry_start_date = ctk.CTkLabel(self, textvariable = self.start_date_text_var)
        
        self.generate_button = ctk.CTkButton(self, text = 'Generar historia clínica', command = lambda : HistoriaClinica.generatePdf(self),
                                            font = ("Calibri",15), fg_color="#4287f5",hover_color = "#196ef7",
                                            border_width=2.8,border_color="black",text_color='black')
          
    def create_layout(self):
        self.columnconfigure((0,1,2,3), weight = 1)
        self.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight = 1)
        
        ## HEADER ##
        self.header_label.grid(row = 0, column = 0, columnspan = 4)
        
        ## ENTRY ##
        self.enter_dni_label.grid(row = 1, column = 0, rowspan = 2)
        self.entry_dni.grid(row = 1, column = 1, rowspan = 2)
        
        self.enter_name_label.grid(row = 1, column = 2)
        self.entry_name.grid(row = 1, column = 3)
        
        self.enter_surname_label.grid(row = 2, column = 2)
        self.entry_surname.grid(row = 2, column = 3)
        
        self.submit_dni_button.grid(row = 3, column = 0, columnspan = 2)
        self.submit_fullname_button.grid(row = 3, column = 2, columnspan = 2)
        
        ## DATA ##
        self.header_data_label.grid(row = 4, column = 0, columnspan = 4, pady = 18)
        
        self.dni_label.grid(row = 5, column = 0)
        self.entry_data_dni.grid(row = 5, column = 1)
        
        self.name_label.grid(row = 5, column = 2)
        self.entry_data_name.grid(row = 5, column = 3)
        
        self.surname_label.grid(row = 6, column = 0)
        self.entry_data_surname.grid(row = 6, column = 1)
        
        self.age_label.grid(row = 6, column = 2)
        self.entry_data_age.grid(row = 6, column = 3)
        
        self.phone_label.grid(row = 7, column = 0)
        self.entry_phone.grid(row = 7, column = 1)
        
        self.address_label.grid(row = 7, column = 2)
        self.entry_address.grid(row = 7, column = 3)
        
        self.company_label.grid(row = 8, column = 0)
        self.entry_company.grid(row = 8, column = 1)
        
        self.job_label.grid(row = 8, column = 2)
        self.entry_job.grid(row = 8, column = 3)
        
        self.art_label.grid(row = 9, column = 0)
        self.entry_art.grid(row = 9, column = 1)
        
        self.siniester_label.grid(row = 9, column = 2)
        self.entry_siniester.grid(row = 9, column = 3)
        
        self.accident_date_label.grid(row = 10, column = 0)
        self.entry_accident_date.grid(row = 10, column = 1)
        
        self.dr_label.grid(row = 10, column = 2)
        self.entry_dr.grid(row = 10, column = 3)
        
        self.generate_button.grid(row = 11, column = 0, columnspan = 4, pady = 18)
    
    def generatePdf(self):
        answer = messagebox.askquestion(title = 'Confirmación', message = '¿Seguro que desea continuar?')
        if answer == "yes":
            output_pdf = '..\\files\historia_clinica.pdf'
            
            dni = self.dni_text_var.get()
            name = self.name_text_var.get()
            surname = self.surname_text_var.get()
            art = self.art_text_var.get()
            age = self.age_text_var.get()
            phone = self.phone_text_var.get()
            address = self.address_text_var.get()
            company = self.company_text_var.get()
            job = self.job_text_var.get()
            dr = self.dr_text_var.get()
            accident_date = self.accident_date_text_var.get()
            siniester = self.siniester_text_var.get()
            start_date = self.start_date_text_var.get()
            
            
            #-------------------- pdf creation ------------------------- #
            
            pdf = FPDF('P','mm','Legal')
            pdf.add_page()
            pdf.set_font('helvetica','',14)
            pdf.set_margins(left=0,top=41,right=0)
            
            pdf.cell(0,10,"Paciente: " + surname +", " + name, new_x="LMARGIN", new_y="NEXT")
            pdf.cell(85,10, "Edad: " + age)
            pdf.cell(65,10, "D.N.I: " + dni)
            pdf.cell(65,10, "A.R.T: " + art, new_x="LMARGIN", new_y="NEXT")
            pdf.cell(85,10, "Tel: " + phone)
            pdf.cell(85,10, "Domicilio: " + address, new_x="LMARGIN", new_y="NEXT")
            pdf.cell(85,10, "Empresa: " + company)
            pdf.cell(85,10, "Puesto de trabajo: " + job, new_x="LMARGIN", new_y="NEXT")
            pdf.cell(85,10, "Dr. Derivante: " + dr)
            pdf.cell(75,10, "Fecha de accidente: " + accident_date)
            pdf.cell(65,10, "N° siniestro: " + siniester, new_x="LMARGIN", new_y="NEXT")
            pdf.cell(150,10, "Diagnóstico Médico: ..........................................................")
            pdf.cell(70,10, "Fecha de inicio: " + start_date, new_x="LMARGIN", new_y="NEXT")
            pdf.cell(0,10,"Dominancia: ...............", new_x="LMARGIN", new_y="NEXT")
                
            pdf.output(output_pdf)
            
            
            # print generated pdf
            #os.startfile(output_pdf, 'print')
            clear_fields(self)
                
app = App()
app.mainloop()