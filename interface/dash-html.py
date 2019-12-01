import dash
import dash_core_components as dcc
import dash_html_components as html

from flask import Flask, render_template, make_response

app = dash.Dash()
app.layout = html.Div(
                className="three columns",
                children=html.Div([
                    dcc.Graph(
                        id='right-top-graph',
                        figure={
                            'data': [{
                                'x': [1, 2, 3],
                                'y': [3, 1, 2],
                                'type': 'bar'
                            }],
                            'layout': {
                                'height': 400,
                                'margin': {'l': 10, 'b': 20, 't': 0, 'r': 0}
                            }
                        }
                    ),


                ])
            )

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)