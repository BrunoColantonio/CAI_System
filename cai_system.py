import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import pdfkit
import jinja2
import os

def get_pacient(obj, query_arg):
        conn = sqlite3.connect('cai_database.db')
        
        if(query_arg =='dni'):
            dni = int(obj.entry_dni_var.get())
            query = f'''SELECT P.Dni, P.Nombre, P.Apellido, A.Nombre
                    FROM Paciente P
                    INNER JOIN Art A on P.Art = A.Id
                    WHERE P.Dni = {dni}'''
                    
        else:
            name = obj.entry_name_var.get()
            name = name.lower().capitalize()
            surname = obj.entry_surname_var.get()
            surname = surname.lower().capitalize()
            query = f'''SELECT P.Dni, P.Nombre, P.Apellido, A.Nombre
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
        
        conn.close()

def get_pacient_event(obj, event, query_arg):
       conn = sqlite3.connect('cai_database.db')
       if(query_arg =='dni'):
            dni = int(obj.entry_dni_var.get())
            query = f'''SELECT P.Dni, P.Nombre, P.Apellido, A.Nombre
                    FROM Paciente P
                    INNER JOIN Art A on P.Art = A.Id
                    WHERE P.Dni = {dni}'''
                    
       else:
            name = obj.entry_name_var.get()
            name = name.lower().capitalize()
            surname = obj.entry_surname_var.get()
            surname = surname.lower().capitalize()
            query = f'''SELECT P.Dni, P.Nombre, P.Apellido, A.Nombre
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
        
       conn.close()

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
        self.header_label = ctk.CTkLabel(self, text = 'Generar ficha paciente', font = ("Arial",25), compound = 'center')
        
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
        
        self.generate_button = ctk.CTkButton(self, text = 'Generar ficha', command = lambda : GenerarFichaFrame.generatePdf(self))
          
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
        self.generate_button.grid(row = 9, column = 0, columnspan = 4)

    def clear_fields(self):
        self.dni_text_var.set('')
        self.name_text_var.set('')
        self.surname_text_var.set('')
        self.art_text_var.set('')
        self.entry_dni_var.set('')
        self.entry_name_var.set('')
        self.entry_surname_var.set('')
    
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
            
        self.clear_fields()
               
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
        self.art_label = ctk.CTkLabel(self, text = 'Ingrese ART del paciente:', font = ("Arial",15), compound = 'center')
        self.entry_art_var = ctk.StringVar()
        self.entry_art = ctk.CTkEntry(self, textvariable = self.entry_art_var)
        self.entry_art.bind('<Return>', lambda event: AltaPacienteFrame.create_pacient_event(self,event))
        self.submit_button = ctk.CTkButton(self, text = 'Enviar', command = lambda : AltaPacienteFrame.create_pacient(self))
        
    def create_layout(self):
        self.columnconfigure((0,1), weight = 1)
        self.rowconfigure((0,1,2,3,4,5), weight = 1)
        
        self.header_label.grid(row = 0, column = 0, columnspan = 2)
        self.dni_label.grid(row = 1, column = 0)
        self.entry_dni.grid(row = 1, column = 1)
        self.name_label.grid(row = 2, column = 0)
        self.entry_name.grid(row = 2, column = 1)
        self.surname_label.grid(row = 3, column = 0)
        self.entry_surname.grid(row = 3, column = 1)
        self.art_label.grid(row = 4, column = 0)
        self.entry_art.grid(row = 4, column = 1)
        self.submit_button.grid(row = 5, column = 0, columnspan = 2)
        
    def clear_fields(self):
        self.entry_dni_var.set('')
        self.entry_name_var.set('')
        self.entry_surname_var.set('')
        self.entry_art_var.set('')
    
    def create_pacient(self):
        conn = sqlite3.connect('cai_database.db')
        dni = int(self.entry_dni_var.get())
        name = self.entry_name_var.get()
        name = name.lower().capitalize()
        surname = self.entry_surname_var.get()
        surname = surname.lower().capitalize()
        art = self.entry_art_var.get()
        
        ## validate entry
        if(dni <= 0 or name == '' or surname == '' or art == ''):
            messagebox.showerror(title = 'Error: Campos en blanco', message = f'Debe completar todos los campos')
            
        else:
            ## validate ART name
            if(art == '-'):
                art = 'PARTICULAR'
            art = art.upper()
            query = f"SELECT Id FROM Art WHERE Nombre = '{art}' "
            cursor = conn.execute(query)
            data = cursor.fetchone()
            if(data == None):
                messagebox.showerror(title = 'Error: ART invalida', message = f'La ART: {art} no existe')
            else:
                art = data[0]
                query = f"INSERT INTO Paciente (Dni,Nombre,Apellido,Art) VALUES ({dni},'{name}','{surname}',{art})"
                
                try:
                    cursor = conn.execute(query)
                    conn.commit()
                except sqlite3.Error as err:
                    messagebox.showerror(title = 'Error: Dni no valido', message = f'Ya existe el paciente con dni: {dni}')
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
        art = self.entry_art_var.get()
        
        ## validate entry
        if(dni <= 0 or name == '' or surname == '' or art == ''):
            messagebox.showerror(title = 'Error: Campos en blanco', message = f'Debe completar todos los campos')
            
        else:
            ## validate ART name
            if(art == '-'):
                art = 'PARTICULAR'
            art = art.upper()
            query = f"SELECT Id FROM Art WHERE Nombre = '{art}' "
            cursor = conn.execute(query)
            data = cursor.fetchone()
            if(data == None):
                messagebox.showerror(title = 'Error: ART invalida', message = f'La ART: {art} no existe')
            else:
                art = data[0]
                query = f"INSERT INTO Paciente (Dni,Nombre,Apellido,Art) VALUES ({dni},'{name}','{surname}',{art})"
                
                try:
                    cursor = conn.execute(query)
                    conn.commit()
                except sqlite3.Error as err:
                    messagebox.showerror(title = 'Error: Dni no valido', message = f'Ya existe el paciente con dni: {dni}')
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
        self.pacient_label = ctk.CTkLabel(self, text = 'Datos del paciente:', font = ("Arial",25), compound = 'center')
        
        self.dni_label = ctk.CTkLabel(self, text = 'D.N.I:', font = ("Arial",15), compound = 'center')
        self.dni_text_var = ctk.StringVar()
        self.dni_data_entry = ctk.CTkEntry(self, textvariable = self.dni_text_var)
        self.dni_data_entry.bind('<Return>', lambda event: ModificarPacienteFrame.update_pacient_event(self,event))
        
        self.name_label = ctk.CTkLabel(self, text = 'Nombre:', font = ("Arial",15), compound = 'center')
        self.name_text_var = ctk.StringVar()
        self.name_data_entry = ctk.CTkEntry(self, textvariable = self.name_text_var)
        self.name_data_entry.bind('<Return>', lambda event: ModificarPacienteFrame.update_pacient_event(self,event))
        
        self.surname_label = ctk.CTkLabel(self, text = 'Apellido:', font = ("Arial",15), compound = 'center')
        self.surname_text_var = ctk.StringVar()
        self.surname_data_entry = ctk.CTkEntry(self, textvariable = self.surname_text_var)
        self.surname_data_entry.bind('<Return>', lambda event: ModificarPacienteFrame.update_pacient_event(self,event))
        
        self.art_label = ctk.CTkLabel(self, text = 'A.R.T:', font = ("Arial",15), compound = 'center')
        self.art_text_var = ctk.StringVar()
        self.art_data_entry = ctk.CTkEntry(self, textvariable = self.art_text_var)
        self.art_data_entry.bind('<Return>', lambda event: ModificarPacienteFrame.update_pacient_event(self,event))
        
        self.update_button = ctk.CTkButton(self, text = 'Actualizar', command = lambda : ModificarPacienteFrame.update_pacient(self))

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
        self.dni_data_entry.grid(row = 5, column = 2, columnspan = 2)
        self.name_label.grid(row = 6, column = 0, columnspan = 2) 
        self.name_data_entry.grid(row = 6, column = 2, columnspan = 2)
        self.surname_label.grid(row = 7, column = 0, columnspan = 2)
        self.surname_data_entry.grid(row = 7, column = 2, columnspan = 2)
        self.art_label.grid(row = 8, column = 0, columnspan = 2)
        self.art_data_entry.grid(row = 8, column = 2, columnspan = 2)
        self.update_button.grid(row = 9, column = 0, columnspan = 4)
       
    def clear_fields(self):
        self.dni_text_var.set('')
        self.name_text_var.set('')
        self.surname_text_var.set('')
        self.art_text_var.set('')
        self.entry_dni_var.set('')
        self.entry_name_var.set('')
        self.entry_surname_var.set('')
        
    def update_pacient(self):
        dni = int(self.dni_text_var.get())
        name = self.name_text_var.get()
        name = name.lower().capitalize()
        surname = self.surname_text_var.get()
        surname = surname.lower().capitalize()
        art = self.art_text_var.get()
        
        conn = sqlite3.connect('cai_database.db')
        
        ## validate entry
        if(dni <= 0 or name == '' or surname == '' or art == ''):
            messagebox.showerror(title = 'Error: Campos en blanco', message = f'Debe completar todos los campos')
        
        else:
             ## validate ART name
            if(art == '-'):
                art = 'PARTICULAR'
            art = art.upper()
            query = f"SELECT Id FROM Art WHERE Nombre = '{art}' "
            cursor = conn.execute(query)
            data = cursor.fetchone()
            if(data == None):
                messagebox.showerror(title = 'Error: ART invalida', message = f'La ART: {art} no existe')
            else:
                art = data[0]
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
                                    SET Dni = {dni}, Nombre = '{name}', Apellido = '{surname}', Art = {art}
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
                                SET Dni = {dni}, Nombre = '{name}', Apellido = '{surname}', Art = {art}
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
                        
        self.clear_fields()
        
    def update_pacient_event(self,event):
        dni = int(self.dni_text_var.get())
        name = self.name_text_var.get()
        name = name.lower().capitalize()
        surname = self.surname_text_var.get()
        surname = surname.lower().capitalize()
        art = self.art_text_var.get()
        
        conn = sqlite3.connect('cai_database.db')
        
        ## validate entry
        if(dni <= 0 or name == '' or surname == '' or art == ''):
            messagebox.showerror(title = 'Error: Campos en blanco', message = f'Debe completar todos los campos')
        
        else:
             ## validate ART name
            if(art == '-'):
                art = 'PARTICULAR'
            art = art.upper()
            query = f"SELECT Id FROM Art WHERE Nombre = '{art}' "
            cursor = conn.execute(query)
            data = cursor.fetchone()
            if(data == None):
                messagebox.showerror(title = 'Error: ART invalida', message = f'La ART: {art} no existe')
            else:
                art = data[0]
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
                                    SET Dni = {dni}, Nombre = '{name}', Apellido = '{surname}', Art = {art}
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
                                SET Dni = {dni}, Nombre = '{name}', Apellido = '{surname}', Art = {art}
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
                        
        self.clear_fields()
                
App()