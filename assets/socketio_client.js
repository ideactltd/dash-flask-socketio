// socketio has been loaded in the app.py as an external script
const socket = io("");  // Default connection to the local server as Flask does

socket.on("connect", () => {
  console.log(socket.id); // x8WIv7-mJelg7on_ALbx
});

socket.on("update", function(data) {
    console.log(data);
    window.dash_clientside.set_props("socket_data_store", {data: data});
});
