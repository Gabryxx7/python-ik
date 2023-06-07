from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
from dash_bootstrap_templates import ThemeSwitchAIO, ThemeChangerAIO, template_from_url
import frontend.components.root as root
from frontend.components.cheatsheets_tab import cheatsheet
from style_settings import EXTERNAL_STYLESHEETS, GLOBAL_PAGE_STYLE
from frontend.components.plot_3d import plot3d, GRAPH_ID, MachinePlotter
from frontend.components.example_tabs import controls, colors, buttons, graph
from models.arm import Arm
from models.basic.joint import Joint
import json
from models_definitions import arm_test, plane_test, circle_test, machine
from frontend.pages.arm_page import ArmPage
from frontend.pages.compound_model_page import CompoundModelPage
from frontend.pages.plane_page import PlanePage

BASE_PLOTTER = MachinePlotter()

MESSAGE_SECTION_ID = "message-kinematics"
PARAMETERS_SECTION_ID = "parameters-kinematics"

app = Dash(__name__, external_stylesheets=root.external_css)

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

tabs = []
for page in pages:
    page_layout = page.get_page()
    page.add_callback()
    tabs.append(dcc.Tab(page_layout, label=page.label, value=page.id))
    triggers[page.id] = page.trigger.input

main_plot_page = html.Div([
                    html.Div([
                            # dcc.Checklist(robots_show_options.copy(), [robots_show_options[0]], style={'display': 'flex', 'padding': '0.5rem', 'place-content': 'space-evenly'}, id='show-robots-checklist'),
                            dcc.Tabs(tabs,
                            value=initial_page.id,
                            id="view-panel-tabs")
                        ],
                        className="sidebar"
                    ),
                    html.Div([plot3d, info_panel], className="view-panel")
                ], className="main-container")
tabs = []
tabs.append(dcc.Tab(main_plot_page,
                style={'position': 'relative', 'width': '100%'},
                label="Home"))
tabs.append(dcc.Tab([cheatsheet], label="Cheatsheet"))

app.layout = dmc.MantineProvider(
    inherit=True,
    children=[
        dbc.Container([
                # root.Navbar,
                dbc.Row([
                    root.header,
                    dbc.Col(
                        dcc.Tabs(tabs, style={'flex-direction': 'column'}),
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
def switch_model_visibility(tab_id):
    global prev_tab_id
    if tab_id == prev_tab_id:
        return
    prev_tab_id = tab_id
    for page in pages:
        page.model.set_visibility(tab_id == page.id)

def update_graph(*callback_data):
    inputs = callback_data[0]
    states = callback_data[1]
    # with open("data_debug_pre.json", "w") as f:
    #     json.dump(states['figure'], f, indent=2)
    switch_model_visibility(inputs['tab-id'])
    # for i in range(0, len(plane.arms)):
    #     states['figure']['data'] = plane.arms[i].draw(states['figure']['data'])
    # for i in range(0, len(plane.pistons)):
    #     states['figure']['data'] = plane.pistons[i].draw(states['figure']['data'])
    # if plane.planes[0].ik_res is not None:
    #     for i in range(0,3):
    #         plane.pistons[i].joints[-1].origin_pos[2] = plane.planes[0].ik_res[i]
    #     plane.forward_kinematics()
    # states['figure']['data'] = plane.draw(states['figure']['data'])
    
    plane_test.forward_kinematics()
    for page in pages:
        states['figure']['data'] = page.model.draw(states['figure']['data'])
    states['figure']['data'] = IK_point.draw(states['figure']['data'])
        
    BASE_PLOTTER.change_camera_view(states['figure'], states['relayout'])
    BASE_PLOTTER._draw_scene(states['figure'])
    # with open("data_debug_post.json", "w") as f:
    #   json.dump(states['figure'], f, indent=2)
    return states['figure']


graph_out = Output(GRAPH_ID, 'figure')
graph_state = {'figure': State(GRAPH_ID, "figure"), 'relayout': State(GRAPH_ID, "relayoutData")}
# triggers['machine'] = machine_page.trigger.input,
app.callback(graph_out, triggers, graph_state)(update_graph)

if __name__ == "__main__":
    # Run app and display result inline in the notebook
    app.run_server(debug=True, port=8051)