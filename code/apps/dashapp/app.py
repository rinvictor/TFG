import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import style
from pymongo import MongoClient
import pandas as pd
import create_figures as figures
import dash_utils as du
from datetime import datetime, timedelta
import db_credentials


def getdataframe(sensor_type):
    client = MongoClient(db_credentials.url, db_credentials.port)
    db = client["greenhouseDB"]
    collection = db['sensors_data']
    results = collection.find({'type': sensor_type})
    df = pd.DataFrame(list(results))
    return df


def getcontrollerdataframe(controller_type):
    client = MongoClient(db_credentials.url, db_credentials.port)
    db = client["greenhouseDB"]
    collection = db['controllers_data']
    results = collection.find({'type': controller_type})
    df = pd.DataFrame(list(results))
    return df


app = dash.Dash(name=__name__, assets_folder='assets', external_stylesheets=[dbc.themes.SANDSTONE])
server = app.server
app.title = "Víctor Rincón: My TFG"

sidebar = html.Div(
    [
        html.Div(
            dbc.Col(
                html.A(
                    html.Img(
                        src=app.get_asset_url("index.png"),
                        height='48px',
                        alt="ETSIT URJC"),
                    href="https://www.urjc.es/etsit",
                    target="_blank"),
            ),
            style={"background-color": "#754C24"}
        ),
        html.Hr(),
        html.P(
            "Menu", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.DropdownMenu(
                    [dbc.DropdownMenuItem("Ambient temperature", href="/amb_temp_fig"),
                     dbc.DropdownMenuItem("Ambient humidity", href="/amb_hum_fig"),
                     dbc.DropdownMenuItem("Ground temperature", href="/ground_temp_fig"),
                     dbc.DropdownMenuItem("Ground humidity", href="/ground_hum_fig"),
                     ],
                    label="Sensors data",
                    nav=True
                ),
                dbc.DropdownMenu(
                    [dbc.DropdownMenuItem("IRRIGATION", href="/irr_data_fig", className='dropbtn')],
                    label="Controllers data",
                    nav=True
                ),
                dbc.NavItem(dbc.NavLink("Documentation", href="/documentation"))
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className='sidebar',
)

content = html.Div(id="page-content", style=style.CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(
            children=[
                html.H1(children='My Final Project Degree',
                        className="header-title"),
                html.H3(children='Develop of an automation and monitoring distributed system for a greenhouse',
                        className="header-description"),
                html.Hr()
            ],
            className='header'
        ), html.Div(
            children=[
                html.P("This is a data visualization web app developed as a part of the system that has been built as "
                       "a final project degree for the Telematics Engineering degree. The project consists of an "
                       "autonomous distributed system for monitoring and care of a greenhouse."),
                html.P(children=["This app is based on Python, Dash and Plotly for the data visualization. All data is "
                                 "retrieved from the different sensors and processed using a Raspberry Pi 3B+ and an "
                                 "Arduino and sended to a MongoDB database hosted in a Docker container in the ETSIT "
                                 "labs from Universidad Rey Juan Carlos. You can have a look to their webpage ",
                                 html.A("here", href="https://labs.etsit.urjc.es/", target="_blank")]),
                html.P("The project has four clearly differentiated main parts, this visualization web application "
                       "deployed using Heroku, the aforementioned data collection system, a Python app for the "
                       "autonomous control of the greenhouse and a Telegram bot that is used not only for monitoring "
                       "the whole system but also to obtain real-time data as well as getting it from the database, "
                       "this bot is deployed in the Raspberry Pi 3B+."),
                html.P(
                    "If you are interested you can have a look to the documentation section to learn more about it."),
                html.Hr(),
                html.H5(children=["Developed by: ",
                                  html.A(
                                      "Víctor Rincón Yepes",
                                      href="https://www.linkedin.com/in/victor-rinc%C3%B3n-yepes-969242206/",
                                      target="_blank"),
                                  html.Br(),
                                  "Advised and tutored by: ",
                                  html.A(
                                      "David Roldán Alvarez",
                                      href="https://gestion2.urjc.es/pdi/ver/david.roldan",
                                      target="_blank")
                                  ]
                        )]
        )

    elif pathname == "/amb_temp_fig":
        df = getdataframe("ambient temperature")
        # By defect values
        yesterday = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
        today = datetime.strftime(datetime.now(), '%Y-%m-%d')
        df = du.date_filter(df, start_date=yesterday, end_date=today)

        options = []
        for c in df["sensorID"].unique():
            options.append({"label": c, "value": c})
        html_plot = html.Div([
            html.H2("AMBIENT TEMPERATURE", className='card-title'),
            html.Hr(),
            dbc.Row([
                dbc.Col(html.Div(dcc.DatePickerRange(
                    id='date_picker_ambient_temperature',
                    clearable=True,
                    calendar_orientation='horizontal',
                    first_day_of_week=1
                )), width=9),
                dbc.Col(html.Div(dcc.Dropdown(id="dropdown_ambient_temperature", options=options, multi=True,
                                              style={"height": "48px"})), width=3)
            ]),
            html.Hr(),
            dcc.Graph(
                id='ambient_temperature_fig',
                figure=figures.create_temperature_fig(df),
                className='card'
            ),
            html.H5("Ambient temperature graph.")
        ])

    elif pathname == "/amb_hum_fig":

        df = getdataframe("ambient humidity")
        yesterday = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
        today = datetime.strftime(datetime.now(), '%Y-%m-%d')
        df = du.date_filter(df, start_date=yesterday, end_date=today)

        options = []
        for c in df["sensorID"].unique():
            options.append({"label": c, "value": c})
        html_plot = html.Div([
            html.H2("Ambient humidity", className='card-title'),
            html.Hr(),
            dbc.Row([
                dbc.Col(html.Div(dcc.DatePickerRange(
                    id='date_picker_ambient_humidity',
                    clearable=True,
                    calendar_orientation='horizontal',
                    first_day_of_week=1
                )), width=9),
                dbc.Col(html.Div(dcc.Dropdown(id="dropdown_ambient_humidity", options=options, multi=True,
                                              style={"width": "200px"})), width=3)
            ]),
            html.Hr(),
            dcc.Graph(
                id='ambient_humidity_fig',
                figure=figures.create_humidity_fig(df),
                className='card'
            ),
            html.H5("Ambient humidity graph.")
        ])

    elif pathname == "/ground_temp_fig":
        df = getdataframe("ground temperature")
        yesterday = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
        today = datetime.strftime(datetime.now(), '%Y-%m-%d')
        df = du.date_filter(df, start_date=yesterday, end_date=today)
        options = []
        for c in df["sensorID"].unique():
            options.append({"label": c, "value": c})
        html_plot = html.Div([
            html.H2("GROUND TEMPERATURE", className='card-title'),
            html.Hr(),
            dbc.Row([
                dbc.Col(html.Div(dcc.DatePickerRange(
                    id='date_picker_ground_temperature',
                    clearable=True,
                    calendar_orientation='horizontal',
                    first_day_of_week=1
                )), width=9),
                dbc.Col(html.Div(dcc.Dropdown(id="dropdown_ground_temperature", options=options, multi=True,
                                              style={"width": "200px"})), width=3)
            ]),
            html.Hr(),
            dcc.Graph(
                id='ground_temperature_fig',
                figure=figures.create_temperature_fig(df),
                className='card'
            ),
            html.H5("Ground temperature graph.")
        ])

    elif pathname == "/ground_hum_fig":
        df = getdataframe("ground humidity")
        yesterday = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
        today = datetime.strftime(datetime.now(), '%Y-%m-%d')
        df = du.date_filter(df, start_date=yesterday, end_date=today)
        options = []
        for c in df["sensorID"].unique():
            options.append({"label": c, "value": c})
        html_plot = html.Div([
            html.H2("GROUND HUMIDITY", className='card-title'),
            html.Hr(),
            dbc.Row([
                dbc.Col(html.Div(dcc.DatePickerRange(
                    id='date_picker_ground_humidity',
                    clearable=True,
                    calendar_orientation='horizontal',
                    first_day_of_week=1
                )), width=9),
                dbc.Col(html.Div(dcc.Dropdown(id="dropdown_ground_humidity", options=options, multi=True,
                                              style={"height": "48px"})), width=3)
            ]),
            html.Hr(),
            dcc.Graph(
                id='ground_humidity_fig',
                figure=figures.create_humidity_fig(df),
                className='card'
            ),
            html.H5("Ground humidity graph.")
        ])

    elif pathname == "/irr_data_fig":
        df = getcontrollerdataframe("irrigation")
        yesterday = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
        today = datetime.strftime(datetime.now(), '%Y-%m-%d')
        df = du.date_filter(df, start_date=yesterday, end_date=today)
        options = []
        for c in df["controllerID"].unique():
            options.append({"label": c, "value": c})
        html_plot = html.Div([
            html.H2("IRRIGATION DATA", className='card-title'),
            html.Hr(),
            dbc.Row([
                dbc.Col(html.Div(dcc.DatePickerRange(
                    id='date_picker_irrigation_data',
                    clearable=True,
                    calendar_orientation='horizontal',
                    first_day_of_week=1
                )), width=9),
                dbc.Col(html.Div(dcc.Dropdown(id="dropdown_irrigation_data", options=options, multi=True,
                                              style={"height": "48px"})), width=3)
            ]),
            html.Hr(),
            dcc.Graph(
                id='irrigation_data_fig',
                figure=figures.create_irrigation_data_fig(df),
                className='card'
            ),
            html.H5("Irrigation data graph.")
        ])

    elif pathname == "/documentation":
        return html.Div(
            children=[
                html.H1(children='Documentation',
                        className="header-title"),
                html.H3(children='In this page you can have a look to the documentation section...',
                        className="header-description"),
                html.Hr()
            ],
            className='header'
        ), html.Div(
            children=[
                html.P(children=["Any information you need to know or any relevant updates will be published in the "
                                 "Github repository. You can check out this repository ",
                                 html.A("here", href="https://github.com/rinvictor/TFG", target="_blank")]),
                html.P(children=["The Telegram bot developed as a part of this project is available in ",
                                 html.A("t.me/greenhouseTFGBot")]),
                html.P(children=["This is an open-source project developed under the GNU General Public License v3.0, "
                                 "for further information you can click ",
                                 html.A("here", href="https://github.com/rinvictor/TFG/blob/main/LICENSE", target="_blank")]),

                html.P(children=["If you have any questions or suggestions, please do not hesitate to contact me. "
                                 "And remember... All pull requests are very welcome! "])
                ]
        )


    else:
        # If the user tries to reach a different page, return a 404 message
        html_plot = html.Div(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.H2(f"The pathname {pathname} doesn't exist..."),
            ]
        )
    return html_plot


@app.callback(
    Output('ambient_temperature_fig', 'figure'),
    [Input('date_picker_ambient_temperature', 'start_date'),
     Input('date_picker_ambient_temperature', 'end_date'),
     Input('dropdown_ambient_temperature', 'value')]
)
def update_output(start_date, end_date, value):
    df = getdataframe("ambient temperature")
    yesterday = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
    today = datetime.strftime(datetime.now(), '%Y-%m-%d')
    if not value and not start_date and not end_date:
        df = du.date_filter(df, start_date=yesterday, end_date=today)
    if start_date or end_date:
        df = du.date_filter(df, start_date, end_date)
    if value and len(value) > 0 and start_date and end_date:
        df = du.date_filter(df, start_date, end_date)
        df = df[df['sensorID'].isin(value)]
    if value and not start_date:
        df = du.date_filter(df, start_date=yesterday, end_date=today)
        df = df[df['sensorID'].isin(value)]

    fig = figures.create_temperature_fig(df)
    return fig


@app.callback(
    Output('ambient_humidity_fig', 'figure'),
    [Input('date_picker_ambient_humidity', 'start_date'),
     Input('date_picker_ambient_humidity', 'end_date'),
     Input('dropdown_ambient_humidity', 'value')]
)
def update_output(start_date, end_date, value):
    # If no filter has been selected
    df = getdataframe("ambient humidity")
    yesterday = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
    today = datetime.strftime(datetime.now(), '%Y-%m-%d')
    if not value and not start_date and not end_date:
        df = du.date_filter(df, start_date=yesterday, end_date=today)
    if start_date or end_date:
        df = du.date_filter(df, start_date, end_date)
    if value and len(value) > 0 and start_date and end_date:
        df = du.date_filter(df, start_date, end_date)
        df = df[df['sensorID'].isin(value)]
    if value and not start_date:
        df = du.date_filter(df, start_date=yesterday, end_date=today)
        df = df[df['sensorID'].isin(value)]

    fig = figures.create_humidity_fig(df)
    return fig


@app.callback(
    Output('ground_temperature_fig', 'figure'),
    [Input('date_picker_ground_temperature', 'start_date'),
     Input('date_picker_ground_temperature', 'end_date'),
     Input('dropdown_ground_temperature', 'value')]
)
def update_output(start_date, end_date, value):
    df = getdataframe("ground temperature")
    yesterday = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
    today = datetime.strftime(datetime.now(), '%Y-%m-%d')
    if not value and not start_date and not end_date:
        df = du.date_filter(df, start_date=yesterday, end_date=today)
    if start_date or end_date:
        df = du.date_filter(df, start_date, end_date)
    if value and len(value) > 0 and start_date and end_date:
        df = du.date_filter(df, start_date, end_date)
        df = df[df['sensorID'].isin(value)]
    if value and not start_date:
        df = du.date_filter(df, start_date=yesterday, end_date=today)
        df = df[df['sensorID'].isin(value)]

    fig = figures.create_temperature_fig(df)
    return fig


@app.callback(
    Output('ground_humidity_fig', 'figure'),
    [Input('date_picker_ground_humidity', 'start_date'),
     Input('date_picker_ground_humidity', 'end_date'),
     Input('dropdown_ground_humidity', 'value')]
)
def update_output(start_date, end_date, value):
    df = getdataframe("ground humidity")
    yesterday = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
    today = datetime.strftime(datetime.now(), '%Y-%m-%d')
    if not value and not start_date and not end_date:
        df = du.date_filter(df, start_date=yesterday, end_date=today)
    if start_date or end_date:
        df = du.date_filter(df, start_date, end_date)
    if value and len(value) > 0 and start_date and end_date:
        df = du.date_filter(df, start_date, end_date)
        df = df[df['sensorID'].isin(value)]
    if value and not start_date:
        df = du.date_filter(df, start_date=yesterday, end_date=today)
        df = df[df['sensorID'].isin(value)]

    fig = figures.create_humidity_fig(df)
    return fig


@app.callback(
    Output('irrigation_data_fig', 'figure'),
    [Input('date_picker_irrigation_data', 'start_date'),
     Input('date_picker_irrigation_data', 'end_date'),
     Input('dropdown_irrigation_data', 'value')]
)
def update_output(start_date, end_date, value):
    df = getcontrollerdataframe("irrigation")
    if not value and not start_date and not end_date:
        start_date = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
        today = datetime.strftime(datetime.now(), '%Y-%m-%d')
        df = du.date_filter(df, start_date=start_date, end_date=today)
    if start_date or end_date:
        df = du.date_filter(df, start_date, end_date)
    if value and len(value) > 0:
        df = df[df['controllerID'].isin(value)]

    fig = figures.create_irrigation_data_fig(df)
    return fig


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8080, use_reloader=True, debug=False)
