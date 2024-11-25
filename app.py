#%%
import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.io as pio
import openpyxl

#%%
print(f"Dash version: {dash.__version__}")

#%%


# Set Plotly theme
dbs = dbc.themes
pio.templates.default = "plotly_white"

# Load data
data_path = r"Seasonality Screener 241014.xlsx"
df = pd.read_excel(data_path)

# Initialize the app with LUX theme
app = dash.Dash(__name__, external_stylesheets=[dbs.LUX])
server = app.server

# App layout
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Seasonality Screener Dashboard", className='text-center text-primary mb-4'), width=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.Label("Filter by Type"),
                dcc.Dropdown(
                    id='filter-type',
                    options=[
                        {'label': i, 'value': i} for i in df['Type'].unique()
                    ],
                    value=None,
                    multi=True
                ),
            ], width=4),
            dbc.Col([
                html.Label("Filter by Name"),
                dcc.Dropdown(
                    id='filter-name',
                    options=[
                        {'label': i, 'value': i} for i in df['Name'].unique()
                    ],
                    value=None,
                    multi=True
                ),
            ], width=4)
        ]),
        dbc.Row([
            dbc.Col([
                dash_table.DataTable(
                    id='data-table',
                    columns=[
                        {'name': i, 'id': i} for i in df.columns
                    ],
                    data=df.to_dict('records'),
                    style_table={
                        'height': '400px',
                        'overflowY': 'auto'
                    },
                    page_action='none',
                    style_cell={
                        'textAlign': 'left',
                        'padding': '10px',
                        'whiteSpace': 'normal'
                    },
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                )
            ], width=12)
        ])
    ])
])

# Callbacks for filtering
@app.callback(
    Output('data-table', 'data'),
    [Input('filter-type', 'value'),
     Input('filter-name', 'value')]
)
def update_table(selected_types, selected_names):
    filtered_df = df
    if selected_types:
        filtered_df = filtered_df[filtered_df['Type'].isin(selected_types)]
    if selected_names:
        filtered_df = filtered_df[filtered_df['Name'].isin(selected_names)]
    return filtered_df.to_dict('records')

if __name__ == "__main__":
    app.run_server(debug=False)


app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.LUX])
server = app.server

sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True
)

app.layout = dbc.Container([
    
    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
], fluid=True)


if __name__ == "__main__":
    app.run_server(debug=False)


# %%
