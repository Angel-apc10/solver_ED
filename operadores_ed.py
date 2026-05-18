import sympy

# Definimos las variables y la función
x = sympy.symbols('x')
y = sympy.Function('y')(x)

# Ecuación "Normal" (Lineal de primer orden) ---
# Ecuación: y' + 2y = e^x
#eq_normal = sympy.Eq(y.diff(x) + 2*y, sympy.exp(x))

eq_normal = sympy.Eq(y.diff(x), 4*x) # Ecuación: y' = 4x (lineal de primer orden)
sol_normal = sympy.dsolve(eq_normal, y)
print("Solución Normal:", sol_normal)

def resolver_edo():
    eq_input = input("Ingrese la ecuación diferencial (ejemplo: y' + 2*y = exp(x)): ")
    sol_normal = sympy.dsolve(interpretar_edo(eq_input), y)
    print("Solución:", sol_normal)
    

def interpretar_edo(eq_input):
    extract = eq_input.split("=")
    derivada_str = extract[0].strip()
    derivada_str = derivada_str.replace("y'", "y.diff(x)")
    expresion_str = extract[1].strip()
    return sympy.Eq(eval(derivada_str), eval(expresion_str))
    
resolver_edo()
    
# Para obtener propiedades de la ecuación diferencial como orden, linealidad:
#orden = sympy.ode_order(eq_homogenea, y)

#es_lineal = sympy.checkodesol(eq_homogenea, sol_homogenea) # (Simplificación conceptual)