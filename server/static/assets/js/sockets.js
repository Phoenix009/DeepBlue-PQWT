let queue;

function waitForSocketConnection(socket, callback){
    setTimeout(
        function () {
            if (socket.readyState === 1) {
                if (callback != null){
                    callback();
                }
            } else {
                waitForSocketConnection(socket, callback);
            }
        }, 5); // wait 5 milisecond for the connection...
}

const roomName = JSON.parse(document.getElementById('room-name').textContent);

const chatSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/queues/' +
    roomName +
    '/'
);

waitForSocketConnection(chatSocket, ()=>{
    chatSocket.send(JSON.stringify({
        'type': 'UPD',
    }));
});

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    switch(data.type){
        case "MSG": 
            handleMessage(data.body);
            break;
        case "UPD":
            queue = data.body;
            handleUpdate(data.body);
            break;
    }
}
