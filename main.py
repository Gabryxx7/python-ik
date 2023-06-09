from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash_vtk
import pandas as pd
import plotly.express as px
from dash_bootstrap_templates import ThemeSwitchAIO, ThemeChangerAIO, template_from_url
import frontend.components.root as root
from frontend.components.cheatsheets_tab import cheatsheet
from style_settings import EXTERNAL_STYLESHEETS, GLOBAL_PAGE_STYLE
# from frontend.components.plot_3d import plotly_graph, GRAPH_ID, MachinePlotter
from frontend.components.example_tabs import controls, colors, buttons, graph
from models.arm import Arm
from models.basic.joint import Joint
import json
from models_definitions import arm_test, plane_test, circle_test, machine
from frontend.pages.arm_page import ArmPage
from frontend.pages.compound_model_page import CompoundModelPage
from frontend.pages.plane_page import PlanePage
from utils.plotly_plotter import PlotlyPlotter, BASE_FIGURE
# from utils.vtk_view import vtk_view
from utils.vtk_view import get_vtk_view
from utils.vtk_view import VTK_ID, VTK_ALG_ID, VTK_SLIDER_ID, VTK_CHECKLIST_ID
import random


MESSAGE_SECTION_ID = "message-kinematics"
PARAMETERS_SECTION_ID = "parameters-kinematics"

app = Dash(__name__, external_stylesheets=root.external_css)

GRAPH_ID = "graph-kinematics"

plotly_graph = dcc.Graph(id=GRAPH_ID, figure=BASE_FIGURE, className="plotly-graph")



""" ========================= LAYOUT ========================= """
robots_show_options = ['Plane', 'Test Arm']
arm_page = ArmPage(arm_test, app, label="Arm Test")
circle_page = PlanePage(circle_test, app, label="Circle Test")

machine_page = CompoundModelPage(machine, app, label="Machine")
IK_point = Joint("IK_Point", [300, 200, 100], trace_params={'color':"#555555"})
plane_page = PlanePage(plane_test, app, label="Plane Test")

info_panel = html.Div("", className="info-panel")

pages = []
pages.append(machine_page)
pages.append(arm_page)
pages.append(circle_page)
pages.append(plane_page)

initial_page = pages[0]

triggers = {}
triggers['tab-id'] = Input('view-panel-tabs', 'value')

machine_tabs = []
for page in pages:
    page_layout = page.get_page()
    page.add_callback()
    machine_tabs.append(dcc.Tab(page_layout, label=page.label, value=page.id))
    triggers[page.id] = page.trigger.input

arm_test.update()
vtk_view = get_vtk_view(arm_test.get_vtk_model_data())

plots_tabs = []
plots_tabs.append(dcc.Tab(plotly_graph, label="Plotly", value='plotly'))
# plots_tabs.append(dcc.Tab([vtk_view, vtk_controls], label="VTK", value='vtk'))
plots_tabs.append(dcc.Tab(vtk_view, label="VTK", value='vtk'))

main_plot_page = html.Div([
                    html.Div([
                            # dcc.Checklist(robots_show_options.copy(), [robots_show_options[0]], style={'display': 'flex', 'padding': '0.5rem', 'place-content': 'space-evenly'}, id='show-robots-checklist'),
                            dcc.Tabs(machine_tabs,
                            value=initial_page.id,
                            id="view-panel-tabs")
                        ],
                        className="sidebar"
                    ),
                    html.Div([dcc.Tabs(plots_tabs, value='vtk', id='plots-tabs'), info_panel], className="view-panel")
                    # html.Div([plotly_graph, info_panel], className="view-panel")
                ], className="main-container")

pages_tabs = []
pages_tabs.append(dcc.Tab(main_plot_page,
                style={'position': 'relative', 'width': '100%'},
                label="Home"))
pages_tabs.append(dcc.Tab([cheatsheet], label="Cheatsheet"))

app.layout = dmc.MantineProvider(
    inherit=True,
    children=[
        dbc.Container([
                # root.Navbar,
                dbc.Row([
                    root.header,
                    dbc.Col(
                        dcc.Tabs(pages_tabs, style={'flex-direction': 'column'}),
                        className="d-flex align-items-start justify-items-start flex-row")
                ])
            ],
            className="dbc d-flex",
            style={'padding-left': '0'},
            fluid=True,
        )
    ])

prev_tab_id = initial_page.id
initial_page.model.set_visibility(True)
        
def plot_plotly(*callback_data):
    global prev_tab_id
    inputs = callback_data[0]
    states = callback_data[1]
    # PlotlyPlotter.export_trace(states['figure'], postfix="pre")
    # Switch tab visibility
    if inputs['tab-id'] != prev_tab_id:
        prev_tab_id = inputs['tab-id']
        for page in pages:
            page.model.set_visibility(inputs['tab-id'] == page.id)
            
    plane_test.forward_kinematics()
    for page in pages:
        states['figure']['data'] = page.model.draw_plotly(states['figure']['data'])
    states['figure']['data'] = IK_point.draw_plotly(states['figure']['data'])
    
    PlotlyPlotter.change_camera_view(states['figure'], states['relayout'])
    PlotlyPlotter._draw_scene(states['figure'])
    return states['figure']
    # PlotlyPlotter.export_trace(states['figure'], postfix="post")

def plot_vtk(*callback_data):
    inputs = callback_data[0]
    states = callback_data[1]
    pass

graph_out = Output(GRAPH_ID, 'figure')
graph_state = {'figure': State(GRAPH_ID, "figure"), 'relayout': State(GRAPH_ID, "relayoutData")}
# triggers['machine'] = machine_page.trigger.input,
app.callback(graph_out, triggers, graph_state)(plot_plotly)
# app.callback(graph_out, triggers, graph_state)(plot_plotly)

def update_cone(*callback_data):
    slider_val = callback_data[0]
    checked_values = callback_data[1]
    new_state = {"resolution": slider_val, "capping": "capping" in checked_values}
    return new_state, random.random()

# vtk_outputs = [Output(VTK_ALG_ID, "state"), Output(VTK_ID, "triggerResetCamera")]
# vtk_inputs = [Input(VTK_SLIDER_ID, "value"), Input(VTK_CHECKLIST_ID, "value")]
# app.callback(vtk_outputs, vtk_inputs)(update_cone)


if __name__ == "__main__":
    # Run app and display result inline in the notebook
    app.run_server(debug=True, port=8051)