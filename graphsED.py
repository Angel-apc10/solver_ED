import numpy as np
import sympy as sp
from matplotlib.figure import Figure

def generar_campo_direcciones(eq_sympy):
    """
    Recibe la ecuación diferencial de SymPy, despeja y' (dy/dx) 
    y genera una Figura de Matplotlib con su campo de direcciones.
    """
    # 1. Creamos la figura de Matplotlib
    figura = Figure(figsize=(5, 3), facecolor="white")
    ejes = figura.add_subplot(111)
    
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
                Valores_Pendiente = np.full_size(X.shape, Valores_Pendiente)
        
        # 4. Calculamos los componentes vectoriales (U, V) de las flechas
        # Ángulo de la pendiente: theta = arctan(dy/dx)
        Fondo_Angulo = np.arctan(Valores_Pendiente)
        U = np.cos(Fondo_Angulo)
        V = np.sin(Fondo_Angulo)
        
        # 5. Dibujamos las flechas (Quiver plot)
        # color='#081F56' para mantener tu gama de azules
        ejes.quiver(X, Y, U, V, angles='xy', color='#081F56', alpha=0.6, pivot='middle')
        
        # Configuración estética de la gráfica
        ejes.set_title("Campo de Direcciones de la EDO", fontsize=10, color="#081F56", fontweight="bold")
        ejes.grid(True, linestyle='--', alpha=0.5)
        ejes.set_xlim([-5, 5])
        ejes.set_ylim([-5, 5])
        ejes.tick_params(labelsize=8)
        
    except Exception as e:
        # Si algo falla de camino (ej. ecuaciones de orden mayor que 1), muestra un aviso amigable
        ejes.clear()
        ejes.text(0.5, 0.5, f"Gráfica no disponible para esta ecuación\n({str(e)})", 
                  fontsize=9, color="gray", horizontalalignment='center', verticalalignment='center')
        ejes.axis('off')
        
    return figura