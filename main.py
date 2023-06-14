from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import dash
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
from objects.joint import Joint
import json
from models_definitions import arm_test, plane_test, circle_test, machine
from frontend.pages.arm_page import ArmPage
from frontend.pages.compound_model_page import CompoundModelPage
from frontend.pages.plane_page import PlanePage
from utils.plotly_plotter import PlotlyPlotter, BASE_FIGURE
# from utils.vtk_view import vtk_view
from utils.vtk_view import get_vtk_geoms, get_vtk_view
from utils.vtk_view import VTK_ID, VTK_ALG_ID, VTK_SLIDER_ID, VTK_CHECKLIST_ID
import random
from timeit import default_timer as timer
import time
from frontend.components.trigger import Trigger

debug_data = {}

MESSAGE_SECTION_ID = "message-kinematics"
PARAMETERS_SECTION_ID = "parameters-kinematics"

app = Dash(__name__, external_stylesheets=root.external_css)

GRAPH_ID = "graph-kinematics"
DEUBG_TEXT_ID_P = "textarea_id_p"
DEUBG_TEXT_ID_V = "textarea_id_v"

plotly_graph = dcc.Graph(id=GRAPH_ID, figure=BASE_FIGURE, className="plotly-graph")
debug_textarea_p = dcc.Textarea(
        id=DEUBG_TEXT_ID_P,
        value="Debug code"
    )
debug_textarea_v = dcc.Textarea(
        id=DEUBG_TEXT_ID_V,
        value="Debug code"
    )
trigger = Trigger('main-trigger')


""" ========================= MODELS SETUP ========================= """
models = []
# models.append(machine)
# models.append(arm_test)
# models.append(circle_test)
# models.append(plane_test)

vtk_outputs = []
vtk_models = []
vtk_geoms = []
for model in models:
    model.update()
    vtk_model_data = model.get_vtk_model_data()
    vtk_models.append(vtk_model_data)
    states_out = [Output(m['id'], 'state') for m in vtk_model_data]
    actors_out = [Output("repr_"+m['id'], 'actor') for m in vtk_model_data]
    properties_out = [Output("repr_"+m['id'], 'property') for m in vtk_model_data]
    vtk_outputs.append([states_out, actors_out, properties_out])
    vtk_geoms += get_vtk_geoms(vtk_model_data)

vtk_view = get_vtk_view(vtk_geoms)

""" ========================= PAGES SETUP ========================= """
robots_show_options = ['Plane', 'Test Arm']
pages = []

machine_page = CompoundModelPage(machine, app, label="Machine")
pages.append(machine_page)

arm_page = ArmPage(arm_test, app, label="Arm Test")
pages.append(arm_page)

circle_page = PlanePage(circle_test, app, label="Circle Test")
pages.append(circle_page)

plane_page = PlanePage(plane_test, app, label="Plane Test")
pages.append(plane_page)

info_panel = html.Div(children=[debug_textarea_p, debug_textarea_v], className="info-panel")
IK_point = Joint("IK_Point", [300, 200, 100], trace_params={'color':"#555555"})
initial_page = pages[0]

triggers = {}
triggers['tab-id'] = Input('view-panel-tabs', 'value')

machine_tabs = []
for page in pages:
    page_layout = page.get_page()
    page.add_callback()
    machine_tabs.append(dcc.Tab(page_layout, label=page.label, value=page.id))
    triggers[page.id] = page.trigger.input


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
                    html.Div([dcc.Tabs(plots_tabs, value='plotly', id='plots-tabs'), info_panel], className="view-panel")
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
                trigger.component,
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

def update_visibility(*callback_data):
    global prev_tab_id
    inputs = callback_data[0]
    states = callback_data[1]
    # Switch tab visibility
    if inputs['tab-id'] != prev_tab_id:
        prev_tab_id = inputs['tab-id']
        for page in pages:
            page.model.set_visibility(inputs['tab-id'] == page.id)
    return dash.no_update

def plot_plotly(*callback_data):
    global debug_data
    start = timer()
    inputs = callback_data[0]
    states = callback_data[1]
    PlotlyPlotter.export_trace(states['figure'], postfix="pre")
            
    plane_test.forward_kinematics()
    for page in pages:
        states['figure']['data'] = page.model.draw_plotly(states['figure']['data'])
    states['figure']['data'] = IK_point.draw_plotly(states['figure']['data'])
    
    PlotlyPlotter.change_camera_view(states['figure'], states['relayout'])
    PlotlyPlotter._draw_scene(states['figure'])
    end = timer()
    if 'plotly_time' not in debug_data.keys():
        debug_data['plotly_time'] = {"title": "VTK Draw Time: ", "value": [""]}
    # debug_data['plotly_time']['value'].append(f"{end-start:.3f}")
    debug_data['plotly_time']['value'][0] = f"{end-start:.3f}"
    dbg_str = ""
    for k in debug_data.keys():
        dd = debug_data[k]
        for val in dd.keys():
            dbg_str += f"{dd[val]}"
        dbg_str += "\n"
    return [states['figure'], dbg_str]
    # PlotlyPlotter.export_trace(states['figure'], postfix="post")


def update_vtk_models(*callback_data):
    global debug_data
    start = timer()
    # inputs = callback_data[0]
    # states = callback_data[1]
    # print(f"VTK Callbakc update {callback_data}")
    vtk_outputs = []
    for model in models:
        model.update()
        updated_vtk_models = model.update_vtk_model_data()
        new_states = [m['state'] for m in updated_vtk_models]
        new_actor = [m['actor'] for m in updated_vtk_models]
        new_properties = [m['property'] for m in updated_vtk_models]
        vtk_outputs.append([new_states, new_actor, new_properties])
    end = timer()
    if 'vtk_time' not in debug_data.keys():
        debug_data['vtk_time'] = {"title": "VTK Draw Time: ", "value": [""]}
    # debug_data['vtk_time']['value'].append(f"{end-start:.3f}")
    debug_data['vtk_time']['value'][0] = f"{end-start:.3f}"
    dbg_str = ""
    for k in debug_data.keys():
        dd = debug_data[k]
        for val in dd.keys():
            dbg_str += f"{dd[val]}"
        dbg_str += "\n"
    vtk_outputs.append(dbg_str)
    return vtk_outputs

graph_out = [Output(GRAPH_ID, 'figure'), Output(DEUBG_TEXT_ID_P, 'value')]
graph_state = {'figure': State(GRAPH_ID, "figure"), 'relayout': State(GRAPH_ID, "relayoutData")}
# triggers['machine'] = machine_page.trigger.input,
app.callback(graph_out, triggers, graph_state)(plot_plotly)
# app.callback(graph_out, triggers, graph_state)(plot_plotly)


vtk_inputs = triggers
vtk_outputs.append(Output(DEUBG_TEXT_ID_V, 'value'))
# [print(f"\n\n{vtk_out}") for vtk_out in vtk_outputs]
app.callback(vtk_outputs, vtk_inputs, graph_state)(update_vtk_models)


app.callback(trigger.output, triggers, graph_state)(update_visibility)


if __name__ == "__main__":
    # Run app and display result inline in the notebook
    app.run_server(debug=True, port=8051)