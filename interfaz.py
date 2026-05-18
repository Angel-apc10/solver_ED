import tkinter as tk
import ttkbootstrap as ttk

class app():
    def __init__(self):
        self.root = ttk.Window(themename="cerculean")
        self.root.title("Calculadora de EDS")
        self.root.geometry("400x400")
        
    def crear_widgets(self):
        self.label = ttk.Label(self.root, text= "Calculadora de Ecuaciones Diferenciales :D")
        self.label.pack(pady=20)
        self.label.config(font=("display", 10, "bold"), background="#1f77b4", foreground="white", padding=10)

if __name__ == "__main__":
    my_app = app()
    my_app.crear_widgets()
    my_app.root.mainloop()
        