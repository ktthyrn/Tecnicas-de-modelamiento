import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import solve_ivp

# --- 1. Registro de la página ---
dash.register_page(__name__, path='/aplicaciones-sir', name='Aplicaciones SIR (Resumen)')

# --- 2. Funciones para generar las Gráficas (simuladas en vivo) ---

def grafica_caso1_epidemia():
    # Parámetros del Caso 1
    N = 7138
    I0, R0 = 1, 0
    S0 = N - I0 - R0
    beta = 1 / 7138
    gamma = 0.40
    t_max = 30 # 30 días es suficiente para ver este brote

    # Ecuaciones
    def sir_model(t, y):
        S, I, R = y
        dSdt = -beta * S * I
        dIdt = beta * S * I - gamma * I
        dRdt = gamma * I
        return [dSdt, dIdt, dRdt]

    # Resolver
    t_eval = np.linspace(0, t_max, 200)
    sol = solve_ivp(sir_model, [0, t_max], [S0, I0, R0], t_eval=t_eval)

    # Figura
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sol.t, y=sol.y[0], name='Susceptibles', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=sol.t, y=sol.y[1], name='Infectados', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=sol.t, y=sol.y[2], name='Recuperados', line=dict(color='green')))
    
    fig.update_layout(
        title="Dinámica de la Epidemia (N=7138)",
        xaxis_title="Días",
        yaxis_title="Estudiantes",
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='white'
    )
    return fig

def grafica_caso2_rumor():
    # Parámetros del Caso 2
    # S=266, I=1, R=8 (Total ~275)
    S0, I0, R0 = 266, 1, 8
    b = 0.004
    k_normal = 0.01
    k_alto = 0.02
    t_max = 15

    def rumor_model(t, y, k_val):
        S, I, R = y
        dSdt = -b * S * I
        dIdt = b * S * I - k_val * I
        dRdt = k_val * I
        return [dSdt, dIdt, dRdt]

    t_eval = np.linspace(0, t_max, 200)
    
    # Simulación 1 (k=0.01)
    sol1 = solve_ivp(lambda t, y: rumor_model(t, y, k_normal), [0, t_max], [S0, I0, R0], t_eval=t_eval)
    # Simulación 2 (k=0.02) - Solo para comparar
    sol2 = solve_ivp(lambda t, y: rumor_model(t, y, k_alto), [0, t_max], [S0, I0, R0], t_eval=t_eval)

    fig = go.Figure()
    # Curvas principales (k=0.01)
    fig.add_trace(go.Scatter(x=sol1.t, y=sol1.y[0], name='Susceptibles (k=0.01)', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=sol1.t, y=sol1.y[1], name='Propagadores (k=0.01)', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=sol1.t, y=sol1.y[2], name='Racionales (k=0.01)', line=dict(color='green')))
    
    # Comparación (k=0.02) - Punteada
    fig.add_trace(go.Scatter(x=sol2.t, y=sol2.y[1], name='Propagadores (k=0.02)', line=dict(color='red', dash='dot')))

    fig.update_layout(
        title="Propagación del Rumor (Comparativa k)",
        xaxis_title="Días",
        yaxis_title="Alumnos",
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='white'
    )
    return fig

def grafica_caso3_politica():
    # Parámetros del Caso 3
    S0, I0, R0 = 10000, 50, 0
    b = 0.00005
    k = 0.00002
    t_max = 100

    def policy_model(t, y):
        S, I, R = y
        dSdt = -b * S * I
        dIdt = b * S * I - k * I
        dRdt = k * I
        return [dSdt, dIdt, dRdt]

    t_eval = np.linspace(0, t_max, 200)
    sol = solve_ivp(policy_model, [0, t_max], [S0, I0, R0], t_eval=t_eval)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sol.t, y=sol.y[0], name='Susceptibles', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=sol.t, y=sol.y[1], name='Influyentes', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=sol.t, y=sol.y[2], name='Rechazadores', line=dict(color='green')))
    
    fig.update_layout(
        title="Adopción de Política Pública",
        xaxis_title="Días",
        yaxis_title="Ciudadanos",
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='white'
    )
    return fig


# --- 3. Definición del Layout ---
layout = html.Div(className='content-container', children=[
    
    html.Div(className='card', style={'width': '100%'}, children=[
        
        html.H1("Aplicaciones y Generalización del Modelo SIR"),
        
        dcc.Markdown(r"""
            Como hemos visto en los modelos SIR y SEIR, el sistema básico de Ecuaciones
            Diferenciales puede modelar la propagación de una enfermedad.
            
            Sin embargo, el concepto de "contagio" es más general. El mismo modelo
            matemático puede usarse para describir cualquier proceso donde una "idea"
            o "estado" se transfiere por contacto en una población cerrada.
        """),
        
        html.Hr(),

        # --- Pestañas (Tabs) ---
        dcc.Tabs(id='tabs-sir-aplicaciones', value='tab-1', children=[
            
            # --- PESTAÑA 1: EPIDEMIA ---
            dcc.Tab(label='Caso 1: Epidemia', value='tab-1', children=[
                html.Div(className='tab-content', children=[
                    html.H3("Escenario: Brote de Enfermedad"),
                    dcc.Markdown(r"""
                        * **S (Susceptibles):** Estudiantes sanos.
                        * **I (Infectados):** Estudiantes enfermos que contagian.
                        * **R (Recuperados):** Estudiantes inmunes.
                    """),
                    
                    html.H4("Parámetros: N=7138, R0 ≈ 2.5"),
                    
                    # AQUÍ ESTÁ EL CAMBIO: dcc.Graph en lugar de html.Img
                    dcc.Graph(figure=grafica_caso1_epidemia()),
                    
                    dcc.Markdown(r"""
                        **Conclusión Clave:** Dado que $R_0 > 1$, la epidemia es inevitable.
                        El pico ocurre cuando los susceptibles bajan al umbral crítico $S_c \approx 2855$.
                    """, mathjax=True)
                ])
            ]),
            
            # --- PESTAÑA 2: RUMOR ---
            dcc.Tab(label='Caso 2: Rumor', value='tab-2', children=[
                html.Div(className='tab-content', children=[
                    html.H3("Escenario: Rumor en la Facultad"),
                    dcc.Markdown(r"""
                        * **S:** Alumnos que no han oído el rumor.
                        * **I (Propagadores):** Alumnos que creen y difunden.
                        * **R (Racionales):** Alumnos que no creen/olvidan.
                    """),

                    html.H4("Parámetros: N=275, b=0.004"),
                    dcc.Markdown("Comparamos $k=0.01$ (línea sólida) vs $k=0.02$ (línea punteada)."),

                    # AQUÍ ESTÁ EL CAMBIO: dcc.Graph en lugar de html.Img
                    dcc.Graph(figure=grafica_caso2_rumor()),

                    dcc.Markdown(r"""
                        **Conclusión Clave:** El modelo muestra cómo el factor social $k$ (escepticismo)
                        es crítico para "aplanar la curva" del rumor.
                    """, mathjax=True)
                ])
            ]),
            
            # --- PESTAÑA 3: POLÍTICA PÚBLICA ---
            dcc.Tab(label='Caso 3: Política', value='tab-3', children=[
                html.Div(className='tab-content', children=[
                    html.H3("Escenario: Adopción de Política"),
                    dcc.Markdown(r"""
                        * **S:** Ciudadanos que no han adoptado.
                        * **I (Influyentes):** Ciudadanos que promueven.
                        * **R (Rechazadores):** Ciudadanos que rechazan.
                    """),

                    html.H4("Parámetros: N=10,050, b=0.00005, k=0.00002"),

                    # AQUÍ ESTÁ EL CAMBIO: dcc.Graph en lugar de html.Img
                    dcc.Graph(figure=grafica_caso3_politica()),

                    dcc.Markdown(r"""
                        **Conclusión Clave:** El modelo simula procesos sociales lentos.
                        Permite estimar cómo campañas ($b$) o barreras ($k$) impactan la adopción.
                    """, mathjax=True)
                ])
            ]),
            
        ]) 
    ]) 
])