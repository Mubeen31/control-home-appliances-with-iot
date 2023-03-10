import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import dash_daq as daq
import dash_bootstrap_components as dbc
import pyrebase
from data import config

firebase = pyrebase.initialize_app(config)
db = firebase.database()

metaTags = [
    {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minium-scale=0.5'}]

app = dash.Dash(__name__, meta_tags=metaTags)
server = app.server

app.layout = html.Div([

    dcc.Interval(id='blink_image',
                 interval=1 * 3000,
                 n_intervals=0),

    html.Div([
        html.Div([
            html.Div([
                html.Img(src=app.get_asset_url('iot.png'),
                         className='image'),
                html.Div('IOT Home Appliances',
                         className='title_text')
            ], className='title_row')
        ], className='title_background twelve columns')
    ], className='row'),

    html.Div([
        html.Div([

            html.Div([
                dbc.Spinner(html.Div(id='light_image')),
                html.Div(id='light_image_dark'),
                html.Div([
                    daq.PowerButton(id='light_button',
                                    on=False,
                                    color='#FF5E5E',
                                    size=40),
                    html.Div(id='power_button_one'),
                ], className='light_power_button')
            ], className='blink_column'),

        ], className='light twelve columns')
    ], className='row'),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dbc.Spinner(id='heater_image'),
                    html.Div(id='heater_image_dark'),
                    html.Div([
                        daq.PowerButton(id='heater_button',
                                        on=False,
                                        color='#FF5E5E',
                                        size=40),
                        html.Div(id='power_button_two'),
                    ], className='light_power_button')
                ], className='blink_column'),

                html.Div([
                    html.Div('Room Temperature', style={'color': '#bfbfbf'}),
                    dbc.Spinner(html.Div(id='room_temp')),
                ], className='heater_margin_column')
            ], className='heater_column')
        ], className='light twelve columns')
    ], className='row'),

])


@app.callback(Output('power_button_one', 'children'),
              [Input('light_button', 'on')])
def update_value(light):
    light_on = 'Light is on'
    light_off = 'Light is off'
    if light == True:
        db.update({"L1": "0"})
        return [
            html.Div(light_on, style={'color': 'white'})
        ]
    elif light == False:
        db.update({"L1": "1"})
        return [
            html.Div(light_off, style={'color': 'white'})
        ]


@app.callback(Output('light_image', 'children'),
              [Input('light_button', 'on')],
              [Input('blink_image', 'n_intervals')])
def update_value(light, n_intervals):
    if light == True:
        return [
            html.Img(src=app.get_asset_url('bulb.png')),
        ]
    else:
        return None


@app.callback(Output('light_image_dark', 'children'),
              [Input('light_button', 'on')],
              [Input('blink_image', 'n_intervals')])
def update_value(light, n_intervals):
    if light == True:
        return None
    else:
        return [
            html.Img(src=app.get_asset_url('cross.png')),
        ]


@app.callback(Output('power_button_two', 'children'),
              [Input('heater_button', 'on')])
def update_value(heater):
    light_on = 'Heater is on'
    light_off = 'Heater is off'

    if heater == True:
        db.update({"L2": "0"})
        return [
            html.Div(light_on, style={'color': 'white'})
        ]
    elif heater == False:
        db.update({"L2": "1"})
        return [
            html.Div(light_off, style={'color': 'white'})
        ]


@app.callback(Output('heater_image', 'children'),
              [Input('heater_button', 'on')],
              [Input('blink_image', 'n_intervals')])
def update_value(heater, n_intervals):
    if heater == True:
        return [
            html.Img(src=app.get_asset_url('heater.png')),
        ]
    else:
        return None


@app.callback(Output('heater_image_dark', 'children'),
              [Input('heater_button', 'on')],
              [Input('blink_image', 'n_intervals')])
def update_value(heater, n_intervals):
    if heater == True:
        return None
    else:
        return [
            html.Img(src=app.get_asset_url('cross.png')),
        ]


@app.callback(Output('room_temp', 'children'),
              [Input('heater_button', 'on')],
              [Input('blink_image', 'n_intervals')])
def update_value(heater, n_intervals):
    temp_value = db.child('DHT').get('Temperature')
    for item in temp_value.each():
        temp = item.val()

    if heater == True and temp <= 18.0:
        return [
            html.Div('{0:.2f} ??C'.format(temp),
                     style={'color': '#bfbfbf',
                            'fontWeight': 'bold',
                            'fontSize': '20px',
                            'margin-top': '-5px'
                            })
        ]
    elif heater == True and temp >= 18.1:
        return [

            html.Div('{0:.2f} ??C'.format(temp),
                     style={'color': '#DE3163',
                            'fontWeight': 'bold',
                            'fontSize': '20px',
                            'margin-top': '-5px'})
        ]
    elif heater == False and temp <= 18.0:
        return [

            html.Div('{0:.2f} ??C'.format(temp),
                     style={'color': '#bfbfbf',
                            'fontWeight': 'bold',
                            'fontSize': '20px',
                            'margin-top': '-5px'
                            })
        ]
    elif heater == False and temp >= 18.1:
        return [
            html.Div('{0:.2f} ??C'.format(temp),
                     style={'color': '#DE3163',
                            'fontWeight': 'bold',
                            'fontSize': '20px',
                            'margin-top': '-5px'
                            })
        ]


if __name__ == '__main__':
    app.run_server(debug=True)
