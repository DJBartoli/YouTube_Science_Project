import dash
import dash_bootstrap_components as dbc

from dash import dcc, html


app = dash.Dash(__name__, use_pages=True)

server = app.server

app.layout = html.Div(
    [
        # Header section
        html.Header([
            dbc.NavbarSimple(
                children=[
                    # Generating navigation links dynamically from the registered pages
                    dbc.NavItem(dbc.NavLink(page['name'], href=page['path']))
                    for page in dash.page_registry.values() if page['name'] != 'Imprint'
                ],
                brand="Visualizing YouTube",
                brand_href="/",
                color="#dd2b2b",
                dark=True,
                fixed='Top'
            )
        ]),
        html.Hr(),
        dash.page_container,

        # Footer section
        html.Footer([
            dbc.NavbarSimple(
                children=[
                    dbc.NavItem(dbc.NavLink('Imprint', href='/imprint')),
                ],
                color='#606060',
                dark=True,
                links_left=True,
            )

        ],
            style={'margin-top': '20px', 'height': '50px'}
        ),
    ]
)

# ------------------------------------------------------------------------------
# Starting the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
