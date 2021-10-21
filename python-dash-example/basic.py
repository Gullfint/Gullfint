import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import json

df=pd.read_csv('wheels.csv')                                                        # Make the dataframe

app = dash.Dash()                                                                   # Make the application


app.layout = html.Div([                                                             # Set the layout
            html.H1('This is the general title'),
            html.Div(dcc.Graph(id='my-ref',                                         # Container for plot
                        figure={
                            'data':[go.Scatter(
                                x=df['wheels'],
                                y=df['color'],
                                #dy=1,                                              # gridlike
                                mode ='markers',                                    # markers/lines/markers+lines
                                marker={'size': 15}
                            )],
                            'layout':go.Layout(
                                title='My title', 
                                hovermode='closest', 
                                xaxis={'title':'x-axis title'}, 
                                yaxis={'title':'y-axis title'},
                                )}
            )),
            html.Div(html.Pre(id='hover-data', style={'paddingTop': 35}),          # Container for hoover data
                    style={'width':'30%'}),                                         # Outermost Div style
])


@app.callback(Output('hover-data', 'children'), 
                    [Input('my-ref', 'hoverData')])
def callback_image(hoverData):
    return json.dumps(hoverData, indent=2)

if __name__=='__main__':                                                            # Run server
    app.run_server()
