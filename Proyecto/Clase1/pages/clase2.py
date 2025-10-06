import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np


dash.register_page(__name__, path='/capacidad-carga', name='Capacidad de Carga')


K = 2000  
P0 = 100  
r = 0.1   


t = np.linspace(0, 100, 50)
poblacion = K / (1 + ((K - P0) / P0) * np.exp(-r * t))




trace_poblacion = go.Scatter(
    x=t,
    y=poblacion,
    mode='lines+markers',
    name='Población',
    line=dict(color='#880e4f'), 
    marker=dict(color='#880e4f', size=8, symbol='circle') 
)


trace_capacidad = go.Scatter(
    x=[0, 100],
    y=[K, K],
    mode='lines',
    name='Capacidad de Carga (K)',
    line=dict(color='grey', dash='dash') 
)


fig = go.Figure(data=[trace_poblacion, trace_capacidad])


fig.update_layout(
    title=dict(
        text='<b>Crecimiento Logístico vs. Capacidad de Carga</b>',
        font=dict(color='#880e4f', size=20)
    ),
    title_x=0.5,
    xaxis_title='Tiempo (t)',
    yaxis_title='Población P(t)',
    height=450,
    legend=dict(x=0.02, y=0.98), 
    plot_bgcolor='white',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=True, gridcolor='lightgrey', zeroline=True, zerolinewidth=2, zerolinecolor='black'),
    yaxis=dict(showgrid=True, gridcolor='lightgrey', zeroline=True, zerolinewidth=2, zerolinecolor='black')
)



layout = html.Div(className='content-container', children=[
    
    
    html.Div(className='left-column card', children=[
        html.H2("Modelo de Crecimiento Logístico"),
        
        
        dcc.Markdown(r"""
            El modelo de crecimiento exponencial es útil, pero no es realista a largo plazo porque
            no considera las limitaciones de recursos (espacio, comida, etc.). El **modelo logístico**
            introduce el concepto de **capacidad de carga (K)**.

            La capacidad de carga *K* es el tamaño máximo de población que un entorno determinado
            puede sostener indefinidamente. A medida que la población *P(t)* se acerca a *K*,
            la tasa de crecimiento disminuye.

            La ecuación diferencial que describe este comportamiento es:

            $$
            \frac{dP}{dt} = rP \left(1 - \frac{P}{K}\right)
            $$

            La solución a esta ecuación nos da la curva logística, que tiene una forma característica
            de "S". En nuestra simulación, usamos *K = 2000*, *P₀ = 100* y *r = 0.1*.
        """, mathjax=True),
    ]),
    
    
    html.Div(className='right-column card', children=[
        html.H2("Gráfica"),
        dcc.Graph(figure=fig)
    ])
])
