handleMessage = (body) => {
    document.querySelector('#chat-text').value += (body.username + ': ' + body.message + '\n')
}

handleUpdate = (body)=>{
    queue = body.queue;
    for(let i =0; i<queue.length; i++){
    }

    tbody = document.querySelector('#root')
    tbody.innerHTML = '';
    for(var i = 0; i<queue.length; i++){
        tbody.innerHTML += `
            <tr>
                <td>${ queue[i].id }</td>
                <td>${ queue[i].patient_name }</td>
                <td>${ queue[i].joined_at }</td>
                <td><button class = "btn btn-sm btn-danger">Remove</button></td>
                <td><button class = "btn btn-sm btn-success">Send</button></td>
            </tr>
        `;
    }
}