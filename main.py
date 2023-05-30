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
from model import test_model, plane_model, PISTON_START_HEIGHT_RATIO

BASE_PLOTTER = MachinePlotter()

MESSAGE_SECTION_ID = "message-kinematics"
PARAMETERS_SECTION_ID = "parameters-kinematics"

app = Dash(__name__, external_stylesheets=root.external_css)

# plane_model['piston_widgets'] = []
# plane_model['piston_inputs'] = []
# for i in range(0, len(plane_model['pistons'])):
#     piston_widget, piston_input = make_piston_widget(plane_model['pistons'][i].uuid, f"Piston {i+1}", PISTON_START_HEIGHT_RATIO, _min=0, _max=1, _input_resolution=0.05)
#     plane_model['piston_widgets'].append(piston_widget)
#     plane_model['piston_inputs'].append(piston_input)

# plane_model['arm_joint0_widgets'] = []
# plane_model['arm_joint0_inputs'] = []
# plane_model['tf_widgets'] = []
# plane_model['tf_outputs'] = []
# plane_model['tf_widgets_ee'] = []
# plane_model['tf_outputs_ee'] = []
# for i in range(0, len(plane_model['arms'])):
#     arm_joint0_widget, arm_joint0_inpt = make_quaternion_widget(app, plane_model['arms'][i].joints[0])
#     tf_widget, tf_output = make_transform_widget(app, plane_model['arms'][i].joints[0])
#     tf_widget_ee, tf_output_ee = make_transform_widget(app, plane_model['arms'][i].joints[1])
#     plane_model['arm_joint0_widgets'].append(arm_joint0_widget)
#     plane_model['arm_joint0_inputs'].append(arm_joint0_inpt)
#     plane_model['tf_widgets'].append(tf_widget)
#     plane_model['tf_outputs'].append(tf_output)
#     plane_model['tf_widgets_ee'].append(tf_widget_ee)
#     plane_model['tf_outputs_ee'].append(tf_output_ee)

# test_model['joints_widgets'] = []
# test_model['joints_inputs'] = []
# test_model['tf_widgets'] = []
# test_model['tf_outputs'] = []
# for i in range(0, len(test_model['arm'].joints)):
#     arm_widget, arm_inpt = make_quaternion_widget(app, test_model['arm'].joints[i])
#     tf_widget, tf_output = make_transform_widget(app, test_model['arm'].joints[i])
#     test_model['joints_widgets'].append(arm_widget)
#     test_model['joints_inputs'].append(arm_inpt)
#     test_model['tf_widgets'].append(tf_widget)
#     test_model['tf_outputs'].append(tf_output)

left_side_width = '25vw'
right_side_width = '70vw'
plot_height = "70vh"
info_panel_height = "30vh"
""" ========================= LAYOUT ========================= """
# pistons_widgets = html.Div(plane_model['piston_widgets'] + plane_model['arm_joint0_widgets'], style={'display': 'flex', 'width': left_side_width, 'max-width': left_side_width, 'flex-wrap': 'wrap', 'flex-direction': 'row'})
# test_arm_widgets = html.Div(test_model['joints_widgets'], style={'display': 'flex', 'width': left_side_width, 'max-width': left_side_width, 'flex-wrap': 'wrap', 'flex-direction': 'row'})
robots_show_options = ['Plane', 'Test Arm']
# info_panel = html.Div(plane_model['tf_widgets']+plane_model['tf_widgets_ee'],
#                       className="info-panel d-flex align-items-start justify-items-start flex-row", style={'gap': '1rem', 'padding': '1rem', 'width': 'right_side_width', 'flex-wrap': 'nowrap'})
# plane_page = html.Div([pistons_widgets, info_panel], style={'display': 'flex', 'flex-direction': 'row'})
model_page, model_inputs, model_outputs = test_model['arm'].get_widget(app)

main_plot_page = html.Div([
                    html.Div([
                            # dcc.Checklist(robots_show_options.copy(), [robots_show_options[0]], style={'display': 'flex', 'padding': '0.5rem', 'place-content': 'space-evenly'}, id='show-robots-checklist'),
                            dbc.Tabs([
                                # dbc.Tab(plane_page, label="Plane", style={"padding": "1rem"}),
                                # dbc.Tab(test_arm_widgets, label="Test Arm", style={"padding": "1rem"}),
                                dbc.Tab(model_page, label="Test Arm", style={"padding": "1rem"}),
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


def update_graph_test(test_arm_quat, figure, relayout_data):
    BASE_PLOTTER._draw_arm(figure, test_model['arm'])
    BASE_PLOTTER.change_camera_view(figure, relayout_data)
    return figure
    
def update_graph(plane_quat, piston_heights, test_arm_quat, show_robots_checks, figure, relayout_data):
    for i in range(0, len(plane_model['arms'])):
        plane_model['arms'][i].joints[-2]._origin[2] = float(plane_model['pistons'][i].joints[-1]._origin[2]) * float(piston_heights[i])
        plane_model['arms'][i].joints[-2].rotate(quaternion=plane_quat[i][0])
        plane_model['arms'][i].forward_kinematics()
    
    for i in range(0, len(test_model['arm'].joints)):
        test_model['arm'].joints[i].rotate(quaternion=test_arm_quat[i][0])
    test_model['arm'].forward_kinematics()
    return draw_plot(figure, relayout_data, show_robots_checks)

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


# add_quat_widget_callback(app)
# show_robots_checks = Input('show-robots-checklist', 'value')
# inpts = [plane_model['arm_joint0_inputs'], plane_model['piston_inputs'], test_model['joints_inputs'], show_robots_checks]
graph_out = Output(GRAPH_ID, 'figure')
graph_state = [State(GRAPH_ID, "figure"), State(GRAPH_ID, "relayoutData")]

inpts = [model_inputs]
app.callback(graph_out, inpts, graph_state)(update_graph_test)
test_model['arm'].register_model_callbacks(app)


if __name__ == "__main__":
    # Run app and display result inline in the notebook
    app.run_server(debug=True, port=8051)