
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_bootstrap_templates import ThemeSwitchAIO, ThemeChangerAIO, template_from_url
from jupyter_dash import JupyterDash
from dash_iconify import DashIconify
from components.cheatsheets_tab import cheatsheet

# The Custom css is actually automatically loaded, everything in assets/css is automatically loadecd
themes_map = {
    "custom": [
        {
            "url": "custom.css",
            # "local_path": "assets/custom.css",
        }
    ],
    "templates": [
        {
            "name": "morph",
            "url": dbc.themes.MORPH,
            # "local_path": "/Users/marinig/Documents/GitHub/python-ik/external_css/morph.css",
        },
        {
            "name": "cyborg",
            "url": dbc.themes.CYBORG,
            # "local_path": "/Users/marinig/Documents/GitHub/python-ik/external_css/cyborg.css",
        },
    ]
}

themes = [t['url'] for t in themes_map['templates']]
themes_templates = [template_from_url(t) for t in themes]
dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css")
fa_css = 'https://use.fontawesome.com/releases/v5.8.1/css/all.css'
external_css = [themes[0], dbc_css, fa_css]

header_title = html.Span([html.H4("ThemeSwitchAIO Demo", className="text-white p-2 mb-2 text-center")])
switcher = html.Span([ThemeSwitchAIO(aio_id="theme", themes=themes, switch_props={"value": False})], style={'position': '/*absolute*/', 'left': '/*1rem*/'})
switcher_input = Input(ThemeSwitchAIO.ids.switch("theme"), "value")

navlink_style = {'color': 'inherit', 'background-color': 'inherit'}
Navbar = dmc.Navbar(
    p="0px",                  #providing medium padding all side
    fixed=False,             #Setting fixed to false
    width={"base": '0px'},     #Initial size of navbar ie. 300px
    hidden=True,             #we want to hide for smaller screen
    hiddenBreakpoint='md',   #after past medium size navbar will be hidden.
    height='100vh',          #providing height of navbar
    id='sidebar',
    children=[
      html.Div([
        switcher,
            # dmc.NavLink(
            #     label="With icon",
            #     icon=DashIconify(icon="bi:house-door-fill", height=16),
            #     style=navlink_style
            # ),
            # dmc.NavLink(
            #     opened=False,
            #     label="With right section",
            #     icon=DashIconify(icon="tabler:gauge", height=16),
            #     rightSection=DashIconify(icon="tabler-chevron-right", height=16),
            #     style=navlink_style
            # ),
            # dmc.NavLink(
            #     label="Disabled",
            #     icon=DashIconify(icon="tabler:circle-off", height=16),
            #     disabled=True,
            #     style=navlink_style
            # ),
            # dmc.NavLink(
            #     label="With description",
            #     description="Additional information",
            #     icon=dmc.Badge(
            #         "3", size="xs", variant="filled", color="red", w=16, h=16, p=0
            #     ),
            #     style=navlink_style
            # ),
            # dmc.NavLink(
            #     label="Active subtle",
            #     icon=DashIconify(icon="tabler:activity", height=16),
            #     rightSection=DashIconify(icon="tabler-chevron-right", height=16),
            #     variant="subtle",
            #     active=True,
            # ),
          ])
    ],
    style={'overflow':'hidden', 'transition': 'width 0.3s ease-in-out', 'background-color': 'var(--bs-body-bg)', 'color': 'var(--bs-body-color)'}
)
ham_menu = dmc.Button(
          children=[DashIconify(icon="ci:hamburger-lg", width=24, height=24,color="#c2c7d0")],
          variant="subtle", 
          p=1,
          id='sidebar-button',
          style={'position': 'absolute', 'left': '2rem'}
        )
@dash.callback(
    [Output("sidebar", "width"), Output("sidebar", "p")],          #what we wanted to change
    Input("sidebar-button", "n_clicks"), #width will change when btn is triggered
    [State('sidebar','width'), State('sidebar','p')],            #store inital width
    prevent_initial_call=True,
    )
def sidebar(opened, width, padding):
    if opened:
        if width['base'] == 500:         #if initial width is 300 then return 70
            return [{"base": '0px'}, '0px']
        else:
            return [{"base": 500}, 'md']
#Provide style={'display':'flex'} under html.Div, then button will be beside navbar.

header = html.Div([ham_menu, header_title],className="d-flex align-items-center justify-content-center")