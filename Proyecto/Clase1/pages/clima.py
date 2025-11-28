import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import requests
import pandas as pd
from datetime import datetime

# --- 1. Registro de la página ---
dash.register_page(__name__, path='/clima-peru', name='Clima en Perú (API)')

# --- 2. Datos de las Ciudades (Coordenadas para la API) ---
ciudades = {
    "Lima": {"lat": -12.0464, "lon": -77.0428, "color": "red"},
    "Cusco": {"lat": -13.5320, "lon": -71.9675, "color": "orange"},
    "Arequipa": {"lat": -16.4090, "lon": -71.5375, "color": "blue"},
    "Iquitos": {"lat": -3.7437, "lon": -73.2516, "color": "green"},
    "Piura": {"lat": -5.1945, "lon": -80.6328, "color": "yellow"},
    "Puno": {"lat": -15.8402, "lon": -70.0219, "color": "purple"},
    "Trujillo": {"lat": -8.1160, "lon": -79.0300, "color": "cyan"},
    "Huancayo": {"lat": -12.0651, "lon": -75.2049, "color": "brown"}
}

# --- 3. Layout (Interfaz Gráfica) ---
layout = html.Div(className='content-container', children=[
    
    # --- Columna Izquierda: Mapa ---
    html.Div(className='left-column card', children=[
        html.H2("Mapa de Estaciones"),
        dcc.Markdown("Haz clic en una ciudad para consultar la API de Open-Meteo en tiempo real."),
        
        dcc.Graph(
            id='mapa-peru',
            figure=go.Figure(
                data=[
                    # Creamos los puntos en el mapa
                    go.Scattermapbox(
                        lat=[datos["lat"] for datos in ciudades.values()],
                        lon=[datos["lon"] for datos in ciudades.values()],
                        mode='markers+text',
                        marker=go.scattermapbox.Marker(size=14, color='red'),
                        text=list(ciudades.keys()), # Nombres de las ciudades
                        textposition="top right",
                        hoverinfo='text'
                    )
                ],
                layout=go.Layout(
                    mapbox_style="open-street-map", # Estilo de mapa gratuito
                    mapbox=dict(
                        center=dict(lat=-9.19, lon=-75.015), # Centro de Perú
                        zoom=4
                    ),
                    margin={"r":0,"t":0,"l":0,"b":0},
                    height=450
                )
            )
        )
    ]),
    
    # --- Columna Derecha: Pronóstico (Resultado de la API) ---
    html.Div(className='right-column card', children=[
        html.H2("Pronóstico Horario (24h)"),
        dcc.Loading( # Muestra un circulito de carga mientras llama a la API
            id="loading-clima",
            type="circle",
            children=[
                dcc.Graph(id='grafica-clima'),
                html.Div(id='info-extra', style={'marginTop': '20px'})
            ]
        )
    ])
])

# --- 4. Callback: El puente entre el Mapa y la API ---
@callback(
    [Output('grafica-clima', 'figure'),
     Output('info-extra', 'children')],
    Input('mapa-peru', 'clickData')
)
def actualizar_clima(clickData):
    
    # A. Determinar qué ciudad se seleccionó (Por defecto Lima)
    ciudad_seleccionada = "Lima"
    if clickData:
        ciudad_seleccionada = clickData['points'][0]['text']
    
    coords = ciudades[ciudad_seleccionada]
    lat, lon = coords['lat'], coords['lon']
    
    # B. ¡LLAMADA A LA API! (Aquí ocurre la magia)
    # Usamos la API de Open-Meteo
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m&timezone=auto&forecast_days=1"
    
    try:
        response = requests.get(url) # Hacemos la petición GET
        data = response.json() # Convertimos la respuesta a JSON
        
        # C. Procesar los datos (Extraer horas y temperaturas)
        hourly_data = data['hourly']
        tiempos = hourly_data['time']
        temperaturas = hourly_data['temperature_2m']
        humedad = hourly_data['relative_humidity_2m']
        
        # Convertir las fechas feas "2023-11-10T00:00" a objetos datetime
        fechas_formateadas = [datetime.fromisoformat(t) for t in tiempos]
        
        # D. Crear la Gráfica
        fig = go.Figure()
        
        # Línea de Temperatura
        fig.add_trace(go.Scatter(
            x=fechas_formateadas, 
            y=temperaturas,
            mode='lines+markers',
            name='Temperatura (°C)',
            line=dict(color='#ff7f50', width=3)
        ))
        
        # Línea de Humedad (Opcional, para que se vea más pro)
        fig.add_trace(go.Scatter(
            x=fechas_formateadas, 
            y=humedad,
            mode='lines',
            name='Humedad (%)',
            line=dict(color='#87ceeb', dash='dot'),
            yaxis='y2' # Eje Y secundario
        ))

        fig.update_layout(
            title=f"Clima en {ciudad_seleccionada} (Hoy)",
            xaxis_title="Hora",
            yaxis_title="Temperatura (°C)",
            yaxis2=dict(
                title="Humedad (%)",
                overlaying='y',
                side='right'
            ),
            hovermode="x unified",
            legend=dict(x=0, y=1.1, orientation='h'),
            plot_bgcolor='white',
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        # Info extra
        temp_actual = temperaturas[datetime.now().hour]
        mensaje = dcc.Markdown(f"""
            **Resumen para {ciudad_seleccionada}:**
            * Temperatura estimada actual: **{temp_actual}°C**
            * Fuente de datos: [Open-Meteo API](https://open-meteo.com/)
        """)
        
        return fig, mensaje

    except Exception as e:
        # Si la API falla (sin internet, etc.)
        fig_error = go.Figure()
        fig_error.update_layout(title=f"Error al conectar con la API: {str(e)}")
        return fig_error, "Error de conexión"