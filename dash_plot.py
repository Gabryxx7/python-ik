import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
from page_layout import *

from style_settings import EXTERNAL_STYLESHEETS, GLOBAL_PAGE_STYLE
from plotter import MachinePlotter

BASE_PLOTTER = MachinePlotter()

app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
my_dates = [1,2,3,4]

# ......................
# Page layout
# ......................
GRAPH_ID = "graph-kinematics"
DROPDOWN_ID = "select-date"
MESSAGE_SECTION_ID = "message-kinematics"
PARAMETERS_SECTION_ID = "parameters-kinematics"

app.layout = html.Div([
      html.H1("3D Charts", style={"textAlign": "center"}),
      html.Div([dcc.Dropdown(id=DROPDOWN_ID, options=[{'label': i, 'value': i} for i in my_dates], value="2018-02-06")], className="six columns", style={"width": "40%", "margin-left": "auto", "margin-right": "auto", "display": "block"}),
      get_page_layout(GRAPH_ID, MESSAGE_SECTION_ID)
    ],className="container",
    style=GLOBAL_PAGE_STYLE)


# app.layout = html.Div([
#     html.H1("3D Charts", style={"textAlign": "center"}),
#     get_page_layout("my-graph", "my-section"),
#     html.Div([html.Div([html.Span("Type Of Chart : ")], className="six columns",
#                        style={"textAlign": "right", "padding-right": 30, "padding-top": 7}),
#               html.Div([dcc.Dropdown(id='select-date', options=[{'label': i, 'value': i} for i in my_dates],
#                                      value="2018-02-06")], className="six columns",
#                        style={"width": "40%", "margin-left": "auto", "margin-right": "auto", "display": "block"}),
#               ], className="row", style={"width": "80%"}),
#     html.Div([dcc.Graph(id=GRAPH_ID, figure=BASE_FIGURE)], className="row")
# ], className="container")

@app.callback(
    Output(GRAPH_ID, 'figure'),
    [Input(DROPDOWN_ID, 'value')],
    State(GRAPH_ID, "figure"))
def update_graph(dropdown_value, figure):
  BASE_PLOTTER.update(figure)
  print("Updating figure")
  return figure
    # global df_sliced

    # df_sliced = df_size.loc[selected:selected]
    # df_sliced = df_sliced.rolling(6).mean()
    # df_sliced = df_sliced.dropna()

    # trace2 = [go.Surface(
    #     z = df_sliced.values,
    #     colorscale='Rainbow', colorbar={"thickness": 10, "len": 0.5, "title": {"text": "Volume"}})]
    # layout2 = go.Layout(
    #     title="Orderbook Structure " + str(selected), height=1000, width=1000, scene = dict(
    #                 xaxis_title='Order Level - Bid Side[0-9], Ask Side[10-19]',
    #                 yaxis_title='Time 08.00 until 22.00 (5Min Intervals)',
    #                 zaxis_title='Volume (Trailing Mean - 30Min)',
    #                 aspectmode='cube'),
    #     scene_camera_eye=dict(x=2, y=-1.5, z=1.25),
    # )
    # return {"data": trace2, "layout": layout2}

if __name__ == '__main__':
  app.run_server(debug=True)