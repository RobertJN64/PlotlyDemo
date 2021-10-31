import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import Input, Output
import plotly.express as px
import pandas

# mode = "dark"
mode = 'light'  # TODO - drop down dark theme


class App:
    def __init__(self):
        if mode == "dark":
            theme = dbc.themes.DARKLY
            folder = 'assets/dark_assets'
        else:
            theme = dbc.themes.FLATLY
            folder = 'assets/light_assets'

        self.app = dash.Dash(__name__, title="Example Dash App", external_stylesheets=[theme], assets_folder=folder)

        self.df: pandas.DataFrame = px.data.gapminder(pretty_names=True)
        options = [{'label': 'None', 'value': 'None'}]
        for col in self.df.columns:
            options.append({'label': col, 'value': col})

        # region data defaults
        self.x = 'GDP per Capita'
        self.y = 'Life Expectancy'
        self.color = 'Continent'
        self.animaxis = 'Year'
        self.size = 'Population'
        self.hover_name = 'Country'

        self.log_x = True
        self.log_y = False
        self.max_size = 50
        # endregion

        self.fig = self.updateGraph()

        graph = dbc.Card([
            dcc.Graph(id='example-graph', figure=self.fig)
        ], body=True)

        config = dbc.Card([

            dbc.Label("X Axis: "),
            dcc.Dropdown(id='xaxis', options=options, value=self.x),
            html.P(),

            dbc.Label("Y Axis: "),
            dcc.Dropdown(id='yaxis', options=options, value=self.y),
            html.P(),

            dbc.Label("Color: "),
            dcc.Dropdown(id='color', options=options, value=self.color),
            html.P(),

            dbc.Label("Size: "),
            dcc.Dropdown(id='size', options=options, value=self.size),
            html.P(),

            dbc.Label("Animation Axis: "),
            dcc.Dropdown(id='animaxis', options=options, value=self.animaxis),
            html.P(),

            dbc.Label("Hover Name: "),
            dcc.Dropdown(id='hovername', options=options, value=self.hover_name)

        ], body=True)

        self.app.layout = dbc.Container([
            html.H1("Dash Demo Example"),
            html.Hr(),
            dbc.Row([
                dbc.Col(config, md=4),
                dbc.Col(graph, md=8)]
            ),
            html.P()],
            fluid=True,
            className='dash-bootstrap')

        inputs = []
        for item in ['xaxis', 'yaxis', 'color', 'size', 'animaxis', 'hovername']:
            inputs.append(Input(item, "value"))
        self.app.callback(Output("example-graph", "figure"), inputs)(self.updateGraphFromWebsite)

    def updateGraph(self):
        if mode == "dark":
            template = "plotly_dark"
        else:
            template = "plotly"
        rangex = [self.df[self.x].min() * 0.9, self.df[self.x].max() * 1.1]
        rangey = [self.df[self.y].min() * 0.9, self.df[self.y].max() * 1.1]
        self.fig = px.scatter(self.df, x=self.x, y=self.y, animation_frame=self.animaxis, size=self.size,
                              color=self.color, log_x=self.log_x, log_y=self.log_y, hover_name=self.hover_name,
                              size_max=self.max_size, range_x=rangex, range_y=rangey, template=template)
        return self.fig

    def run(self):
        self.app.run_server(host='0.0.0.0', debug=True)

    def notNone(self):
        if self.color == 'None':
            self.color = None
        if self.size == 'None':
            self.size = None
        if self.animaxis == 'None':
            self.animaxis = None
        if self.hover_name == 'None':
            self.hover_name = None

    def updateGraphFromWebsite(self, x, y, color, size, animaxis, hovername):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.animaxis = animaxis
        self.hover_name = hovername
        self.notNone()
        return self.updateGraph()


if __name__ == '__main__':
    App().run()
