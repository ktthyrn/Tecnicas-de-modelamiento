import sys
sys.path.append('.') 

import dash
from dash import html, dcc

mathjax_script = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"

app = dash.Dash(__name__, use_pages=True, external_scripts=[mathjax_script])
server = app.server 

app.layout = html.Div([
    html.Header([
        html.H1("Técnicas de Modelamiento Matemático"),

        # --- BARRA DE NAVEGACIÓN MODIFICADA CON DROPDOWN ---
        html.Nav([
            
            # 1. Link de Inicio (queda separado y visible)
            dcc.Link(
                "Inicio",
                # Busca la página 'inicio' registrada
                href=dash.page_registry['pages.inicio']['relative_path'], 
                className='nav-link'
            ),
            
            # 2. Contenedor del Dropdown "Modelos"
            html.Div([
                
                # El "botón" visible (es un link falso)
                html.A(
                    "Modelos ▼", # El texto del botón con una flechita
                    href="#", # href="#" evita que la página recargue
                    className='nav-link dropdown-btn' # Clases para estilo
                ),
                
                # El contenido que se despliega
                html.Div([
                    # Iteramos y creamos un link para cada página
                    # PERO saltamos la página de 'inicio'
                    dcc.Link(
                        f"{page['name']}",
                        href=page["relative_path"],
                        className='dropdown-link' # Nueva clase para links internos
                    ) for page in dash.page_registry.values() if page['module'] != 'pages.inicio'
                
                ], className='dropdown-content') # Contenedor de links
                
            ], className='dropdown-container') # Contenedor principal del dropdown

        ]) # Fin de html.Nav
        # --- FIN BARRA DE NAVEGACIÓN ---

    ], className='app-header'),

    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)