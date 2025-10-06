import dash
from dash import html, dcc

# --- 1. Registro de la página de inicio ---
dash.register_page(__name__, path='/', name='Inicio')

# --- 2. Definición del Layout de la Página ---
layout = html.Div(className='content-container', children=[
    
    html.Div(className='card', style={'width': '100%'}, children=[
        
        # --- SECCIÓN DE PRESENTACIÓN ---
        html.H1("Presentación del Proyecto", style={'textAlign': 'center'}),
        html.Hr(),
        
        html.H2("Presentación personal"),
        html.P(
            "Mi nombre es Katherin Cardenas, soy estudiante del sexto ciclo de la carrera de Computación "
            "Científica en la Universidad Nacional Mayor de San Marcos. Este proyecto interactivo es el resultado "
            "de mi interés por aplicar los fundamentos del modelamiento matemático en la resolución de problemas "
            "complejos, un área que conecta directamente con mi principal campo de estudio: la ciberseguridad."
        ),

        # --- SECCIÓN DE OBJETIVOS ---
        html.H2("Objetivos del Proyecto"),
        html.P(
            "El propósito de este trabajo es demostrar la aplicación práctica de las técnicas de modelamiento "
            "matemático estudiadas en el curso. A través de ejemplos interactivos, se busca ilustrar cómo los "
            "conceptos teóricos pueden ser implementados para analizar y visualizar sistemas dinámicos."
        ),
        html.Ul([
            html.Li([
                html.Strong("Análisis de Ecuaciones Diferenciales: "),
                "Visualizar el comportamiento de modelos fundamentales, como el crecimiento exponencial y el "
                "logístico, para comprender sus propiedades y limitaciones."
            ]),
            html.Li([
                html.Strong("Implementación de Modelos: "),
                "Aplicar los conceptos del curso para construir simulaciones numéricas que representen "
                "fenómenos del mundo real de manera simplificada."
            ]),
            html.Li([
                html.Strong("Visualización Interactiva de Datos: "),
                "Utilizar herramientas como Dash y Plotly para crear interfaces que permitan explorar los "
                "parámetros de un modelo y observar su impacto en los resultados en tiempo real."
            ])
        ]),

        # --- SECCIÓN DE INTERESES ---
        html.H2("Temas Relacionados de Interés"),
        html.Ul([
            html.Li("Modelamiento de Amenazas y Ethical Hacking"),
            html.Li("Ciencia de Datos Aplicada a la Seguridad"),
            html.Li("Criptografía y Arquitecturas Seguras"),
            html.Li("Automatización de Procesos de Seguridad")
        ]),

        html.Hr(),
        html.P([
            "Para conocer más sobre mis otros proyectos, puedes visitar mi ",
            html.A(
                "portafolio personal", 
                href="https://ktthyrn.github.io/kattyspage", 
                target="_blank", 
                style={'color': '#880e4f', 'fontWeight': 'bold'}
            ),
            "."
        ], style={'textAlign': 'center', 'marginTop': '20px'})
    ])
])
