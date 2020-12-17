
var socket;
const SOCKET_URL = 'ws://' + window.location.host + '/ws/queues/' + roomName + '/'

// document.querySelector('#submit').onclick = function (e) {
//     const messageInputDom = document.querySelector('#input');
//     const message = messageInputDom.value;
//     chatSocket.send(JSON.stringify({
//         'message': message,
//         'username': user_username,
//     }));
//     messageInputDom.value = '';
// };
// const chatSocket = new WebSocket(
    
// );
socket = new WebSocket(SOCKET_URL);
const socketOnMessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data);
    getPatientsData();
}

const updateQueue = ()=>{
    socket.send(JSON.stringify({
        'message': 'Update table',
        'username': 'admin',
    }));
}

function websocketWaiter(){
    setTimeout(function(){
        socket.onmessage = socketOnMessage;
    }, 1000);
};

websocketWaiter();