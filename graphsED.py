import numpy as np
import sympy as sp
from matplotlib.figure import Figure

#Creamos una clase para el gráfico de direcciones (prueba)
class direction_field():
    
    def __init__(self):
        self.figura = Figure(figsize=(5, 3), facecolor="white")
        self.ejes = self.figura.add_subplot(111)
    
    def generar_campo(self, eq_sympy):
        try:
            x_sym = sp.symbols('x')
            y_sym = sp.Function('y')(x_sym)
            
            # Intentamos despejar dy/dx (y') de la ecuación recibida
            # Ejemplo: dy + 2y = 0 -> dy = -2y
            dy = y_sym.diff(x_sym)
            expresion_despejada = sp.solve(eq_sympy, dy)
            
            if not expresion_despejada:
                raise Exception("No se pudo despejar y'")
                
            # Tomamos la primera solución del despeje
            f_expr = expresion_despejada[0]
            
            # Convertimos la expresión de SymPy en una función rápida de NumPy (evaluable)
            # Si la expresión no contiene 'x', le avisamos a lambdify para que lo maneje
            f_num = sp.lambdify((x_sym, y_sym), f_expr, modules=['numpy'])
            
            # 2. Creamos la rejilla de puntos para la gráfica (valores de x de -5 a 5, y de -5 a 5)
            x_vals = np.linspace(-5, 5, 20)
            y_vals = np.linspace(-5, 5, 20)
            X, Y = np.meshgrid(x_vals, y_vals)
            
            # 3. Calculamos la pendiente (oscuridad/dirección) en cada punto de la rejilla
            # Usamos un try/except interno por si hay divisiones entre cero (ej. y/x cuando x=0)
            with np.errstate(divide='ignore', invalid='ignore'):
                Valores_Pendiente = f_num(X, Y)
                # Si el resultado es un número fijo (no depende de x o y), NumPy devuelve un escalar.
                # Lo convertimos a una matriz del mismo tamaño que la rejilla.
                if isinstance(Valores_Pendiente, (int, float, np.number)):
                    Valores_Pendiente = np.full(X.shape, Valores_Pendiente)
            
            # 4. Calculamos los componentes vectoriales (U, V) de las flechas
            # Ángulo de la pendiente: theta = arctan(dy/dx)
            Fondo_Angulo = np.arctan(Valores_Pendiente)
            U = np.cos(Fondo_Angulo)
            V = np.sin(Fondo_Angulo)
            
            # 5. Dibujamos las flechas (Quiver plot)
            # color='#081F56' para mantener tu gama de azules
            self.ejes.quiver(X, Y, U, V, angles='xy', color='#081F56', alpha=0.6, pivot='middle')
            
            # Configuración estética de la gráfica
            self.ejes.set_title("Campo de Direcciones de la EDO", fontsize=10, color="#081F56", fontweight="bold")
            self.ejes.grid(True, linestyle='--', alpha=0.5)
            self.ejes.set_xlim([-5, 5])
            self.ejes.set_ylim([-5, 5])
            self.ejes.tick_params(labelsize=8)
            
        except Exception as e:
            # Si algo falla de camino (ej. ecuaciones de orden mayor que 1), muestra un aviso amigable
            self.ejes.clear()
            self.ejes.text(0.5, 0.5, f"Gráfica no disponible para esta ecuación\n({str(e)})", 
                    fontsize=9, color="gray", horizontalalignment='center', verticalalignment='center')
            self.ejes.axis('off')
            
        return self.figura
        
#Create a new class for general plot (try):
class general_plot():
    def __init__(self):
        self.figura = Figure(figsize = (5,3), facecolor = "white")
        self.ejes = self.figura.add_subplot(111)
        
    def generar_grafica(self, solucion_sympy, tiene_pvi = False):
        try:
            x_sym = sp.symbols('x')
            # Extraemos la parte derecha de la igualdad (la solución matemática explícita)
            expresion = solucion_sympy.rhs
            
            # Definimos el rango numérico de evaluación para el eje X
            x_vals = np.linspace(-5, 5, 200)
            
            if tiene_pvi:
                # --- CASO 1: SOLUCIÓN PARTICULAR (PVI) ---
                # Como ya no hay constantes libres (C1, C2), lambdificamos directamente
                f_num = sp.lambdify(x_sym, expresion, modules=['numpy'])
                y_vals = f_num(x_vals)
                
                # Dibujamos la curva única con tu azul preferido en formato sólido
                self.ejes.plot(x_vals, y_vals, color='#081F56', linewidth=2, label="Solución Particular")
            else:
                # --- CASO 2: SOLUCIÓN GENERAL ---
                # Buscamos qué constantes libres quedan en la expresión (C1, C2, etc.)
                constantes = sorted(list(expresion.free_symbols - {x_sym}), key=lambda s: s.name)
                
                if len(constantes) == 1:
                    # EDO de primer orden: Evaluamos dándole 5 valores distintos a C1 para crear la familia
                    c1_sym = constantes[0]
                    f_num = sp.lambdify((x_sym, c1_sym), expresion, modules=['numpy'])
                    
                    valores_c1 = [-2, -1, 0, 1, 2]
                    for c1 in valores_c1:
                        y_vals = f_num(x_vals, c1)
                        self.ejes.plot(x_vals, y_vals, alpha=0.7, linestyle='-', label=f"C1 = {c1}")
                        
                elif len(constantes) == 2:
                    # EDO de segundo orden: Evaluamos combinaciones de C1 y C2
                    c1_sym, c2_sym = constantes[0], constantes[1]
                    f_num = sp.lambdify((x_sym, c1_sym, c2_sym), expresion, modules=['numpy'])
                    
                    combinaciones_c = [(-1, 1), (0, 1), (1, -1), (2, 0)]
                    for c1, c2 in combinaciones_c:
                        y_vals = f_num(x_vals, c1, c2)
                        self.ejes.plot(x_vals, y_vals, alpha=0.7, linestyle='-', label=f"C1={c1}, C2={c2}")
                else:
                    # Si por alguna razón matemática no hay constantes pero no vino marcado como PVI
                    f_num = sp.lambdify(x_sym, expresion, modules=['numpy'])
                    self.ejes.plot(x_vals, f_num(x_vals), color='#081F56', label="Solución")
            
            # Configuraciones estéticas de alta calidad
            self.ejes.set_title("Curva de Solución de la EDO", fontsize=10, color="#081F56", fontweight="bold")
            self.ejes.set_xlabel("x", fontsize=8, color="#081F56")
            self.ejes.set_ylabel("y(x)", fontsize=8, color="#081F56")
            self.ejes.grid(True, linestyle='--', alpha=0.5)
            self.ejes.set_xlim([-5, 5])
            self.ejes.set_ylim([-5, 5]) # Límite estándar para controlar desbordes de exponenciales
            self.ejes.tick_params(labelsize=8)
            self.ejes.legend(fontsize=7, loc='best')
            
        except Exception as e:
            self.ejes.clear()
            self.ejes.text(0.5, 0.5, f"No se pudo generar la curva analítica\n({str(e)})", 
                    fontsize=9, color="gray", horizontalalignment='center', verticalalignment='center')
            self.ejes.axis('off')
            
        return self.figura