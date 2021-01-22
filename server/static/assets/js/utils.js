handleMessage = (body) => {
    document.querySelector('#chat-text').value += (body.username + ': ' + body.message + '\n')
}
function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

handleRemove = (id)=>{
    const URL = '/queues/patients/remove/';
    const data = {
        'id': id,
        'room_name': roomName,
    }
    const csrftoken = getToken('csrftoken'); 
    const config = {
        method:'POST',
        headers:{
            'Content-Type':'applicaiton/json',
            'X-CSRFToken':csrftoken,
        }, 
        body:JSON.stringify(data),
    }
    fetch(URL,config)
    .then((response)=>response.json())
    .then((data)=>{
        console.log(data);
    });
}

handleComplete = (id)=>{
    const URL = '/queues/patients/complete/';
    const data = {
        'id': id,
        'room_name': roomName,
    }
    const csrftoken = getToken('csrftoken'); 
    const config = {
        method:'POST',
        headers:{
            'Content-Type':'applicaiton/json',
            'X-CSRFToken':csrftoken,
        }, 
        body:JSON.stringify(data),
    }
    fetch(URL,config)
    .then((response)=>response.json())
    .then((data)=>{
        console.log(data);
    });
}

// This displays patients information when patient enters ID
getPatientsWaitime = ()=>{
    // getting all elements 
    console.log(queue)
    const waitTimeInfo = document.getElementById('wait-time-info');
    const patientIdElement = document.getElementById('patientId');
    const positionElement = document.getElementById('position');
    const joinedAtElement = document.getElementById('joinedAt');
    const spanPatientId = document.getElementById('spanPatientid');
    const userNameElement = document.getElementById('userName');
    const waitTimeElement = document.getElementById('waitTime');
    patientId = parseInt(patientIdElement.value);
    
    if(patientId==undefined){
        console.log('undefined')
        return;
    }
    let maxId = -1;
    let minId = 10000;
    let joinedAt;
    let userName;
    let wait_time;
    for(const q of queue){
        console.log(patientId,q.id)
        if(q.id === patientId){
            console.log(q.joined_at)
            joinedAt = q.joined_at;
            userName = q.patient_name;
            waitTime = q.wait_time;
        }
        maxId = Math.max(q.id,maxId);
        minId = Math.min(q.id, minId);
    }
    if(joinedAt == undefined){
        patientIdElement.classList.add('is-invalid');
        spanPatientId.className = 'invalid-feedback';
        return;
    }
    waitTimeElement.innerHTML = waitTime;
    waitTimeInfo.classList.remove('d-none');
    userNameElement.innerHTML = "Welcome , " + userName;
    let position = patientId - minId + 1;
    console.log(position);
    joinedAtElement.innerHTML = joinedAt;
    positionElement.innerHTML = position;
}


updateRoot2Table = ()=>{
    
    tbody = document.querySelector('#root2')
    tbody.innerHTML = '';
    for(var i = 0; i<queue.length; i++){
        tbody.innerHTML += `
            <tr>
                <td>${ queue[i].id }</td>
                <td>${ queue[i].patient_name }</td>
                <td>${ queue[i].joined_at }</td>
            </tr>
        `;
    }
}

handleUpdate = (body)=>{
    queue = body.queue;
    
    tbody = document.querySelector('#root')
    if(tbody==undefined){
        // updateRoot2Table(queue);
        return;
    }
    tbody.innerHTML = '';
    for(var i = 0; i<queue.length; i++){
        tbody.innerHTML += `
            <tr>
                <td>${ queue[i].id }</td>
                <td>${ queue[i].patient_name }</td>
                <td>${ queue[i].joined_at }</td>
                <td>${ queue[i].wait_time }</td>
                <td>
                    <button onclick="handleRemove(${ queue[i].id })" class="btn btn-sm btn-danger">Remove</button>
                </td>
                <td>
                    <button onclick="handleComplete(${ queue[i].id })" class = "btn btn-sm btn-success">Complete</button>
                </td>
            </tr>
        `;
    }
    
}
