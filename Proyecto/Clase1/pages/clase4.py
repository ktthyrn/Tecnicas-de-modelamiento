#REFACTORIZAMOS LLAMANDO LA FUNCION DEL ARCHIVO FUNCIONES.PY

import dash
from dash import html, dcc, callback, Input, Output, State

from utils.funciones import grafica_logistica

dash.register_page(__name__, path='/modelo-llamado', name='Modelo con llamado')

layout = html.Div(className='content-container', children=[
    
    html.Div(className='left-column card', children=[
        html.H2("Parámetros del modelo (Refactorizado)"),
        html.Label("Población inicial P(0):", className='input-label'),
        dcc.Input(id='input-p0-ref', type='number', value=200, className='input-field'),
        html.Label("Tasa de crecimiento (r):", className='input-label'),
        dcc.Input(id='input-r-ref', type='number', value=0.04, className='input-field'),
        html.Label("Capacidad de carga (K):", className='input-label'),
        dcc.Input(id='input-k-ref', type='number', value=750, className='input-field'),
        html.Label("Tiempo máximo (t):", className='input-label'),
        dcc.Input(id='input-t-ref', type='number', value=100, className='input-field'),
        html.Button('Generar gráfica', id='btn-generar-ref', n_clicks=0, className='btn-generar')
    ]),
    
    html.Div(className='right-column card', children=[
        html.H2("Gráfica"),
        dcc.Graph(id='graph-logistico-refactorizado')
    ])
])


@callback(
    Output('graph-logistico-refactorizado', 'figure'),
    Input('btn-generar-ref', 'n_clicks'),
    State('input-p0-ref', 'value'),
    State('input-r-ref', 'value'),
    State('input-k-ref', 'value'),
    State('input-t-ref', 'value')
)
def update_graph_refactorizado(n_clicks, p0, r, k, t_max):
    # ¡Mira qué limpio!
    # Simplemente llamamos a nuestra función importada y le pasamos los parámetros.
    fig = grafica_logistica(p0, r, k, t_max)
    return fig
