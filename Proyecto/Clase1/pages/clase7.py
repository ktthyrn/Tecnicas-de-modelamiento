import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import solve_ivp # Usamos el mismo solucionador

# --- 1. Registro de la página ---
# El 'name' aparecerá en tu menú desplegable
dash.register_page(__name__, path='/modelo-seir', name='Modelo SEIR')

# --- 2. Definición del Layout ---
layout = html.Div(className='content-container', children=[
    
    # --- Columna Izquierda: Controles y Explicación ---
    html.Div(className='left-column card', children=[
        html.H2("Modelo SEIR - Con Incubación"),
        
        dcc.Markdown(r"""
El modelo SEIR añade un compartimento al SIR:
* **S:** Susceptibles
* **E:** Expuestos (contagiados, pero aún **no** infecciosos)
* **I:** Infectados (infecciosos)
* **R:** Recuperados

Este modelo es más realista para enfermedades con un período de incubación.

Las ecuaciones que lo describen son:
$$
\begin{aligned}
\frac{dS}{dt} &= - \frac{\beta S I}{N} \\
\frac{dE}{dt} &= \frac{\beta S I}{N} - \sigma E \\
\frac{dI}{dt} &= \sigma E - \gamma I \\
\frac{dR}{dt} &= \gamma I
\end{aligned}
$$
* **N:** Población total
* **$\beta$ (beta):** Tasa de transmisión
* **$\gamma$ (gamma):** Tasa de recuperación
* **$\sigma$ (sigma):** Tasa de incubación (1 / días de incubación)
""", mathjax=True),
        
        html.Hr(),

        html.Label("Población Total (N):", className='input-label'),
        dcc.Input(id='input-N-seir', type='number', value=1000, className='input-field'),

        html.Label("Tasa de transmisión (β):", className='input-label'),
        dcc.Input(id='input-beta-seir', type='number', value=0.5, step=0.01, className='input-field'),

        html.Label("Tasa de recuperación (γ):", className='input-label'),
        dcc.Input(id='input-gamma-seir', type='number', value=0.1, step=0.01, className='input-field'),
        
        html.Label("Tasa de incubación (σ):", className='input-label'),
        dcc.Input(id='input-sigma-seir', type='number', value=0.2, step=0.01, className='input-field'),
        
        html.Label("Infectados iniciales (I₀):", className='input-label'),
        dcc.Input(id='input-I0-seir', type='number', value=1, className='input-field'),
        
        html.Label("Expuestos iniciales (E₀):", className='input-label'),
        dcc.Input(id='input-E0-seir', type='number', value=0, className='input-field'),

        html.Label("Tiempo de simulación (días):", className='input-label'),
        dcc.Input(id='input-tiempo-seir', type='number', value=100, className='input-field'),

        html.Button('Simular Epidemia SEIR', id='btn-simular-seir', n_clicks=0, className='btn-generar')
    ]),
    
    # --- Columna Derecha: Gráfica ---
    html.Div(className='right-column card', children=[
        html.H2("Evolución de la Epidemia (SEIR)"),
        dcc.Graph(id='graph-seir-evolucion')
    ])
])

# --- 3. Función para crear el gráfico base (vacío o con datos) ---
def crear_figura_seir(t=None, S=None, E=None, I=None, R=None, t_max=100):
    fig = go.Figure()

    if t is not None:
        # Si hay datos, dibujamos las curvas
        fig.add_trace(go.Scatter(
            x=t, y=S, mode='lines', name='Susceptibles (S)', line=dict(color='blue')
        ))
        fig.add_trace(go.Scatter(
            x=t, y=E, mode='lines', name='Expuestos (E)', line=dict(color='orange')
        ))
        fig.add_trace(go.Scatter(
            x=t, y=I, mode='lines', name='Infectados (I)', line=dict(color='red')
        ))
        fig.add_trace(go.Scatter(
            x=t, y=R, mode='lines', name='Recuperados (R)', line=dict(color='green')
        ))
    
    # Damos estilo a la figura (con datos o vacía)
    fig.update_layout(
        title=dict(text='<b>Evolución del Modelo SEIR</b>', font=dict(color='#880e4f', size=16)),
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
    Output('graph-seir-evolucion', 'figure'),
    Input('btn-simular-seir', 'n_clicks'),
    State('input-N-seir', 'value'),
    State('input-beta-seir', 'value'),
    State('input-gamma-seir', 'value'),
    State('input-sigma-seir', 'value'),
    State('input-I0-seir', 'value'),
    State('input-E0-seir', 'value'),
    State('input-tiempo-seir', 'value')
)
def update_seir_graph(n_clicks, N, beta, gamma, sigma, I0, E0, t_max):
    
    # Si el botón no se ha presionado, muestra el gráfico vacío
    if n_clicks == 0:
        return crear_figura_seir(t_max=t_max) # Devuelve gráfico base con ejes

    # --- A. Sanatizar Inputs ---
    try:
        N = int(N)
        I0 = int(I0)
        E0 = int(E0)
        beta = float(beta)
        gamma = float(gamma)
        sigma = float(sigma)
        t_max = int(t_max)
    except (ValueError, TypeError):
        return crear_figura_seir(t_max=t_max) # Error en inputs, devuelve vacío

    # --- B. Condiciones Iniciales ---
    R0 = 0
    S0 = N - I0 - E0 - R0 # S0 se calcula con los 3 restantes
    y0 = [S0, E0, I0, R0] # Vector de condiciones iniciales (¡4 elementos!)

    # --- C. Definir el sistema de Ecuaciones (las 4 ecuaciones) ---
    def seir_model(t, y):
        S, E, I, R = y
        dSdt = - (beta * S * I) / N
        dEdt = (beta * S * I) / N - sigma * E
        dIdt = sigma * E - gamma * I
        dRdt = gamma * I
        return [dSdt, dEdt, dIdt, dRdt]

    # --- D. Resolver el sistema ---
    t_span = [0, t_max]
    t_eval = np.linspace(0, t_max, 500) 
    
    sol = solve_ivp(
        seir_model, 
        t_span, 
        y0, 
        t_eval=t_eval, 
        method='RK45'
    )

    # --- E. Extraer resultados ---
    t = sol.t
    S = sol.y[0]
    E = sol.y[1]
    I = sol.y[2]
    R = sol.y[3]

    # --- F. Devolver la figura con los datos ---
    return crear_figura_seir(t, S, E, I, R, t_max)