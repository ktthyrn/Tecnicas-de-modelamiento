import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__, path='/modelo-interactivo', name='Modelo Interactivo')

layout = html.Div(className='content-container', children=[
    
    html.Div(className='left-column card', children=[
        html.H2("Parámetros del modelo"),

        html.Label("Población inicial P(0):", className='input-label'),
        dcc.Input(
            id='input-p0',
            type='number',
            value=200, 
            className='input-field'
        ),

        
        html.Label("Tasa de crecimiento (r):", className='input-label'),
        dcc.Input(
            id='input-r',
            type='number',
            value=0.04,
            className='input-field'
        ),

        
        html.Label("Capacidad de carga (K):", className='input-label'),
        dcc.Input(
            id='input-k',
            type='number',
            value=750,
            className='input-field'
        ),
        
        
        html.Label("Tiempo máximo (t):", className='input-label'),
        dcc.Input(
            id='input-t',
            type='number',
            value=100,
            className='input-field'
        ),

        
        html.Button('Generar gráfica', id='btn-generar', n_clicks=0, className='btn-generar')
    ]),
    
    
    html.Div(className='right-column card', children=[
        html.H2("Gráfica"),
        
        dcc.Graph(id='graph-logistico-interactivo')
    ])
])



@callback(
    
    Output('graph-logistico-interactivo', 'figure'),
    
    Input('btn-generar', 'n_clicks'),
    State('input-p0', 'value'),
    State('input-r', 'value'),
    State('input-k', 'value'),
    State('input-t', 'value')
)
def update_graph(n_clicks, p0, r, k, t_max):
    
    t = np.linspace(0, t_max, 100)
    poblacion = k / (1 + ((k - p0) / p0) * np.exp(-r * t))
    

    trace_poblacion = go.Scatter(x=t, y=poblacion, mode='lines', name='Población', line=dict(color='#880e4f'))
    trace_capacidad = go.Scatter(x=[0, t_max], y=[k, k], mode='lines', name='Capacidad de Carga (K)', line=dict(color='grey', dash='dash'))


    fig = go.Figure(data=[trace_poblacion, trace_capacidad])
    

    fig.update_layout(
        title=dict(text='<b>Modelo Logístico de Crecimiento Poblacional</b>', font=dict(color='#880e4f', size=16)),
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
    

    return fig
