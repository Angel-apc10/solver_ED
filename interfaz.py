import tkinter as tk
import ttkbootstrap as ttk
import operadores_ed as op

class app():
    def __init__(self):
        self.root = ttk.Window(themename="cerculean")
        self.root.title("Calculadora de EDS")
        self.root.geometry("400x400")
        
    def crear_widgets(self):
        self.label = ttk.Label(self.root, text= "Calculadora de Ecuaciones Diferenciales :D")
        self.label.pack(pady=20)
        self.label.config(font=("display", 10, "bold"), background="#1f77b4", foreground="white", padding=10)
        
        self.label = ttk.Label(self.root, text= "Ingrese la ecuación diferencial: ")
        self.label.pack(pady=10)
        self.label.config(font = ("display", 10, "bold"))
        
        self.text_box = ttk.Entry(self.root, width = 25)
        self.text_box.pack(pady=10)
        
    def create_button(self):
        self.button = ttk.Button(self.root, text="Calcular", command=self.realizar_calculo)
        self.button.pack(pady=10)
    
        #Control de estado del botón (habilitado/deshabilitado)
        self.button.config(state="disabled")
        self.text_box.bind("<KeyRelease>", self.controlar_estado_boton)
        
    #Frame para mostrar propiedades de la ecuación diferencial 
    def create_frame(self):
        self.frame = ttk.Frame(self.root, padding = 12)
        self.frame.pack(pady=10)

    def controlar_estado_boton(self, event):
        if self.text_box.get().strip():
            self.button.config(state="normal")
        else:
            self.button.config(state="disabled")
            
    def realizar_calculo(self):
        ed_input = self.text_box.get()
        resultado = op.resolver_edo(ed_input)
        re_label = ttk.Label(self.frame, text=f"Solución: {resultado}")
        re_label.pack(pady=10)

if __name__ == "__main__":
    my_app = app()
    my_app.crear_widgets()
    my_app.create_frame()
    my_app.create_button()
    my_app.root.mainloop()
        