
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import operadores_ed as op

#Importacion para latex 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class app():
    def __init__(self):
        self.root = ttk.Window(themename="cerculean")
        self.root.title("Simulador de Ecuaciones Diferenciales")
        self.root.geometry("600x500")
        
    def crear_widgets(self):
        
        self.label = ttk.Label(self.root, text= "Simulador de Ecuaciones Diferenciales ")
        self.label.pack(pady=20)
        self.label.config(font=("display", 10, "bold"), background="#1f77b4", foreground="white", padding=10)
        
        self.label = ttk.Label(self.root, text= "Ingrese la ecuación diferencial: ")
        self.label.pack(pady=10)
        self.label.config(font = ("display", 10, "bold"))
        
        self.text_box = ttk.Entry(self.root, width = 25)
        self.text_box.pack(pady=10)
        
        self.button = ttk.Button(self.root, text="Calcular", command=self.realizar_calculo, style = "success")
        self.button.pack(pady=10)
        
        #Control de estado del botón (habilitado/deshabilitado)
        self.button.config(state="disabled")
        self.text_box.bind("<KeyRelease>", self.controlar_estado_boton)
        #Frame para mostrar los resultados
        self.frame = ttk.Frame(self.root, padding = 12, relief= "flat", style = "info")
        self.frame.pack(pady=10)
        
        #Lienzo de matplotlib para el latex
        self.figure = Figure(figsize = (5, 1.2), facecolor = "white")
        self.ejes = self.figure.add_subplot(111)
        
        self.ejes.get_xaxis().set_visible(False)
        self.ejes.get_yaxis().set_visible(False)
        for spine in self.ejes.spines.values():
            spine.set_visible(False)
            
        self.canvas_latex = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas_latex.get_tk_widget().pack(fill=BOTH, expand=YES)
        
              
    def controlar_estado_boton(self, event):
        if self.text_box.get().strip():
            self.button.config(state="normal")
        else:
            self.button.config(state="disabled")
    
    def realizar_calculo(self):
        ed_input = self.text_box.get().lower()
        try:
            # Mandamos a resolver al backend (operadores_ed)
            resultado = op.resolver_edo(ed_input)
            
            # 1. Obtenemos la expresión en formato LaTeX desde SymPy
            import sympy as sp
            res_latex = sp.latex(resultado)
            formula_completa = f"${res_latex}$" # Envoltura matemática
            
            # 2. Limpiamos el gráfico anterior y dibujamos el LaTeX centrado
            self.ejes.clear()
            self.ejes.text(0.5, 0.5, formula_completa, 
                           fontsize=14, color="#083192", # Conservando tu azul preferido
                           horizontalalignment='center', verticalalignment='center')
            
            # 3. Refrescamos el Canvas en pantalla
            self.canvas_latex.draw()
            
        except Exception as e:
            # Si algo falla en el parseo o resolución, lo muestra de forma segura
            self.ejes.clear()
            self.ejes.text(0.5, 0.5, f"Error en la ecuación", 
                           fontsize=12, color="red", 
                           horizontalalignment='center', verticalalignment='center')
            self.canvas_latex.draw()
        
if __name__ == "__main__":
    my_app = app()
    my_app.crear_widgets()
    my_app.root.mainloop()
        