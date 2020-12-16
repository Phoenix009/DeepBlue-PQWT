const user_username = JSON.parse(document.getElementById('user_username').textContent);
const roomName = JSON.parse(document.getElementById('room-name').textContent); 

const addPatientURL = `/queues/add-patient/${roomName}/`

document.querySelector('#submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'username': user_username,
    }));
    messageInputDom.value = '';
};
const chatSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/queues/' +
    roomName +
    '/'
);

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data);
    document.querySelector('#chat-text').value += (data.username + ': ' + data.message + '\n');
}