import re
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
from tkinter.font import Font
import sqlite3
from fpdf import FPDF
from datetime import datetime
import sys
import os

## GLOBAL VARIABLES
DEFAULT_ART_MSG = 'Seleccione A.R.T'
ENTRY_WIDTH = 250

font_type = 'Calibri'
header_font_size = 30
HEADER_FONT = (font_type, header_font_size)

label_font_size = 18
LABEL_FONT = (font_type,label_font_size)

entry_font_size = 20
ENTRY_FONT = (font_type,entry_font_size)

button_font_size = 18
BUTTON_FONT = (font_type,button_font_size)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def create_general_widgets(obj,header_text,button_text,button_func):
    obj.header_label = ctk.CTkLabel(obj, text = header_text, font = HEADER_FONT, compound = 'center')
        
    ## DNI entry ##
    obj.enter_dni_label = ctk.CTkLabel(obj, text = 'D.N.I:', font = LABEL_FONT, compound = 'center')
    obj.entry_dni_var = ctk.StringVar()
    obj.entry_dni = ctk.CTkEntry(obj, textvariable = obj.entry_dni_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
    obj.entry_dni.bind('<Return>', lambda event, query_arg='dni': get_pacient_event(obj,event,query_arg))
    obj.submit_dni_button = ctk.CTkButton(obj, text = 'Enviar', command = lambda : get_pacient(obj,'dni'),
                                            font = BUTTON_FONT, fg_color="#4287f5",hover_color = "#196ef7",
                                            border_width=2.8,border_color="black",text_color='black')
        
    ## Name entry ##
    obj.enter_name_label = ctk.CTkLabel(obj, text = 'NOMBRE:', font = LABEL_FONT, compound = 'center')
    obj.enter_surname_label = ctk.CTkLabel(obj, text = 'APELLIDO:', font = LABEL_FONT, compound = 'center')
    obj.entry_name_var = ctk.StringVar()
    obj.entry_name = ctk.CTkEntry(obj, textvariable = obj.entry_name_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
    obj.entry_surname_var = ctk.StringVar()
    obj.entry_surname = ctk.CTkEntry(obj, textvariable = obj.entry_surname_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
    obj.entry_surname.bind('<Return>', lambda event, query_arg = 'fullname': get_pacient_event(obj,event,query_arg))
    obj.submit_fullname_button = ctk.CTkButton(obj, text = 'Enviar', command = lambda : get_pacient(obj,'fullname'),
                                                font = BUTTON_FONT, fg_color="#4287f5",hover_color = "#196ef7",
                                                border_width=2.8,border_color="black",text_color='black')
        
    ## Data Results ## 
    obj.header_data_label = ctk.CTkLabel(obj, text = 'Datos del paciente:', font = HEADER_FONT, compound = 'center')
        
    obj.dni_label = ctk.CTkLabel(obj, text = 'D.N.I:', font = LABEL_FONT, compound = 'center')
    obj.dni_text_var = ctk.StringVar()
    obj.entry_data_dni = ctk.CTkLabel(obj, textvariable = obj.dni_text_var, font = LABEL_FONT)
        
    obj.name_label = ctk.CTkLabel(obj, text = 'NOMBRE:', font = LABEL_FONT, compound = 'center')
    obj.name_text_var = ctk.StringVar()
    obj.entry_data_name = ctk.CTkLabel(obj, textvariable = obj.name_text_var, font = LABEL_FONT)
        
    obj.surname_label = ctk.CTkLabel(obj, text = 'APELLIDO:', font = LABEL_FONT, compound = 'center')
    obj.surname_text_var = ctk.StringVar()
    obj.entry_data_surname = ctk.CTkLabel(obj, textvariable = obj.surname_text_var, font = LABEL_FONT)
        
    obj.age_label = ctk.CTkLabel(obj, text = 'EDAD:', font = LABEL_FONT, compound = 'center')
    obj.age_text_var = ctk.StringVar()
    obj.entry_data_age = ctk.CTkLabel(obj, textvariable = obj.age_text_var, font = LABEL_FONT)
        
    obj.phone_label = ctk.CTkLabel(obj, text = 'TELEFONO:', font = LABEL_FONT, compound = 'center')
    obj.phone_text_var = ctk.StringVar()
    obj.entry_phone = ctk.CTkLabel(obj, textvariable = obj.phone_text_var, font = LABEL_FONT)
        
    obj.address_label = ctk.CTkLabel(obj, text = 'DOMICILIO:', font = LABEL_FONT, compound = 'center')
    obj.address_text_var = ctk.StringVar()
    obj.entry_address = ctk.CTkLabel(obj, textvariable = obj.address_text_var, font = LABEL_FONT)
        
    obj.company_label = ctk.CTkLabel(obj, text = 'EMPRESA:', font = LABEL_FONT, compound = 'center')
    obj.company_text_var = ctk.StringVar()
    obj.entry_company = ctk.CTkLabel(obj, textvariable = obj.company_text_var, font = LABEL_FONT)
        
    obj.job_label = ctk.CTkLabel(obj, text = 'PUESTO DE TRABAJO:', font = LABEL_FONT, compound = 'center')
    obj.job_text_var = ctk.StringVar()
    obj.entry_job = ctk.CTkLabel(obj, textvariable = obj.job_text_var, font = LABEL_FONT)
        
    obj.art_label = ctk.CTkLabel(obj, text = 'A.R.T:', font = LABEL_FONT, compound = 'center')
    obj.art_text_var = ctk.StringVar()
    obj.entry_art = ctk.CTkLabel(obj, textvariable = obj.art_text_var, font = LABEL_FONT)
        
    obj.siniester_label = ctk.CTkLabel(obj, text = 'N° SINIESTRO:', font = LABEL_FONT, compound = 'center')
    obj.siniester_text_var = ctk.StringVar()
    obj.entry_siniester = ctk.CTkLabel(obj, textvariable = obj.siniester_text_var, font = LABEL_FONT)
        
    obj.accident_date_label = ctk.CTkLabel(obj, text = 'FECHA DE ACCIDENTE:', font = LABEL_FONT, compound = 'center')
    obj.accident_date_text_var = ctk.StringVar()
    obj.entry_accident_date = ctk.CTkLabel(obj, textvariable = obj.accident_date_text_var, font = LABEL_FONT)
        
    obj.dr_label = ctk.CTkLabel(obj, text = 'DR DERIVANTE:', font = LABEL_FONT, compound = 'center')
    obj.dr_text_var = ctk.StringVar()
    obj.entry_dr = ctk.CTkLabel(obj, textvariable = obj.dr_text_var, font = LABEL_FONT)
        
    obj.start_date_label = ctk.CTkLabel(obj, text = 'FECHA DE INICIO', font = LABEL_FONT, compound = 'center')
    obj.start_date_text_var = ctk.StringVar()
    obj.entry_start_date = ctk.CTkLabel(obj, textvariable = obj.start_date_text_var, font = LABEL_FONT)
        
    obj.button = ctk.CTkButton(obj, text = button_text, command = lambda : button_func(obj),
                                        font = BUTTON_FONT, fg_color="#4287f5",hover_color = "#196ef7",
                                        border_width=2.8,border_color="black",text_color='black')
    
    obj.clear_button = ctk.CTkButton(obj, text = 'Limpiar', command = lambda : clear_fields(obj),
                                            font = BUTTON_FONT, fg_color="#c7c4bd",hover_color = "#a19e97",
                                            border_width=2.8,border_color="black",text_color='black')

def create_general_layout(obj):
    obj.columnconfigure((0,1,2,3), weight = 1)
    obj.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12), weight = 1)
    
    ## HEADER ##
    obj.header_label.grid(row = 0, column = 0, columnspan = 4)
    
    ## ENTRY ##
    obj.enter_dni_label.grid(row = 1, column = 0, rowspan = 2)
    obj.entry_dni.grid(row = 1, column = 1, rowspan = 2)
    
    obj.enter_name_label.grid(row = 1, column = 2)
    obj.entry_name.grid(row = 1, column = 3)
    
    obj.enter_surname_label.grid(row = 2, column = 2)
    obj.entry_surname.grid(row = 2, column = 3)
    
    obj.submit_dni_button.grid(row = 3, column = 0, columnspan = 2)
    obj.submit_fullname_button.grid(row = 3, column = 2, columnspan = 2)
    
    ## DATA ##
    obj.header_data_label.grid(row = 4, column = 0, columnspan = 4, pady = 18)
    
    obj.dni_label.grid(row = 5, column = 0)
    obj.entry_data_dni.grid(row = 5, column = 1)
    
    obj.name_label.grid(row = 5, column = 2)
    obj.entry_data_name.grid(row = 5, column = 3)
    
    obj.surname_label.grid(row = 6, column = 0)
    obj.entry_data_surname.grid(row = 6, column = 1)
    
    obj.age_label.grid(row = 6, column = 2)
    obj.entry_data_age.grid(row = 6, column = 3)
    
    obj.phone_label.grid(row = 7, column = 0)
    obj.entry_phone.grid(row = 7, column = 1)
    
    obj.address_label.grid(row = 7, column = 2)
    obj.entry_address.grid(row = 7, column = 3)
    
    obj.company_label.grid(row = 8, column = 0)
    obj.entry_company.grid(row = 8, column = 1)
    
    obj.job_label.grid(row = 8, column = 2)
    obj.entry_job.grid(row = 8, column = 3)
    
    obj.art_label.grid(row = 9, column = 0)
    obj.entry_art.grid(row = 9, column = 1)
    
    obj.siniester_label.grid(row = 9, column = 2)
    obj.entry_siniester.grid(row = 9, column = 3)
    
    obj.accident_date_label.grid(row = 10, column = 0)
    obj.entry_accident_date.grid(row = 10, column = 1)
    
    obj.dr_label.grid(row = 10, column = 2)
    obj.entry_dr.grid(row = 10, column = 3)
    
    obj.button.grid(row = 11, column = 0, columnspan = 4, pady = 18)
    obj.clear_button.grid(row = 12, column = 3,pady = 18)

def normalize_string(string):
    if(string == ""):
        return None
    string_aux = re.sub(' +', ' ', string)
    if(string_aux[-1] == " "):
        string_aux = string_aux[:-1]
    
    string_aux = string_aux.lower()
    string_aux = string_aux.split(" ")
        
    new_string = ""
    for i in string_aux:
        new_string += i.capitalize() + " "
    new_string = new_string[:-1]
    
    return new_string

def is_valid_date(date):
    #date = str(date)
    #size = len(date)
    #if(size < 8):
    if(len(date) < 8):
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
    conn = sqlite3.connect(resource_path('database\cai_database.db'))
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
    
    conn = sqlite3.connect(resource_path('database\cai_database.db'))
    query = f"SELECT Dni FROM Paciente WHERE Dni = {dni} "
    cursor = conn.execute(query)
    data = cursor.fetchone()
    
    #already exists one person with that dni
    if(data != None):
        return False
    else:
        return True

def get_art():
    conn = sqlite3.connect(resource_path('database\cai_database.db'))
    query = 'SELECT Nombre FROM Art'
    cursor = conn.execute(query)
    data = cursor.fetchall()
    
    arts = list()
    for art in data:
        arts.append(art[0])
        
    return arts
    
def combo_art_func(obj, event):
    obj.art_text_var.set(obj.entry_data_art.get())  

def get_pacient(obj, query_arg):
        obj_name = obj.__class__.__name__
        conn = sqlite3.connect(resource_path('database\cai_database.db'))
        
        if(query_arg =='dni'):
            dni = int(obj.entry_dni_var.get())
            query = f'''SELECT P.Dni, P.Nombre, P.Apellido, A.Nombre, P.Siniestro,
                    P.Puesto_Trabajo, P.Fecha_Accidente, P.Telefono, P.Dr_derivante,
                    P.Fecha_Inicio, P.Empresa, P.Domicilio, P.Edad
                    FROM Paciente P
                    INNER JOIN Art A on P.Art = A.Id
                    WHERE P.Dni = {dni} '''
                    
        else:
            name = normalize_string(obj.entry_name_var.get())
            
            surname = normalize_string(obj.entry_surname_var.get())
            
            query = f'''SELECT P.Dni, P.Nombre, P.Apellido, A.Nombre, P.Siniestro, 
                    P.Puesto_Trabajo, P.Fecha_Accidente, P.Telefono, P.Dr_derivante,
                    P.Fecha_Inicio, P.Empresa, P.Domicilio, P.Edad
                    FROM Paciente P
                    INNER JOIN Art A on P.Art = A.Id
                    WHERE P.Nombre LIKE '{name}%' AND P.Apellido = '{surname}' '''
            
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
            
            if(obj_name == 'ModificarPacienteFrame'):
                #aux variable for update function
                obj.prev_dni = data[0]
                #updating art ComboBox in update window
                obj.entry_data_art.set(data[3])
            
        conn.close()

def get_pacient_event(obj, event, query_arg):
    obj_name = obj.__class__.__name__
    conn = sqlite3.connect(resource_path('database\cai_database.db'))
    
    if(query_arg =='dni'):
        dni = int(obj.entry_dni_var.get())
        query = f'''SELECT P.Dni, P.Nombre, P.Apellido, A.Nombre, P.Siniestro,
                P.Puesto_Trabajo, P.Fecha_Accidente, P.Telefono, P.Dr_derivante,
                P.Fecha_Inicio, P.Empresa, P.Domicilio, P.Edad
                FROM Paciente P
                INNER JOIN Art A on P.Art = A.Id
                WHERE P.Dni = {dni} '''
                
    else:
        name = normalize_string(obj.entry_name_var.get())
        
        surname = normalize_string(obj.entry_surname_var.get())
        
        query = f'''SELECT P.Dni, P.Nombre, P.Apellido, A.Nombre, P.Siniestro, 
                P.Puesto_Trabajo, P.Fecha_Accidente, P.Telefono, P.Dr_derivante,
                P.Fecha_Inicio, P.Empresa, P.Domicilio, P.Edad
                FROM Paciente P
                INNER JOIN Art A on P.Art = A.Id
                WHERE P.Nombre LIKE '{name}%' AND P.Apellido = '{surname}' '''
        
    cursor = conn.execute(query)
    data = cursor.fetchone()
    if(data == None and query_arg == 'dni'):
        messagebox.showerror(title = 'Error: Dni no valido', message = f'No existe el paciente con dni: {dni}')
    elif(data == None and query_arg == 'fullname'):
        messagebox.showerror(title = 'Error: Nombre no valido', message = f'No existe el paciente con nombre: {surname}, {name}')
    else:
        conn.close()
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
        
        if(obj_name == 'ModificarPacienteFrame'):
            #aux variable for update function
            obj.prev_dni = data[0]
            #updating art ComboBox in update window
            obj.entry_data_art.set(data[3]) 

def get_fields(obj,called_from):  
    dni = obj.dni_text_var.get()
    name = normalize_string(obj.name_text_var.get())
    surname = normalize_string(obj.surname_text_var.get())
    art = obj.art_text_var.get()
    

    if(dni == '' or name == '' or surname == '' or art == ''):
            return["blank_fields"]
        
    
    if(not dni.isdigit()):
        return["digit_field_err",'DNI']
    dni = int(dni)
    #validate DNI if function was called in creation method
    if(called_from == 'create'):
        if(not dni_is_valid(dni)):
                return["invalid_dni",dni]
        
    ## validate ART name
    is_valid, art_id = validate_art(art)
    if (not is_valid):
        return["invalid_art",art]
        
    accident_date = obj.accident_date_text_var.get()
    if(not is_valid_date(accident_date)):
        return["invalid_date"]
    
    accident_date = format_date(accident_date)
        
    age = obj.age_text_var.get()
    if(not age.isdigit() and age != ''):
        return["digit_field_err",'EDAD']
        
    phone = obj.phone_text_var.get()
    if(not phone.isdigit() and phone != ''):
        return["digit_field_err",'TELEFONO']
    
    address = normalize_string(obj.address_text_var.get())
        
    company = normalize_string(obj.company_text_var.get())
      
    job = normalize_string(obj.job_text_var.get())
        
    siniester = obj.siniester_text_var.get()
    siniester = siniester.upper()
            
    dr = normalize_string(obj.dr_text_var.get())
    
    return [dni,name,surname,age,phone,address,company,job,art_id,siniester,accident_date,dr]
     
def clear_fields(obj):
        obj_name = obj.__class__.__name__
        obj.entry_dni_var.set('')
        obj.entry_name_var.set('')
        obj.entry_surname_var.set('')
        obj.dni_text_var.set('')
        obj.name_text_var.set('')
        obj.surname_text_var.set('')
        if(obj_name == 'ModificarPacienteFrame'):
            obj.entry_data_art.set(DEFAULT_ART_MSG)
        else:
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

def generate_sign_pdf(obj):
        answer = messagebox.askquestion(title = 'Confirmación', message = '¿Seguro que desea continuar?')
        if answer == "yes":
            output_pdf = resource_path('files\planilla_asistencia.pdf')
            dni = obj.dni_text_var.get()
            name = obj.name_text_var.get()
            surname = obj.surname_text_var.get()
            art = obj.art_text_var.get()
            
            #-------------------- pdf creation ------------------------- #
            
            # if art = galeno, create especific galeno's pdf
            if(art == 'GALENO'):
                siniester = obj.siniester_text_var.get()
                job = obj.job_text_var.get()
                accident_date = obj.accident_date_text_var.get()
                start_date = obj.start_date_text_var.get()
                
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
            
                pdf.cell(60,16,"Nombre y apellido: ")
                pdf.set_font('helvetica','',25)
                name = name.upper()
                surname = surname.upper()
                pdf.cell(0,16,surname +", " + name, new_x="LMARGIN", new_y="NEXT")
                
                pdf.set_font('helvetica','',18)
                pdf.cell(80,16,"D.N.I: " + dni)
                pdf.cell(20,16,"A.R.T: ")
                pdf.set_font('helvetica','',25)
                pdf.cell(0,16,art, new_x="LMARGIN", new_y="NEXT")
                
                
                
                pdf.set_font('helvetica','',18)
                pdf.cell(0,16,"TURNO: ........................",new_x="LMARGIN",new_y="NEXT")
                
                pdf.output(output_pdf)
            
            
            # print generated pdf
            os.startfile(output_pdf, 'print')
            obj_name = obj.__class__.__name__
            if(obj_name == 'GenerarFichaFrame'):
                clear_fields(obj)

def generate_clinic_pdf(obj):
        answer = messagebox.askquestion(title = 'Confirmación', message = '¿Seguro que desea continuar?')
        if answer == "yes":
            obj_name = obj.__class__.__name__
            output_pdf = resource_path('files\historia_clinica.pdf')
            
            dni = obj.dni_text_var.get()
            name = obj.name_text_var.get()
            surname = obj.surname_text_var.get()
            art = obj.art_text_var.get()
            age = obj.age_text_var.get()
            phone = obj.phone_text_var.get()
            address = obj.address_text_var.get()
            company = obj.company_text_var.get()
            job = obj.job_text_var.get()
            dr = obj.dr_text_var.get()
            siniester = obj.siniester_text_var.get()
            
            if(obj_name == 'AltaPacienteFrame'):
                accident_date = obj.accident_date_text_var.get()
                accident_date = format_date(accident_date)
                current_date = datetime.now()
                current_date = current_date.strftime('%d/%m/%Y')
                start_date = current_date
            else:
                accident_date = obj.accident_date_text_var.get()
                start_date = obj.start_date_text_var.get()
            
            #-------------------- pdf creation ------------------------- #
            
            pdf = FPDF('P','mm','Legal')
            pdf.add_page()
            pdf.set_font('helvetica','',14)
            pdf.set_margins(left=0,top=41,right=0)
            
            name = name.upper()
            surname = surname.upper()
            pdf.cell(0,10,"Paciente: " + surname +", " + name, new_x="LMARGIN", new_y="NEXT")
            pdf.cell(85,10, "Edad: " + age)
            pdf.cell(50,10, "D.N.I: " + dni)
            pdf.cell(90,10, "A.R.T: " + art, new_x="LMARGIN", new_y="NEXT")
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
            os.startfile(output_pdf, 'print')
            
            if(obj_name == 'HistoriaClinica'):
                clear_fields(obj)

class App(ctk.CTk):
    def __init__(self):
        # main setup
        super().__init__()
        self.title('Fichas pacientes')
        self.iconbitmap(resource_path('images\logo.ico'))
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
        self.add('ALTA')
        self.add('BAJA')
        self.add('MODIFICAR')
        self.add('PLANILLA')
        self.add('HISTORIA CLINICA')
        self.add('ALTA ART')
        
        # widgets
        AltaPacienteFrame(self.tab('ALTA'))
        BajaPacienteFrame(self.tab('BAJA'))
        ModificarPacienteFrame(self.tab('MODIFICAR'))
        GenerarFichaFrame(self.tab('PLANILLA'))
        HistoriaClinica(self.tab('HISTORIA CLINICA'))
        AltaARTFrame(self.tab('ALTA ART'))
        
class GenerarFichaFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        create_general_widgets(self,'Generar planilla firmas paciente','Generar planilla', lambda self: generate_sign_pdf(self))
        create_general_layout(self)
        self.pack(expand = True, fill = 'both')        
               
class AltaPacienteFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)  
        self.create_widgets()
        self.create_layout()
        self.pack(expand = True, fill = 'both')
       
    def create_widgets(self):
        self.header_label = ctk.CTkLabel(self, text = 'Dar de alta paciente:', font = ("Calibri",30), compound = 'center')
        
        self.dni_label = ctk.CTkLabel(self, text = 'D.N.I:', font = LABEL_FONT, compound = 'center')
        self.dni_text_var = ctk.StringVar()
        self.entry_data_dni = ctk.CTkEntry(self, textvariable = self.dni_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        
        self.name_label = ctk.CTkLabel(self, text = 'NOMBRE:', font = LABEL_FONT, compound = 'center')
        self.name_text_var = ctk.StringVar()
        self.entry_data_name = ctk.CTkEntry(self, textvariable = self.name_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        
        self.surname_label = ctk.CTkLabel(self, text = 'APELLIDO:', font = LABEL_FONT, compound = 'center')
        self.surname_text_var = ctk.StringVar()
        self.entry_data_surname = ctk.CTkEntry(self, textvariable = self.surname_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        
        self.age_label = ctk.CTkLabel(self, text = 'EDAD:', font = LABEL_FONT, compound = 'center')
        self.age_text_var = ctk.StringVar()
        self.entry_data_age = ctk.CTkEntry(self, textvariable = self.age_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        
        self.phone_label = ctk.CTkLabel(self, text = 'TELEFONO:', font = LABEL_FONT, compound = 'center')
        self.phone_text_var = ctk.StringVar()
        self.entry_data_phone = ctk.CTkEntry(self, textvariable = self.phone_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        
        self.address_label = ctk.CTkLabel(self, text = 'DOMICILIO:', font = LABEL_FONT, compound = 'center')
        self.address_text_var = ctk.StringVar()
        self.entry_data_address = ctk.CTkEntry(self, textvariable = self.address_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        
        self.company_label = ctk.CTkLabel(self, text = 'EMPRESA:', font = LABEL_FONT, compound = 'center')
        self.company_text_var = ctk.StringVar()
        self.entry_data_company = ctk.CTkEntry(self, textvariable = self.company_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        
        self.job_label = ctk.CTkLabel(self, text = 'PUESTO DE TRABAJO:', font = LABEL_FONT, compound = 'center')
        self.job_text_var = ctk.StringVar()
        self.entry_data_job = ctk.CTkEntry(self, textvariable = self.job_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        
        self.art_label = ctk.CTkLabel(self, text = 'A.R.T:', font = LABEL_FONT, compound = 'center')
        self.art_text_var = ctk.StringVar()
        self.entry_data_art = ctk.CTkComboBox(self, state = 'readonly', values = get_art(), 
                                              font = LABEL_FONT, width = ENTRY_WIDTH, border_color='black',
                                              button_color = "#4287f5", justify = 'center',
                                              command = lambda event: combo_art_func(self, event))
        self.entry_data_art.set(DEFAULT_ART_MSG)
            
        self.siniester_label = ctk.CTkLabel(self, text = 'N° SINIESTRO:', font = LABEL_FONT, compound = 'center')
        self.siniester_text_var = ctk.StringVar()
        self.entry_data_siniester = ctk.CTkEntry(self, textvariable = self.siniester_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        
        self.accident_date_label = ctk.CTkLabel(self, text = 'FECHA ACCIDENTE:', font = LABEL_FONT, compound = 'center')
        self.accident_date_text_var = ctk.StringVar()
        self.entry_data_accident_date = ctk.CTkEntry(self, textvariable = self.accident_date_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        
        self.dr_label = ctk.CTkLabel(self, text = 'DR DERIVANTE:', font = LABEL_FONT, compound = 'center')
        self.dr_text_var = ctk.StringVar()
        self.entry_data_dr = ctk.CTkEntry(self, textvariable = self.dr_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        self.entry_data_dr.bind('<Return>', lambda event: AltaPacienteFrame.create_pacient_event(self,event))
        
        self.start_date_label = ctk.CTkLabel(self, text = 'FECHA DE INICIO:', font = LABEL_FONT, compound = 'center')
        self.start_date_text_var = ctk.StringVar()
        self.entry_data_start_date = ctk.CTkEntry(self, textvariable = self.start_date_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        
        self.submit_button = ctk.CTkButton(self, text = 'Enviar', command = lambda : AltaPacienteFrame.create_pacient(self),
                                            font = BUTTON_FONT, fg_color="#4287f5",hover_color = "#196ef7",
                                            border_width=2.8,border_color="black",text_color='black')
        self.file_button = ctk.CTkButton(self, text = 'Imprimir planilla', command = lambda : generate_sign_pdf(self),
                                            font = BUTTON_FONT, fg_color="#4287f5",hover_color = "#196ef7",
                                            border_width=2.8,border_color="black",text_color='black')
        
        self.clinic_button = ctk.CTkButton(self, text = 'Imprimir historia clínica', command = lambda : generate_clinic_pdf(self),
                                            font = BUTTON_FONT, fg_color="#4287f5",hover_color = "#196ef7",
                                            border_width=2.8,border_color="black",text_color='black')
        
        self.clear_button = ctk.CTkButton(self, text = 'Limpiar', command = self.clear_fields,
                                            font = BUTTON_FONT, fg_color="#c7c4bd",hover_color = "#a19e97",
                                            border_width=2.8,border_color="black",text_color='black')
        
    def create_layout(self):
        self.columnconfigure((0,1,2,3), weight = 1)
        self.rowconfigure((0,1,2,3,4,5,6,7,8), weight = 1)
        
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
        self.file_button.grid(row = 8, column = 0, pady = 18)
        self.clinic_button.grid(row = 8, column = 1,pady = 18)
        self.clear_button.grid(row = 8, column = 3, pady = 18)
        
    def update_art_list(self):
        self.entry_data_art.configure(values = get_art())
    
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
        self.update_art_list()
        self.entry_data_art.set("Seleccione A.R.T")
    
    def create_pacient(self):
        fields = get_fields(self,'create')
        
        if(len(fields) == 12):
            dni = fields[0]
            name = fields[1]
            surname = fields[2]
            age = fields[3]
            phone = fields[4]
            address = fields[5]
            company = fields[6]
            job = fields[7]
            art = fields[8]
            siniester = fields[9]
            accident_date = fields[10]
            dr = fields[11]
            
            current_date = datetime.now()
            current_date = current_date.strftime('%d/%m/%Y')
            start_date = current_date
            
            conn = sqlite3.connect(resource_path('database\cai_database.db'))
            query = f'''INSERT INTO Paciente 
                        (Dni,Nombre,Apellido,Edad,Art,Siniestro,Puesto_Trabajo,Fecha_Accidente,Telefono,Dr_derivante,Fecha_Inicio,Empresa,Domicilio) 
                        VALUES ({dni},'{name}','{surname}','{age}',{art},'{siniester}','{job}','{accident_date}','{phone}','{dr}','{start_date}','{company}','{address}');'''
            try:
                cursor = conn.execute(query)
                conn.commit()
            except sqlite3.Error as er:
                print(er)
                messagebox.showerror(title = 'Error', message = 'Algo ha salido mal :(')
            else:
                messagebox.showinfo(title = 'Operacion satisfactoria!', message = f'Se ha dado de alta al paciente {surname}, {name}')
            finally:
                conn.close()
    
        else:
            match fields[0]:
                case "blank_fields":
                    messagebox.showerror(title = 'Error: Datos no validos', message = 'El DNI, NOMBRE, APELLIDO y ART no pueden estar en blanco')
                
                case "digit_field_err":
                    messagebox.showerror(title = 'Error: Datos no validos', message = f'El campo: {fields[1]} no puede contener letras')
                
                case "invalid_dni":
                    messagebox.showerror(title = 'Error: Dni no valido', message = f'Ya existe el paciente con dni: {fields[1]}')
                
                case "invalid_art":
                    messagebox.showerror(title = 'Error: ART invalida', message = f'La ART: {fields[1]} no existe')
                
                case "invalid_date":
                    messagebox.showerror(title = 'Error: Fecha no valida', message = 'Ingresar fecha en formato DDMMAAAA')
                               
    def create_pacient_event(self, event):
        fields = get_fields(self,'create')
        
        if(len(fields) == 12):
            dni = fields[0]
            name = fields[1]
            surname = fields[2]
            age = fields[3]
            phone = fields[4]
            address = fields[5]
            company = fields[6]
            job = fields[7]
            art = fields[8]
            siniester = fields[9]
            accident_date = fields[10]
            dr = fields[11]
            
            current_date = datetime.now()
            current_date = current_date.strftime('%d/%m/%Y')
            start_date = current_date
            
            conn = sqlite3.connect(resource_path('database\cai_database.db'))
            query = f'''INSERT INTO Paciente 
                        (Dni,Nombre,Apellido,Edad,Art,Siniestro,Puesto_Trabajo,Fecha_Accidente,Telefono,Dr_derivante,Fecha_Inicio,Empresa,Domicilio) 
                        VALUES ({dni},'{name}','{surname}','{age}',{art},'{siniester}','{job}','{accident_date}','{phone}','{dr}','{start_date}','{company}','{address}');'''
            try:
                cursor = conn.execute(query)
                conn.commit()
            except sqlite3.Error as er:
                print(er)
                messagebox.showerror(title = 'Error', message = 'Algo ha salido mal :(')
            else:
                messagebox.showinfo(title = 'Operacion satisfactoria!', message = f'Se ha dado de alta al paciente {surname}, {name}')
            finally:
                conn.close()
    
        else:
            match fields[0]:
                case "blank_fields":
                    messagebox.showerror(title = 'Error: Datos no validos', message = 'El DNI, NOMBRE, APELLIDO y ART no pueden estar en blanco')
                
                case "digit_field_err":
                    messagebox.showerror(title = 'Error: Datos no validos', message = f'El campo: {fields[1]} no puede contener letras')
                
                case "invalid_dni":
                    messagebox.showerror(title = 'Error: Dni no valido', message = f'Ya existe el paciente con dni: {fields[1]}')
                
                case "invalid_art":
                    messagebox.showerror(title = 'Error: ART invalida', message = f'La ART: {fields[1]} no existe')
                
                case "invalid_date":
                    messagebox.showerror(title = 'Error: Fecha no valida', message = 'Ingresar fecha en formato DDMMAAAA')

class AltaARTFrame(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.create_widgets()
        self.create_layout()
        self.pack(expand = True, fill = 'both')

    def create_widgets(self):
        self.header_label = ctk.CTkLabel(self, text = 'Dar de alta ART', font = ("Calibri",30), compound = 'center')
        self.name_label = ctk.CTkLabel(self, text = 'A.R.T:', font = LABEL_FONT, compound = 'center')
        self.entry_name_var = ctk.StringVar()
        self.entry_name = ctk.CTkEntry(self, textvariable = self.entry_name_var, width = 300, border_color='black', font = ENTRY_FONT)
        self.entry_name.bind('<Return>', lambda event: AltaARTFrame.create_art_event(self,event))
        self.submit_button = ctk.CTkButton(self, text = 'Dar de alta', command = lambda : AltaARTFrame.create_art(self),
                                            font = BUTTON_FONT, fg_color="#4287f5",hover_color = "#196ef7",
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
        conn = sqlite3.connect(resource_path('database\cai_database.db'))
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
        conn = sqlite3.connect(resource_path('database\cai_database.db'))
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
        create_general_widgets(self,'Dar de baja paciente','Dar de baja',BajaPacienteFrame.delete_pacient)
        create_general_layout(self)
        self.pack(expand = True, fill = 'both')
    
    def delete_pacient(self):
        dni = int(self.dni_text_var.get())
        name = self.name_text_var.get()
        surname = self.surname_text_var.get()
        
        answer = messagebox.askquestion(title = 'Confirmación', message = f'¿Seguro que desea dar de baja al paciente {surname}, {name}?')
        
        if answer == "yes":
            conn = sqlite3.connect(resource_path('database\cai_database.db'))
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
        self.enter_dni_label = ctk.CTkLabel(self, text = 'D.N.I:', font = LABEL_FONT, compound = 'center')
        self.entry_dni_var = ctk.StringVar()
        self.entry_dni = ctk.CTkEntry(self, textvariable = self.entry_dni_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        self.entry_dni.bind('<Return>', lambda event, query_arg='dni': get_pacient_event(self,event,query_arg))
        self.submit_dni_button = ctk.CTkButton(self, text = 'Enviar', command = lambda : get_pacient(self,'dni'),
                                               font = BUTTON_FONT, fg_color="#4287f5",hover_color = "#196ef7",
                                               border_width=2.8,border_color="black",text_color='black')
        
        ## Name entry ##
        self.enter_name_label = ctk.CTkLabel(self, text = 'NOMBRE:', font = LABEL_FONT, compound = 'center')
        self.enter_surname_label = ctk.CTkLabel(self, text = 'APELLIDO:', font = LABEL_FONT, compound = 'center')
        self.entry_name_var = ctk.StringVar()
        self.entry_name = ctk.CTkEntry(self, textvariable = self.entry_name_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        self.entry_surname_var = ctk.StringVar()
        self.entry_surname = ctk.CTkEntry(self, textvariable = self.entry_surname_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        self.entry_surname.bind('<Return>', lambda event, query_arg = 'fullname': get_pacient_event(self,event,query_arg))
        self.submit_fullname_button = ctk.CTkButton(self, text = 'Enviar', command = lambda : get_pacient(self,'fullname'),
                                                    font = BUTTON_FONT, fg_color="#4287f5",hover_color = "#196ef7",
                                                    border_width=2.8,border_color="black",text_color='black')
        
        ## Data Results ## 
        self.header_data_label = ctk.CTkLabel(self, text = 'Datos del paciente:', font = ("Calibri",30), compound = 'center')
        
        self.dni_label = ctk.CTkLabel(self, text = 'D.N.I:', font = LABEL_FONT, compound = 'center')
        self.dni_text_var = ctk.StringVar()
        self.entry_data_dni = ctk.CTkEntry(self, textvariable = self.dni_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        self.entry_data_dni.bind('<Return>', lambda event: AltaPacienteFrame.create_pacient_event(self,event))
        
        self.name_label = ctk.CTkLabel(self, text = 'NOMBRE:', font = LABEL_FONT, compound = 'center')
        self.name_text_var = ctk.StringVar()
        self.entry_data_name = ctk.CTkEntry(self, textvariable = self.name_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        self.entry_data_name.bind('<Return>', lambda event: AltaPacienteFrame.create_pacient_event(self,event))
        
        self.surname_label = ctk.CTkLabel(self, text = 'APELLIDO:', font = LABEL_FONT, compound = 'center')
        self.surname_text_var = ctk.StringVar()
        self.entry_data_surname = ctk.CTkEntry(self, textvariable = self.surname_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        self.entry_data_surname.bind('<Return>', lambda event: AltaPacienteFrame.create_pacient_event(self,event))
        
        self.age_label = ctk.CTkLabel(self, text = 'EDAD:', font = LABEL_FONT, compound = 'center')
        self.age_text_var = ctk.StringVar()
        self.entry_data_age = ctk.CTkEntry(self, textvariable = self.age_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        self.entry_data_age.bind('<Return>', lambda event: AltaPacienteFrame.create_pacient_event(self,event))
        
        self.phone_label = ctk.CTkLabel(self, text = 'TELEFONO:', font = LABEL_FONT, compound = 'center')
        self.phone_text_var = ctk.StringVar()
        self.entry_data_phone = ctk.CTkEntry(self, textvariable = self.phone_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        self.entry_data_phone.bind('<Return>', lambda event: AltaPacienteFrame.create_pacient_event(self,event))
        
        self.address_label = ctk.CTkLabel(self, text = 'DOMICILIO:', font = LABEL_FONT, compound = 'center')
        self.address_text_var = ctk.StringVar()
        self.entry_data_address = ctk.CTkEntry(self, textvariable = self.address_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        self.entry_data_address.bind('<Return>', lambda event: AltaPacienteFrame.create_pacient_event(self,event))
        
        self.company_label = ctk.CTkLabel(self, text = 'EMPRESA:', font = LABEL_FONT, compound = 'center')
        self.company_text_var = ctk.StringVar()
        self.entry_data_company = ctk.CTkEntry(self, textvariable = self.company_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        self.entry_data_company.bind('<Return>', lambda event: AltaPacienteFrame.create_pacient_event(self,event))
        
        self.job_label = ctk.CTkLabel(self, text = 'PUESTO DE TRABAJO:', font = LABEL_FONT, compound = 'center')
        self.job_text_var = ctk.StringVar()
        self.entry_data_job = ctk.CTkEntry(self, textvariable = self.job_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        self.entry_data_job.bind('<Return>', lambda event: AltaPacienteFrame.create_pacient_event(self,event))
        
        self.art_label = ctk.CTkLabel(self, text = 'A.R.T:', font = LABEL_FONT, compound = 'center')
        self.art_text_var = ctk.StringVar()
        self.entry_data_art = ctk.CTkComboBox(self, state = 'readonly', values = get_art(), 
                                              font = LABEL_FONT, width = ENTRY_WIDTH, border_color='black',
                                              button_color = "#4287f5", justify = 'center', 
                                              command = lambda event: combo_art_func(self, event))
        self.entry_data_art.set(DEFAULT_ART_MSG)
        
        self.siniester_label = ctk.CTkLabel(self, text = 'N° SINIESTRO:', font = LABEL_FONT, compound = 'center')
        self.siniester_text_var = ctk.StringVar()
        self.entry_data_siniester = ctk.CTkEntry(self, textvariable = self.siniester_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        self.entry_data_siniester.bind('<Return>', lambda event: AltaPacienteFrame.create_pacient_event(self,event))
        
        self.accident_date_label = ctk.CTkLabel(self, text = 'FECHA ACCIDENTE:', font = LABEL_FONT, compound = 'center')
        self.accident_date_text_var = ctk.StringVar()
        self.entry_data_accident_date = ctk.CTkEntry(self, textvariable = self.accident_date_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        self.entry_data_accident_date.bind('<Return>', lambda event: AltaPacienteFrame.create_pacient_event(self,event))
        
        self.dr_label = ctk.CTkLabel(self, text = 'DR DERIVANTE:', font = LABEL_FONT, compound = 'center')
        self.dr_text_var = ctk.StringVar()
        self.entry_data_dr = ctk.CTkEntry(self, textvariable = self.dr_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        self.entry_data_dr.bind('<Return>', lambda event: AltaPacienteFrame.create_pacient_event(self,event))
        
        self.start_date_label = ctk.CTkLabel(self, text = 'FECHA DE INICIO:', font = LABEL_FONT, compound = 'center')
        self.start_date_text_var = ctk.StringVar()
        self.entry_data_start_date = ctk.CTkEntry(self, textvariable = self.start_date_text_var, width = ENTRY_WIDTH, border_color='black', font = ENTRY_FONT)
        self.entry_data_start_date.bind('<Return>', lambda event: AltaPacienteFrame.create_pacient_event(self,event))
        
        self.update_button = ctk.CTkButton(self, text = 'Actualizar datos', command = lambda : ModificarPacienteFrame.update_pacient(self),
                                            font = BUTTON_FONT, fg_color="#4287f5",hover_color = "#196ef7",
                                            border_width=2.8,border_color="black",text_color='black')
        
        
        self.clear_button = ctk.CTkButton(self, text = 'Limpiar', command = lambda : clear_fields(self),
                                            font = BUTTON_FONT, fg_color="#c7c4bd",hover_color = "#a19e97",
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
        parsed_date = self.accident_date_text_var.get()
        parsed_date = parsed_date.replace('/',"")
        self.accident_date_text_var.set(parsed_date)
        
        fields = get_fields(self,'update')
        
        if(len(fields) == 12):
            dni = fields[0]
            name = fields[1]
            surname = fields[2]
            age = fields[3]
            phone = fields[4]
            address = fields[5]
            company = fields[6]
            job = fields[7]
            art = fields[8]
            siniester = fields[9]
            accident_date = fields[10]
            dr = fields[11]
                
            parsed_date = self.start_date_text_var.get()
            parsed_date = parsed_date.replace('/',"")
            self.start_date_text_var.set(parsed_date)
            
            start_date = self.start_date_text_var.get()
            
            #validate date
            if(not is_valid_date(start_date)):
                messagebox.showerror(title = 'Error: Fecha no valida', message = 'Ingresar fecha en formato DDMMAAAA')
            
            else:
                start_date = format_date(start_date)

                conn = sqlite3.connect(resource_path('database\cai_database.db'))
                query = f'SELECT * FROM Paciente WHERE dni = {dni}'
                cursor = conn.execute(query)
                data = cursor.fetchone()
                    
                
                #If data == None its because dni was modified
                if(data == None):
                    query = f'''SELECT * FROM Paciente WHERE Nombre = '{name}' AND Apellido = '{surname}' '''
                    cursor = conn.execute(query)
                    data = cursor.fetchone()
                        
                    if(data == None):
                        messagebox.showerror(title = 'Error', message = f'Algo ha salido mal :(')
                    else:
                        query = f'''UPDATE Paciente 
                                    SET Dni = {dni}, Nombre = '{name}', Apellido = '{surname}', Art = {art},
                                    Siniestro = '{siniester}', Puesto_Trabajo = '{job}', Fecha_Accidente = '{accident_date}',
                                    Telefono = '{phone}', Dr_derivante = '{dr}', Fecha_Inicio = '{start_date}', 
                                    Empresa = '{company}', Domicilio = '{address}', Edad = '{age}'
                                    WHERE Nombre = '{name}' AND Apellido = '{surname}' '''
                            
                        try:
                            conn.execute(query)
                            conn.commit()
                        except sqlite3.Error as err:
                            messagebox.showerror(title = 'Error', message = f'Algo ha salido mal :(')
                        else:
                            messagebox.showinfo(title = 'Operacion satisfactoria!', message = f'Se han modificado los datos del paciente {surname}, {name}')
                            clear_fields(self)
                            self.entry_data_art.set("Seleccione A.R.T")
                        finally:
                            conn.close()
                        
                
                else:
                    if(dni != self.prev_dni):
                        messagebox.showerror(title = 'Error: Dni no valido', message = f'Ya existe el paciente con dni: {dni}')
                    else:
                        query = f'''UPDATE Paciente 
                                    SET Dni = {dni}, Nombre = '{name}', Apellido = '{surname}', Art = {art},
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
                            clear_fields(self)
                            self.update_art_list()
                        finally:
                            conn.close()
        else:
            match fields[0]:
                case "blank_fields":
                    messagebox.showerror(title = 'Error: Datos no validos', message = 'El DNI, NOMBRE, APELLIDO y ART no pueden estar en blanco')
                
                case "digit_field_err":
                    messagebox.showerror(title = 'Error: Datos no validos', message = f'El campo: {fields[1]} no puede contener letras')
                
                case "invalid_dni":
                    messagebox.showerror(title = 'Error: Dni no valido', message = f'Ya existe el paciente con dni: {fields[1]}')
                
                case "invalid_art":
                    messagebox.showerror(title = 'Error: ART invalida', message = f'La ART: {fields[1]} no existe')
                
                case "invalid_date":
                    messagebox.showerror(title = 'Error: Fecha no valida', message = 'Ingresar fecha en formato DDMMAAAA')
        
    def update_pacient_event(self,event):
        parsed_date = self.accident_date_text_var.get()
        parsed_date = parsed_date.replace('/',"")
        self.accident_date_text_var.set(parsed_date)
        
        fields = get_fields(self,'update')
        
        if(len(fields) == 12):
            dni = fields[0]
            name = fields[1]
            surname = fields[2]
            age = fields[3]
            phone = fields[4]
            address = fields[5]
            company = fields[6]
            job = fields[7]
            art = fields[8]
            siniester = fields[9]
            accident_date = fields[10]
            dr = fields[11]
                
            parsed_date = self.start_date_text_var.get()
            parsed_date = parsed_date.replace('/',"")
            self.start_date_text_var.set(parsed_date)
            
            start_date = self.start_date_text_var.get()
            
            #validate date
            if(not is_valid_date(start_date)):
                messagebox.showerror(title = 'Error: Fecha no valida', message = 'Ingresar fecha en formato DDMMAAAA')
            
            else:
                start_date = format_date(start_date)

                conn = sqlite3.connect(resource_path('database\cai_database.db'))
                query = f'SELECT * FROM Paciente WHERE dni = {dni}'
                cursor = conn.execute(query)
                data = cursor.fetchone()
                    
                
                #If data == None its because dni was modified
                if(data == None):
                    query = f'''SELECT * FROM Paciente WHERE Nombre = '{name}' AND Apellido = '{surname}' '''
                    cursor = conn.execute(query)
                    data = cursor.fetchone()
                        
                    if(data == None):
                        messagebox.showerror(title = 'Error', message = f'Algo ha salido mal :(')
                    else:
                        query = f'''UPDATE Paciente 
                                    SET Dni = {dni}, Nombre = '{name}', Apellido = '{surname}', Art = {art},
                                    Siniestro = '{siniester}', Puesto_Trabajo = '{job}', Fecha_Accidente = '{accident_date}',
                                    Telefono = '{phone}', Dr_derivante = '{dr}', Fecha_Inicio = '{start_date}', 
                                    Empresa = '{company}', Domicilio = '{address}', Edad = '{age}'
                                    WHERE Nombre = '{name}' AND Apellido = '{surname}' '''
                            
                        try:
                            conn.execute(query)
                            conn.commit()
                        except sqlite3.Error as err:
                            messagebox.showerror(title = 'Error', message = f'Algo ha salido mal :(')
                        else:
                            messagebox.showinfo(title = 'Operacion satisfactoria!', message = f'Se han modificado los datos del paciente {surname}, {name}')
                            clear_fields(self)
                            self.update_art_list()
                            self.entry_data_art.set("Seleccione A.R.T")
                        finally:
                            conn.close()
                        
                
                else:
                    if(dni != self.prev_dni):
                        messagebox.showerror(title = 'Error: Dni no valido', message = f'Ya existe el paciente con dni: {dni}')
                    else:
                        query = f'''UPDATE Paciente 
                                    SET Dni = {dni}, Nombre = '{name}', Apellido = '{surname}', Art = {art},
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
                            clear_fields(self)
                        finally:
                            conn.close()
        else:
            match fields[0]:
                case "blank_fields":
                    messagebox.showerror(title = 'Error: Datos no validos', message = 'El DNI, NOMBRE, APELLIDO y ART no pueden estar en blanco')
                
                case "digit_field_err":
                    messagebox.showerror(title = 'Error: Datos no validos', message = f'El campo: {fields[1]} no puede contener letras')
                
                case "invalid_dni":
                    messagebox.showerror(title = 'Error: Dni no valido', message = f'Ya existe el paciente con dni: {fields[1]}')
                
                case "invalid_art":
                    messagebox.showerror(title = 'Error: ART invalida', message = f'La ART: {fields[1]} no existe')
                
                case "invalid_date":
                    messagebox.showerror(title = 'Error: Fecha no valida', message = 'Ingresar fecha en formato DDMMAAAA')

    def update_art_list(self):
        self.entry_data_art.configure(values = get_art())
    
class HistoriaClinica(ctk.CTkFrame):  
    def __init__(self, parent):
        super().__init__(parent)
        create_general_widgets(self,'Generar historia clínica','Generar historia clínica',lambda self: generate_clinic_pdf(self))   
        create_general_layout(self)
        self.pack(expand = True, fill = 'both')    
 
    
                
app = App()
app.mainloop()