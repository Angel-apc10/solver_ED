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
    
def resolver_edo(eq_input, x0_val= None, y0_val = None, dy0_val = None):
    '''Función unificada que ahora puede resolver una EDO general o particular
    con (PVI) si se le proporciona un valor a la condicion a x0 o a y0
    '''
    '''Ahora se acepta dy_0 (valor de derivada en x0)'''
    try: 
        # 1. Interpretamos la ecuación
        eq = interpretar_edo(eq_input)
        # 2. Obtenemos las propiedades mediante clasificación y orden de SymPy
        orden = sympy.ode_order(eq, y)
        clasificaciones = sympy.classify_ode(eq, y)
        
        # Analizamos las clasificaciones para determinar linealidad y homogeneidad
        es_lineal = any("linear" in c for c in clasificaciones)
        es_homogenea = any("homogeneous" in c for c in clasificaciones)
        
        #Establecemos la lógica para resolver las condiciones iniciales
        #Si se reciben ambos valores, se configura el diccionario 'ics' de Sympy
        condiciones_iniciales = None
        
        if x0_val is not None and y0_val is not None:
            if orden ==1:
                condiciones_iniciales = {y.subs(x, x0_val): y0_val}
            elif orden == 2 and dy0_val is not None:
                condiciones_iniciales = {
                    y.subs(x, x0_val): y0_val,
                    y.diff(x).subs(x, x0_val): dy0_val
                }
                
        # 3. Resolvemos la ecuación
        solucion = sympy.dsolve(eq, y, ics = condiciones_iniciales)
        # 4. Retornamos todo empaquetado
        return {
            "status": "success",
            "orden": orden,
            "lineal": "Sí" if es_lineal else "No",
            "homogenea": "Sí" if es_homogenea else "No",
            "solucion": solucion # Objeto SymPy original listo para pasarse a LaTeX
        }
        
    except Exception as e:
        return {
            "status": "error",
            "mensaje": str(e)
        }
     
def interpretar_edo(eq_input):
    #Se valida que tenga un signo gual para evitar errores en el split
    if "=" not in eq_input:
        eq_input = f"{eq_input} = 0"
        
    lado_izq, lado_der = eq_input.split("=")
    #Truco para acondicionar el segundo orden, es vital remplazar primero la segunda derivada antes que la primera
    for lado in [lado_izq, lado_der]:
        lado = lado.replace("y''", "y.diff(x)").replace("ddy", "y.diff(x,2)")
        lado = lado.replace("y'", "y.diff(x)").replace("dy", "y.diff(x)")

    #Procesamos ambas partes
    expr_izq = convertir_expresion(lado_izq.strip().replace("y''", "y.diff(x, 2)").replace("ddy", "y.diff(x, 2)").replace("y'", "y.diff(x)").replace("dy", "y.diff(x)"))
    expr_der = convertir_expresion(lado_der.strip().replace("y''", "y.diff(x, 2)").replace("ddy", "y.diff(x, 2)").replace("y'", "y.diff(x)").replace("dy", "y.diff(x)"))

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