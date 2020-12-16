function getCookie(name) {
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
const csrftoken = getCookie('csrftoken');

const addPatient = (event)=>{
    console.log('add patient')
    const data = {
        'firstName':firstName,
        'lastName': lastName,
        'email':email,
        'queueId' : queueId, 
    }
    const configfetch = {
        method : 'POST',
        headers : {
            'Content-Type' : 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken' : csrftoken,
        },
        body : JSON.stringify(data),
    }
    fetch(addPatientURL,configfetch)
    .then((response)=>response.json())
    .then((message)=>{
        console.log(message);
        updateQueue();
    });
}

const addPatientForm = document.getElementById('add-patient');
addPatientForm.addEventListener('submit', function(e){
    e.preventDefault();
    addPatient();
});