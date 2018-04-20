import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from flask_cors import CORS
import plotly.graph_objs as go

app = dash.Dash()

server = app.server
CORS(server)

df = pd.read_csv('vis_data.csv')
df_3d = pd.read_csv('vis_data_3d.csv')
df_siamese = pd.read_csv('vis_data_siamese.csv')
df_siamese_3d = pd.read_csv('vis_data_siamese_3d.csv')

unique_classes = df['categ'].unique()
dis_dropdown_options = [{'label': str(i), 'value': str(i)} for i in unique_classes]

tabs = [{'label': '2D Visualization', 'value': 1}, {'label': '3D Visualization', 'value': 2},
        {'label': '2D Siamese Visualization', 'value': 3}, {'label': '3D Siamese Visualization', 'value': 4}]

app.layout = html.Div([
    html.H1(
        children='Diseases Vis. Map',
        style={'textAlign': 'center'}
    ),

    html.Div([
        dcc.Tabs(
            id='tabs',
            tabs=tabs,
            value=1
        )
    ], style={
        'fontFamily': 'Sans-Serif'
    }),

    html.Div(
        children='''
            31 classes (31 colors)
            ''',
        style={'textAlign': 'center'}
    ),

    html.Div([
        dcc.Dropdown(
            id='dis-dropdown',
            options=dis_dropdown_options,
            multi=True,
            value=[i['value'] for i in dis_dropdown_options]
        )
    ], style={'width': '100%', 'display': 'inline-block'}),
    
    dcc.Graph(id='dis-graph'),
])

@app.callback(
    dash.dependencies.Output('dis-graph', 'figure'),
    [dash.dependencies.Input('dis-dropdown', 'value'),
    dash.dependencies.Input('tabs', 'value')])
def update_figure(dis_dropdown_values, tabs_value):
    data = []
    if(tabs_value == 1):
        dff = df[df['categ'].isin(dis_dropdown_values)]
        data = [
            go.Scatter(
                x=dff['X'],
                y=dff['Y'],
                text=dff['name'] + '<br>' + dff['categ'],
                mode='markers',
                opacity=0.8,
                marker={
                    'size': 12,
                    'line': {'width': 0.5, 'color': 'white'},
                    'color' : dff['color'],
                },
                hoverinfo='text'
            )
        ]
    elif(tabs_value == 2):
        dff = df_3d[df_3d['categ'].isin(dis_dropdown_values)]
        data = [
            go.Scatter3d(
                x=dff['X'],
                y=dff['Y'],
                z=dff['Z'],
                text=dff['name'] + '<br>' + dff['categ'],
                mode='markers',
                opacity=0.7,
                marker={
                    'color' : dff['color'],
                },
                hoverinfo='text'
            )
        ]
    elif(tabs_value == 3):
        dff = df_siamese[df_siamese['categ'].isin(dis_dropdown_values)]
        data = [
            go.Scatter(
                x=dff['X'],
                y=dff['Y'],
                text=dff['name'] + '<br>' + dff['categ'],
                mode='markers',
                opacity=0.8,
                marker={
                    'size': 12,
                    'line': {'width': 0.5, 'color': 'white'},
                    'color' : dff['color'],
                },
                hoverinfo='text'
            )
        ]
    else:
        dff = df_siamese_3d[df_siamese_3d['categ'].isin(dis_dropdown_values)]
        data = [
            go.Scatter3d(
                x=dff['X'],
                y=dff['Y'],
                z=dff['Z'],
                text=dff['name'] + '<br>' + dff['categ'],
                mode='markers',
                opacity=0.8,
                marker={
                    'color' : dff['color'],
                },
                hoverinfo='text'
            )
        ]
    layout = go.Layout(
        title='Diseases map',
        height=700,
        margin={'l': 40, 'b': 40, 't': 100, 'r': 10},
        legend={'x': 0, 'y': 1},
        hovermode='closest'
    )
    return {'data': data, 'layout': layout}

if __name__ == '__main__':
    app.run_server()