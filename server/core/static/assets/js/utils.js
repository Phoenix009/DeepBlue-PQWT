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


updateRoot2Table = (queue)=>{
    max_id = 10000;
    min_id = -1;
    for(const q of queue){
        max_id = Math.max(max_id,q.id);
        min_id = Math.max(min_id, q.id);
    }
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
        updateRoot2Table(queue);
        return;
    }
    tbody.innerHTML = '';
    for(var i = 0; i<queue.length; i++){
        tbody.innerHTML += `
            <tr>
                <td>${ queue[i].id }</td>
                <td>${ queue[i].patient_name }</td>
                <td>${ queue[i].joined_at }</td>
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
