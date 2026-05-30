# Simulador de Ecuaciones Diferenciales

Este es un simulador interactivo desarrollado en python, diseñado para poder resolver, analizar y visualizar ecuaciones diferenciales homógeneas ordinarias de primer orden,
con soporte para ecuaciones homogéneas y Problemas de Valor inicial (PVI)

## Características
* **Motor Simbólico Robustecido:** Desarrollado con SymPy, permitiendo entradas con sintaxis natural (ej. `y' = 5x` o `2x`).
* **Visualización en LaTeX:** Renderizado matemático de las soluciones mediante Matplotlib.
* **Análisis Automático:** Clasificación instantánea del orden, linealidad y homogeneidad de la ecuación.
* **Campo de Direcciones:** Interpretación gráfica del comportamiento geométrico de la EDO (Slope Fields).
* **Soporte PVI:** Resolución de soluciones particulares ingresando condiciones iniciales y(x_0) = y_0

## Tecnologías y librerías:
* **Python 3.12+**
* **ttkbootstrap** (Interfaz gráfica moderna inspirada en tkinter)
* **SymPy** (Cálculo simbólico)
* **Matplotlib** & **NumPy** (Generación de gráficas y procesamiento númerico)

# Instalación
Para correr el simulador de manera local, siga las siguientes instrucciones:
1. Clone este repositorio:
   ´´´bash
   git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
2. Instale las dependencias necesarias para su ejecución:
   pip install sympy numpy matplotlib ttkbootstrap
3. Ejecute la aplicación:
   python interfaz.py
   
## Funcionamiento del programa 
<img width="699" height="750" alt="imagen" src="https://github.com/user-attachments/assets/0404f077-ab6a-4611-a4c4-a1ac63f50882" />

# Pantalla completa
<img width="1852" height="1122" alt="imagen" src="https://github.com/user-attachments/assets/d7f5fe53-7075-4f95-9362-f08753c8ca9f" />
