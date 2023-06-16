
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO, ThemeChangerAIO, template_from_url
from frontend.dash.components.cheatsheets_tab import cheatsheet
from frontend.dash.components.navbar import Navbar, ham_menu

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


header_title = html.Span([html.H4("VR Inverse Kinematics Sandbox", className="text-white p-2 mb-2 text-center")])
switcher = html.Span([ThemeSwitchAIO(aio_id="theme", themes=themes, switch_props={"value": False})])
switcher_input = Input(ThemeSwitchAIO.ids.switch("theme"), "value")

# actions = [ham_menu, switcher]
actions = [switcher]
actions_container = html.Div(actions, className="actions-container")
header = html.Div([actions_container, header_title], className="header-container")
