
import ttkbootstrap as ttk
import operadores_ed as op
#Importación del icono o logo con la carpeta resources
import os
import graphsED as grd
#Importacion para latex 
from ttkbootstrap.constants import * #type: ignore
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class app():
    def __init__(self):
        self.root = ttk.Window(themename="morph")
        self.root.title("Simulador de Ecuaciones Diferenciales")
        self.root.geometry("700x720")
        
    def crear_widgets(self):
        
        self.label = ttk.Label(self.root, text= "Simulador de Ecuaciones Diferenciales ")
        self.label.pack(pady=20, padx = 15)
        self.label.config(font=("display", 10, "bold"), background="white", foreground="#081F56", 
                           padding=10, relief = "raised", borderwidth=2, width = 40, anchor="center")
        
        self.label = ttk.Label(self.root, text= "Ingrese la ecuación diferencial: ")
        self.label.pack(pady=10)
        self.label.config(font = ("display", 10, "bold"), foreground = "#081F56")
        
        #Creamos un frame contenedor
        self.frm_c = ttk.Frame(self.root, padding= 15, style = 'light')
        self.frm_c.pack(pady= 15)
        self.frm_c.config(relief= 'ridge')
        
        self.text_box = ttk.Entry(self.frm_c, width = 45)
        self.text_box.grid(row=0, column=0, columnspan=2, pady=(0, 15), padx=10)
        self.text_box.config(foreground = "black")
        
        #Subframe para almacenar condiciones de valores iniciales
        self.frame_condition = ttk.Frame(self.frm_c, padding= 8,  style = 'light')
        self.frame_condition.grid(column=0, row = 1, sticky= 'w', padx=10)
        self.frame_condition.config(relief = 'ridge', width= 15, height= 18)
        #Botones para operaciones (calcular)
        self.button = ttk.Button(self.frm_c, text="Calcular", command=self.realizar_calculo, style = "success-outline")
        self.button.grid(column = 1, row = 1)
        
        #Control de estado del botón (habilitado/deshabilitado)
        self.button.config(state="disabled")
        self.text_box.bind("<KeyRelease>", self.controlar_estado_boton)
        
        #Agregamos una etiqueta para señalar la condición inicial (opcional)
        self.lab_cd = ttk.Label(self.frame_condition, text="Condición Inicial (Opcional):", font=('display', 9, 'bold'), background= "#005085", foreground="#F7F7F7")
        self.lab_cd.grid(row=0, column=0, columnspan=4, sticky='w', pady=(0, 5))
        
        #Etiqueta de y
        self.lab_y_open = ttk.Label(self.frame_condition, text = "y (", font = ('display', 10, 'bold'), foreground = "#081F56")
        self.lab_y_open.grid(row = 1, column = 0, padx = 2)
        
        #Insertamos entradas para la condiciones
        #Entrada x0
        self.tc_x = ttk.Entry(self.frame_condition, width=6, justify = 'center')
        self.tc_x.grid(row = 1, column = 1, padx = 2, ipady = 1)
        
        self.lab_y_close = ttk.Label(self.frame_condition, text = ") =", font = ('display', 10, 'bold'), foreground = "#081F56")
        self.lab_y_close.grid(row = 1, column = 2, padx = 2)
        
        #Entrada para y0
        self.tc_y0 = ttk.Entry(self.frame_condition, width=6, justify='center')
        self.tc_y0.grid(row=1, column=3, padx=2, ipady=1)
        
        #Frame para mostrar los resultados
        self.frame = ttk.Frame(self.root, padding = 15, relief= "ridge", style = "light")
        self.frame.pack(pady=15, padx= 20)
        
        #Frame para la gráfica del campo de direcciones
        self.frame_grafica = ttk.Frame(self.root, padding = 10, relief = "ridge", style = "light")
        self.frame_grafica.pack(pady=10, padx = 20, fill = BOTH, expand = YES)
        
        #Inicializar un canva vacío para el campo de direcciones, se actualizará al resolver la ecuación
        self.fig_dinamica = Figure(figsize = (5, 3), facecolor = "white")
        ax = self.fig_dinamica.add_subplot(111)
        ax.text(0.5, 0.5, "La gráfica se generará al calcular", color = "#081F56", fontsize=12, ha='center', va='center')
        ax.axis('off')
        
        self.canvas_grafica = FigureCanvasTkAgg(self.fig_dinamica, master=self.frame_grafica)
        self.canvas_grafica.get_tk_widget().pack(fill=BOTH, expand=YES)
        
        #Subtitulo interno para la solución
        self.sol_title = ttk.Label(self.frame, text = "Solución General:")
        self.sol_title.pack(anchor = 'w', pady = (0,5))
        self.sol_title.config(font = ("display", 11, "bold"),background = "#005085", foreground = "#EAEAEA")
        #Lienzo de matplotlib para el latex
        self.figure = Figure(figsize = (5, 1.2), facecolor = "white")
        self.ejes = self.figure.add_subplot(111)
        self.ejes.get_xaxis().set_visible(False) 
        self.ejes.get_yaxis().set_visible(False)
        
        for spine in self.ejes.spines.values():
            spine.set_visible(False)
        
        self.canvas_latex = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas_latex.get_tk_widget().pack(fill=BOTH, expand=YES)
        #Subtitulo para mostrar las propiedades de la ecuación diferencial
        self.prop_title = ttk.Label(self.frame, text = "Propiedades de la Ecuación Diferencial:")
        self.prop_title.pack(pady=10)
        self.prop_title.config(font = ("display", 11, "bold"), background = "#005085", foreground = "#EAEAEA")
           
        #Subgframe interno para desplegar una mini tabla de propiedades
        self.subframe_props = ttk.Frame(self.frame, style = "info")  
        self.subframe_props.pack(fill= X, pady = 5) 
        # Usamos .grid() para alinearlas como columnas de una tabla perfectamente distribuidas.
        self.lbl_orden = ttk.Label(self.subframe_props, text="Orden: --", font=("display", 9), padding=6, relief="flat", width=15, anchor="center")
        self.lbl_orden.grid(row=0, column=0, padx=5, sticky=EW)
        
        self.lbl_lineal = ttk.Label(self.subframe_props, text="Lineal: --", font=("display", 9), padding=6, relief="flat", width=15, anchor="center")
        self.lbl_lineal.grid(row=0, column=1, padx=5, sticky=EW)
        
        self.lbl_homogenea = ttk.Label(self.subframe_props, text="Homogénea: --", font=("display", 9), padding=6, relief="flat", width=15, anchor="center")
        self.lbl_homogenea.grid(row=0, column=2, padx=5, sticky=EW)
        
        # Esto hace que las 3 columnas de la tabla midan exactamente lo mismo y se expandan proporcionalmente
        self.subframe_props.columnconfigure((0, 1, 2), weight=1)
        
    def controlar_estado_boton(self, event):
        if self.text_box.get().strip():
            self.button.config(state="normal")
        else:
            self.button.config(state="disabled")
    
    def realizar_calculo(self):
        ed_input = self.text_box.get().lower()
        
        #1. Leer las condiciones iniciales desde la interfaz
        str_x0 = self.tc_x.get().strip()
        str_y0 = self.tc_y0.get().strip()
        
        x0_val = None
        y0_val = None
        
        #Validar si ambas cajas tienen texto para procesar un PVI
        if str_x0 and str_y0:
            try:
                #Convertimos las entradas a valores flotantes
                x0_val = float(str_x0)
                y0_val = float(str_y0)
                self.sol_title.config (text = "Solución Particular (PVI): ")
            except ValueError:
                #En caso de ingresen letras en vez de números en las condiciones iniciales
                self.ejes.clear()
                self.ejes.text(0.5, 0.5, "Error: Las condiciones iniciales\ndeben ser números.", 
                               fontsize=11, color="red", ha='center', va='center')
                self.canvas_latex.draw()
                return # Detiene la ejecución para que no truene el programa
        else: 
            #Si está vacío, aseguramos la solución general
            self.sol_title.config (text= "Solución General: ")
            
        try:
            # Mandamos a resolver al backend una sola vez (corregido el doble llamado)
            resultado = op.resolver_edo(ed_input, x0_val, y0_val)
            
            if resultado["status"] == "success":
                # 1. Obtenemos la expresión en formato LaTeX desde SymPy
                import sympy as sp
                res_latex = sp.latex(resultado["solucion"])
                formula_completa = f"${res_latex}$" 
                
                # 2. Limpiamos y dibujamos el LaTeX
                self.ejes.clear()
                self.ejes.text(0.5, 0.5, formula_completa, 
                               fontsize=14, color="#081F56", 
                               horizontalalignment='center', verticalalignment='center')
                self.canvas_latex.draw()
                
                 #3. Rellenamos las etiquetas individuales (la tabla) dinámicamente cambiando su estilo para resaltar
                self.lbl_orden.config(text=f"Orden: {resultado['orden']}", background="white", foreground="#081F56", relief="raised")
                self.lbl_lineal.config(text=f"Lineal: {resultado['lineal']}", background="white", foreground="#081F56", relief="raised")
                self.lbl_homogenea.config(text=f"Homogénea: {resultado['homogenea']}", background="white", foreground="#081F56", relief="raised")
                
                #Generación de gráfica de campo de direcciones con la función del nuevo módulo
                self.canvas_grafica.get_tk_widget().destroy()  # Limpiamos el canvas anterior
                eq_objeto = op.interpretar_edo(ed_input)  # Obtenemos el objeto de la ecuación diferencial
                
                import graphsED as grd
                self.figura_dinamica = grd.generar_campo_direcciones(eq_objeto)  # Generamos la nueva figura con el campo de direcciones
                self.canvas_grafica = FigureCanvasTkAgg(self.figura_dinamica, master=self.frame_grafica)
                self.canvas_grafica.get_tk_widget().pack(fill=BOTH, expand=YES)  # Creamos un nuevo canvas con la figura actualizada
                
            else:
                raise Exception(resultado["mensaje"])
                
        except Exception as e:
            self.ejes.clear()
            self.ejes.text(0.5, 0.5, f"Error en la ecuación", 
                           fontsize=12, color="red", 
                           horizontalalignment='center', verticalalignment='center')
            self.canvas_latex.draw()
            
            # Reseteamos las etiquetas si hay un error
            self.lbl_orden.config(text="Orden: --", background=None, relief="flat") #type:ignore
            self.lbl_lineal.config(text="Lineal: --", background=None, relief="flat") #type: ignore
            self.lbl_homogenea.config(text="Homogénea: --", background=None, relief="flat") #type: ignore
            
if __name__ == "__main__":
    my_app = app()
    my_app.crear_widgets()
    my_app.root.mainloop()