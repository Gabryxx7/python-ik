from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
from dash_bootstrap_templates import ThemeSwitchAIO, ThemeChangerAIO, template_from_url
import components.root as root
from components.cheatsheets_tab import cheatsheet
from style_settings import EXTERNAL_STYLESHEETS, GLOBAL_PAGE_STYLE
from components.plot_3d import plot3d, GRAPH_ID, MachinePlotter
from components.example_tabs import controls, colors, buttons, graph
from components.quaternion_widget import quaternion_widget, add_quat_widget_callback, add_quaternion_listener

BASE_PLOTTER = MachinePlotter()

MESSAGE_SECTION_ID = "message-kinematics"
PARAMETERS_SECTION_ID = "parameters-kinematics"

app = Dash(__name__, external_stylesheets=root.external_css)

""" ========================= LAYOUT ========================= """
tabs = []
tabs.append(dbc.Tab([
                dbc.Row(
                    [
                        html.Div(quaternion_widget, style={'width': '30%'}),
                        html.Div(plot3d, style={'width': '70%'})
                    ],
                    style={'position': 'relative', 'padding': '1rem', 'width': '100%'})
                ],
                label="Home"
            )
        )
tabs.append(dbc.Tab([cheatsheet], label="Cheatsheet"))

app.layout = dmc.MantineProvider(
    inherit=True,
    children=[
        dbc.Container([
                # root.Navbar,
                dbc.Row([
                    root.header,
                    dbc.Col(
                        dbc.Tabs(tabs, style={'flex-direction': 'column'}),
                        className="d-flex align-items-start justify-items-start flex-row")
                ])
            ],
            className="dbc d-flex",
            style={'padding-left': '0'},
            fluid=True,
        )
    ])

add_quat_widget_callback(app)

def update_graph(quaternion_values, figure):
    BASE_PLOTTER.update(figure, quaternion_values)
    # print(f"Updating figure: {quaternion_values}")
    return figure

add_quaternion_listener(app, update_graph, Output(GRAPH_ID, 'figure'), State(GRAPH_ID, "figure"))
if __name__ == "__main__":
    # Run app and display result inline in the notebook
    app.run_server(debug=True, port=8051)