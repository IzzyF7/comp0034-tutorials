# Imports for Dash and Dash.html
from dash import Dash, html
import dash_bootstrap_components as dbc

# Variable that defines the meta tag for the viewport
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]

# Variable that contains the external_stylesheet to use, in this case Bootstrap styling from dash bootstrap components (dbc)
external_stylesheets = [dbc.themes.PULSE]

# Create an instance of the Dash app
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags)

# Add an HTML layout to the Dash app
app.layout = dbc.Container([
    # Layout goes here
    dbc.Row([
        html.H1("Paralympics Data Analytics"),
        html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent congue luctus elit nec gravida.")
    ]),
    dbc.Select(
        options=[
            {"label": "Events", "value": "events"},  # The value is in the format of the column heading in the data
            {"label": "Sports", "value": "sports"},
            {"label": "Countries", "value": "countries"},
            {"label": "Athletes", "value": "participants"},
        ],
        value="events",  # The default selection
        id="dropdown-input",  # id uniquely identifies the element, will be needed later for callbacks
    ),
    html.Div(
        [
            dbc.Label("Select the Paralympic Games type"),
            dbc.Checklist(
                options=[
                    {"label": "Summer", "value": "summer"},
                    {"label": "Winter", "value": "winter"},
                ],
                value=["summer"],  # Values is a list as you can select 1 AND 2
                id="checklist-input",
            ),
        ]
    ),

    html.Div(
        [
    # Column 1 children
    # className="img-fluid" is a Bootstrap class and prevents the image spanning the next column
    html.Img(src=app.get_asset_url('line-chart-placeholder.png'), className="img-fluid"),

    # Column 2 children
    html.Img(src=app.get_asset_url('bar-chart-placeholder.png'), className="img-fluid"),
        ]
    ),

    # Column 2 children
    dbc.Card([
        dbc.CardImg(src=app.get_asset_url("logos/2022_Beijing.jpg"), top=True),
        dbc.CardBody([
            html.H4("Beijing 2022", className="card-title"),
            html.P("Number of athletes: XX", className="card-text"),
            html.P("Number of events: XX", className="card-text"),
            html.P("Number of countries: XX", className="card-text"),
            html.P("Number of sports: XX", className="card-text"),
        ]),
    ],
        style={"width": "18rem"},
    )
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)