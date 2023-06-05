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
# from components.quaternion_widget import  make_quaternion_widget
# from components.piston_widget import make_piston_widget, add_piston_slider_listener
from machine.arm import Arm
from machine.joint import Joint
import json
from model import arm_test, plane, triangle
from components.arm_page import ArmPage
from components.compound_model_page import CompoundModelPage
from components.plane_page import PlanePage

BASE_PLOTTER = MachinePlotter()

MESSAGE_SECTION_ID = "message-kinematics"
PARAMETERS_SECTION_ID = "parameters-kinematics"

app = Dash(__name__, external_stylesheets=root.external_css)

""" ========================= LAYOUT ========================= """
robots_show_options = ['Plane', 'Test Arm']
arm_page = ArmPage(arm_test, app)
arm_page_layout = arm_page.get_page()
arm_page.add_callback()
plane_page = CompoundModelPage(plane, app)
plane_page_layout = plane_page.get_page()
plane_page.add_callback()
IK_point = Joint("IK_Point", [300, 200, 100], color="#555555")

triangle_page = PlanePage(triangle, app)
triangle_page_layout = triangle_page.get_page()
triangle_page.add_callback()

info_panel = html.Div("", className="info-panel")

main_plot_page = html.Div([
                    html.Div([
                            # dcc.Checklist(robots_show_options.copy(), [robots_show_options[0]], style={'display': 'flex', 'padding': '0.5rem', 'place-content': 'space-evenly'}, id='show-robots-checklist'),
                            dcc.Tabs([
                                dcc.Tab(plane_page_layout, label="Plane", value=plane_page.id),
                                dcc.Tab(triangle_page_layout, label="Triangle", value=triangle_page.id),
                                # dcc.Tab(test_arm_widgets, label="Test Arm"),
                                dcc.Tab(arm_page_layout, label="Test Arm", value=arm_page.id),
                                dcc.Tab(html.Label(dcc.Markdown(f"** QUATERNION **")), label="Nothing")],
                            value=plane_page.id,
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

def switch_model_visibility(tab, fig_data):
    if tab == plane_page.id:
        if not plane_page.model.visible:
            print(f"Showing plane tab {plane_page.model.name}")
            plane_page.model.set_visibility(True)
            triangle_page.model.set_visibility(False)
            arm_page.model.set_visibility(False)
    elif tab == arm_page.id:
        if not arm_page.model.visible:
            print(f"Showing arm tab {arm_page.model.name}")
            plane_page.model.set_visibility(False)
            triangle_page.model.set_visibility(False)
            arm_page.model.set_visibility(True)
    elif tab == triangle_page.id:
        if not triangle_page.model.visible:
            print(f"Showing triangle tab {triangle_page.model.name}")
            plane_page.model.set_visibility(False)
            triangle_page.model.set_visibility(True)
            arm_page.model.set_visibility(False)

def update_graph(*callback_data):
    inputs = callback_data[0]
    states = callback_data[1]
    switch_model_visibility(inputs['tab-id'], states['figure']['data'])
    # for i in range(0, len(plane.arms)):
    #     states['figure']['data'] = plane.arms[i].draw(states['figure']['data'])
    # for i in range(0, len(plane.pistons)):
    #     states['figure']['data'] = plane.pistons[i].draw(states['figure']['data'])
    states['figure']['data'] = arm_test.draw(states['figure']['data'])
    states['figure']['data'] = plane.draw(states['figure']['data'])
    states['figure']['data'] = triangle.draw(states['figure']['data'])
    
    states['figure']['data'] = IK_point.draw(states['figure']['data'])
    
    triangle.forward_kinematics()
    BASE_PLOTTER.change_camera_view(states['figure'], states['relayout'])
    BASE_PLOTTER._draw_scene(states['figure'])
    return states['figure']


graph_out = Output(GRAPH_ID, 'figure')
graph_state = {'figure': State(GRAPH_ID, "figure"), 'relayout': State(GRAPH_ID, "relayoutData")}
print("******* PLANE TRIGGER *******")
triggers = {'arm': arm_page.trigger.input, 'plane':plane_page.trigger.input, 'triangle':triangle_page.trigger.input, 'tab-id': Input('view-panel-tabs', 'value')}
# triggers = {'arm': arm_page.trigger.input}
# triggers = {'plane':plane_page.trigger.input}
app.callback(graph_out, triggers, graph_state)(update_graph)

if __name__ == "__main__":
    # Run app and display result inline in the notebook
    app.run_server(debug=True, port=8051)