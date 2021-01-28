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
let previousRoomName;
try{
    previousRoomName = JSON.parse(document.getElementById('previous_room').textContent);
} catch(err){
    console.log(err);
}

const chatSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/queues/' +
    roomName +
    '/'
);
let previousChatSocket;
if(previousRoomName){
     previousChatSocket = new WebSocket(
        'ws://' +
        window.location.host +
        '/ws/queues/' +
        previousRoomName +
        '/'
    );
}


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
            try{
                updatePatientsData(data.body);
            } 
            catch(error){
                console.log(error)
            }
            break;
    }
}
if(previousChatSocket){
    previousChatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        switch(data.type){
            case "UPD":
                chatSocket.send(JSON.stringify({
                    'type': 'UPD',
                }));
                break;

        }
    }
}
