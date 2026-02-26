# Import Packages
import dash
from dash import Dash, html
import dash_ag_grid as dag
import dash_bootstrap_components as dbc

# initialize dash app
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR, dbc_css], use_pages=True)

# ======================
# ===== App Layout =====
# ======================

# layout
app.layout = dbc.Container([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Brackets", href=dash.page_registry['pages.bracket_history']['path'])),
            dbc.NavItem(dbc.NavLink("Bracket View", href=dash.page_registry['pages.bracket_view']['path'])),
            dbc.NavItem(dbc.NavLink("Testing", href=dash.page_registry['pages.testing']['path']))
        ],
        brand="Melee Analyzer",
        brand_href=dash.page_registry['pages.home']['path'],
        color='primary',
        dark=True
    ),
    dash.page_container
])

if __name__ == "__main__":
    app.run(debug=True)