import sympy
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application,
    convert_xor, function_exponentiation
)

# Definimos las variables y la función
x = sympy.symbols('x')
y = sympy.Function('y')(x)

TRANSFORMACIONES = (
    standard_transformations +
    (implicit_multiplication_application, convert_xor, function_exponentiation)
)

#Diccionario de nombres permitidos para evaluar y recibir entradas seguras
nombres_Permitidos = {
    'x': x,
    'y': y,
    
    #FUnciones exponenciales
    'exp': sympy.exp,
    'log': sympy.log,
    'ln': sympy.log,
    'sqrt': sympy.sqrt,
    
    #Funciones trigonométricas
    'sin': sympy.sin,
    'cos': sympy.cos,
    'tan': sympy.tan,
    'sec': sympy.sec,
    'csc': sympy.csc,   
    'cot': sympy.cot,
    
    #Constantes
    'pi': sympy.pi,
    'e': sympy.E
}

def convertir_expresion(texto:str):
    texto = texto.strip()
    
    return parse_expr(texto, 
                      transformations=TRANSFORMACIONES, 
                      local_dict=nombres_Permitidos,
                      evaluate=True)
    
def resolver_edo(eq_input):
    #eq_input = input("Ingrese la ecuación diferencial (ejemplo: y' + 2*y = exp(x)): ")
    sol_normal = sympy.dsolve(interpretar_edo(eq_input), y)
    #print("Solución general de la ecuación diferencial: ", sol_normal)
    #print("y = ", sol_normal.rhs)
    return sol_normal
    
def interpretar_edo(eq_input):
    lado_izq, lado_der = eq_input.split("=")

    lado_izq = lado_izq.strip()
    lado_der = lado_der.strip()

    lado_izq = lado_izq.replace("y'", "y.diff(x)")

    expr_izq = convertir_expresion(lado_izq)
    expr_der = convertir_expresion(lado_der)

    return sympy.Eq(expr_izq, expr_der)
    
def obtener_propiedades_edo(eq_input):
    eq = interpretar_edo(eq_input)
    orden = sympy.ode_order(eq, y)
    es_lineal = sympy.checkodesol(eq, sympy.dsolve(eq, y))
    
    print("Propiedades de la ecuación diferencial")
    print(f"Orden: {orden} ")
    
    if es_lineal == True:
        print("La ecuación es lineal.")
        
    return orden, es_lineal