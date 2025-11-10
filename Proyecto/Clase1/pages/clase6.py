import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import solve_ivp # ¡Importante!

# --- 1. Registro de la página ---
# El 'name' aparecerá en tu menú desplegable
dash.register_page(__name__, path='/modelo-sir', name='Modelo SIR')

# --- 2. Definición del Layout ---
layout = html.Div(className='content-container', children=[
    
    # --- Columna Izquierda: Controles y Explicación ---
    html.Div(className='left-column card', children=[
        html.H2("Modelo SIR - Epidemiología"),
        
        dcc.Markdown(r"""
            El modelo SIR es uno de los modelos epidemiológicos más simples.
            Divide a la población en tres compartimentos:
            * **S:** Susceptibles (pueden contagiarse)
            * **I:** Infectados (están enfermos y contagian)
            * **R:** Recuperados (son inmunes o han fallecido)
            
           
            * **N:** Población total
            * **$\beta$ (beta):** Tasa de transmisión
            * **$\gamma$ (gamma):** Tasa de recuperación
        """, mathjax=True),
        
        html.Hr(),

        html.Label("Población Total (N):", className='input-label'),
        dcc.Input(id='input-N', type='number', value=1000, className='input-field'),

        html.Label("Tasa de transmisión (β):", className='input-label'),
        dcc.Input(id='input-beta', type='number', value=0.3, step=0.01, className='input-field'),

        html.Label("Tasa de recuperación (γ):", className='input-label'),
        dcc.Input(id='input-gamma', type='number', value=0.1, step=0.01, className='input-field'),

        html.Label("Infectados iniciales (I₀):", className='input-label'),
        dcc.Input(id='input-I0', type='number', value=1, className='input-field'),
        
        html.Label("Tiempo de simulación (días):", className='input-label'),
        dcc.Input(id='input-tiempo', type='number', value=100, className='input-field'),

        html.Button('Simular Epidemia', id='btn-simular-sir', n_clicks=0, className='btn-generar')
    ]),
    
    # --- Columna Derecha: Gráfica ---
    html.Div(className='right-column card', children=[
        html.H2("Evolución de la Epidemia"),
        dcc.Graph(id='graph-sir-evolucion')
    ])
])

# --- 3. Función para crear el gráfico base (vacío o con datos) ---
def crear_figura_sir(t=None, S=None, I=None, R=None, t_max=100):
    fig = go.Figure()

    if t is not None:
        # Si hay datos, dibujamos las curvas
        fig.add_trace(go.Scatter(
            x=t, y=S, mode='lines', name='Susceptibles (S)', line=dict(color='blue')
        ))
        fig.add_trace(go.Scatter(
            x=t, y=I, mode='lines', name='Infectados (I)', line=dict(color='red')
        ))
        fig.add_trace(go.Scatter(
            x=t, y=R, mode='lines', name='Recuperados (R)', line=dict(color='green')
        ))
    
    # Damos estilo a la figura (con datos o vacía)
    fig.update_layout(
        title=dict(text='<b>Evolución del Modelo SIR</b>', font=dict(color='#880e4f', size=16)),
        title_x=0.5,
        xaxis_title='Tiempo (días)',
        yaxis_title='Número de personas',
        height=450,
        legend=dict(x=0.02, y=0.98),
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=True, gridcolor='lightgrey', zeroline=True, 
            zerolinewidth=2, zerolinecolor='black', range=[0, t_max]
        ),
        yaxis=dict(
            showgrid=True, gridcolor='lightgrey', zeroline=True, 
            zerolinewidth=2, zerolinecolor='black'
        )
    )
    return fig

# --- 4. Callback para actualizar el gráfico ---
@callback(
    Output('graph-sir-evolucion', 'figure'),
    Input('btn-simular-sir', 'n_clicks'),
    State('input-N', 'value'),
    State('input-beta', 'value'),
    State('input-gamma', 'value'),
    State('input-I0', 'value'),
    State('input-tiempo', 'value')
)
def update_sir_graph(n_clicks, N, beta, gamma, I0, t_max):
    
    # Si el botón no se ha presionado, muestra el gráfico vacío
    if n_clicks == 0:
        return crear_figura_sir(t_max=t_max) # Devuelve gráfico base con ejes

    # --- A. Sanatizar Inputs ---
    try:
        N = int(N)
        I0 = int(I0)
        beta = float(beta)
        gamma = float(gamma)
        t_max = int(t_max)
    except (ValueError, TypeError):
        return crear_figura_sir(t_max=t_max) # Error en inputs, devuelve vacío

    # --- B. Condiciones Iniciales ---
    R0 = 0
    S0 = N - I0 - R0
    y0 = [S0, I0, R0] # Vector de condiciones iniciales

    # --- C. Definir el sistema de Ecuaciones (las 3 ecuaciones) ---
    def sir_model(t, y):
        S, I, R = y
        dSdt = - (beta * S * I) / N
        dIdt = (beta * S * I) / N - gamma * I
        dRdt = gamma * I
        return [dSdt, dIdt, dRdt]

    # --- D. Resolver el sistema ---
    t_span = [0, t_max]
    # t_eval son los puntos en el tiempo donde queremos la solución
    t_eval = np.linspace(0, t_max, 500) 
    
    sol = solve_ivp(
        sir_model, 
        t_span, 
        y0, 
        t_eval=t_eval, 
        method='RK45' # Un método de resolución estándar
    )

    # --- E. Extraer resultados ---
    t = sol.t
    S = sol.y[0]
    I = sol.y[1]
    R = sol.y[2]

    # --- F. Devolver la figura con los datos ---
    return crear_figura_sir(t, S, I, R, t_max)