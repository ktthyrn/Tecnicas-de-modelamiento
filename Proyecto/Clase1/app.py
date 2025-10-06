import dash
from dash import html, dcc


mathjax_script = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"

app = dash.Dash(__name__, use_pages=True, external_scripts=[mathjax_script])


app.layout = html.Div([
    
    html.Header([
        
        html.H1("Técnicas de Modelamiento Matemático"),
        
        
        html.Nav([
            
            dcc.Link(
                f"{page['name']}", 
                href=page["relative_path"],
                
                className='nav-link'
            ) for page in dash.page_registry.values()
        ])
    
    ], className='app-header'),

    
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)