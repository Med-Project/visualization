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

unique_classes = df['categ'].unique()
dis_dropdown_options = [{'label': str(i), 'value': str(i)} for i in unique_classes]

app.layout = html.Div([
    html.H1(
        children='Diseases Vis. Map',
        style={'textAlign': 'center'}
    ),

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
    [dash.dependencies.Input('dis-dropdown', 'value')])
def update_figure(dis_dropdown_values):
    dff = df[df['categ'].isin(dis_dropdown_values)]
    figure={
        'data': [
            go.Scatter(
                x=dff['X'],
                y=dff['Y'],
                text=dff['name'] + '<br>' + dff['categ'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 12,
                    'line': {'width': 0.5, 'color': 'white'},
                    'color' : dff['color'],
                },
                hoverinfo='text'
            )
        ],
        'layout': go.Layout(
            title='Diseases map',
            margin={'l': 40, 'b': 40, 't': 100, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }
    return figure

if __name__ == '__main__':
    app.run_server(port=80)