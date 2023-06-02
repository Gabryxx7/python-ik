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
from model import arm_test, plane
from components.arm_page import ArmPage
from components.plane_model_page import PlaneModelPage

BASE_PLOTTER = MachinePlotter()

MESSAGE_SECTION_ID = "message-kinematics"
PARAMETERS_SECTION_ID = "parameters-kinematics"

app = Dash(__name__, external_stylesheets=root.external_css)

""" ========================= LAYOUT ========================= """
robots_show_options = ['Plane', 'Test Arm']
arm_page = ArmPage(arm_test, app)
arm_page_layout = arm_page.get_page()
arm_page.add_callback()
plane_page = PlaneModelPage(plane, app)
plane_page_layout = plane_page.get_page()
plane_page.add_callback()

info_panel = html.Div("", className="info-panel")

main_plot_page = html.Div([
                    html.Div([
                            # dcc.Checklist(robots_show_options.copy(), [robots_show_options[0]], style={'display': 'flex', 'padding': '0.5rem', 'place-content': 'space-evenly'}, id='show-robots-checklist'),
                            dcc.Tabs([
                                dcc.Tab(plane_page_layout, label="Plane", value=plane_page.id),
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
    print(f"Switching visibility: {tab}")
    if tab == plane_page.id:
        plane_page.plane.set_visibility(True)
        arm_page.model.set_visibility(False)
    if tab == arm_page.id:
        plane_page.plane.set_visibility(False)
        arm_page.model.set_visibility(True)

def update_graph(*callback_data):
    inputs = callback_data[0]
    states = callback_data[1]
    switch_model_visibility(inputs['tab-id'], states['figure']['data'])
    for i in range(0, len(plane.arms)):
        states['figure']['data'] = plane.arms[i].draw(states['figure']['data'])
    for i in range(0, len(plane.pistons)):
        states['figure']['data'] = plane.pistons[i].draw(states['figure']['data'])
    states['figure']['data'] = arm_test.draw(states['figure']['data'])
    states['figure']['data'] = plane.draw(states['figure']['data'])
    BASE_PLOTTER.change_camera_view(states['figure'], states['relayout'])
    BASE_PLOTTER._draw_scene(states['figure'])
    return states['figure']

# def draw_plot(figure, relayout_data, robots_to_show=None):
#     if robots_to_show is None:
#         robots_to_show = robots_show_options
    
#     test_model['arm'].set_visibility(robots_show_options[1] in robots_to_show)
#     BASE_PLOTTER._draw_arm(figure, test_model['arm'])
    
#     for i in range(0, len(plane_model['arms'])):
#         plane_model['arms'][i].set_visibility(robots_show_options[0] in robots_to_show)
#         plane_model['pistons'][i].set_visibility(robots_show_options[0] in robots_to_show)
#         BASE_PLOTTER._draw_arm(figure, plane_model['arms'][i])
#         BASE_PLOTTER._draw_arm(figure, plane_model['pistons'][i])
#     plane_model['plane'].set_visibility(robots_show_options[0] in robots_to_show)
#     BASE_PLOTTER._draw_arm(figure, plane_model['plane'])

#     BASE_PLOTTER.change_camera_view(figure, relayout_data)
#     # print(f"Updating figure: {quaternion_values}")
#     return figure

graph_out = Output(GRAPH_ID, 'figure')
graph_state = {'figure': State(GRAPH_ID, "figure"), 'relayout': State(GRAPH_ID, "relayoutData")}
print("******* PLANE TRIGGER *******")
triggers = {'arm': arm_page.trigger.input, 'plane':plane_page.trigger.input, 'tab-id': Input('view-panel-tabs', 'value')}
# triggers = {'arm': arm_page.trigger.input}
# triggers = {'plane':plane_page.trigger.input}
app.callback(graph_out, triggers, graph_state)(update_graph)

if __name__ == "__main__":
    # Run app and display result inline in the notebook
    app.run_server(debug=True, port=8051)