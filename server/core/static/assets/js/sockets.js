



// document.querySelector('#submit').onclick = function (e) {
//     const messageInputDom = document.querySelector('#input');
//     const message = messageInputDom.value;
//     chatSocket.send(JSON.stringify({
//         'message': message,
//         'username': user_username,
//     }));
//     messageInputDom.value = '';
// };
const chatSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/queues/' +
    roomName +
    '/'
);

chatSocket.onmessage = function (e) {
    getPatientsData();
}

const updateQueue = ()=>{
    chatSocket.send(JSON.stringify({
        'message': 'Update table',
        'username': 'admin',
    }));
}