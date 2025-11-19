import dash
from dash import html, dcc

# --- 1. Registro de la página ---
# ¡Tu menú desplegable "Modelos" la detectará automáticamente!
dash.register_page(__name__, path='/aplicaciones-sir', name='Aplicaciones SIR (Resumen)')

# --- 2. Definición del Layout ---
layout = html.Div(className='content-container', children=[
    
    # Usamos un 'card' de ancho completo, igual que tu página de 'inicio.py'
    html.Div(className='card', style={'width': '100%'}, children=[
        
        html.H1("Aplicaciones y Generalización del Modelo SIR"),
        
        dcc.Markdown(r"""
            Como hemos visto en los modelos SIR y SEIR, el sistema básico de Ecuaciones
            Diferenciales puede modelar la propagación de una enfermedad.
            
            Sin embargo, el concepto de "contagio" es más general. El mismo modelo
            matemático puede usarse para describir cualquier proceso donde una "idea"
            o "estado" se transfiere por contacto en una población cerrada.
            
            A continuación, se presentan 3 estudios de caso basados en las asignaciones
            del curso, que demuestran la flexibilidad del modelo.
        """, mathjax=True),
        
        html.Hr(),

        # --- 3. Pestañas (Tabs) para comparar los 3 casos ---
        dcc.Tabs(id='tabs-sir-aplicaciones', value='tab-1', children=[
            
            # --- PESTAÑA 1: EPIDEMIA ---
            dcc.Tab(label='Caso 1: Epidemia (Enfermedad)', value='tab-1', children=[
                html.Div(className='tab-content', children=[
                    html.H3("Escenario: Brote de Enfermedad"),
                    dcc.Markdown(r"""
                        * **S (Susceptibles):** Estudiantes sanos.
                        * **I (Infectados):** Estudiantes enfermos que contagian.
                        * **R (Recuperados):** Estudiantes inmunes.
                    """),
                    
                    html.H4("Parámetros del Caso"),
                    dcc.Markdown(r"""
                        * $N = 7138$
                        * $S_0 = 7137$, $I_0 = 1$, $R_0 = 0$
                        * $\beta = 1 / 7138$
                        * $k = 0.40$
                        * **$R_0$ (Num. Reproductivo): $\approx 2.5$**
                    """, mathjax=True),
                    
                    html.Img(src=dash.get_asset_url('simulacion_a1.png')),
                    
                    dcc.Markdown(r"""
                        **Conclusión Clave:** Dado que $R_0 > 1$, la epidemia es inevitable.
                        El pico ocurre cuando los susceptibles bajan al umbral crítico $S_c = k / \beta \approx 2855$.
                    """, mathjax=True)
                ])
            ]),
            
            # --- PESTAÑA 2: RUMOR ---
            dcc.Tab(label='Caso 2: Propagación de Rumor', value='tab-2', children=[
                html.Div(className='tab-content', children=[
                    html.H3("Escenario: Rumor en la Facultad"),
                    dcc.Markdown(r"""
                        * **S (Susceptibles):** Alumnos que no han oído el rumor.
                        * **I (Infectados/Propagadores):** Alumnos que creen y difunden el rumor.
                        * **R (Racionales):** Alumnos y docentes que no creen o ya olvidaron el rumor.
                    """),

                    html.H4("Parámetros del Caso"),
                    dcc.Markdown(r"""
                        * $N = 275$
                        * $S_0 = 266$, $I_0 = 1$, $R_0 = 8$
                        * $b = 0.004$
                        * Se analizan dos tasas de "racionalidad" $k$: $0.01$ y $0.02$.
                    """, mathjax=True),

                    html.Img(src=dash.get_asset_url('grafica_rumor.png')),

                    dcc.Markdown(r"""
                        **Conclusión Clave:** El modelo muestra cómo el factor social $k$ (escepticismo,
                        olvido, intervención de autoridad) es crítico para "aplanar la curva" del rumor.
                    """, mathjax=True)
                ])
            ]),
            
            # --- PESTAÑA 3: POLÍTICA PÚBLICA ---
            dcc.Tab(label='Caso 3: Adopción de Política', value='tab-3', children=[
                html.Div(className='tab-content', children=[
                    html.H3("Escenario: Adopción de Política de Reciclaje"),
                    dcc.Markdown(r"""
                        * **S (Susceptibles):** Ciudadanos que no han adoptado la política.
                        * **I (Influyentes):** Ciudadanos que adoptaron y promueven la política.
                        * **R (Rechazadores):** Ciudadanos que deciden no adoptar la política.
                    """),

                    html.H4("Parámetros del Caso"),
                    dcc.Markdown(r"""
                        * $N = 10,050$
                        * $S_0 = 10,000$, $I_0 = 50$, $R_0 = 0$
                        * $b = 0.00005$ (Tasa de adopción)
                        * $k = 0.00002$ (Tasa de rechazo)
                    """, mathjax=True),

                    html.Img(src=dash.get_asset_url('simulacion_a3.png')),

                    dcc.Markdown(r"""
                        **Conclusión Clave:** El modelo puede simular procesos sociales lentos.
                        Permite a los planificadores estimar cómo las campañas (que afectan a $b$)
                        o las barreras (que afectan a $k$) impactan la adopción de una idea.
                    """, mathjax=True)
                ])
            ]),
            
        ]) # Fin de dcc.Tabs
        
    ]) # Fin de 'card'
]) # Fin de 'content-container'