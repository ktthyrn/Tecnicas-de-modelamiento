import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np


dash.register_page(__name__, path='/clase-1', name='Crecimiento Poblacional')


P0 = 100
r = 0.03
t = np.linspace(0, 100, 11)
poblacion = P0 * np.exp(r * t)


trace = go.Scatter(
    x=t,
    y=poblacion,
    mode='lines+markers',
    name='Población',
    line=dict(color='#880e4f', dash='dot'),
    marker=dict(color='#880e4f', size=8, symbol='square')
)

fig = go.Figure(data=[trace])


fig.update_layout(
    title=dict(
        text='<b>Crecimiento de la población</b>',
        font=dict(color='#880e4f', size=20)
    ),
    title_x=0.5,
    xaxis_title='Tiempo (t)',
    yaxis_title='Población P(t)',
    height=450,
    margin=dict(l=40, r=20, t=60, b=40),
    plot_bgcolor='white',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(
        family="Exo 2, sans-serif",
        size=14,
        color="#333"
    ),
    
    xaxis=dict(
        showgrid=True, 
        gridcolor='lightgrey',
        zeroline=True, 
        zerolinewidth=2,
        zerolinecolor='black'
    ),
    yaxis=dict(
        showgrid=True, 
        gridcolor='lightgrey',
        zeroline=True, 
        zerolinewidth=2,
        zerolinecolor='black'
    )
)

layout = html.Div(className='content-container', children=[
    
   
    html.Div(className='left-column card', children=[
        html.H2("Crecimiento de la población"),
        
        dcc.Markdown(r"""
            Para modelar el crecimiento de la población mediante una ecuación diferencial, primero 
            tenemos que introducir algunas variables y términos relevantes. La variable *t*, representará 
            el tiempo. Las unidades de tiempo pueden ser horas, días, semanas, meses o incluso años.

            La variable *P* representará a la población. Como la población varía con el 
            tiempo, se entiende que es una función del tiempo. Por lo tanto, utilizamos la notación *P(t)*. 
            Si *P(t)* es una función diferenciable, entonces la primera derivada $\frac{dP}{dt}$ 
            representa la tasa instantánea de cambio de la población en función del tiempo.

            Un ejemplo de función de crecimiento exponencial es $P(t) = P_0 e^{rt}$. En esta función, *P(t)* representa la población en el momento *t*, $P_0$ representa la población inicial (población en el 
            tiempo *t* = 0), y la constante *r > 0* se denomina tasa de crecimiento. Aquí $P_0 = 100$ y *r = 0.03*.
        """, mathjax=True),
    ]),
    
    
    html.Div(className='right-column card', children=[
        html.H2("Gráfica"),
        dcc.Graph(figure=fig, config={'displayModeBar': True})
    ])
])

