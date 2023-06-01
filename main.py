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

left_side_width = '30vw'
right_side_width = '60vw'
plot_height = "100vh"
info_panel_height = "0vh"
""" ========================= LAYOUT ========================= """
robots_show_options = ['Plane', 'Test Arm']
arm_page = ArmPage(arm_test, app)
arm_page_layout = arm_page.get_page()
arm_page.add_callback()
plane_page = PlaneModelPage(plane, app)
plane_page_layout = plane_page.get_page()
plane_page.add_callback()

main_plot_page = html.Div([
                    html.Div([
                            # dcc.Checklist(robots_show_options.copy(), [robots_show_options[0]], style={'display': 'flex', 'padding': '0.5rem', 'place-content': 'space-evenly'}, id='show-robots-checklist'),
                            dbc.Tabs([
                                dbc.Tab(plane_page_layout, label="Plane", style={"padding": "1rem"}),
                                # dbc.Tab(test_arm_widgets, label="Test Arm", style={"padding": "1rem"}),
                                dbc.Tab(arm_page_layout, label="Test Arm", style={"padding": "1rem"}),
                                dbc.Tab(html.Label(dcc.Markdown(f"** QUATERNION **")), label="Nothing", style={"padding": "1rem"})],
                                ),
                        ],
                        # style={'width': 'left_side_width'}
                    ),
                    dbc.Row([plot3d], style={'width': 'right_side_width','position': 'absolute', 'top': info_panel_height, 'left': left_side_width, 'margin-left': '1rem', 'height': plot_height, 'width': right_side_width})
                ], className="main-container-plot3d", style={'position': 'relative', 'display': 'flex', 'width': '100vw'})
tabs = []
tabs.append(dbc.Tab(main_plot_page,
                style={'position': 'relative', 'width': '100%'},
                label="Home"))
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

    
def update_graph(*callback_data):
    inputs = callback_data[0]
    states = callback_data[1]
    BASE_PLOTTER._draw_arm(states['figure'], arm_test)
    for i in range(0, len(plane.arms)):
        BASE_PLOTTER._draw_arm(states['figure'], plane.arms[i])
    for i in range(0, len(plane.pistons)):
        BASE_PLOTTER._draw_arm(states['figure'], plane.pistons[i])
    BASE_PLOTTER.change_camera_view(states['figure'], states['relayout'])
    return states['figure']
    # for i in range(0, len(plane_model['arms'])):
    #     plane_model['arms'][i].joints[-2]._origin[2] = float(plane_model['pistons'][i].joints[-1]._origin[2]) * float(piston_heights[i])
    #     plane_model['arms'][i].joints[-2].rotate(quaternion=plane_quat[i][0])
    #     plane_model['arms'][i].forward_kinematics()
    
    
    return draw_plot(states['figure'], states['relayout'])

def draw_plot(figure, relayout_data, robots_to_show=None):
    if robots_to_show is None:
        robots_to_show = robots_show_options
    
    test_model['arm'].set_visibility(robots_show_options[1] in robots_to_show)
    BASE_PLOTTER._draw_arm(figure, test_model['arm'])
    
    for i in range(0, len(plane_model['arms'])):
        plane_model['arms'][i].set_visibility(robots_show_options[0] in robots_to_show)
        plane_model['pistons'][i].set_visibility(robots_show_options[0] in robots_to_show)
        BASE_PLOTTER._draw_arm(figure, plane_model['arms'][i])
        BASE_PLOTTER._draw_arm(figure, plane_model['pistons'][i])
    plane_model['plane'].set_visibility(robots_show_options[0] in robots_to_show)
    BASE_PLOTTER._draw_arm(figure, plane_model['plane'])

    BASE_PLOTTER.change_camera_view(figure, relayout_data)
    # print(f"Updating figure: {quaternion_values}")
    return figure


graph_out = Output(GRAPH_ID, 'figure')
graph_state = {'figure': State(GRAPH_ID, "figure"), 'relayout': State(GRAPH_ID, "relayoutData")}
print("******* PLANE TRIGGER *******")
# triggers = {'arm': arm_page.trigger.input, 'plane':plane_page.trigger.input}
# triggers = {'arm': arm_page.trigger.input}
triggers = {'plane':plane_page.trigger.input}
app.callback(graph_out, triggers, graph_state)(update_graph)

if __name__ == "__main__":
    # Run app and display result inline in the notebook
    app.run_server(debug=True, port=8051)