import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import pdfkit
import jinja2
import os
"""
def execute_query(query):
    conn = sqlite3.connect('cai_database.db')
    cursor = conn.execute(query)
    data = cursor.fetchone()
    return data
    """
    
def is_valid_date(date):
    aux_date1 = date.split("/")
    aux_date2 = date.split("-")
    if(len(aux_date1) == 1 and len(aux_date2) == 1):
        return False
    else:
        return True

def validate_art(art):
    ## validate ART name
    conn = sqlite3.connect('cai_database.db')
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
    conn = sqlite3.connect('cai_database.db')
    query = f"SELECT Dni FROM Paciente WHERE Dni = {dni} "
    cursor = conn.execute(query)
    data = cursor.fetchone()
    
    #already exists one person with that dni
    if(data != None):
        return False
    else:
        return True

def get_pacient(obj, query_arg):
        conn = sqlite3.connect('cai_database.db')
        
        if(query_arg =='dni'):
            dni = int(obj.entry_dni_var.get())
            query = f'''SELECT P.Dni, P.Nombre, P.Apellido, A.Nombre, P.Siniestro,
                    P.Puesto_Trabajo, P.Fecha_Accidente, P.Telefono, P.Dr_derivante,
                    P.Dominancia, P.Fecha_Inicio, P.Empresa, P.Domicilio
                    FROM Paciente P
                    INNER JOIN Art A on P.Art = A.Id
                    WHERE P.Dni = {dni} '''
                    
        else:
            name = obj.entry_name_var.get()
            name = name.lower().capitalize()
            surname = obj.entry_surname_var.get()
            surname = surname.lower().capitalize()
            query = f'''SELECT P.Dni, P.Nombre, P.Apellido, A.Nombre, P.Siniestro, 
                    P.Puesto_Trabajo, P.Fecha_Accidente, P.Telefono, P.Dr_derivante,
                    P.Dominancia, P.Fecha_Inicio, P.Empresa, P.Domicilio
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
            obj.dominancia_text_var.set(data[9])
            obj.start_date_text_var.set(data[10])
            obj.company_text_var.set(data[11])
            obj.address_text_var.set(data[12])
            
        
        conn.close()

def get_pacient_event(obj, event, query_arg):
    conn = sqlite3.connect('cai_database.db')
        
    if(query_arg == 'dni'):
        dni = int(obj.entry_dni_var.get())
        query = f'''SELECT P.Dni, P.Nombre, P.Apellido, A.Nombre, P.Siniestro,
                    P.Puesto_Trabajo, P.Fecha_Accidente, P.Telefono, P.Dr_derivante,
                    P.Dominancia, P.Fecha_Inicio, P.Empresa, P.Domicilio
                    FROM Paciente P
                    INNER JOIN Art A on P.Art = A.Id
                    WHERE P.Dni = {dni} '''          
    else:
        name = obj.entry_name_var.get()
        name = name.lower().capitalize()
        surname = obj.entry_surname_var.get()
        surname = surname.lower().capitalize()
        query = f'''SELECT P.Dni, P.Nombre, P.Apellido, A.Nombre, P.Siniestro, 
                    P.Puesto_Trabajo, P.Fecha_Accidente, P.Telefono, P.Dr_derivante,
                    P.Dominancia, P.Fecha_Inicio, P.Empresa, P.Domicilio
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
        obj.dominancia_text_var.set(data[9])
        obj.start_date_text_var.set(data[10])
        obj.company_text_var.set(data[11])
        obj.address_text_var.set(data[12])
            
        
    conn.close()

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
        obj.dominancia_text_var.set('')
        obj.start_date_text_var.set('')

class App(ctk.CTk):
    def __init__(self):
        # main setup
        super().__init__()
        self.title('Fichas pacientes')
        self.iconbitmap('cai_logo.ico')
        self.state('zoomed')
        
        #widgets
        #self.menu = Menu(self)
        #self.main = Main(self)
        self.main = Main(self)
        
        # layout
        self.columnconfigure(0, weight = 1)
        self.rowconfigure((0), weight = 1)
        
        # run
        self.mainloop()
        
class Main(ctk.CTkTabview):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row = 0, column = 0, sticky = 'nsew')
        
        # tabs
        self.add('Generar ficha')
        self.add('Dar de alta paciente')
        self.add('Dar de alta ART')
        self.add('Dar de baja paciente')
        self.add('Modificar datos paciente')
        
        # widgets
        GenerarFichaFrame(self.tab('Generar ficha'))
        AltaPacienteFrame(self.tab('Dar de alta paciente'))
        BajaPacienteFrame(self.tab('Dar de baja paciente'))
        ModificarPacienteFrame(self.tab('Modificar datos paciente'))
        AltaARTFrame(self.tab('Dar de alta ART'))

class GenerarFichaFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.create_widgets()
        self.create_layout()
        self.pack(expand = True, fill = 'both')
         
    def create_widgets(self):        
        self.header_label = ctk.CTkLabel(self, text = 'Generar ficha asistencia paciente', font = ("Arial",25), compound = 'center')
        
        ## DNI entry ##
        self.enter_dni_label = ctk.CTkLabel(self, text = 'Ingrese DNI paciente:', font = ("Arial",15), compound = 'center')
        self.entry_dni_var = ctk.StringVar()
        self.entry_dni = ctk.CTkEntry(self, textvariable = self.entry_dni_var)
        self.entry_dni.bind('<Return>', lambda event, query_arg='dni': get_pacient_event(self,event,query_arg))
        self.submit_dni_button = ctk.CTkButton(self, text = 'Enviar', command = lambda : get_pacient(self,'dni'))
        
        ## Name entry ##
        self.enter_name_label = ctk.CTkLabel(self, text = 'Ingrese nombre paciente:', font = ("Arial",15), compound = 'center')
        self.enter_surname_label = ctk.CTkLabel(self, text = 'Ingrese apellido paciente:', font = ("Arial",15), compound = 'center')
        self.entry_name_var = ctk.StringVar()
        self.entry_name = ctk.CTkEntry(self, textvariable = self.entry_name_var)
        self.entry_surname_var = ctk.StringVar()
        self.entry_surname = ctk.CTkEntry(self, textvariable = self.entry_surname_var)
        self.entry_surname.bind('<Return>', lambda event, query_arg = 'fullname': get_pacient_event(self,event,query_arg))
        self.submit_fullname_button = ctk.CTkButton(self, text = 'Enviar', command = lambda : get_pacient(self,'fullname'))
        
        ## Data Results ## 
        self.header_data_label = ctk.CTkLabel(self, text = 'Datos del paciente:', font = ("Arial",25), compound = 'center')
        
        self.dni_label = ctk.CTkLabel(self, text = 'DNI del paciente:', font = ("Arial",15), compound = 'center')
        self.dni_text_var = ctk.StringVar()
        self.entry_data_dni = ctk.CTkEntry(self, textvariable = self.dni_text_var)
        
        self.name_label = ctk.CTkLabel(self, text = 'Nombre del paciente:', font = ("Arial",15), compound = 'center')
        self.name_text_var = ctk.StringVar()
        self.entry_data_name = ctk.CTkEntry(self, textvariable = self.name_text_var)
        
        self.surname_label = ctk.CTkLabel(self, text = 'Apellido del paciente:', font = ("Arial",15), compound = 'center')
        self.surname_text_var = ctk.StringVar()
        self.entry_data_surname = ctk.CTkEntry(self, textvariable = self.surname_text_var)
        
        self.phone_label = ctk.CTkLabel(self, text = 'Telefono del paciente:', font = ("Arial",15), compound = 'center')
        self.phone_text_var = ctk.StringVar()
        self.entry_phone = ctk.CTkEntry(self, textvariable = self.phone_text_var)
        
        self.address_label = ctk.CTkLabel(self, text = 'Dirección del paciente:', font = ("Arial",15), compound = 'center')
        self.address_text_var = ctk.StringVar()
        self.entry_address = ctk.CTkEntry(self, textvariable = self.address_text_var)
        
        self.company_label = ctk.CTkLabel(self, text = 'Empresa donde trabaja el paciente:', font = ("Arial",15), compound = 'center')
        self.company_text_var = ctk.StringVar()
        self.entry_company = ctk.CTkEntry(self, textvariable = self.company_text_var)
        
        self.job_label = ctk.CTkLabel(self, text = 'Puesto de trabajo del paciente:', font = ("Arial",15), compound = 'center')
        self.job_text_var = ctk.StringVar()
        self.entry_job = ctk.CTkEntry(self, textvariable = self.job_text_var)
        
        self.art_label = ctk.CTkLabel(self, text = 'ART del paciente:', font = ("Arial",15), compound = 'center')
        self.art_text_var = ctk.StringVar()
        self.entry_art = ctk.CTkEntry(self, textvariable = self.art_text_var)
        
        self.siniester_label = ctk.CTkLabel(self, text = 'N° Siniestro del paciente:', font = ("Arial",15), compound = 'center')
        self.siniester_text_var = ctk.StringVar()
        self.entry_siniester = ctk.CTkEntry(self, textvariable = self.siniester_text_var)
        
        self.accident_date_label = ctk.CTkLabel(self, text = 'Fecha de accidente:', font = ("Arial",15), compound = 'center')
        self.accident_date_text_var = ctk.StringVar()
        self.entry_accident_date = ctk.CTkEntry(self, textvariable = self.accident_date_text_var)
        
        self.dr_label = ctk.CTkLabel(self, text = 'Dr derivante del paciente:', font = ("Arial",15), compound = 'center')
        self.dr_text_var = ctk.StringVar()
        self.entry_dr = ctk.CTkEntry(self, textvariable = self.dr_text_var)
        
        self.dominancia_label = ctk.CTkLabel(self, text = 'Dominancia del paciente:', font = ("Arial",15), compound = 'center')
        self.dominancia_text_var = ctk.StringVar()
        self.entry_dominancia = ctk.CTkEntry(self, textvariable = self.dominancia_text_var)
        
        self.start_date_label = ctk.CTkLabel(self, text = 'Fecha de inicio:', font = ("Arial",15), compound = 'center')
        self.start_date_text_var = ctk.StringVar()
        self.entry_start_date = ctk.CTkEntry(self, textvariable = self.start_date_text_var)
        
        self.generate_button = ctk.CTkButton(self, text = 'Generar ficha asistencia', command = lambda : GenerarFichaFrame.generatePdf(self))
          
    def create_layout(self):
        """self.columnconfigure((0,1,2,3), weight = 1)
        self.rowconfigure((0,1,2,3,4,5,6,7,8,9,10), weight = 1)
        
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
        self.pacient_label.grid(row = 4, column = 0, columnspan = 4)
        self.dni_label.grid(row = 5, column = 0, columnspan = 2)
        self.dni_data_label.grid(row = 5, column = 2, columnspan = 2)
        self.name_label.grid(row = 6, column = 0, columnspan = 2) 
        self.name_data_label.grid(row = 6, column = 2, columnspan = 2)
        self.surname_label.grid(row = 7, column = 0, columnspan = 2)
        self.surname_data_label.grid(row = 7, column = 2, columnspan = 2)
        self.art_label.grid(row = 8, column = 0, columnspan = 2)
        self.art_data_label.grid(row = 8, column = 2, columnspan = 2)
        self.generate_button.grid(row = 9, column = 0, columnspan = 4)"""
        
        self.columnconfigure((0,1,2,3), weight = 1)
        self.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16), weight = 1)
        
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
        self.header_data_label.grid(row = 4, column = 0, columnspan = 4, pady = 15)
        
        self.dni_label.grid(row = 5, column = 0)
        self.entry_data_dni.grid(row = 5, column = 1)
        
        self.name_label.grid(row = 5, column = 2)
        self.entry_data_name.grid(row = 5, column = 3)
        
        self.surname_label.grid(row = 6, column = 0)
        self.entry_data_surname.grid(row = 6, column = 1)
        
        self.phone_label.grid(row = 6, column = 2)
        self.entry_phone.grid(row = 6, column = 3)
        
        self.address_label.grid(row = 7, column = 0)
        self.entry_address.grid(row = 7, column = 1)
        
        self.company_label.grid(row = 7, column = 2)
        self.entry_company.grid(row = 7, column = 3)
        
        self.job_label.grid(row = 8, column = 0)
        self.entry_job.grid(row = 8, column = 1)
        
        self.art_label.grid(row = 8, column = 2)
        self.entry_art.grid(row = 8, column = 3)
        
        self.siniester_label.grid(row = 9, column = 0)
        self.entry_siniester.grid(row = 9, column = 1)
        
        self.accident_date_label.grid(row = 9, column = 2)
        self.entry_accident_date.grid(row = 9, column = 3)
        
        self.dr_label.grid(row = 10, column = 0)
        self.entry_dr.grid(row = 10, column = 1)
        
        self.dominancia_label.grid(row = 10, column = 2)
        self.entry_dominancia.grid(row = 10, column = 3)
        
        self.start_date_label.grid(row = 11, column = 0)
        self.entry_start_date.grid(row = 11, column = 1)
        
        self.generate_button.grid(row = 12, column = 0, columnspan = 4, pady = 15)
    
    def generatePdf(self):
        answer = messagebox.askquestion(title = 'Confirmación', message = '¿Seguro que desea continuar?')
        if answer == "yes":
            dni = int(self.dni_text_var.get())
            name = self.name_text_var.get()
            surname = self.surname_text_var.get()
            art = self.art_text_var.get()
            #--------------------creacion pdf------------------------- #
            pdf_variables = {'dni': dni, 'surname': surname, 'name': name, 'art': art}
            template_loader = jinja2.FileSystemLoader('./')
            template_env = jinja2.Environment(loader = template_loader)
            
            html_template = 'doc_test.html'
            final_template = template_env.get_template(html_template)
            output_text = final_template.render(pdf_variables)
            
            path = "C:/Program Files/wkhtmltopdf/wkhtmltopdf.exe" 
            pdf_config = pdfkit.configuration(wkhtmltopdf = path)
            output_pdf = 'planilla_firmas.pdf'
            pdfkit.from_string(output_text, output_pdf, configuration=pdf_config)
            
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
        self.header_label = ctk.CTkLabel(self, text = 'Dar de alta paciente:', font = ("Arial",25), compound = 'center')
        
        self.dni_label = ctk.CTkLabel(self, text = 'Ingrese DNI del paciente:', font = ("Arial",15), compound = 'center')
        self.entry_dni_var = ctk.StringVar()
        self.entry_dni = ctk.CTkEntry(self, textvariable = self.entry_dni_var)
        
        self.name_label = ctk.CTkLabel(self, text = 'Ingrese nombre del paciente:', font = ("Arial",15), compound = 'center')
        self.entry_name_var = ctk.StringVar()
        self.entry_name = ctk.CTkEntry(self, textvariable = self.entry_name_var)
        
        self.surname_label = ctk.CTkLabel(self, text = 'Ingrese apellido del paciente:', font = ("Arial",15), compound = 'center')
        self.entry_surname_var = ctk.StringVar()
        self.entry_surname = ctk.CTkEntry(self, textvariable = self.entry_surname_var)
        
        self.phone_label = ctk.CTkLabel(self, text = 'Ingrese telefono del paciente:', font = ("Arial",15), compound = 'center')
        self.entry_phone_var = ctk.StringVar()
        self.entry_phone = ctk.CTkEntry(self, textvariable = self.entry_phone_var)
        
        self.address_label = ctk.CTkLabel(self, text = 'Ingrese dirección del paciente:', font = ("Arial",15), compound = 'center')
        self.entry_address_var = ctk.StringVar()
        self.entry_address = ctk.CTkEntry(self, textvariable = self.entry_address_var)
        
        self.company_label = ctk.CTkLabel(self, text = 'Ingrese empresa donde trabaja el paciente:', font = ("Arial",15), compound = 'center')
        self.entry_company_var = ctk.StringVar()
        self.entry_company = ctk.CTkEntry(self, textvariable = self.entry_company_var)
        
        self.job_label = ctk.CTkLabel(self, text = 'Ingrese puesto de trabajo del paciente:', font = ("Arial",15), compound = 'center')
        self.entry_job_var = ctk.StringVar()
        self.entry_job = ctk.CTkEntry(self, textvariable = self.entry_job_var)
        
        self.art_label = ctk.CTkLabel(self, text = 'Ingrese ART del paciente:', font = ("Arial",15), compound = 'center')
        self.entry_art_var = ctk.StringVar()
        self.entry_art = ctk.CTkEntry(self, textvariable = self.entry_art_var)
        
        self.siniester_label = ctk.CTkLabel(self, text = 'Ingrese N° Siniestro del paciente:', font = ("Arial",15), compound = 'center')
        self.entry_siniester_var = ctk.StringVar()
        self.entry_siniester = ctk.CTkEntry(self, textvariable = self.entry_siniester_var)
        
        self.accident_date_label = ctk.CTkLabel(self, text = 'Ingrese fecha de accidente:', font = ("Arial",15), compound = 'center')
        self.entry_accident_date_var = ctk.StringVar()
        self.entry_accident_date = ctk.CTkEntry(self, textvariable = self.entry_accident_date_var)
        
        self.dr_label = ctk.CTkLabel(self, text = 'Ingrese Dr derivante del paciente:', font = ("Arial",15), compound = 'center')
        self.entry_dr_var = ctk.StringVar()
        self.entry_dr = ctk.CTkEntry(self, textvariable = self.entry_dr_var)
        
        self.dominancia_label = ctk.CTkLabel(self, text = 'Ingrese dominancia del paciente:', font = ("Arial",15), compound = 'center')
        self.entry_dominancia_var = ctk.StringVar()
        self.entry_dominancia = ctk.CTkEntry(self, textvariable = self.entry_dominancia_var)
        
        self.start_date_label = ctk.CTkLabel(self, text = 'Ingrese fecha de inicio:', font = ("Arial",15), compound = 'center')
        self.entry_start_date_var = ctk.StringVar()
        self.entry_start_date = ctk.CTkEntry(self, textvariable = self.entry_start_date_var)
        self.entry_start_date.bind('<Return>', lambda event: AltaPacienteFrame.create_pacient_event(self,event))
        
        self.submit_button = ctk.CTkButton(self, text = 'Enviar', command = lambda : AltaPacienteFrame.create_pacient(self))
        
    def create_layout(self):
        self.columnconfigure((0,1,2,3), weight = 1)
        self.rowconfigure((0,1,2,3,4,5,6,7,8), weight = 1)
        
        self.header_label.grid(row = 0, column = 0, columnspan = 4)
        
        self.dni_label.grid(row = 1, column = 0)
        self.entry_dni.grid(row = 1, column = 1)
        
        self.name_label.grid(row = 1, column = 2)
        self.entry_name.grid(row = 1, column = 3)
        
        self.surname_label.grid(row = 2, column = 0)
        self.entry_surname.grid(row = 2, column = 1)
        
        self.phone_label.grid(row = 2, column = 2)
        self.entry_phone.grid(row = 2, column = 3)
        
        self.address_label.grid(row = 3, column = 0)
        self.entry_address.grid(row = 3, column = 1)
        
        self.company_label.grid(row = 3, column = 2)
        self.entry_company.grid(row = 3, column = 3)
        
        self.job_label.grid(row = 4, column = 0)
        self.entry_job.grid(row = 4, column = 1)
        
        self.art_label.grid(row = 4, column = 2)
        self.entry_art.grid(row = 4, column = 3)
        
        self.siniester_label.grid(row = 5, column = 0)
        self.entry_siniester.grid(row = 5, column = 1)
        
        self.accident_date_label.grid(row = 5, column = 2)
        self.entry_accident_date.grid(row = 5, column = 3)
        
        self.dr_label.grid(row = 6, column = 0)
        self.entry_dr.grid(row = 6, column = 1)
        
        self.dominancia_label.grid(row = 6, column = 2)
        self.entry_dominancia.grid(row = 6, column = 3)
        
        self.start_date_label.grid(row = 7, column = 0)
        self.entry_start_date.grid(row = 7, column = 1)
        
        self.submit_button.grid(row = 8, column = 0, columnspan = 4)
        
    def clear_fields(self):
        self.entry_dni_var.set('')
        self.entry_name_var.set('')
        self.entry_surname_var.set('')
        self.entry_art_var.set('')
        self.entry_phone_var.set('')
        self.entry_address_var.set('')
        self.entry_company_var.set('')
        self.entry_job_var.set('')
        self.entry_siniester_var.set('')
        self.entry_accident_date_var.set('')
        self.entry_dr_var.set('')
        self.entry_dominancia_var.set('')
        self.entry_start_date_var.set('')
    
    def create_pacient(self):
        conn = sqlite3.connect('cai_database.db')
        
        dni = int(self.entry_dni_var.get())
        
        name = self.entry_name_var.get()
        name = name.lower().capitalize()
        
        surname = self.entry_surname_var.get()
        surname = surname.lower().capitalize()
        
        phone = int(self.entry_phone_var.get())
        
        address = self.entry_address_var.get()
        
        company = self.entry_company_var.get()
        company = company.lower().capitalize()
        
        job = self.entry_job_var.get()
        job = job.lower().capitalize()
        
        art = self.entry_art_var.get()
        
        siniester = self.entry_siniester_var.get()
        
        accident_date = self.entry_accident_date_var.get()
        
        dr = self.entry_dr_var.get()
        
        dominancia = self.entry_dominancia_var.get()
        
        start_date = self.entry_start_date_var.get()
        
        #validate dates
        if(not is_valid_date(accident_date) or not is_valid_date(start_date)):
            messagebox.showerror(title = 'Error: Fecha no valida', message = 'Ingresar fecha en formato DD-MM-AAA o DD/MM/AAA')
        else:
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
                                (Dni,Nombre,Apellido,Art,Siniestro,Puesto_Trabajo,Fecha_Accidente,Telefono,Dr_derivante,Dominancia,Fecha_Inicio,Empresa,Domicilio) 
                                VALUES ({dni},'{name}','{surname}',{art_id},'{siniester}','{job}','{accident_date}',{phone},'{dr}','{dominancia}','{start_date}','{company}','{address}')'''
                    try:
                        cursor = conn.execute(query)
                        conn.commit()
                    except sqlite3.Error as err:
                        messagebox.showerror(title = 'Error', message = 'Algo ha salido mal :(')
                    else:
                        messagebox.showinfo(title = 'Operacion satisfactoria!', message = f'Se ha dado de alta al paciente {surname}, {name}')
                    finally:
                        conn.close()
                    
        self.clear_fields()
    
    def create_pacient_event(self, event):
        conn = sqlite3.connect('cai_database.db')
        
        dni = int(self.entry_dni_var.get())
        
        name = self.entry_name_var.get()
        name = name.lower().capitalize()
        
        surname = self.entry_surname_var.get()
        surname = surname.lower().capitalize()
        
        phone = int(self.entry_phone_var.get())
        
        address = self.entry_address_var.get()
        
        company = self.entry_company_var.get()
        company = company.lower().capitalize()
        
        job = self.entry_job_var.get()
        job = job.lower().capitalize()
        
        art = self.entry_art_var.get()
        
        siniester = self.entry_siniester_var.get()
        
        accident_date = self.entry_accident_date_var.get()
        
        dr = self.entry_dr_var.get()
        
        dominancia = self.entry_dominancia_var.get()
        
        start_date = self.entry_start_date_var.get()
        
        #validate dates
        if(not is_valid_date(accident_date) or not is_valid_date(start_date)):
            messagebox.showerror(title = 'Error: Fecha no valida', message = 'Ingresar fecha en formato DD-MM-AAA o DD/MM/AAA')
        else:
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
                                (Dni,Nombre,Apellido,Art,Siniestro,Puesto_Trabajo,Fecha_Accidente,Telefono,Dr_derivante,Dominancia,Fecha_Inicio,Empresa,Domicilio) 
                                VALUES ({dni},'{name}','{surname}',{art_id},'{siniester}','{job}','{accident_date}',{phone},'{dr}','{dominancia}','{start_date}','{company}','{address}')'''
                    try:
                        cursor = conn.execute(query)
                        conn.commit()
                    except sqlite3.Error as err:
                        messagebox.showerror(title = 'Error', message = 'Algo ha salido mal :(')
                    else:
                        messagebox.showinfo(title = 'Operacion satisfactoria!', message = f'Se ha dado de alta al paciente {surname}, {name}')
                    finally:
                        conn.close()
                    
        self.clear_fields()

class AltaARTFrame(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.create_widgets()
        self.create_layout()
        self.pack(expand = True, fill = 'both')

    def create_widgets(self):
        self.header_label = ctk.CTkLabel(self, text = 'Dar de alta ART', font = ("Arial",25), compound = 'center')
        self.name_label = ctk.CTkLabel(self, text = 'Ingrese el nombre de la ART:', font = ("Arial",15), compound = 'center')
        self.entry_name_var = ctk.StringVar()
        self.entry_name = ctk.CTkEntry(self, textvariable = self.entry_name_var)
        self.entry_name.bind('<Return>', lambda event: AltaARTFrame.create_art_event(self,event))
        self.submit_button = ctk.CTkButton(self, text = 'Dar de alta', command = lambda : AltaARTFrame.create_art(self))
        
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
        conn = sqlite3.connect('cai_database.db')
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
        conn = sqlite3.connect('cai_database.db')
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
        self.header_label = ctk.CTkLabel(self, text = 'Dar de baja paciente', font = ("Arial",25), compound = 'center')
        
        ## DNI entry ##
        self.enter_dni_label = ctk.CTkLabel(self, text = 'Ingrese DNI paciente:', font = ("Arial",15), compound = 'center')
        self.entry_dni_var = ctk.StringVar()
        self.entry_dni = ctk.CTkEntry(self, textvariable = self.entry_dni_var)
        self.entry_dni.bind('<Return>', lambda event, query_arg='dni': get_pacient_event(self,event,query_arg))
        self.submit_dni_button = ctk.CTkButton(self, text = 'Enviar', command = lambda : get_pacient(self,'dni'))
        
        ## Name entry ##
        self.enter_name_label = ctk.CTkLabel(self, text = 'Ingrese nombre paciente:', font = ("Arial",15), compound = 'center')
        self.enter_surname_label = ctk.CTkLabel(self, text = 'Ingrese apellido paciente:', font = ("Arial",15), compound = 'center')
        self.entry_name_var = ctk.StringVar()
        self.entry_name = ctk.CTkEntry(self, textvariable = self.entry_name_var)
        self.entry_surname_var = ctk.StringVar()
        self.entry_surname = ctk.CTkEntry(self, textvariable = self.entry_surname_var)
        self.entry_surname.bind('<Return>', lambda event, query_arg = 'fullname': get_pacient_event(self,event,query_arg))
        self.submit_fullname_button = ctk.CTkButton(self, text = 'Enviar', command = lambda : get_pacient(self,'fullname'))
        
        ## Data Results ## 
        self.pacient_label = ctk.CTkLabel(self, text = 'Datos del paciente:', font = ("Arial",25), compound = 'center')
        
        self.dni_label = ctk.CTkLabel(self, text = 'D.N.I:', font = ("Arial",15), compound = 'center')
        self.dni_text_var = ctk.StringVar()
        self.dni_data_label = ctk.CTkLabel(self, textvariable = self.dni_text_var, font = ("Arial",15), compound = 'center')
        
        self.name_label = ctk.CTkLabel(self, text = 'Nombre:', font = ("Arial",15), compound = 'center')
        self.name_text_var = ctk.StringVar()
        self.name_data_label = ctk.CTkLabel(self, textvariable = self.name_text_var, font = ("Arial",15), compound = 'center')
        
        self.surname_label = ctk.CTkLabel(self, text = 'Apellido:', font = ("Arial",15), compound = 'center')
        self.surname_text_var = ctk.StringVar()
        self.surname_data_label = ctk.CTkLabel(self, textvariable = self.surname_text_var, font = ("Arial",15), compound = 'center')
        
        self.art_label = ctk.CTkLabel(self, text = 'A.R.T:', font = ("Arial",15), compound = 'center')
        self.art_text_var = ctk.StringVar()
        self.art_data_label = ctk.CTkLabel(self, textvariable = self.art_text_var, font = ("Arial",15), compound = 'center')
        
        self.delete_button = ctk.CTkButton(self, text = 'Dar de baja', command = lambda : BajaPacienteFrame.delete_pacient(self))
        
    def create_layout(self):
        self.columnconfigure((0,1,2,3), weight = 1)
        self.rowconfigure((0,1,2,3,4,5,6,7,8,9,10), weight = 1)
        
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
        self.pacient_label.grid(row = 4, column = 0, columnspan = 4)
        self.dni_label.grid(row = 5, column = 0, columnspan = 2)
        self.dni_data_label.grid(row = 5, column = 2, columnspan = 2)
        self.name_label.grid(row = 6, column = 0, columnspan = 2) 
        self.name_data_label.grid(row = 6, column = 2, columnspan = 2)
        self.surname_label.grid(row = 7, column = 0, columnspan = 2)
        self.surname_data_label.grid(row = 7, column = 2, columnspan = 2)
        self.art_label.grid(row = 8, column = 0, columnspan = 2)
        self.art_data_label.grid(row = 8, column = 2, columnspan = 2)
        self.delete_button.grid(row = 9, column = 0, columnspan = 4)
       
    def clear_fields(self):
        self.dni_text_var.set('')
        self.name_text_var.set('')
        self.surname_text_var.set('')
        self.art_text_var.set('')
        self.entry_dni_var.set('')
        self.entry_name_var.set('')
        self.entry_surname_var.set('')
    
    def delete_pacient(self):
        dni = int(self.dni_text_var.get())
        name = self.name_text_var.get()
        surname = self.surname_text_var.get()
        
        answer = messagebox.askquestion(title = 'Confirmación', message = f'¿Seguro que desea dar de baja al paciente {surname}, {name}?')
        
        if answer == "yes":
            conn = sqlite3.connect('cai_database.db')    
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
                    
        self.clear_fields()
               
class ModificarPacienteFrame(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.create_widgets()
        self.create_layout()
        self.pack(expand = True, fill = 'both')

    def create_widgets(self):
        self.header_label = ctk.CTkLabel(self, text = 'Modificar datos paciente', font = ("Arial",25), compound = 'center')
        
        ## DNI entry ##
        self.enter_dni_label = ctk.CTkLabel(self, text = 'Ingrese DNI paciente:', font = ("Arial",15), compound = 'center')
        self.entry_dni_var = ctk.StringVar()
        self.entry_dni = ctk.CTkEntry(self, textvariable = self.entry_dni_var)
        self.entry_dni.bind('<Return>', lambda event, query_arg='dni': get_pacient_event(self,event,query_arg))
        self.submit_dni_button = ctk.CTkButton(self, text = 'Enviar', command = lambda : get_pacient(self,'dni'))
        
        ## Name entry ##
        self.enter_name_label = ctk.CTkLabel(self, text = 'Ingrese nombre paciente:', font = ("Arial",15), compound = 'center')
        self.enter_surname_label = ctk.CTkLabel(self, text = 'Ingrese apellido paciente:', font = ("Arial",15), compound = 'center')
        self.entry_name_var = ctk.StringVar()
        self.entry_name = ctk.CTkEntry(self, textvariable = self.entry_name_var)
        self.entry_surname_var = ctk.StringVar()
        self.entry_surname = ctk.CTkEntry(self, textvariable = self.entry_surname_var)
        self.entry_surname.bind('<Return>', lambda event, query_arg = 'fullname': get_pacient_event(self,event,query_arg))
        self.submit_fullname_button = ctk.CTkButton(self, text = 'Enviar', command = lambda : get_pacient(self,'fullname'))
        
        ## Data Results ## 
        self.header_data_label = ctk.CTkLabel(self, text = 'Datos del paciente:', font = ("Arial",25), compound = 'center')
        
        self.dni_label = ctk.CTkLabel(self, text = 'DNI del paciente:', font = ("Arial",15), compound = 'center')
        self.dni_text_var = ctk.StringVar()
        self.entry_data_dni = ctk.CTkEntry(self, textvariable = self.dni_text_var)
        
        self.name_label = ctk.CTkLabel(self, text = 'Nombre del paciente:', font = ("Arial",15), compound = 'center')
        self.name_text_var = ctk.StringVar()
        self.entry_data_name = ctk.CTkEntry(self, textvariable = self.name_text_var)
        
        self.surname_label = ctk.CTkLabel(self, text = 'Apellido del paciente:', font = ("Arial",15), compound = 'center')
        self.surname_text_var = ctk.StringVar()
        self.entry_data_surname = ctk.CTkEntry(self, textvariable = self.surname_text_var)
        
        self.phone_label = ctk.CTkLabel(self, text = 'Telefono del paciente:', font = ("Arial",15), compound = 'center')
        self.phone_text_var = ctk.StringVar()
        self.entry_phone = ctk.CTkEntry(self, textvariable = self.phone_text_var)
        
        self.address_label = ctk.CTkLabel(self, text = 'Dirección del paciente:', font = ("Arial",15), compound = 'center')
        self.address_text_var = ctk.StringVar()
        self.entry_address = ctk.CTkEntry(self, textvariable = self.address_text_var)
        
        self.company_label = ctk.CTkLabel(self, text = 'Empresa donde trabaja el paciente:', font = ("Arial",15), compound = 'center')
        self.company_text_var = ctk.StringVar()
        self.entry_company = ctk.CTkEntry(self, textvariable = self.company_text_var)
        
        self.job_label = ctk.CTkLabel(self, text = 'Puesto de trabajo del paciente:', font = ("Arial",15), compound = 'center')
        self.job_text_var = ctk.StringVar()
        self.entry_job = ctk.CTkEntry(self, textvariable = self.job_text_var)
        
        self.art_label = ctk.CTkLabel(self, text = 'ART del paciente:', font = ("Arial",15), compound = 'center')
        self.art_text_var = ctk.StringVar()
        self.entry_art = ctk.CTkEntry(self, textvariable = self.art_text_var)
        
        self.siniester_label = ctk.CTkLabel(self, text = 'N° Siniestro del paciente:', font = ("Arial",15), compound = 'center')
        self.siniester_text_var = ctk.StringVar()
        self.entry_siniester = ctk.CTkEntry(self, textvariable = self.siniester_text_var)
        
        self.accident_date_label = ctk.CTkLabel(self, text = 'Fecha de accidente:', font = ("Arial",15), compound = 'center')
        self.accident_date_text_var = ctk.StringVar()
        self.entry_accident_date = ctk.CTkEntry(self, textvariable = self.accident_date_text_var)
        
        self.dr_label = ctk.CTkLabel(self, text = 'Dr derivante del paciente:', font = ("Arial",15), compound = 'center')
        self.dr_text_var = ctk.StringVar()
        self.entry_dr = ctk.CTkEntry(self, textvariable = self.dr_text_var)
        
        self.dominancia_label = ctk.CTkLabel(self, text = 'Dominancia del paciente:', font = ("Arial",15), compound = 'center')
        self.dominancia_text_var = ctk.StringVar()
        self.entry_dominancia = ctk.CTkEntry(self, textvariable = self.dominancia_text_var)
        
        self.start_date_label = ctk.CTkLabel(self, text = 'Fecha de inicio:', font = ("Arial",15), compound = 'center')
        self.start_date_text_var = ctk.StringVar()
        self.entry_start_date = ctk.CTkEntry(self, textvariable = self.start_date_text_var)
        
        self.update_button = ctk.CTkButton(self, text = 'Actualizar datos', command = lambda : ModificarPacienteFrame.update_pacient(self))

    def create_layout(self):
        self.columnconfigure((0,1,2,3), weight = 1)
        self.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16), weight = 1)
        
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
        self.header_data_label.grid(row = 4, column = 0, columnspan = 4, pady = 15)
        
        self.dni_label.grid(row = 5, column = 0)
        self.entry_data_dni.grid(row = 5, column = 1)
        
        self.name_label.grid(row = 5, column = 2)
        self.entry_data_name.grid(row = 5, column = 3)
        
        self.surname_label.grid(row = 6, column = 0)
        self.entry_data_surname.grid(row = 6, column = 1)
        
        self.phone_label.grid(row = 6, column = 2)
        self.entry_phone.grid(row = 6, column = 3)
        
        self.address_label.grid(row = 7, column = 0)
        self.entry_address.grid(row = 7, column = 1)
        
        self.company_label.grid(row = 7, column = 2)
        self.entry_company.grid(row = 7, column = 3)
        
        self.job_label.grid(row = 8, column = 0)
        self.entry_job.grid(row = 8, column = 1)
        
        self.art_label.grid(row = 8, column = 2)
        self.entry_art.grid(row = 8, column = 3)
        
        self.siniester_label.grid(row = 9, column = 0)
        self.entry_siniester.grid(row = 9, column = 1)
        
        self.accident_date_label.grid(row = 9, column = 2)
        self.entry_accident_date.grid(row = 9, column = 3)
        
        self.dr_label.grid(row = 10, column = 0)
        self.entry_dr.grid(row = 10, column = 1)
        
        self.dominancia_label.grid(row = 10, column = 2)
        self.entry_dominancia.grid(row = 10, column = 3)
        
        self.start_date_label.grid(row = 11, column = 0)
        self.entry_start_date.grid(row = 11, column = 1)
        
        self.update_button.grid(row = 12, column = 0, columnspan = 4, pady = 15)
        
    def update_pacient(self):
        conn = sqlite3.connect('cai_database.db')
        
        dni = int(self.dni_text_var.get())
        
        name = self.name_text_var.get()
        name = name.lower().capitalize()
        
        surname = self.surname_text_var.get()
        surname = surname.lower().capitalize()
        
        phone = int(self.phone_text_var.get())
        
        address = self.address_text_var.get()
        
        company = self.company_text_var.get()
        company = company.lower().capitalize()
        
        job = self.job_text_var.get()
        job = job.lower().capitalize()
        
        art = self.art_text_var.get()
        
        siniester = self.siniester_text_var.get()
        
        accident_date = self.accident_date_text_var.get()
        
        dr = self.dr_text_var.get()
        
        dominancia = self.dominancia_text_var.get()
        
        start_date = self.start_date_text_var.get()
        
        #validate dates
        if(not is_valid_date(accident_date) or not is_valid_date(start_date)):
            messagebox.showerror(title = 'Error: Fecha no valida', message = 'Ingresar fecha en formato DD-MM-AAA o DD/MM/AAA')
        
        else:
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
                                    Telefono = {phone}, Dr_derivante = '{dr}', Dominancia = '{dominancia}', 
                                    Fecha_Inicio = '{start_date}', Empresa = '{company}', Domicilio = '{address}'
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
                                Telefono = {phone}, Dr_derivante = '{dr}', Dominancia = '{dominancia}', 
                                Fecha_Inicio = '{start_date}', Empresa = '{company}', Domicilio = '{address}'
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
        conn = sqlite3.connect('cai_database.db')
        
        dni = int(self.entry_dni_var.get())
        
        name = self.entry_name_var.get()
        name = name.lower().capitalize()
        
        surname = self.entry_surname_var.get()
        surname = surname.lower().capitalize()
        
        phone = int(self.entry_phone_var.get())
        
        address = self.entry_address_var.get()
        
        company = self.entry_company_var.get()
        company = company.lower().capitalize()
        
        job = self.entry_job_var.get()
        job = job.lower().capitalize()
        
        art = self.entry_art_var.get()
        
        siniester = self.entry_siniester_var.get()
        
        accident_date = self.entry_accident_date_var.get()
        
        dr = self.entry_dr_var.get()
        
        dominancia = self.entry_dominancia_var.get()
        
        start_date = self.entry_start_date_var.get()
        
        #validate dates
        if(not is_valid_date(accident_date) or not is_valid_date(start_date)):
            messagebox.showerror(title = 'Error: Fecha no valida', message = 'Ingresar fecha en formato DD-MM-AAA o DD/MM/AAA')
        
        else:
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
                                    Telefono = {phone}, Dr_derivante = '{dr}', Dominancia = '{dominancia}', 
                                    Fecha_Inicio = '{start_date}', Empresa = '{company}', Domicilio = '{address}'
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
                                Telefono = {phone}, Dr_derivante = '{dr}', Dominancia = '{dominancia}', 
                                Fecha_Inicio = '{start_date}', Empresa = '{company}', Domicilio = '{address}'
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
                
App()