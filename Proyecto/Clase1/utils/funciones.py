import plotly.graph_objects as go
import numpy as np

def grafica_logistica(p0, r, k, t_max):

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