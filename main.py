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
from components.quaternion_widget import  make_quaternion_widget
from components.piston_widget import make_piston_widget, add_piston_slider_listener
import json
from model import arm_test, arm1, arm1_2, arm2, arm2_2, arm3, arm3_2, plane, PISTON_START_HEIGHT_RATIO

BASE_PLOTTER = MachinePlotter()

MESSAGE_SECTION_ID = "message-kinematics"
PARAMETERS_SECTION_ID = "parameters-kinematics"

app = Dash(__name__, external_stylesheets=root.external_css)

piston1_widget = make_piston_widget(arm1.uuid, "Piston 1", PISTON_START_HEIGHT_RATIO, _min=0, _max=1, _input_resolution=0.05)
piston2_widget = make_piston_widget(arm2.uuid, "Piston 2", PISTON_START_HEIGHT_RATIO, _min=0, _max=1, _input_resolution=0.05)
piston3_widget = make_piston_widget(arm3.uuid, "Piston 3", PISTON_START_HEIGHT_RATIO, _min=0, _max=1, _input_resolution=0.05)

arm_1_2_widget, arm_1_2_widget_inpt = make_quaternion_widget(app, arm1_2.joints[0].uuid, arm1_2.joints[0].name, arm1_2.joints[0].color)
arm_2_2_widget, arm_2_2_widget_inpt = make_quaternion_widget(app, arm2_2.joints[0].uuid, arm2_2.joints[0].name, arm2_2.joints[0].color)
arm_3_2_widget, arm_3_2_widget_inpt = make_quaternion_widget(app, arm3_2.joints[0].uuid, arm3_2.joints[0].name, arm3_2.joints[0].color)

arm_test_widget_1, arm_test_widget_1_inpt = make_quaternion_widget(app, arm_test.joints[0].uuid, arm_test.joints[0].name, arm_test.joints[0].color)
arm_test_widget_2, arm_test_widget_2_inpt = make_quaternion_widget(app, arm_test.joints[1].uuid, arm_test.joints[1].name, arm_test.joints[1].color)
arm_test_widget_3, arm_test_widget_3_inpt = make_quaternion_widget(app, arm_test.joints[2].uuid, arm_test.joints[2].name, arm_test.joints[2].color)
""" ========================= LAYOUT ========================= """
pistons_widgets = dbc.Row([arm_1_2_widget,arm_2_2_widget,arm_3_2_widget,piston1_widget,piston2_widget, piston3_widget])
test_arm_widgets = dbc.Row([arm_test_widget_1,arm_test_widget_2,arm_test_widget_3])
robots_show_options = ['Plane', 'Test Arm']
main_plot_page = html.Div([
                    html.Div([
                            dcc.Checklist(robots_show_options.copy(), [robots_show_options[0]], style={'display': 'flex', 'padding': '0.5rem', 'place-content': 'space-evenly'}, id='show-robots-checklist'),
                            dbc.Tabs([
                                dbc.Tab(pistons_widgets, label="Plane", style={"padding": "1rem"}),
                                dbc.Tab(test_arm_widgets, label="Test Arm", style={"padding": "1rem"}),
                                dbc.Tab(html.Label(dcc.Markdown(f"** QUATERNION **")), label="Nothing", style={"padding": "1rem"})],
                                ),
                        ],
                        style={'width': '30%'}
                    ),
                    html.Div(plot3d, style={'width': '70%'})
                ], className="main-container-plot3d", style={'position': 'relative', 'display': 'flex', 'width': '100%'})
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


def update_graph(plane_quat, test_arm_quat, piston_heights, show_robots_checks, figure, relayout_data):
    piston_height_ratio = piston_heights[0]
    arm1_2.joints[0]._origin[2] = float(arm1.joints[1]._origin[2]) * float(piston_height_ratio)
    arm1_2.joints[0].rotate(quaternion=plane_quat[0][0])
    # arm1_2.joints[1]._origin[2] = float(arm1_2.joints[0]._origin[2]) + float(50.0)
    arm1_2.forward_kinematics()
    piston_height_ratio = piston_heights[1]
    arm2_2.joints[0]._origin[2] = float(arm2.joints[1]._origin[2]) * float(piston_height_ratio)
    arm2_2.joints[0].rotate(quaternion=plane_quat[1][0])
    # arm2_2.joints[1]._origin[2] = float(arm2_2.joints[0]._origin[2]) + float(50.0)
    arm2_2.forward_kinematics()
    piston_height_ratio = piston_heights[2]
    arm3_2.joints[0]._origin[2] = float(arm3.joints[1]._origin[2]) * float(piston_height_ratio)
    arm3_2.joints[0].rotate(quaternion=plane_quat[2][0])
    # arm3_2.joints[1]._origin[2] = float(arm3_2.joints[0]._origin[2]) + float(50.0)
    arm3_2.forward_kinematics()
    # BASE_PLOTTER.update(figure, plane_quat)
    # print(figure)
    # print("\n")
    # with open("data_debug1.json", "w") as f:
    #     json.dump(figure, f)
    
    # Swap w and z
    # w = plane_quat[0]
    # z = plane_quat[3]
    # plane_quat[0] = z
    # plane_quat[3] = w
    # print(plane_quat[1][0])
    
    
    # arm_test.joints[0]._origin[2] = float(arm_test.joints[1]._origin[2]) * float(piston_height_ratio)
    # arm_test.joints[1]._origin[2] = float(arm_test.joints[0]._origin[2]) + float(50.0)
    arm_test.joints[0].rotate(quaternion=test_arm_quat[0][0])
    # arm_test.joints[0].trace['line']['color'] = "#EE5A24"
    arm_test.joints[1].rotate(quaternion=test_arm_quat[1][0])
    # arm_test.joints[1].trace['line']['color'] = "#EE5A24"
    arm_test.joints[2].rotate(quaternion=test_arm_quat[2][0])
    # arm_test.joints[2].trace['line']['color'] = "#EE5A24"
    arm_test.forward_kinematics()
    return draw_plot(figure, relayout_data, show_robots_checks)

def draw_plot(figure, relayout_data, robots_to_show=None):
    if robots_to_show is None:
        robots_to_show = robots_show_options
    
    arm1.set_visibility(robots_show_options[0] in robots_to_show)
    arm_test.set_visibility(robots_show_options[1] in robots_to_show)
    arm_test.set_visibility(robots_show_options[1] in robots_to_show)
    BASE_PLOTTER._draw_arm(figure, arm_test)
    
    arm1.set_visibility(robots_show_options[0] in robots_to_show)
    BASE_PLOTTER._draw_arm(figure, arm1)
    
    arm1_2.set_visibility(robots_show_options[0] in robots_to_show)
    BASE_PLOTTER._draw_arm(figure, arm1_2)
    
    arm2.set_visibility(robots_show_options[0] in robots_to_show)
    BASE_PLOTTER._draw_arm(figure, arm2)
    
    arm2_2.set_visibility(robots_show_options[0] in robots_to_show)
    BASE_PLOTTER._draw_arm(figure, arm2_2)
    
    arm3.set_visibility(robots_show_options[0] in robots_to_show)
    BASE_PLOTTER._draw_arm(figure, arm3)
    
    arm3_2.set_visibility(robots_show_options[0] in robots_to_show)
    BASE_PLOTTER._draw_arm(figure, arm3_2)
    
    plane.set_visibility(robots_show_options[0] in robots_to_show)
    BASE_PLOTTER._draw_arm(figure, plane)
    
    BASE_PLOTTER.change_camera_view(figure, relayout_data)
    # print(f"Updating figure: {quaternion_values}")
    return figure


# add_quat_widget_callback(app)
quat_inpt = [arm_1_2_widget_inpt, arm_2_2_widget_inpt, arm_3_2_widget_inpt]
quat_inpt_test = [arm_test_widget_1_inpt, arm_test_widget_2_inpt, arm_test_widget_3_inpt]
piston_inpt = [Input(arm1.uuid, "value"), Input(arm2.uuid, "value"), Input(arm3.uuid, "value")]
show_robots_checks = Input('show-robots-checklist', 'value')
inpts = [quat_inpt, quat_inpt_test, piston_inpt, show_robots_checks]
graph_out = Output(GRAPH_ID, 'figure')
graph_state = [State(GRAPH_ID, "figure"), State(GRAPH_ID, "relayoutData")]
app.callback(graph_out, inpts, graph_state)(update_graph)
# add_piston_slider_listener(app, arm2.uuid, update_piston2_height, Output(GRAPH_ID, 'figure'), [State(GRAPH_ID, "figure"), State(GRAPH_ID, "relayoutData")])
# add_piston_slider_listener(app, arm3.uuid, update_piston3_height, Output(GRAPH_ID, 'figure'), [State(GRAPH_ID, "figure"), State(GRAPH_ID, "relayoutData")])

if __name__ == "__main__":
    # Run app and display result inline in the notebook
    app.run_server(debug=True, port=8051)