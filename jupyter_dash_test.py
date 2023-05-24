"""
This is a minimal example of changing themes with the ThemeSwitchAIO component
Note - this requires dash-bootstrap-components>=1.0.0 and dash>=2.0
    pip install dash-bootstrap-templates=1.0.0.

The ThemeSwitchAIO component updates the Plotly default figure template when the
theme changes, but the figures must be updated in a callback in order to render with the new template.

This example demos:
 - how to update the figure for the new theme in a callback
 - using the dbc class which helps improve the style when the themes are switched. See the dbc.css file in the dash-bootstrap-templates library.

"""

from dash import Dash, dcc, html, dash_table, Input, Output, callback
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO, ThemeChangerAIO, template_from_url
import components.root as root
import dash_mantine_components as dmc
from components.cheatsheets_tab import cheatsheet


df = px.data.gapminder()
years = df.year.unique()
continents = df.continent.unique()

app = Dash(__name__, external_stylesheets=root.external_css)

df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    }
)

buttons = html.Div(
    [
        dbc.Button("Primary", color="primary"),
        dbc.Button("Secondary", color="secondary"),
        dbc.Button("Success", color="success"),
        dbc.Button("Warning", color="warning"),
        dbc.Button("Danger", color="danger"),
        dbc.Button("Info", color="info"),
        dbc.Button("Light", color="light"),
        dbc.Button("Dark", color="dark"),
        dbc.Button("Link", color="link"),
    ],
    className="m-4",
)


table = html.Div(
    dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i, "deletable": True} for i in df.columns],
        data=df.to_dict("records"),
        page_size=10,
        editable=True,
        cell_selectable=True,
        filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto"},
        row_selectable="multi",
    ),
    className="dbc-row-selectable",
)

dropdown = html.Div(
    [
        dbc.Label("Select indicator (y-axis)"),
        dcc.Dropdown(
            ["gdpPercap", "lifeExp", "pop"],
            "pop",
            id="indicator",
            clearable=False,
        ),
    ],
    className="mb-4",
)

checklist = html.Div(
    [
        dbc.Label("Select Continents"),
        dbc.Checklist(
            id="continents",
            options=[{"label": i, "value": i} for i in continents],
            value=continents,
            inline=True,
        ),
    ],
    className="mb-4",
)

slider = html.Div(
    [
        dbc.Label("Select Years"),
        dcc.RangeSlider(
            years[0],
            years[-1],
            5,
            id="years",
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
            value=[years[2], years[-2]],
            className="p-0",
        ),
    ],
    className="mb-4",
)

theme_colors = [
    "primary",
    "secondary",
    "success",
    "warning",
    "danger",
    "info",
    "light",
    "dark",
    "link",
]
colors = html.Div(
    [dbc.Button(f"{color}", color=f"{color}", size="sm") for color in theme_colors]
)
colors = html.Div(["Theme Colors:", colors], className="mt-2")

controls = dbc.Card(
    [dropdown, checklist, slider],
    body=True,
)


tab1 = dbc.Tab([dcc.Graph(id="line-chart")], label="Line Chart")
tab2 = dbc.Tab([dcc.Graph(id="scatter-chart")], label="Scatter Chart")
tab3 = dbc.Tab([table], label="Table", className="p-4")
tab4 = dbc.Tab([cheatsheet], label="Cheatsheet")
tabs = dbc.Card(dbc.Tabs([tab1, tab2, tab3, tab4]))

graph = html.Div(dcc.Graph(id="graph"), className="m-4")

"""
===============================================================================
Layout
"""
app.layout = dmc.MantineProvider(
    inherit=True,
    children=[
        dbc.Container([
                root.Navbar,
                dbc.Row(
                    [
                        root.header,
                        dbc.Col([controls], width=4),
                        dbc.Col(
                            [
                                tabs,
                                colors,
                                buttons,
                                graph,
                            ],
                            width=8
                        )
                    ],
                style={'position': 'relative'}),
            ],
            className="dbc d-flex",
            style={'padding-left': '0'},
            fluid=True,
        )
    ])


@app.callback(Output("graph", "figure"), root.switcher_input)
def update_graph_theme(toggle):
    template = root.themes_templates[0] if toggle else root.themes_templates[1]
    return px.bar(df, x="Fruit", y="Amount", color="City", barmode="group", template=template)

if __name__ == "__main__":
    # Run app and display result inline in the notebook
    app.run_server(debug=True, port=8051)