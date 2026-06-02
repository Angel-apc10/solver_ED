
import ttkbootstrap as ttk
import operadores_ed as op
import sympy as sp
import graphsED as grd

from ttkbootstrap.constants import * #type: ignore
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk

class app():
    def __init__(self):
        self.root = ttk.Window(themename="morph")
        self.root.title("Simulador de Ecuaciones Diferenciales")
        self.root.geometry("700x720")
    
    #Subdividimos
    def _crear_encabezado(self):
        self.label = ttk.Label(self.root, text= "Simulador de Ecuaciones Diferenciales ")
        self.label.pack(pady=20, padx = 15)
        self.label.config(font=("display", 10, "bold"), background="white", foreground="#081F56", 
                           padding=10, relief = "raised", borderwidth=2, width = 40, anchor="center")
        
        self.label = ttk.Label(self.root, text= "Ingrese la ecuación diferencial: ")
        self.label.pack(pady=10)
        self.label.config(font = ("display", 10, "bold"), foreground = "#081F56")
        
    def _crear_panelEntrada(self, master:ttk.Frame):
        self.text_box = ttk.Entry(master, width = 45)
        self.text_box.grid(row=0, column=0, columnspan=2, pady=(0, 15), padx=10)
        self.text_box.config(foreground = "black")
        
        #Subframe para almacenar condiciones de valores iniciales
        self.frame_condition = ttk.Frame(self.frm_c, padding= 8,  style = 'light')
        self.frame_condition.grid(column=0, row = 1, sticky= 'w', padx=10)
        self.frame_condition.config(relief = 'ridge', width= 15, height= 18)
        
        #Agregamos una etiqueta para señalar la condición inicial (opcional)
        self.lab_cd = ttk.Label(self.frame_condition, text="Condición Inicial (Opcional):", font=('display', 9, 'bold'), background= "#005085", foreground="#F7F7F7")
        self.lab_cd.grid(row=0, column=0, columnspan=4, sticky='w', pady=(0, 5))
        
        #Etiqueta de y
        self.lab_y_open = ttk.Label(self.frame_condition, text = "y (", font = ('display', 10, 'bold'), foreground = "#081F56")
        self.lab_y_open.grid(row = 1, column = 0, padx = 2)
        
        #Insertamos entradas para la condiciones
        #Entrada x0
        self.tc_x0 = ttk.Entry(self.frame_condition, width=6, justify = 'center', font = ('display', 9, "bold"), foreground = "#081F56")
        self.tc_x0.grid(row = 1, column = 1, padx = 2, ipady = 1)
        
        self.lab_y_close = ttk.Label(self.frame_condition, text = ") =", font = ('display', 10, 'bold'), foreground = "#081F56")
        self.lab_y_close.grid(row = 1, column = 2, padx = 2)
        
        #Entrada para y0
        self.tc_y0 = ttk.Entry(self.frame_condition, width=6, justify='center', font = ('display', 9, "bold"), foreground = "#081F56")
        self.tc_y0.grid(row=1, column=3, padx=2, ipady=1)
        
        #Botones para operaciones (calcular)
        self.button = ttk.Button(self.frm_c, text="Calcular", command=self.procesar_calculo, style = "success-outline")
        self.button.grid(column = 1, row = 1)
        self.button.config(state="disabled")
        #Evento teclado
        self.text_box.bind("<KeyRelease>", self.controlar_estado_boton)
        
    def _crear_panelResultados(self, master:ttk.Frame):
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
        
    def _crear_panelGrafica(self, master:ttk.Frame):
        #Inicializar un canva vacío para el campo de direcciones, se actualizará al resolver la ecuación
        self.fig_dinamica = Figure(figsize = (5, 3), facecolor = "white")
        ax = self.fig_dinamica.add_subplot(111)
        ax.text(0.5, 0.5, "La gráfica se generará al calcular", color = "#081F56", fontsize=12, ha='center', va='center')
        ax.axis('off')
        
        self.canvas_grafica = FigureCanvasTkAgg(self.fig_dinamica, master=self.frame_grafica)
        self.canvas_grafica.get_tk_widget().pack(fill=BOTH, expand=YES)
        
        #Navigation toolbar para la gráfica
        self.toolbar = NavigationToolbar2Tk(self.canvas_grafica, self.frame_grafica)
        self.toolbar.update()
        self.toolbar.pack(fill = X, pady = (5,0))
        
    def controlar_estado_boton(self, event):
        if self.text_box.get().strip():
            self.button.config(state="normal")
        else:
            self.button.config(state="disabled")
             
    #Definimos nuestro director principal de widgets
    def crear_widgets(self):
        self._crear_encabezado()
        #Creamos un frame contenedor
        self.frm_c = ttk.Frame(self.root, padding= 15, style = 'light')
        self.frm_c.pack(pady= 15)
        self.frm_c.config(relief= 'ridge')
        self._crear_panelEntrada(self.frm_c)
        
        #Frame para mostrar los resultados
        self.frame = ttk.Frame(self.root, padding = 15, relief= "ridge", style = "light")
        self.frame.pack(pady=15, padx= 20)
        self._crear_panelResultados(self.frame)
        
        #Frame para la gráfica del campo de direcciones
        self.frame_grafica = ttk.Frame(self.root, padding = 10, relief = "ridge", style = "light")
        self.frame_grafica.pack(pady=10, padx = 20, fill = BOTH, expand = YES)
        self._crear_panelGrafica(self.frame_grafica)
        
    # ====================================
    #   OBTENCIÓN DE DATOS Y PROCESAMIENTO
    # =====================================        
    def _obtener_datos(self):
        datos = {
            "ed_input": self.text_box.get().lower(),
            "str_x0": self.tc_x0.get().strip(),
            "str_y0": self.tc_y0.get().strip()
            }
        return datos
    
    def _procesar_condiciones(self, str_x0, str_y0):
        #Validamos que haya entradas para procesar un PVI, si no, se retona un None
        x0_val = None
        y0_val = None
        if str_x0 and str_y0:
            try:
                x0_val = float(str_x0)
                y0_val = float(str_y0)
            except ValueError:
                raise ValueError("Las condiciones iniciales deben de ser números.")
            return x0_val, y0_val
        else:
            return None, None
    # ====================================
    #   Visualización de resultados
    # =====================================    
    def _dibujar_latex(self, formula_completa):
        self.ejes.clear()
        self.ejes.text(0.5, 0.5, formula_completa, 
                               fontsize=14, color="#081F56", 
                               horizontalalignment='center', verticalalignment='center')
        self.canvas_latex.draw()
    
    def _dibujar_tabla_propiedades(self, resultado):
        #3. Rellenamos las etiquetas individuales (la tabla) dinámicamente cambiando su estilo para resaltar
        self.lbl_orden.config(text=f"Orden: {resultado['orden']}", background="white", foreground="#081F56", relief="raised")
        self.lbl_lineal.config(text=f"Lineal: {resultado['lineal']}", background="white", foreground="#081F56", relief="raised")
        self.lbl_homogenea.config(text=f"Homogénea: {resultado['homogenea']}", background="white", foreground="#081F56", relief="raised")
    
    def _generar_grafica(self, resultado, tiene_pvi, ed_input):
        #Generación de gráfica de gráfica
        #Destruimos el widget anterior del frame de gráficas
        self.canvas_grafica.get_tk_widget().destroy()
        self.toolbar.destroy()
         #Instanciamos la clase de la gráfica general
        graficador = grd.general_plot()
             
        #Generamos la figura pasandole el objeto de solución
        self.fig_dinamica  = graficador.generar_grafica(resultado["solucion"], tiene_pvi=tiene_pvi)
                
        # 5. Volvemos a pintar en el frame
        self.canvas_grafica = FigureCanvasTkAgg(self.fig_dinamica, master=self.frame_grafica)
        self.canvas_grafica.get_tk_widget().pack(fill=BOTH, expand=YES)
        
        #6 volvemos a generar el toolbar para la nueva gráfica
        self.toolbar = NavigationToolbar2Tk(self.canvas_grafica, self.frame_grafica)
        self.toolbar.update()
        self.toolbar.pack(fill=X, pady=(5, 0))
    # ====================================
    #   Manejo de excepciones y errores 
    # =====================================
    def _manejar_error(self, mensaje):
        self.ejes.clear()
        # Si el error es por las condiciones iniciales, mostramos ese mensaje específico
        if "condiciones iniciales" in mensaje:
            self.ejes.text(0.5, 0.5, "Error: Las condiciones iniciales\ndeben ser números.", 
                           fontsize=11, color="red", ha='center', va='center')
        else:
            self.ejes.text(0.5, 0.5, "Error en la ecuación", 
                           fontsize=12, color="red", 
                           horizontalalignment='center', verticalalignment='center')
        self.canvas_latex.draw()
            
        # Reseteamos las etiquetas de propiedades
        self.lbl_orden.config(text="Orden: --", background=None, relief="flat")
        self.lbl_lineal.config(text="Lineal: --", background=None, relief="flat")
        self.lbl_homogenea.config(text="Homogénea: --", background=None, relief="flat")
            
    # ====================================
    #  Flujo principal 
    # =====================================
    def procesar_calculo(self):
        datos = self._obtener_datos()
        ed_input = datos["ed_input"]
      
        x0_val, y0_val = self._procesar_condiciones(datos["str_x0"], datos["str_y0"])
        tiene_pvi = (x0_val is not None and y0_val is not None)
        try:
            # Mandamos a resolver al backend una sola vez (corregido el doble llamado)
            resultado = op.resolver_edo(ed_input, x0_val, y0_val)
            if resultado["status"] == "success":
                res_latex = sp.latex(resultado["solucion"])
                formula_completa = f"${res_latex}$"
                # 1. Obtenemos la expresión en formato LaTeX desde SymPy
                self._dibujar_latex(formula_completa)
                self._dibujar_tabla_propiedades(resultado)
                self._generar_grafica(resultado, tiene_pvi=tiene_pvi, ed_input = ed_input)
            else:
                raise Exception(resultado["mensaje"])
        except Exception as e:
            self._manejar_error(str(e))
       
if __name__ == "__main__":
    my_app = app()
    my_app.crear_widgets()
    my_app.root.mainloop()