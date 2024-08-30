import dash
from flask_socketio import SocketIO
from flask import request
from dash import dcc, html, Input, Output, State

external_scripts = [
    {
        "src": "https://cdn.socket.io/4.6.0/socket.io.min.js",
        "integrity": "sha384-c79GN5VsunZvi+Q/WObgk2in0CbZsHnjEqvFxC5DxHn9lTfNce2WW6h2pH6u/kF+",
        "crossorigin": "anonymous",
    }
]

app = dash.Dash(
    __name__,
    external_scripts=external_scripts
)
socketio = SocketIO(app.server)


@socketio.on("connect")
def connect():
    print("Connected:", request.sid)

@socketio.on("disconnect")
def disconnect():
    print("Disconnected")


app.layout = html.Div(id="root_div", children=[
    html.Div(id="display"),
    dcc.Store(id="socket_data_store"),
    html.Button("Send", id="update_button"),
    dcc.Input(id="input", type="text"),
    dcc.Input(id="room", type="text"),
])


@app.callback(
    output=Output("input", "value"),
    inputs=[
        Input("update_button", "n_clicks"),
        State("input", "value"),
        State("room", "value"),
    ]
)
def update_data(n_clicks, value, room):
    if n_clicks:
        socketio.emit("update", {"message": value}, to=room)
    return ""


@app.callback(
    Output("display", "children"),
    [Input("socket_data_store", "data")]
)
def update_display(socket_data):
    print("update_display", socket_data)
    if socket_data:
        return socket_data.get("message", "")
    return ""


socketio.run(app.server, port=8050, debug=True, allow_unsafe_werkzeug=True)
