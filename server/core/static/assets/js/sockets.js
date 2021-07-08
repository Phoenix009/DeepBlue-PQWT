let queue;
let nextPatient;

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
            scrollToBottom();
            break;
        case "NPMSG": 
            handleNextPatientMessage(data.body);
            scrollToBottom();
            break;
        case "LTMSG": 
            handleLunchTimeMessage(data.body);
            scrollToBottom();
            break;
        case "UPD":
            queue = data.body.queue;
            try{
                nextPatientIDVisualizer(queue);
            }catch(err){
                console.log(err);
            }
            try{
                nextPatient = queue[0].patient_id   ;
            }catch(err){
                console.log(err);
            }
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



function scrollToBottom(){
    try{
        var objDiv = document.getElementById("chat-text");
        objDiv.scrollTop = objDiv.scrollHeight - objDiv.clientHeight;
    }
    catch(err){
        console.log(err);
    }
}


