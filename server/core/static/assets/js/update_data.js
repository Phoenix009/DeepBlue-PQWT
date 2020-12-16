const patientsTable = document.getElementById('patients-table');

const updatePatientsTable = data=>{
    try{
        var tblBody = document.createElement("tbody"); 
        for (const patient of data){
            console.log(patient);
            var row = document.createElement("tr");
            // id 
            var patientId = document.createElement('td');
            var patientIdText = document.createTextNode(patient.pk);
            firstName.appendChild(firstNameText);
            row.appendChild(firstName)

            //first name 
            var firstName = document.createElement('td');
            var firstNameText = document.createTextNode(patient.fields.first_name);
            firstName.appendChild(firstNameText);
            row.appendChild(firstName)
    
            // last name 
            var lastName = document.createElement('td');
            var lastNameText = document.createTextNode(patient.fields.last_name);
            lastName.appendChild(lastNameText);
            row.appendChild(lastName)
    
            // email 
            var email = document.createElement('td');
            var emailText = document.createTextNode(patient.fields.email);
            email.appendChild(emailText);
            row.appendChild(email)
            tblBody.appendChild(row)
        }
        patientsTable.innerHTML = '';
        patientsTable.appendChild(tblBody);
    }catch(err){
        console.log(err);
    }
}