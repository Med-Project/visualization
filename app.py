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
        for categ in dff['categ'].unique():
            dff_tmp = dff[dff['categ'] == categ]
            data_tmp = go.Scatter(
                x=dff_tmp['X'],
                y=dff_tmp['Y'],
                text=dff_tmp['name'] + '<br>' + dff_tmp['categ'],
                mode='markers',
                opacity=0.8,
                marker={
                    'size': 12,
                    'line': {'width': 0.5, 'color': 'white'},
                    'color' : dff_tmp['color'],
                },
                hoverinfo='text',
                name = str(categ)
            )
            data.append(data_tmp)
    elif(tabs_value == 2):
        dff = df_3d[df_3d['categ'].isin(dis_dropdown_values)]
        for categ in dff['categ'].unique():
            dff_tmp = dff[dff['categ'] == categ]
            data_tmp = go.Scatter3d(
                x=dff_tmp['X'],
                y=dff_tmp['Y'],
                z=dff_tmp['Z'],
                text=dff_tmp['name'] + '<br>' + dff_tmp['categ'],
                mode='markers',
                opacity=0.7,
                marker={
                    'color' : dff_tmp['color'],
                },
                hoverinfo='text',
                name = str(categ)
            )
            data.append(data_tmp)
    elif(tabs_value == 3):
        dff = df_siamese[df_siamese['categ'].isin(dis_dropdown_values)]
        for categ in dff['categ'].unique():
            dff_tmp = dff[dff['categ'] == categ]
            data_tmp = go.Scatter(
                x=dff_tmp['X'],
                y=dff_tmp['Y'],
                text=dff_tmp['name'] + '<br>' + dff_tmp['categ'],
                mode='markers',
                opacity=0.8,
                marker={
                    'size': 12,
                    'line': {'width': 0.5, 'color': 'white'},
                    'color' : dff_tmp['color'],
                },
                hoverinfo='text',
                name = str(categ)
            )
            data.append(data_tmp)
    else:
        dff = df_siamese_3d[df_siamese_3d['categ'].isin(dis_dropdown_values)]
        for categ in dff['categ'].unique():
            dff_tmp = dff[dff['categ'] == categ]
            data_tmp = go.Scatter3d(
                x=dff_tmp['X'],
                y=dff_tmp['Y'],
                z=dff_tmp['Z'],
                text=dff_tmp['name'] + '<br>' + dff_tmp['categ'],
                mode='markers',
                opacity=0.9,
                marker={
                    'color' : dff_tmp['color'],
                },
                hoverinfo='text',
                name = str(categ)
            )
            data.append(data_tmp)
    layout = go.Layout(
        title='Diseases map',
        height=700,
        margin={'l': 40, 'b': 40, 't': 100, 'r': 10},
        # legend={'x': -.1, 'y': 1.2},
        hovermode='closest',
        xaxis=dict(
            title='Component 1'
        ),
        yaxis=dict(
            title='Component 2'
        )
    )
    return {'data': data, 'layout': layout}

if __name__ == '__main__':
    app.run_server()