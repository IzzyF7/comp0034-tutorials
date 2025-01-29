# Imports for Dash and Dash.html
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from student.dash_single.figures import line_chart
from student.dash_single.figures import bar_gender
from student.dash_single.figures import scatter_geo
from student.dash_single.figures import para_card
from student.dash_single.figures import country_hist
from dash import Input, Output

# Variable that defines the meta tag for the viewport
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]

# Variable that contains the external_stylesheet to use, in this case Bootstrap styling from dash bootstrap components (dbc)
external_stylesheets = [dbc.themes.PULSE]

line_fig = line_chart("sports")
bar_fig = bar_gender("Summer")
map = scatter_geo()
histogram = country_hist()


# Create an instance of the Dash app
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags)
card = para_card("Tokyo 2020", app)

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
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='line-chart', figure=line_fig),
            width=6
        ),
        dbc.Col(
            dcc.Graph(id='map', figure=map),
            width=12
        ), 
        dbc.Col(
            dcc.Graph(id='histogram', figure=histogram),
            width=12
        )
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='bar_chart', figure=bar_fig),
            width=6
        )
    ]),
    dbc.Col(children=[card], id='card', width=4),
])


@app.callback(
    Output('line-chart', 'figure'),  # The component being updated is the line-chart with id="line-chart"
    Output('bar_chart', 'figure'),  # The component being updated is the bar_chart with id="bar_chart"
    Input('dropdown-input', 'value'),  # The input is the dropdown with id="dropdown-input"
    Input('checklist-input', 'value')  # The input is the checklist with id="checklist-input"
)
def update_charts(dropdown_value, checklist_value):
    # Update line chart based on dropdown value
    if dropdown_value == "events":
        line_fig = line_chart("events")
    elif dropdown_value == "sports":
        line_fig = line_chart("sports")
    elif dropdown_value == "countries":
        line_fig = line_chart("countries")
    elif dropdown_value == "participants":
        line_fig = line_chart("participants")
    
    # Update bar chart based on checklist value
    if "summer" in checklist_value and "winter" in checklist_value:
        bar_fig_summer = bar_gender("Summer")
        bar_fig_winter = bar_gender("Winter")
        return line_fig, bar_fig_summer, bar_fig_winter
    elif "summer" in checklist_value:
        bar_fig = bar_gender("Summer")
        return line_fig, bar_fig
    elif "winter" in checklist_value:
        bar_fig = bar_gender("Winter")
        return line_fig, bar_fig
    else:
        bar_fig = bar_gender("None")
        return line_fig, bar_fig
    
# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5050)