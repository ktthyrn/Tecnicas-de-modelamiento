import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import numpy as np
import sys # Para manejar errores

# --- 1. Registro de la página ---
dash.register_page(__name__, path='/campo-vectorial', name='Campo Vectorial')

# --- 2. Definición del Layout ---
layout = html.Div(className='content-container', children=[
    
    # --- Columna Izquierda: Controles ---
    html.Div(className='left-column card', children=[
        html.H2("Campo Vectorial 2D"),
        
        html.Label("Ecuación dx/dt = f(x, y):", className='input-label'),
        dcc.Input(
            id='input-dxdt',
            type='text',
            value='-y',  
            className='input-field'
        ),
        
        html.Label("Ecuación dy/dt = g(x, y):", className='input-label'),
        dcc.Input(
            id='input-dydt',
            type='text',
            value='x',   
            className='input-field'
        ),
        
        html.Label("Rango del Eje X (±):", className='input-label'),
        dcc.Input(
            id='input-range-x',
            type='number',
            value=3,
            className='input-field'
        ),
        
        html.Label("Rango del Eje Y (±):", className='input-label'),
        dcc.Input(
            id='input-range-y',
            type='number',
            value=3,
            className='input-field'
        ),
        
        html.Label("Mallado (N x N):", className='input-label'),
        dcc.Input(
            id='input-mallado',
            type='number',
            value=20,  
            className='input-field'
        ),
        
        html.Button('Generar campo', id='btn-generar-campo', n_clicks=0, className='btn-generar'),
        
        html.Hr(style={'marginTop': '20px'}),
        
        html.H3("Ejemplos para probar:"),
        dcc.Markdown(
            """
            * **Flujo circular:** `dx/dt = -y`, `dy/dt = x`
            * **Punto de silla:** `dx/dt = x`, `dy/dt = -y`
            * **Flujo logístico:** `dx/dt = x*(1-x)`, `dy/dt = y` 
            * **Tu ejemplo:** `dx/dt = np.sin(x)`, `dy/dt = np.cos(y)`
            * **Lotka-Volterra (α=1, β=0.1, δ=0.1, γ=1):**
                * `dx/dt = 1*x - 0.1*x*y`
                * `dy/dt = 0.1*x*y - 1*y`
                * `(Usar rangos X=[0, 50], Y=[0, 50] aprox.)`
            """
        )
    ]),
    
    # --- Columna Derecha: Visualización ---
    html.Div(className='right-column card', children=[
        html.H2("Visualización del Campo Vectorial"),
        
        # Contenedor para mensajes de error
        html.Div(id='error-output-campo', style={
            'color': 'red', 
            'fontWeight': 'bold',
            'marginBottom': '10px'
        }),
        
        dcc.Graph(id='graph-campo-vectorial')
    ])
])

# --- 3. Callback para actualizar el gráfico ---

@callback(
    Output('graph-campo-vectorial', 'figure'),
    Output('error-output-campo', 'children'),
    Input('btn-generar-campo', 'n_clicks'),
    State('input-dxdt', 'value'),
    State('input-dydt', 'value'),
    State('input-range-x', 'value'),
    State('input-range-y', 'value'),
    State('input-mallado', 'value')
)
def update_vector_field(n_clicks, eq_dxdt, eq_dydt, range_x, range_y, mallado):
    
    # --- Figura base (vacía pero con estilo) ---
    fig = go.Figure()
    fig.update_layout(
        title='Introduce las ecuaciones y presiona "Generar"',
        title_x=0.5,
        xaxis_title='Eje X',
        yaxis_title='Eje Y',
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='lightgrey', zeroline=True, zerolinewidth=2, zerolinecolor='red'),
        yaxis=dict(showgrid=True, gridcolor='lightgrey', zeroline=True, zerolinewidth=2, zerolinecolor='red'),
        # Asegura que los ejes tengan la misma escala (aspect ratio 1:1)
        yaxis_scaleanchor="x",
        yaxis_scaleratio=1,
        showlegend=False
    )
    
    if n_clicks == 0:
        return fig, "" # Retorna la figura vacía si no se ha hecho clic

    try:
        # --- A. Crear el mallado (Grid) ---
        # Aseguramos que los valores sean numéricos
        range_x, range_y, mallado = float(range_x), float(range_y), int(mallado)
        
        x_vals = np.linspace(-range_x, range_x, mallado)
        y_vals = np.linspace(-range_y, range_y, mallado)
        x, y = np.meshgrid(x_vals, y_vals)
        
        # --- B. Evaluar las ecuaciones (¡Peligroso! Ver nota abajo) ---
        # Creamos un diccionario seguro para las funciones permitidas
        safe_dict = {
            'np': np,
            'x': x,
            'y': y,
            'cos': np.cos,
            'sin': np.sin,
            'exp': np.exp,
            'sqrt': np.sqrt,
            'log': np.log
        }
        
        # AVISO: eval() es un riesgo de seguridad si la app es pública.
        # Para un proyecto de clase controlado, es aceptable.
        u = eval(eq_dxdt, {"__builtins__": {}}, safe_dict)
        v = eval(eq_dydt, {"__builtins__": {}}, safe_dict)
        
        # --- C. Normalizar los vectores ---
        # (Para que todos tengan la misma longitud y solo muestren dirección)
        magnitud = np.sqrt(u**2 + v**2) + 1e-9 # +1e-9 para evitar división por cero
        u_norm = u / magnitud
        v_norm = v / magnitud
        
        # --- D. Calcular puntos de inicio y fin (como en tu imagen) ---
        # Hacemos que la longitud de la línea sea proporcional al tamaño de la celda
        line_length = (range_x * 2 / mallado) * 0.4
        
        x_end = x + u_norm * line_length
        y_end = y + v_norm * line_length
        
        # --- E. Preparar datos para Plotly ---
        # (Usamos 'None' para separar cada segmento de línea)
        plot_x_lines = []
        plot_y_lines = []
        
        for i in range(mallado):
            for j in range(mallado):
                plot_x_lines.extend([x[i, j], x_end[i, j], None])
                plot_y_lines.extend([y[i, j], y_end[i, j], None])

        # --- F. Crear las trazas (Traces) ---
        # 1. Las líneas del vector
        trace_lines = go.Scatter(
            x=plot_x_lines, 
            y=plot_y_lines, 
            mode='lines',
            name='Vectores',
            line=dict(color='#0000FF', width=1.5) # Líneas azules
        )
        
        # 2. Los puntos de inicio (rojos)
        trace_start = go.Scatter(
            x=x.flatten(), 
            y=y.flatten(),
            mode='markers', 
            name='Punto Inicial',
            marker=dict(color='#FF0000', size=3) # Puntos rojos
        )
        
        # 3. Los puntos de fin (azules)
        trace_end = go.Scatter(
            x=x_end.flatten(), 
            y=y_end.flatten(),
            mode='markers', 
            name='Dirección',
            marker=dict(color='#0000FF', size=3) # Puntos azules
        )
        
        # --- G. Ensamblar la figura ---
        fig = go.Figure(data=[trace_lines, trace_start, trace_end])
        
        # Actualizamos el layout con el estilo y el título dinámico
        fig.update_layout(
            title=f"Campo Vectorial: dx/dt = {eq_dxdt}  |  dy/dt = {eq_dydt}",
            title_x=0.5,
            xaxis_title='Eje X',
            yaxis_title='Eje Y',
            plot_bgcolor='white',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='lightgrey', zeroline=True, zerolinewidth=2, zerolinecolor='red', range=[-range_x*1.05, range_x*1.05]),
            yaxis=dict(showgrid=True, gridcolor='lightgrey', zeroline=True, zerolinewidth=2, zerolinecolor='red', range=[-range_y*1.05, range_y*1.05]),
            yaxis_scaleanchor="x",
            yaxis_scaleratio=1,
            showlegend=False,
            margin=dict(l=40, r=20, t=60, b=40)
        )
        
        return fig, "" # Retorna la figura y ningún error

    except Exception as e:
        # --- H. Manejo de Errores ---
        print(f"Error en callback: {e}", file=sys.stderr)
        error_msg = f"Error al generar el gráfico: {e}. Revisa tus ecuaciones."
        return fig, error_msg # Retorna la fig vacía y el mensaje de error